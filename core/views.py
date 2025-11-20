from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Value, CharField

from accounts.models import UserFollows, UserBlock
from blog.models import Ticket, Review


def home_page(request):
    """
    Page d'accueil publique

    Redirige les utilisateurs connectés vers leur flux
    Affiche la landing page pour les visiteurs
    """

    if request.user.is_authenticated:
        return redirect("feed")

    return render(request, "core/home.html")


@login_required
def feed_page(request):
    """
    Page du flux pour les utilisateurs connectés

    Affiche :
    - Les tickets et critiques des utilisateurs suivis
    - Les propres tickets et critiques de l'utilisateur
    - Les critiques en réponse aux tickets de l'utilisateur

    Exclut les utilisateurs bloqués (bidirectionnel)
    """

    # Récupération des utilisateurs suivis
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list('followed_user', flat=True)

    # Récupération des utilisateurs bloqués (bidirectionnel)
    # 1. Utilisateurs que j'ai bloqués
    blocked_by_me = UserBlock.objects.filter(
        blocker=request.user
    ).values_list('blocked_user_id', flat=True)

    # 2. Utilisateurs qui m'ont bloqué
    blocked_me = UserBlock.objects.filter(
        blocked_user=request.user
    ).values_list('blocker_id', flat=True)

    # Combine les deux listes (set supprime les doublons)
    blocked_ids = set(blocked_by_me) | set(blocked_me)

    # Récupération des tickets (demandes de critique)
    tickets = Ticket.objects.filter(
        Q(user=request.user) |  # Mes tickets
        Q(user__in=followed_users)  # Tickets des utilisateurs suivis
    ).exclude(
        user__id__in=blocked_ids  # Exclut les utilisateurs bloqués
    ).annotate(
        content_type=Value('TICKET', output_field=CharField())
    )

    # Récupération des critiques
    reviews = Review.objects.filter(
        Q(user=request.user) |  # Mes critiques
        Q(user__in=followed_users) |  # Critiques des utilisateurs suivis
        Q(ticket__user=request.user)  # Critiques sur mes tickets
    ).exclude(
        user__id__in=blocked_ids  # Exclut les utilisateurs bloqués
    ).annotate(
        content_type=Value('REVIEW', output_field=CharField())
    )

    # Combine tickets et critiques dans un seul flux
    combined_posts = chain(tickets, reviews)

    # Trie par date (plus récent en premier)
    posts = sorted(
        combined_posts,
        key=lambda post: post.time_created,
        reverse=True
    )

    # Pour chaque ticket, vérifie si l'utilisateur a déjà répondu
    # et si l'auteur est bloqué
    for post in posts:
        if post.content_type == "TICKET":
            # Cherche une critique existante de l'utilisateur pour ce ticket
            post.user_review = Review.objects.filter(
                ticket=post,
                user=request.user
            ).first()

            # Vérifie si l'auteur du ticket est bloqué
            post.is_blocked = post.user.id in blocked_ids

    # Vérifie si l'utilisateur suit au moins une personne
    has_following = UserFollows.objects.filter(user=request.user).exists()

    context = {
        "posts": posts,
        "has_following": has_following,
        "active_page": "feed",
    }

    return render(request, "core/feed.html", context)