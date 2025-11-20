import os
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PIL import Image


class Photo(models.Model):
    """
    Modèle pour stocker les photos uploadées par les utilisateurs

    Les photos sont automatiquement redimensionnées à 800x800 pixels max
    pour optimiser le stockage et les performances
    """

    # Fichier image (stocké dans MEDIA_ROOT/photos/)
    image = models.ImageField(upload_to="photos/", verbose_name="Image")

    # Légende optionnelle
    caption = models.CharField(max_length=128, blank=True, verbose_name="Légende")

    # Utilisateur qui a uploadé la photo
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Uploadeur"
    )

    # Date de création (automatique)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    # Taille maximale pour le redimensionnement
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        """Redimensionne l'image en conservant les proportions"""
        # Vérifier que l'image existe avant de la redimensionner
        if not self.image or not self.image.name:
            return  # Sortir si pas d'image

        # Vérifier que le fichier existe physiquement
        try:
            if not os.path.exists(self.image.path):
                return
        except (ValueError, AttributeError):
            return

        try:
            image = Image.open(self.image.path)

            # Vérifier si le redimensionnement est nécessaire
            if image.height > IMAGE_MAX_SIZE[1] or image.width > IMAGE_MAX_SIZE[0]:
                image.thumbnail(IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)
                image.save(self.image.path)
        except Exception as e:
            # Ne pas bloquer la sauvegarde en cas d'erreur
            print(f"Erreur lors du redimensionnement de l'image : {e}")

    def save(self, *args, **kwargs):
        """Sauvegarde la photo et la redimensionne automatiquement"""
        super().save(*args, **kwargs)

        # ⭐ CORRECTION : Redimensionner uniquement si une image existe
        if self.image:
            self.resize_image()

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def __str__(self):
        return f"Photo de {self.uploader.username} - {self.date_created.strftime('%d/%m/%Y')}"


class Blog(models.Model):
    """
    Modèle pour les articles de blog (critiques de livres)

    Un article contient un titre, un contenu, une photo optionnelle
    et peut être marqué comme favori
    """

    # Photo associée (optionnelle)
    photo = models.ForeignKey(
        Photo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Photo"
    )

    # Titre de l'article
    title = models.CharField(max_length=200, verbose_name="Titre")

    # Contenu de la critique
    content = models.TextField(max_length=5000, verbose_name="Contenu")

    # Auteur de l'article
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur"
    )

    # Date de création (automatique)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    # Marqué comme favori
    starred = models.BooleanField(default=False, verbose_name="Article favori")

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"

    def __str__(self):
        return f"{self.title} par {self.author.username}"


class Ticket(models.Model):
    """
    Modèle pour une demande de critique

    Permet à un utilisateur de demander l'avis de la communauté
    sur un livre ou un article
    """

    # Titre de la demande
    title = models.CharField(max_length=128, verbose_name="Titre")

    # Description détaillée
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="Description"
    )

    # Utilisateur qui demande la critique
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur"
    )

    # Image optionnelle (couverture du livre)
    image = models.ImageField(
        upload_to="tickets/", null=True, blank=True, verbose_name="Image"
    )

    # Date de création (automatique)
    time_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Demande de critique"
        verbose_name_plural = "Demandes de critique"

    def __str__(self):
        return f"Ticket: {self.title} par {self.user.username}"


class Review(models.Model):
    """
    Modèle pour une critique (réponse à un ticket)

    Une critique contient une note de 0 à 5 étoiles,
    un titre et un commentaire détaillé
    """

    # Choix pour la note
    RATING_CHOICES = [
        (0, "0 - Aucune étoile"),
        (1, "1 - ★"),
        (2, "2 - ★★"),
        (3, "3 - ★★★"),
        (4, "4 - ★★★★"),
        (5, "5 - ★★★★★"),
    ]

    # Ticket auquel cette critique répond
    ticket = models.ForeignKey(
        "Ticket", on_delete=models.CASCADE, verbose_name="Ticket"
    )

    # Note de 0 à 5 étoiles
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note"
    )

    # Utilisateur qui a écrit la critique
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur"
    )

    # Titre de la critique
    headline = models.CharField(max_length=128, verbose_name="Titre")

    # Contenu de la critique
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")

    # Date de création (automatique)
    time_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"

    def __str__(self):
        return f"Critique de {self.user.username} - Note: {self.rating}/5"
