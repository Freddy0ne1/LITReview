from django.contrib import admin
from .models import Photo, Blog, Ticket, Review


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("uploader", "caption", "date_created")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_created", "starred")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les demandes de critique"""
    list_display = ("title", "description", "user", "time_created")
    list_filter = ("time_created", "user")
    search_fields = ("title", "description", "user__username")
    readonly_fields = ("time_created",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "body", "rating", "time_created")



