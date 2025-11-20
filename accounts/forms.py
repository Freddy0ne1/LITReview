from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()
TAILWIND_INPUT_CLASS = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"


class LoginForm(forms.Form):
    """
    Formulaire de connexion

    Contient deux champs : nom d'utilisateur et mot de passe
    """

    username = forms.CharField(
        max_length=70,
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Entrez votre nom d'utilisateur",
                "aria-required": "true",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Entrez votre mot de passe",
                "aria-required": "true",
                "autocomplete": "current-password",
            }
        ),
    )


class SignUpForm(UserCreationForm):
    """
    Formulaire d'inscription

    Hérite de UserCreationForm qui fournit les champs username,
    password1, password2 et la validation automatique
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retirer les messages d'aide par défaut (en anglais)
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

        # Personnalisation du champ nom d'utilisateur
        self.fields["username"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Choisissez un nom d'utilisateur",
                "aria-required": "true",
                "aria-describedby": "username_help",
                "autocomplete": "username",
            }
        )

        # Personnalisation du champ mot de passe
        self.fields["password1"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Créez un mot de passe sécurisé",
                "aria-required": "true",
                "aria-describedby": "password1_help",
                "autocomplete": "new-password",
            }
        )

        # Personnalisation de la confirmation du mot de passe
        self.fields["password2"].widget.attrs.update(
            {
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Confirmez votre mot de passe",
                "aria-required": "true",
                "aria-describedby": "password2_help",
                "autocomplete": "new-password",
            }
        )


class ChangePasswordForm(PasswordChangeForm):
    """
    Formulaire personnalisé de changement de mot de passe.
    Hérite de PasswordChangeForm de Django et adapte les labels,
    placeholders et styles pour une interface en français.
    """

    def __init__(self, *args, **kwargs):
        # Appel du constructeur parent pour initialiser le formulaire de base
        super().__init__(*args, **kwargs)

        # Définition des labels en français pour chaque champ
        labels = {
            "old_password": "Mot de passe actuel",
            "new_password1": "Nouveau mot de passe",
            "new_password2": "Confirmer le nouveau mot de passe",
        }

        # Définition des textes d'aide (placeholders) pour guider l'utilisateur
        placeholders = {
            "old_password": "Entrez votre mot de passe actuel",
            "new_password1": "Entrez votre nouveau mot de passe",
            "new_password2": "Confirmez votre nouveau mot de passe",
        }

        # Parcours de tous les champs du formulaire pour les personnaliser
        for field_name, field in self.fields.items():
            # Attribution du label français correspondant au champ
            field.label = labels[field_name]

            # Ajout des attributs HTML au widget du champ :
            # - classe CSS Tailwind pour le style visuel
            # - placeholder pour l'indication dans le champ vide
            field.widget.attrs.update({
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": placeholders[field_name],
            })

class ProfilePictureForm(forms.ModelForm):
    """Formulaire pour uploader/modifier la photo de profil"""

    class Meta:
        model = User
        fields = ["profile_photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du champ photo
        self.fields["profile_photo"].widget.attrs.update(
            {
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "accept": "image/*",
            }
        )

        self.fields["profile_photo"].label = "Photo de profil"
        self.fields["profile_photo"].help_text = (
            "Formats acceptés : JPG, PNG, GIF. Taille max : 5 Mo."
        )


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["follows"]