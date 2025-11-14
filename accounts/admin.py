from django.contrib import admin
from .models import User, UserFollows


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les abonnements"""
    list_display = ("user", "followed_user", "created_at")
    list_filter = ("user", "followed_user", "created_at")
    search_fields = ("user__username", "followed_user__username")

class UserAdmin(admin.ModelAdmin):
    """Liste des utilisateurs"""
    list_display = ("username", "last_login", "date_joined", "is_staff")



admin.site.register(User, UserAdmin)