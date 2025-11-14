from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """
    Formulaire de connexion

    Contient deux champs : nom d'utilisateur et mot de passe
    """

    username = forms.CharField(
        max_length=70,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Entrez votre nom d'utilisateur",
            "aria-required": "true",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Entrez votre mot de passe",
            "aria-required": "true",
            "autocomplete": "current-password",
        })
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
        self.fields["username"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Choisissez un nom d'utilisateur",
            "aria-required": "true",
            "aria-describedby": "username_help",
            "autocomplete": "username",
        })

        # Personnalisation du champ mot de passe
        self.fields['password1'].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Créez un mot de passe sécurisé",
            "aria-required": "true",
            "aria-describedby": "password1_help",
            "autocomplete": "new-password",
        })

        # Personnalisation de la confirmation du mot de passe
        self.fields['password2'].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Confirmez votre mot de passe",
            "aria-required": "true",
            "aria-describedby": "password2_help",
            "autocomplete": "new-password",
        })


class ChangePasswordForm(PasswordChangeForm):
    """
    Formulaire de changement de mot de passe

    Hérite de PasswordChangeForm qui fournit les champs old_password,
    new_password1, new_password2 et la validation automatique
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retirer les messages d'aide par défaut
        self.fields["old_password"].help_text = None
        self.fields["new_password1"].help_text = None
        self.fields["new_password2"].help_text = None

        # Labels en français
        self.fields["old_password"].label = "Mot de passe actuel"
        self.fields["new_password1"].label = "Nouveau mot de passe"
        self.fields["new_password2"].label = "Confirmer le nouveau mot de passe"

        # Personnalisation du mot de passe actuel
        self.fields["old_password"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Entrez votre mot de passe actuel"
        })

        # Personnalisation du nouveau mot de passe
        self.fields["new_password1"].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Entrez votre nouveau mot de passe"
        })

        # Personnalisation de la confirmation
        self.fields['new_password2'].widget.attrs.update({
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Confirmez votre nouveau mot de passe"
        })


class ProfilePictureForm(forms.ModelForm):
    """Formulaire pour uploader/modifier la photo de profil"""

    class Meta:
        model = User
        fields = ["profile_photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du champ photo
        self.fields["profile_photo"].widget.attrs.update({
            "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500",
            "accept": "image/*"
        })

        self.fields["profile_photo"].label = "Photo de profil"
        self.fields["profile_photo"].help_text = "Formats acceptés : JPG, PNG, GIF. Taille max : 5 Mo."