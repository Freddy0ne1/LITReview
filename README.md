# 📚 LITReview

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-5.1.3-green.svg)
![Tailwind](https://img.shields.io/badge/tailwind-3.0+-38B2AC.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)

**LITReview** est une application web communautaire permettant aux utilisateurs de demander et publier des critiques de livres et d'articles.

---

## 🎯 Fonctionnalités principales

### Pour les utilisateurs
- ✅ **Créer des tickets** : Demander une critique sur un livre ou article
- ✅ **Publier des critiques** : Répondre aux demandes avec une note (0-5 étoiles) et un commentaire
- ✅ **Créer ticket + critique** : Publier une critique complète en une seule fois
- ✅ **Gérer ses posts** : Modifier ou supprimer ses propres tickets et critiques
- ✅ **Flux personnalisé** : Voir les publications des utilisateurs suivis

### Gestion des abonnements
- 👥 **Suivre des utilisateurs** : S'abonner pour voir leurs publications
- 🔍 **Recherche** : Trouver des utilisateurs par leur nom
- 📋 **Voir ses abonnements** : Liste des utilisateurs suivis et des abonnés
- 🚫 **Bloquer des utilisateurs** : Empêcher l'interaction avec certains utilisateurs

### Sécurité et confidentialité
- 🔒 **Système de blocage bidirectionnel** : Les utilisateurs bloqués ne voient pas vos posts et vice-versa
- ✅ **Authentification requise** : Toutes les fonctionnalités nécessitent une connexion
- 🛡️ **Autorisations** : Seul l'auteur peut modifier/supprimer son contenu

---

## 🚀 Installation

### Prérequis
- **Python 3.8+** (version recommandée : 3.11)
- **pip** (gestionnaire de paquets Python)
- **Git**
- **Node.js 16+** (requis pour Tailwind CSS)

> ⚠️ **Note importante** : Ce projet utilise Tailwind CSS, il est donc indispensable d'avoir Node.js installé.

---

### Étapes d'installation

#### 1. Installer Node.js

Téléchargez et installez Node.js depuis le site officiel :  
👉 **https://nodejs.org/fr/download**

Vérifiez l'installation :
```bash
node --version
npm --version
```

---

#### 2. Cloner le projet

```bash
git clone https://github.com/Freddy0ne1/LITReview.git
cd LITReview
```

---

#### 3. Créer un environnement virtuel

**Windows :**
```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux :**
```bash
python3 -m venv env
source env/bin/activate
```

> 💡 **Astuce** : Vous pouvez aussi créer l'environnement virtuel directement depuis votre IDE (PyCharm, VS Code, etc.)

---

#### 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```


---

#### 5. Créer un superutilisateur (optionnel)

Pour accéder à l'interface d'administration Django :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte administrateur.

---

#### 6. Installer les dépendances Tailwind CSS

```bash
python manage.py tailwind install
```

**⚠️ Si vous obtenez une erreur** du type :
```
CommandError: 
It looks like node.js and/or npm is not installed or cannot be found.
```

**Solution :** Configurez le chemin vers npm dans `config/settings.py`

##### 7a. Trouvez le chemin d'installation de npm

**Windows :**
```bash
where npm
```

**macOS/Linux :**
```bash
which npm
```

##### 7b. Modifiez `config/settings.py`

Allez en bas du fichier et décommentez/modifiez la ligne appropriée :

```python
# En cas d'erreur pour la détection de Node.js (Windows)
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# En cas d'erreur pour la détection de Node.js (Mac et Linux)
# NPM_BIN_PATH = "/usr/local/bin/npm"
```

##### 7c. Relancez l'installation

```bash
python manage.py tailwind install
```

---

#### 8. Lancer le serveur de développement Tailwind

⚠️ **Important** : Gardez ce terminal ouvert pendant tout le développement

```bash
python manage.py tailwind start
```

Vous devriez voir :
```
--watch
```

---

#### 9. Lancer le serveur Django

⚠️ **Important** : Ouvrez un **NOUVEAU terminal**, activez l'environnement virtuel, puis lancez :

**Windows :**
```bash
env\Scripts\activate
python manage.py runserver
```

**macOS/Linux :**
```bash
source env/bin/activate
python manage.py runserver
```

---

#### 10. Accéder à l'application

Ouvrez votre navigateur et allez sur :  
👉 **http://127.0.0.1:8000**

Pour accéder à l'admin Django :  
👉 **http://127.0.0.1:8000/admin**

---

## 🎬 Premiers pas

Une fois l'installation terminée :

1. **Créez quelques utilisateurs de test** via l'interface d'inscription
2. **Testez les abonnements** : Suivez d'autres utilisateurs
3. **Créez votre premier ticket** : Demandez une critique sur un livre
4. **Publiez une critique** : Répondez à un ticket avec votre avis

### 💡 Suggestion : Créez des comptes de démonstration

Pour tester les interactions entre utilisateurs :

```
Utilisateur 1
- Username: alice
- Password: Test1234!

Utilisateur 2
- Username: bob
- Password: Test1234!
```

Vous pourrez ainsi tester les abonnements, les blocages, et voir le flux personnalisé de chaque utilisateur.

---

## 📂 Structure du projet

```
LITReview/
│
├── accounts/                 # Gestion des utilisateurs
│   ├── models.py             # User, UserFollows, UserBlock
│   ├── views.py              # Connexion, inscription, abonnements, blocages
│   ├── forms.py              # Formulaires utilisateur
│   └── templates/            # Templates de l'app accounts
│       └── accounts/
│           ├── includes/     # Modales réutilisables
│           │   ├── block_modal.html
│           │   ├── unblock_modal.html
│           │   └── unfollow_modal.html
│           ├── blocked_users.html
│           ├── login.html
│           ├── signup.html
│           └── subscriptions.html
│
├── blog/                     # Contenu de l'application
│   ├── models.py             # Ticket, Review, Blog, Photo
│   ├── views.py              # CRUD tickets et critiques
│   ├── forms.py              # Formulaires de contenu
│   └── templates/            # Templates de l'app blog
│       └── blog/
│           ├── includes/     # Modales de suppression
│           │   ├── delete_ticket_modal.html
│           │   └── delete_review_modal.html
│           ├── ticket_create.html
│           ├── review_create.html
│           ├── edit_ticket.html
│           └── user_posts.html
│
├── config/                   # Configuration Django
│   ├── settings.py           # Paramètres du projet
│   ├── urls.py               # URLs racine
│   └── wsgi.py               # Configuration WSGI
│
├── core/                     # Pages principales
│   ├── views.py              # Page d'accueil, flux
│   └── templates/            # Templates de base
│       └── core/
│           ├── base.html     # Template de base
│           ├── feed.html     # Flux principal
│           └── home.html     # Page d'accueil
│
├── media/                    # Fichiers uploadés par les utilisateurs
│   ├── profile_pics/         # Photos de profil
│   ├── photos/               # Photos uploadées
│   └── tickets/              # Images des tickets
│
├── static/                   # Fichiers statiques globaux
│   └── js/
│       └── modals.js         # JavaScript des modales
│
├── theme/                    # Application Tailwind CSS
│   ├── static/               # CSS compilé
│   ├── static_src/           # Sources Tailwind
│   └── templates/            # Templates Tailwind
│
├── manage.py                 # Script de gestion Django
├── requirements.txt          # Dépendances Python
├── db.sqlite3                # Base de données (généré après migration)
└── README.md                 # Ce fichier
```

---

## 🎨 Technologies utilisées

### Backend
- **Django 5.1.3** : Framework web Python
- **SQLite** : Base de données (développement)
- **Pillow** : Traitement d'images

### Frontend
- **HTML5** : Structure des pages
- **Tailwind CSS 3.0+** : Framework CSS utility-first
- **JavaScript ES6** : Modales et interactions

### Outils de développement
- **django-tailwind** : Intégration de Tailwind dans Django
- **Django-Browser-Reload** : Rechargement automatique du navigateur

---

## 📖 Guide d'utilisation

### 1. Créer un compte
1. Sur la page d'accueil, cliquez sur **"S'inscrire"**
2. Remplissez le formulaire d'inscription
3. Connectez-vous avec vos identifiants

### 2. Suivre des utilisateurs
1. Allez dans **"Abonnements"** dans le menu de navigation
2. Utilisez la barre de recherche pour trouver un utilisateur par son nom
3. Cliquez sur **"Envoyer"** pour vous abonner
4. L'utilisateur apparaîtra dans votre liste d'abonnements

### 3. Demander une critique
1. Dans le flux, cliquez sur **"💬 Demander une critique"**
2. Remplissez le formulaire :
   - **Titre** : Nom du livre ou de l'article
   - **Description** : Présentez brièvement le contenu
   - **Image** (optionnel) : Ajoutez une couverture
3. Cliquez sur **"Publier le ticket"**

### 4. Publier une critique

#### Option A : Répondre à un ticket existant
1. Dans le flux, trouvez un ticket qui vous intéresse
2. Cliquez sur **"Créer une critique →"**
3. Donnez votre avis :
   - **Note** : 0 à 5 étoiles
   - **Titre** : Résumez votre opinion
   - **Commentaire** : Développez votre critique
4. Cliquez sur **"Publier la critique"**

#### Option B : Créer ticket + critique en une fois
1. Dans le flux, cliquez sur **"📝 Créer une critique"**
2. Remplissez les informations du livre (section 1)
3. Remplissez votre critique (section 2)
4. Cliquez sur **"Publier la critique"** pour tout publier en une fois

### 5. Gérer vos publications
1. Allez dans **"Vos posts"** dans le menu
2. Vous voyez tous vos tickets et critiques
3. Actions disponibles :
   - **✏️ Modifier** : Modifier le contenu
   - **🗑️ Supprimer** : Supprimer définitivement (avec confirmation)

### 6. Bloquer un utilisateur
1. Dans **"Abonnements"**, trouvez l'utilisateur dans votre liste
2. Cliquez sur **"🚫 Bloquer"**
3. Confirmez le blocage
4. **Effets du blocage :**
   - Vous ne voyez plus ses posts
   - Il ne voit plus vos posts
   - Les abonnements mutuels sont supprimés automatiquement
   - Vous ne pouvez plus vous suivre mutuellement
5. Pour **débloquer** : Allez dans **"Utilisateurs bloqués"** et cliquez sur **"Débloquer"**

---

## 🗂️ Modèles de données

### User (accounts/models.py)
```python
- username          # Nom d'utilisateur (unique)
- profile_photo     # Photo de profil (optionnel)
- role              # Rôle (Creator / Subscriber)
```

### UserFollows (accounts/models.py)
```python
- user              # Utilisateur qui suit
- followed_user     # Utilisateur suivi
- created_at        # Date d'abonnement
```

### UserBlock (accounts/models.py)
```python
- blocker           # Utilisateur qui bloque
- blocked_user      # Utilisateur bloqué
- created_at        # Date de blocage
- reason            # Raison (optionnel)
```

### Ticket (blog/models.py)
```python
- title             # Titre du livre/article
- description       # Description
- user              # Auteur du ticket
- image             # Image de couverture (optionnel)
- time_created      # Date de création
```

### Review (blog/models.py)
```python
- ticket            # Ticket associé
- rating            # Note (0-5)
- headline          # Titre de la critique
- body              # Commentaire détaillé
- user              # Auteur de la critique
- time_created      # Date de création
```

---

## 🎯 Fonctionnalités avancées

### Système de blocage bidirectionnel

Quand Alice bloque Bob :
- ❌ Alice ne voit plus les posts de Bob
- ❌ Bob ne voit plus les posts d'Alice
- ❌ Les abonnements mutuels sont supprimés automatiquement
- ❌ Impossible de se suivre mutuellement
- ✅ Le blocage est réversible (déblocage possible)

### Flux personnalisé intelligent

Le flux affiche intelligemment :
- ✅ Vos propres tickets et critiques
- ✅ Les tickets et critiques des utilisateurs suivis
- ✅ Les critiques en réponse à **vos** tickets (même si l'auteur n'est pas suivi)
- ❌ Aucun contenu des utilisateurs bloqués (bidirectionnel)

**Exemple** : Si Bob répond à votre ticket, vous verrez sa critique même si vous ne le suivez pas.

### Modales de confirmation

Toutes les actions destructives nécessitent une double confirmation via modale :
- 🗑️ Suppression de ticket (avec avertissement : supprime aussi les critiques associées)
- 🗑️ Suppression de critique
- 🚫 Blocage d'utilisateur (avec explication des conséquences)
- ❌ Désabonnement

**Avantages** :
- Évite les suppressions accidentelles
- Interface plus professionnelle que `confirm()` JavaScript
- Accessible au clavier (Escape pour fermer)

---

## 🐛 Dépannage

### Problème : "ModuleNotFoundError"
**Cause** : Les dépendances ne sont pas installées ou l'environnement virtuel n'est pas activé

**Solution** :
```bash
# Activez l'environnement virtuel
env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux

# Installez les dépendances
pip install -r requirements.txt
```

---

### Problème : "No such table"
**Cause** : Les migrations n'ont pas été effectuées

**Solution** :
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Problème : Tailwind ne compile pas
**Cause** : Node.js n'est pas installé ou le chemin npm n'est pas configuré

**Solution** :
```bash
# Vérifiez que Node.js est installé
node --version
npm --version

# Si installé mais erreur persiste, configurez NPM_BIN_PATH dans settings.py
```

---

### Problème : Les styles ne s'appliquent pas
**Cause** : Le serveur Tailwind ne tourne pas en arrière-plan

**Solution** :
```bash
# Dans un terminal séparé, lancez :
python manage.py tailwind start

# Laissez ce terminal ouvert
```

---

### Problème : Les images ne s'affichent pas
**Cause** : Configuration media incorrecte

**Solution** : Vérifiez dans `settings.py` :
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Et dans `urls.py` (en développement) :
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---


## 📜 Licence

Ce projet est développé dans le cadre d'un projet éducatif **OpenClassrooms**.

**Usage** : Éducatif uniquement

---

## 👤 Auteur

**Freddy KHUTI**
- 🐙 GitHub : [@Freddy0ne1](https://github.com/Freddy0ne1)
- 📧 Email : freddykhuti@gmail.com
- 🎓 Formation : Développeur d'application Python - OpenClassrooms

---

## 🙏 Remerciements

- **OpenClassrooms** pour le projet éducatif et l'accompagnement
- **Django Software Foundation** pour le framework web exceptionnel
- **Tailwind Labs** pour le framework CSS utility-first
- **La communauté open source** pour les nombreuses ressources et la documentation
- **Tous les contributeurs** qui ont partagé leurs connaissances sur Youtube 


---

## 🔄 Changelog

### Version 1.0.0 (Novembre 2025)

#### Fonctionnalités principales
- ✅ Système d'authentification complet (inscription, connexion, déconnexion)
- ✅ Gestion des profils utilisateurs avec photo
- ✅ Création et gestion de tickets (demandes de critique)
- ✅ Création et gestion de critiques (notes + commentaires)
- ✅ Création combinée ticket + critique

#### Système social
- ✅ Système d'abonnements (suivre/se désabonner)
- ✅ Recherche d'utilisateurs par nom
- ✅ Système de blocage bidirectionnel
- ✅ Gestion des utilisateurs bloqués

#### Interface utilisateur
- ✅ Flux personnalisé avec filtrage intelligent
- ✅ Modales de confirmation pour actions destructives
- ✅ Design responsive avec Tailwind CSS
- ✅ Accessibilité WCAG compliant
- ✅ Navigation intuitive

#### Sécurité
- ✅ Authentification requise pour toutes les actions
- ✅ Autorisations granulaires (seul l'auteur peut modifier/supprimer)
- ✅ Protection CSRF
- ✅ Validation des formulaires côté serveur

#### Performance et qualité
- ✅ Optimisation des requêtes (select_related, prefetch_related)
- ✅ Gestion efficace des fichiers média
- ✅ Code commenté et documenté
- ✅ Architecture modulaire et maintenable

---

## 🚀 Roadmap (Fonctionnalités futures)

### Version 1.1.0 (Prévu)
- 📧 Notifications par email
- 🔔 Système de notifications en temps réel
- 💬 Commentaires sur les critiques
- ⭐ Système de likes/réactions

### Version 1.2.0 (Prévu)
- 🔍 Recherche avancée (par livre, auteur, genre)
- 🏷️ Système de tags/catégories
- 📊 Statistiques personnelles
- 🎨 Thèmes personnalisables (mode sombre)

### Version 2.0.0 (À long terme)
- 📱 Application mobile (React Native)
- 🌐 API REST complète
- 🤖 Recommandations basées sur l'IA
- 🌍 Support multilingue

---

**🎉 Merci d'utiliser LITReview ! Bonne lecture et bonnes critiques ! 📚**

