from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from . import forms
from .models import UserFollows, User, UserBlock


def login_page(request):
    """
    Vue de connexion utilisateur

    Gère l'authentification et redirige vers le flux
    """

    # Redirection si déjà connecté
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Vérification des identifiants
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Bienvenue, {user} !")

                # Redirection vers la page demandée ou le flux par défaut
                next_url = request.GET.get("next", "feed")
                return redirect(next_url)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez remplir tous les champs correctement.")
    else:
        form = forms.LoginForm()

    context = {
        "form": form,
        "active_page": "login",
    }

    return render(request, "accounts/login.html", context)


def logout_user(request):
    """
    Vue de déconnexion

    Déconnecte l'utilisateur et redirige vers l'accueil
    """
    logout(request)
    messages.info(request, "Vous êtes maintenant déconnecté. À bientôt !")
    return redirect("/")


def signup_page(request):
    """
    Vue d'inscription utilisateur

    Crée un nouveau compte et redirige vers la connexion
    """

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Inscription réussie ! Bienvenue {user.username}, vous pouvez maintenant vous connecter.",
            )
            return redirect("login")
        else:
            messages.error(
                request,
                "Erreur lors de l'inscription. Veuillez corriger les erreurs ci-dessous.",
            )
    else:
        form = forms.SignUpForm()

    context = {
        "form": form,
        "active_page": "singup",
    }

    return render(request, "accounts/signup.html", context)


@login_required
def profile_page(request):
    """
    Vue du profil utilisateur

    Affiche les informations de l'utilisateur connecté
    """
    return render(request, "accounts/profile.html", {"active_page": "profile"})


@login_required
def change_password_page(request):
    """
    Vue de changement de mot de passe

    Permet à l'utilisateur de modifier son mot de passe
    et le garde connecté après la modification
    """

    if request.method == "POST":
        form = forms.ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            # Met à jour la session pour garder l'utilisateur connecté
            update_session_auth_hash(request, user)

            messages.success(request, "Votre mot de passe a été modifié avec succès.")
            return redirect("profile")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = forms.ChangePasswordForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def edit_profile_page(request):
    """
    Vue pour modifier la photo de profil

    Gère l'upload de la photo de profil
    """

    if request.method == "POST":
        # request.FILES contient les fichiers uploadés
        form = forms.ProfilePictureForm(
            request.POST, request.FILES, instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Votre photo de profil a été mise à jour.")
            return redirect("profile")
        else:
            messages.error(request, "Erreur lors de l'upload de la photo.")
    else:
        form = forms.ProfilePictureForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def subscriptions(request):
    """
    Page de gestion des abonnements

    Affiche :
    - Barre de recherche pour suivre un utilisateur
    - Liste des utilisateurs suivis
    - Liste des abonnés
    """

    # Traitement de la recherche (POST)
    if request.method == "POST":
        username_to_follow = request.POST.get("username", "").strip()

        if username_to_follow:
            try:
                user_to_follow = User.objects.get(username__iexact=username_to_follow)

                # Validation : on ne peut pas se suivre soi-même
                if user_to_follow == request.user:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")

                # Validation : vérifier si un blocage existe
                elif UserBlock.objects.filter(
                    Q(blocker=request.user, blocked_user=user_to_follow)
                    | Q(blocker=user_to_follow, blocked_user=request.user)
                ).exists():
                    messages.error(
                        request,
                        "Vous ne pouvez pas suivre cet utilisateur en raison d'un blocage.",
                    )

                # Validation : on ne suit pas déjà cet utilisateur
                elif UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_follow
                ).exists():
                    messages.warning(
                        request, f"Vous suivez déjà {user_to_follow.username}."
                    )

                # Création de l'abonnement
                else:
                    UserFollows.objects.create(
                        user=request.user, followed_user=user_to_follow
                    )
                    messages.success(
                        request, f"Vous suivez maintenant {user_to_follow.username} !"
                    )

            except User.DoesNotExist:
                messages.error(
                    request, f"L'utilisateur {username_to_follow} n'existe pas."
                )
        else:
            messages.warning(request, "Veuillez saisir un nom d'utilisateur.")

        return redirect("subscriptions")

    # Affichage de la page (GET)
    following = UserFollows.objects.filter(user=request.user).select_related(
        "followed_user"
    )

    followers = UserFollows.objects.filter(followed_user=request.user).select_related(
        "user"
    )

    # Récupérer les utilisateurs bloqués
    blocked_users_preview = UserBlock.objects.filter(
        blocker=request.user
    ).select_related("blocked_user")[:3]

    blocked_count = UserBlock.objects.filter(blocker=request.user).count()

    context = {
        "following": following,
        "followers": followers,
        "following_count": following.count(),
        "followers_count": followers.count(),
        "blocked_users_preview": blocked_users_preview,
        "blocked_count": blocked_count,
        "active_page": "subscriptions",
    }

    return render(request, "accounts/subscriptions.html", context)


@login_required
def follow_user(request, user_id):
    """
    Vue pour suivre un utilisateur

    Crée un abonnement entre l'utilisateur connecté et l'utilisateur cible
    """

    user_to_follow = get_object_or_404(User, id=user_id)

    # Validation : on ne peut pas se suivre soi-même
    if user_to_follow == request.user:
        messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect("subscriptions")

    # Vérifier si un blocage existe
    block_exists = UserBlock.objects.filter(
        Q(blocker=request.user, blocked_user=user_to_follow)
        | Q(blocker=user_to_follow, blocked_user=request.user)
    ).exists()

    if block_exists:
        messages.error(
            request, "Vous ne pouvez pas suivre cet utilisateur en raison d'un blocage."
        )
        return redirect("subscriptions")

    # Vérifier si on ne suit pas déjà cet utilisateur
    if UserFollows.objects.filter(
        user=request.user, followed_user=user_to_follow
    ).exists():
        messages.warning(request, f"Vous suivez déjà {user_to_follow.username}.")
        return redirect("subscriptions")

    # Création de l'abonnement
    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)

    messages.success(request, f"Vous suivez maintenant {user_to_follow.username} !")
    return redirect("subscriptions")


@login_required
def unfollow_user(request, user_id):
    """
    Vue pour se désabonner d'un utilisateur

    Supprime l'abonnement existant
    """

    user_to_unfollow = get_object_or_404(User, id=user_id)

    follow = UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow
    ).first()

    if follow:
        follow.delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
    else:
        messages.warning(request, f"Vous ne suiviez pas {user_to_unfollow.username}.")

    return redirect("subscriptions")


@login_required
def block_user(request, user_id):
    """
    Vue pour bloquer un utilisateur

    Crée un blocage et supprime automatiquement les abonnements mutuels
    """

    user_to_block = get_object_or_404(User, id=user_id)

    # Validation : on ne peut pas se bloquer soi-même
    if user_to_block == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect("subscriptions")

    # Vérifier si on n'a pas déjà bloqué cet utilisateur
    if UserBlock.objects.filter(
        blocker=request.user, blocked_user=user_to_block
    ).exists():
        messages.warning(request, f"Vous avez déjà bloqué {user_to_block.username}.")
        return redirect("subscriptions")

    # Création du blocage
    UserBlock.objects.create(blocker=request.user, blocked_user=user_to_block)

    messages.success(request, f"✅ Vous avez bloqué {user_to_block.username}.")
    return redirect("subscriptions")


@login_required
def unblock_user(request, user_id):
    """
    Vue pour débloquer un utilisateur

    Supprime le blocage et permet à nouveau l'interaction
    """

    user_to_unblock = get_object_or_404(User, id=user_id)

    block = UserBlock.objects.filter(
        blocker=request.user, blocked_user=user_to_unblock
    ).first()

    if block:
        block.delete()
        messages.success(request, f"Vous avez débloqué {user_to_unblock.username}.")
    else:
        messages.warning(
            request, f"Vous n'aviez pas bloqué {user_to_unblock.username}."
        )

    return redirect("subscriptions")


@login_required
def blocked_users(request):
    """
    Page affichant la liste des utilisateurs bloqués

    Permet de voir et débloquer les utilisateurs bloqués
    """

    blocked_users = UserBlock.objects.filter(blocker=request.user).select_related(
        "blocked_user"
    )

    context = {
        "blocked_users": blocked_users,
        "blocked_count": blocked_users.count(),
    }

    return render(request, "accounts/blocked_users.html", context)
