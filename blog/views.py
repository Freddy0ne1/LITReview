from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from accounts.models import UserBlock
from . import models, forms


@login_required
def ticket_create(request):
    """
    Vue pour créer une demande de critique (ticket)

    Permet de demander l'avis de la communauté sur un livre ou un article
    """

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            messages.success(
                request, "Votre demande de critique a été publiée avec succès !"
            )
            return redirect("feed")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = forms.TicketForm()

    return render(request, "blog/ticket_create.html", {"form": form})


@login_required
def ticket_and_review_create(request):
    """
    Vue pour créer un ticket et une critique en même temps

    Permet de créer simultanément :
    - Un ticket décrivant un livre/article
    - Une critique avec note de 0 à 5 étoiles

    Utilise une transaction atomique (tout ou rien)
    """

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            # Création du ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Création de la critique liée au ticket
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(
                request, "Votre critique a été publiée avec succès !"
            )
            return redirect("feed")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    return render(
        request,
        "blog/ticket_review_create.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def user_posts(request):
    """
    Vue pour afficher tous les posts de l'utilisateur connecté

    Organisés en trois catégories :
    1. Tickets créés
    2. Critiques créées
    3. Critiques reçues sur les tickets de l'utilisateur
    """

    user_tickets = models.Ticket.objects.filter(user=request.user).order_by(
        "-time_created"
    )
    user_reviews = models.Review.objects.filter(user=request.user).order_by(
        "-time_created"
    )

    # Critiques reçues (écrites par d'autres utilisateurs)
    reviews_received = (
        models.Review.objects.filter(ticket__user=request.user)
        .exclude(user=request.user)
        .order_by("-time_created")
    )

    context = {
        "user_tickets": user_tickets,
        "user_reviews": user_reviews,
        "reviews_received": reviews_received,
        "active_page": "user_posts",
    }

    return render(request, "blog/user_posts.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    """Vue pour modifier un ticket"""

    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    # Vérification : seul l'auteur peut modifier
    if ticket.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce ticket.")
        return redirect("feed")

    if request.method == "POST":
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Votre ticket a été modifié avec succès !")
            return redirect("user_posts")
    else:
        edit_form = forms.TicketForm(instance=ticket)

    context = {
        "edit_form": edit_form,
        "ticket": ticket,
    }

    return render(request, "blog/edit_ticket.html", context=context)


@login_required
def edit_review(request, review_id):
    """Vue pour modifier ou supprimer une critique"""

    review = get_object_or_404(models.Review, id=review_id)

    # Vérification : seul l'auteur peut modifier
    if review.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette critique.")
        return redirect("feed")

    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteConfirmForm()

    if request.method == "POST":
        # Action : Modifier la critique
        if "edit_review" in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Votre critique a été modifiée avec succès !")
                return redirect("user_posts")

        # Action : Supprimer la critique
        elif "delete_review" in request.POST:
            delete_form = forms.DeleteConfirmForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                messages.success(request, "Votre critique a été supprimée.")
                return redirect("user_posts")

    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
        "review": review,
    }

    return render(request, "blog/edit_review.html", context=context)


@login_required
def review_create(request, ticket_id):
    """
    Vue pour créer une critique en réponse à un ticket existant

    Vérifie qu'il n'y a pas de blocage avec l'auteur du ticket
    et que l'utilisateur n'a pas déjà répondu
    """

    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    # Vérifier si un blocage existe avec l'auteur du ticket
    block_exists = UserBlock.objects.filter(
        Q(blocker=request.user, blocked_user=ticket.user)
        | Q(blocker=ticket.user, blocked_user=request.user)
    ).exists()

    if block_exists:
        messages.error(
            request, "Vous ne pouvez pas répondre à ce ticket en raison d'un blocage."
        )
        return redirect("feed")

    # Vérifier si l'utilisateur a déjà répondu
    existing_review = models.Review.objects.filter(
        ticket=ticket, user=request.user
    ).first()
    if existing_review:
        messages.warning(request, "Vous avez déjà publié une critique pour ce ticket.")
        return redirect("feed")

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Votre critique a été publiée avec succès !")
            return redirect("feed")
    else:
        review_form = forms.ReviewForm()

    return render(
        request,
        "blog/review_create.html",
        {"review_form": review_form, "ticket": ticket},
    )


@login_required
def delete_ticket(request, ticket_id):
    """
    Vue pour supprimer un ticket

    Supprime également toutes les critiques associées (CASCADE)
    Seul l'auteur peut supprimer son ticket
    """

    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    # Vérification : seul l'auteur peut supprimer
    if ticket.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce ticket.")
        return redirect("user_posts")

    ticket_title = ticket.title
    ticket.delete()

    messages.success(request, f"Le ticket '{ticket_title}' a été supprimé avec succès.")
    return redirect("user_posts")


@login_required
def delete_review(request, review_id):
    """
    Vue pour supprimer une critique

    Seul l'auteur peut supprimer sa critique
    """

    review = get_object_or_404(models.Review, id=review_id)

    # Vérification : seul l'auteur peut supprimer
    if review.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette critique.")
        return redirect("user_posts")

    review_headline = review.headline
    review.delete()

    messages.success(
        request, f"La critique '{review_headline}' a été supprimée avec succès."
    )
    return redirect("user_posts")
