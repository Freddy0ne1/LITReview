import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from PIL import Image


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec photo de profil et rôle

    Rôles disponibles :
    - CREATOR : Peut créer des tickets et des critiques
    - SUBSCRIBER : Peut seulement consulter le contenu
    """

    # Constantes pour les rôles
    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICES = [
        (CREATOR, "Créateur"),
        (SUBSCRIBER, "Abonné"),
    ]

    # Photo de profil (optionnelle)
    profile_photo = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )

    # Rôle de l'utilisateur
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=SUBSCRIBER,
        blank=True,
        verbose_name="Rôle"
    )

    # Relation ManyToMany pour les abonnements
    follows = models.ManyToManyField(
        "self",
        through="UserFollows",
        symmetrical=False,
        related_name="followed_by",
        verbose_name="Suit"
    )

    # Taille maximale pour le redimensionnement
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        """Redimensionne l'image en conservant les proportions"""
        # Vérifier que l'image existe
        if not self.profile_photo or not self.profile_photo.name:
            return

        # Vérifier que le fichier existe physiquement
        try:
            if not os.path.exists(self.profile_photo.path):
                return
        except (ValueError, AttributeError):
            return

        # Redimensionner avec gestion d'erreurs
        try:
            profile_photo = Image.open(self.profile_photo.path)

            # Redimensionner seulement si nécessaire
            if profile_photo.height > self.IMAGE_MAX_SIZE[1] or profile_photo.width > self.IMAGE_MAX_SIZE[0]:
                profile_photo.thumbnail(self.IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)
                profile_photo.save(self.profile_photo.path)
        except Exception as e:
            print(f"Erreur lors du redimensionnement de l'image : {e}")

    def save(self, *args, **kwargs):
        """Sauvegarde et redimensionne automatiquement la photo de profil"""
        super().save(*args, **kwargs)

        # Redimensionner uniquement si une photo existe
        if self.profile_photo:
            self.resize_image()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']  # Champ natif d'AbstractUser

    def __str__(self):
        return self.username

class UserFollows(models.Model):
    """
    Modèle pour gérer les abonnements entre utilisateurs

    Représente une relation asymétrique "user suit followed_user"
    Contrainte unique : Un utilisateur ne peut suivre qu'une fois un autre

    Relations inversées :
    - user.follows.all() → Utilisateurs suivis
    - user.followed_by.all() → Abonnés (followers)
    """

    # L'utilisateur qui suit (le follower)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Utilisateur"
    )

    # L'utilisateur suivi
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Utilisateur suivi"
    )

    # Date de création de l'abonnement
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'abonnement"
    )

    class Meta:
        # Contrainte unique : évite les doublons
        unique_together = ("user", "followed_user")

        ordering = ["-created_at"]

        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"

        # Index pour améliorer les performances
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["followed_user"]),
        ]

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"

    def save(self, *args, **kwargs):
        """Empêche un utilisateur de se suivre lui-même"""
        if self.user == self.followed_user:
            raise ValueError("Un utilisateur ne peut pas se suivre lui-même.")

        super().save(*args, **kwargs)


class UserBlock(models.Model):
    """
    Modèle pour gérer le blocage d'utilisateurs

    Permet de bloquer un utilisateur pour :
    - Empêcher de voir les posts du bloqueur
    - Empêcher de suivre le bloqueur
    - Empêcher d'interagir avec les posts du bloqueur

    Le blocage supprime automatiquement les abonnements mutuels
    """

    # L'utilisateur qui bloque
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocking",
        verbose_name="Bloqueur"
    )

    # L'utilisateur bloqué
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        verbose_name="Utilisateur bloqué"
    )

    # Date du blocage
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de blocage"
    )

    # Raison du blocage (optionnelle)
    reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Raison du blocage"
    )

    class Meta:
        # Contrainte unique : impossible de bloquer deux fois la même personne
        unique_together = ("blocker", "blocked_user")

        ordering = ["-created_at"]

        verbose_name = "Blocage"
        verbose_name_plural = "Blocages"

        # Index pour améliorer les performances
        indexes = [
            models.Index(fields=["blocker"]),
            models.Index(fields=["blocked_user"]),
        ]

    def __str__(self):
        return f"{self.blocker.username} bloque {self.blocked_user.username}"

    def save(self, *args, **kwargs):
        """
        Empêche de se bloquer soi-même
        Supprime automatiquement les abonnements mutuels
        """

        # Validation : on ne peut pas se bloquer soi-même
        if self.blocker == self.blocked_user:
            raise ValueError("Un utilisateur ne peut pas se bloquer lui-même.")

        super().save(*args, **kwargs)

        # Suppression automatique des abonnements mutuels
        UserFollows.objects.filter(
            Q(user=self.blocker, followed_user=self.blocked_user) |
            Q(user=self.blocked_user, followed_user=self.blocker)
        ).delete()