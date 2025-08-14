# MiniBlog - Blog Minimaliste avec Intégration IA

Un blog moderne et épuré développé avec Vue.js pour le frontend et Django pour le backend, utilisant MySQL comme base de données et intégrant l'intelligence artificielle pour vérifier et améliorer le contenu des articles.

## 🚀 Fonctionnalités

### Fonctionnalités Core

- **Gestion d'articles** : Création, édition, suppression et publication d'articles
- **Interface minimaliste** : Design épuré et responsive pour une expérience de lecture optimale
- **Système d'authentification** : Connexion/déconnexion des auteurs avec JWT
- **Gestion des catégories** : Organisation des articles par catégories
- **Recherche avancée** : Recherche textuelle dans les articles avec filtres
- **Pagination** : Navigation fluide entre les pages d'articles
- **Prévisualisation** : Aperçu des articles avant publication

### 🧠 Intégration IA (Nouveau !)

- **Vérification automatique du contenu** : Analyse de la qualité avec OpenAI GPT
- **Score de qualité** : Évaluation sur 10 avec feedback détaillé
- **Détection de contenu inapproprié** : Modération automatique du contenu
- **Suggestions d'amélioration** : Conseils personnalisés pour améliorer vos articles
- **Analyse SEO** : Recommandations pour optimiser vos articles
- **Vérification grammaticale** : Détection des erreurs de langue

### Fonctionnalités Avancées

- **Éditeur Markdown** : Rédaction des articles en Markdown avec prévisualisation en temps réel
- **Système de tags** : Classification fine des articles
- **SEO optimisé** : Meta tags automatiques, URLs propres
- **Mode brouillon** : Sauvegarde automatique des articles en cours de rédaction
- **Gestion d'images** : Upload et intégration d'images dans les articles
- **Commentaires** : Système de commentaires modéré
- **Mode sombre/clair** : Basculement entre les thèmes

## 🛠 Stack Technologique

### Frontend - Vue.js 3

- **Vue 3** : Framework JavaScript réactif avec Composition API
- **Vue Router** : Navigation SPA
- **Pinia** : Gestion d'état moderne pour Vue
- **Axios** : Client HTTP pour les appels API
- **Vite** : Build tool rapide et moderne
- **Tailwind CSS** : Framework CSS utility-first pour le design minimaliste
- **VueUse** : Collection d'utilitaires Vue

### Backend - Django

- **Django 4.2** : Framework web Python
- **Django REST Framework** : API REST complète
- **Django CORS Headers** : Gestion des CORS pour SPA
- **Pillow** : Traitement d'images
- **django-filter** : Filtrage avancé des données
- **djangorestframework-simplejwt** : Authentification JWT
- **django-environ** : Gestion des variables d'environnement

### 🧠 Intelligence Artificielle

- **OpenAI GPT** : Modèle de langage pour l'analyse de contenu
- **Analyse automatique** : Vérification de la qualité et de la pertinence
- **Modération de contenu** : Détection de contenu inapproprié
- **Suggestions intelligentes** : Recommandations personnalisées

### Base de données

- **MySQL 8.0+** : Base de données relationnelle
- **django-mysql** : Extensions spécifiques à MySQL

### DevOps & Outils

- **Docker & Docker Compose** : Conteneurisation complète
- **Nginx** : Serveur web et reverse proxy (optionnel)
- **GitHub Actions** : CI/CD (à configurer)

## 📋 Prérequis

- **Node.js** 18+ et npm
- **Python** 3.9+
- **MySQL** 8.0+ (ou Docker)
- **Docker** et Docker Compose (recommandé)
- **Clé API OpenAI** pour les fonctionnalités IA

## 🚀 Installation Rapide

### Option 1: Installation automatique (Recommandée)

```bash
# Cloner le repository
git clone <repository-url>
cd miniblog

# Rendre le script exécutable et lancer l'installation
chmod +x install.sh
./install.sh

# Démarrer l'application
./start.sh
```

### Option 2: Installation manuelle

#### 1. Cloner le repository

```bash
git clone <repository-url>
cd miniblog
```

#### 2. Configuration Backend (Django)

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer les variables d'environnement
cp env.example .env
# Éditer .env avec vos paramètres
```

#### 3. Configuration Base de données

```bash
# Créer la base de données MySQL
mysql -u root -p
CREATE DATABASE blog_minimaliste CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Migrations Django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Configuration Frontend (Vue.js)

```bash
cd ../frontend

# Installer les dépendances
npm install

# Copier et configurer les variables d'environnement
cp .env.example .env.local
# Éditer .env.local avec l'URL de votre API Django
```

#### 5. Lancer les serveurs de développement

```bash
# Terminal 1 - Backend Django
cd backend
python manage.py runserver

# Terminal 2 - Frontend Vue.js
cd frontend
npm run dev
```

### Option 3: Déploiement avec Docker

```bash
# Développement
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🔧 Configuration

### Variables d'environnement Backend (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=blog_minimaliste
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
MEDIA_ROOT=/path/to/media

# OpenAI Configuration (Requis pour l'IA)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### Variables d'environnement Frontend (.env.local)

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_MEDIA_BASE_URL=http://localhost:8000/media
```

## 🧠 Utilisation de l'IA

### Vérification automatique du contenu

1. **Créer un article** : Rédigez votre contenu normalement
2. **Vérification IA** : Cliquez sur "Vérifier avec l'IA" dans l'éditeur
3. **Analyse automatique** : L'IA analyse votre contenu et génère un score
4. **Feedback détaillé** : Recevez des recommandations spécifiques
5. **Amélioration continue** : Appliquez les suggestions et revérifiez

### Fonctionnalités IA disponibles

- **Score de qualité** : Évaluation globale sur 10
- **Analyse SEO** : Optimisation des mots-clés et de la structure
- **Vérification grammaticale** : Détection des erreurs de langue
- **Suggestions de style** : Amélioration de l'écriture
- **Modération de contenu** : Détection de contenu inapproprié

## 📚 Structure du projet

```
miniblog/
├── backend/                 # Backend Django
│   ├── blog/               # Application principale du blog
│   │   ├── models.py       # Modèles de données
│   │   ├── serializers.py  # Sérialiseurs DRF
│   │   ├── views.py        # Vues API
│   │   └── urls.py         # Routes API
│   ├── ai_content_checker/ # Application IA
│   │   ├── services.py     # Service OpenAI
│   │   ├── views.py        # API IA
│   │   └── urls.py         # Routes IA
│   ├── config/             # Configuration Django
│   ├── requirements.txt    # Dépendances Python
│   └── manage.py
├── frontend/               # Frontend Vue.js
│   ├── src/
│   │   ├── components/     # Composants Vue réutilisables
│   │   ├── views/          # Pages principales
│   │   ├── stores/         # Stores Pinia
│   │   ├── services/       # Services API
│   │   └── router/         # Configuration des routes
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml      # Configuration Docker
├── install.sh              # Script d'installation automatique
├── start.sh                # Script de démarrage
├── stop.sh                 # Script d'arrêt
└── README.md
```

## 🔒 Sécurité

### Backend Django

- **Variables sensibles** : Utilisation de django-environ
- **CORS** : Configuration stricte des domaines autorisés
- **Authentification JWT** : Tokens sécurisés avec refresh
- **Validation** : Validation stricte de toutes les entrées
- **Permissions** : Système granulaire (auteur/admin)
- **Rate Limiting** : Protection contre les abus
- **Uploads sécurisés** : Validation des fichiers

### Frontend Vue.js

- **XSS Protection** : Sanitisation du contenu
- **Gestion des tokens** : Stockage sécurisé des JWT
- **Validation côté client** : Double validation
- **HTTPS** : Obligatoire en production

### IA et Confidentialité

- **Données locales** : Le contenu n'est pas stocké par OpenAI
- **API sécurisée** : Communication chiffrée avec OpenAI
- **Contrôle utilisateur** : Vérification IA optionnelle

## 🎯 Modèles de données

### Article

```python
- title (CharField)           # Titre de l'article
- slug (SlugField)            # URL unique
- content (TextField)          # Contenu Markdown
- excerpt (TextField)          # Extrait
- status (ChoiceField)         # draft/published
- created_at (DateTimeField)   # Date de création
- updated_at (DateTimeField)   # Date de modification
- published_at (DateTimeField) # Date de publication
- author (ForeignKey User)     # Auteur
- category (ForeignKey)        # Catégorie
- tags (ManyToManyField)      # Tags
- featured_image (ImageField)  # Image principale
- meta_description (CharField) # Description SEO

# Champs IA
- ai_checked (BooleanField)   # Vérifié par l'IA
- ai_score (FloatField)       # Score sur 10
- ai_feedback (TextField)     # Feedback détaillé
```

## �� API Endpoints

### Articles

```
GET    /api/articles/          # Liste des articles
GET    /api/articles/{slug}/   # Détail d'un article
POST   /api/articles/          # Créer un article
PUT    /api/articles/{id}/     # Modifier un article
DELETE /api/articles/{id}/     # Supprimer un article
POST   /api/articles/{id}/publish/  # Publier un article
POST   /api/articles/{id}/check_with_ai/  # Vérifier avec l'IA
```

### IA Content Checker

```
POST   /api/ai/check-article/      # Vérifier le contenu d'un article
POST   /api/ai/check-appropriate/  # Vérifier l'appropriation
POST   /api/ai/suggest-improvements/ # Suggestions d'amélioration
```

### Authentification

```
POST   /api/auth/login/        # Connexion
POST   /api/auth/register/     # Inscription
POST   /api/auth/refresh/      # Refresh token
GET    /api/auth/profile/      # Profil utilisateur
```

## 🧪 Tests

```bash
# Tests backend
cd backend
python manage.py test

# Tests frontend
cd frontend
npm run test:unit
```

## 📈 Performance & Optimisation

### Backend

- **Pagination** : Limitation du nombre d'articles par page
- **Cache** : Redis pour le cache (à configurer)
- **Database** : Index optimisés pour la recherche
- **Media** : CDN pour les images (à configurer)

### Frontend

- **Code splitting** : Division du code par routes
- **Lazy loading** : Chargement différé des composants
- **Images optimisées** : Formats modernes et compression
- **Service Worker** : Cache offline (à implémenter)

## 🔄 Roadmap

- [x] Système d'authentification JWT
- [x] Intégration IA OpenAI
- [x] Vérification automatique du contenu
- [x] Interface responsive moderne
- [x] Gestion des articles et catégories
- [ ] Système de commentaires avancé
- [ ] Newsletter/abonnements
- [ ] Analytics intégrées
- [ ] PWA (Progressive Web App)
- [ ] Thèmes personnalisables
- [ ] API GraphQL
- [ ] Migration vers Nuxt.js (SSR)

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 👥 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :

- Ouvrir une [issue](lien-vers-issues)
- Documentation : [lien-vers-docs]
- Email : [contact@example.com]

## 🎉 Remerciements

- **OpenAI** pour l'API GPT qui alimente nos fonctionnalités IA
- **Vue.js** et **Django** pour leurs frameworks exceptionnels
- **Tailwind CSS** pour le design system moderne
- **La communauté open source** pour tous les outils et bibliothèques

---

**MiniBlog** - Rédigez mieux avec l'intelligence artificielle 🚀