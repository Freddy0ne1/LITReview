from django.urls import path
from blog import views


urlpatterns = [
    # Tickets
    path("ticket/create/", views.ticket_create, name="ticket_create"),
    path("ticket/<int:ticket_id>/edit/", views.edit_ticket, name="edit_ticket"),
    path("ticket/<int:ticket_id>/delete/", views.delete_ticket, name="delete_ticket"),
    # Reviews
    path("ticket/<int:ticket_id>/review/", views.review_create, name="review_create"),
    path("review/create/", views.ticket_and_review_create, name="ticket_review_create"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    # Posts utilisateur
    path("mes-posts/", views.user_posts, name="user_posts"),
]
