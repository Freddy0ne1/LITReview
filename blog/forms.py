# blog/forms.py
from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class PhotoForm(forms.ModelForm):
    """
    Formulaire pour uploader une photo

    Permet d'uploader une image avec une légende optionnelle
    """

    class Meta:
        model = models.Photo
        fields = ["image", "caption"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du champ image
        self.fields["image"].widget.attrs.update({
            "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500",
            "accept": "image/*"
        })

        # Personnalisation du champ légende
        self.fields["caption"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Décrivez votre photo...",
            "rows": 3
        })

        # Labels et aides
        self.fields["image"].label = "Image"
        self.fields["caption"].label = "Légende"
        self.fields["image"].help_text = "Formats acceptés : JPG, PNG, GIF. Taille max : 5 Mo."
        self.fields["caption"].help_text = "Décrivez brièvement cette image (optionnel)."


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une demande de critique

    Permet de demander l'avis de la communauté sur un livre ou article
    """

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True, required=False)

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du titre
        self.fields["title"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Ex: Besoin d'avis sur \"1984\" de George Orwell"
        })

        # Personnalisation de la description
        self.fields["description"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Décrivez le type de critique que vous recherchez...",
            "rows": 8
        })

        # Personnalisation de l'image
        self.fields["image"].widget.attrs.update({
            "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500",
            "accept": "image/*"
        })

        # Labels et aides
        self.fields["title"].label = "Titre de la demande"
        self.fields["description"].label = "Description"
        self.fields["image"].label = "Image (optionnel)"
        self.fields["title"].help_text = "Donnez un titre court et clair (max 128 caractères)."
        self.fields["description"].help_text = "Expliquez quel type de critique vous recherchez (max 2048 caractères)."
        self.fields["image"].help_text = "Ajoutez une image de couverture pour illustrer votre demande (optionnel)."


class DeleteTicketForm(forms.Form):
    """Formulaire de confirmation pour supprimer un ticket"""
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class BlogForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un article de blog

    Permet d'écrire une critique avec un titre et un contenu détaillé
    """

    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du titre
        self.fields["title"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Titre de votre critique..."
        })

        # Personnalisation du contenu
        self.fields["content"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Partagez votre avis détaillé sur ce livre ou cet article...",
            "rows": 10
        })

        # Labels et aides
        self.fields['title'].label = "Titre de la critique"
        self.fields['content'].label = "Votre critique"
        self.fields['title'].help_text = "Donnez un titre accrocheur à votre critique (max 200 caractères)."
        self.fields[
            'content'].help_text = "Développez votre avis, vos impressions et vos recommandations (max 5000 caractères)."


class DeleteBlogForm(forms.Form):
    """Formulaire de confirmation pour supprimer un article de blog"""
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une critique

    Permet de noter un livre/article de 0 à 5 étoiles
    avec un titre et un avis détaillé
    """

    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True, required=False)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

        # Widget RadioSelect pour la note en étoiles
        widgets = {
            'rating': forms.RadioSelect(
                choices=[
                    (0, '0 - Aucune étoile'),
                    (1, '1 - ★'),
                    (2, '2 - ★★'),
                    (3, '3 - ★★★'),
                    (4, '4 - ★★★★'),
                    (5, '5 - ★★★★★'),
                ]
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du titre de la critique
        self.fields['headline'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Titre de votre critique'
        })

        # Personnalisation du contenu de la critique
        self.fields['body'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Partagez votre avis détaillé...',
            'rows': 10
        })

        # Labels
        self.fields['headline'].label = "Titre de votre critique"
        self.fields['rating'].label = "Note"
        self.fields['body'].label = "Votre avis détaillé"


class DeleteReviewForm(forms.Form):
    """Formulaire de confirmation pour supprimer une critique"""
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)