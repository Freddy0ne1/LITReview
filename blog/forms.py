# blog/forms.py
from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()
TAILWIND_INPUT_CLASS = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
TAILWIND_FILE_CLASS = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une demande de critique

    Permet de demander l'avis de la communauté sur un livre ou article
    """

    edit_ticket = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du titre
        self.fields["title"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": 'Ex: Besoin d\'avis sur "1984" de George Orwell',
            }
        )

        # Personnalisation de la description
        self.fields["description"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Décrivez le type de critique que vous recherchez...",
                "rows": 8,
            }
        )

        # Personnalisation de l'image
        self.fields["image"].widget.attrs.update(
            {
                "class": TAILWIND_FILE_CLASS,
                "accept": "image/*",
            }
        )

        # Labels et aides
        self.fields["title"].label = "Titre de la demande"
        self.fields["description"].label = "Description"
        self.fields["image"].label = "Image (optionnel)"
        self.fields["title"].help_text = (
            "Donnez un titre court et clair (max 128 caractères)."
        )
        self.fields["description"].help_text = (
            "Expliquez quel type de critique vous recherchez (max 2048 caractères)."
        )
        self.fields["image"].help_text = (
            "Ajoutez une image de couverture pour illustrer votre demande (optionnel)."
        )


class DeleteConfirmForm(forms.Form):
    """Formulaire générique de confirmation de suppression"""

    confirm_delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une critique

    Permet de noter un livre/article de 0 à 5 étoiles
    avec un titre et un avis détaillé
    """

    edit_review = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]

        # Widget RadioSelect pour la note en étoiles
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (0, "- 0"),
                    (1, "- 1"),
                    (2, "- 2"),
                    (3, "- 3"),
                    (4, "- 4"),
                    (5, "- 5"),
                ]
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du titre de la critique
        self.fields["headline"].widget.attrs.update(
            {"class": TAILWIND_INPUT_CLASS, "placeholder": "Titre de votre critique"}
        )

        # Personnalisation du contenu de la critique
        self.fields["body"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Partagez votre avis détaillé...",
                "rows": 10,
            }
        )

        # Labels
        self.fields["headline"].label = "Titre de votre critique"
        self.fields["rating"].label = "Note"
        self.fields["body"].label = "Votre avis détaillé"
