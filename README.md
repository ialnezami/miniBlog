# Blog Minimaliste

Un blog moderne et épuré développé avec Vue.js pour le frontend et Django pour le backend, utilisant MySQL comme base de données.

## 🚀 Fonctionnalités

### Fonctionnalités Core

- **Gestion d’articles** : Création, édition, suppression et publication d’articles
- **Interface minimaliste** : Design épuré et responsive pour une expérience de lecture optimale
- **Système d’authentification** : Connexion/déconnexion des auteurs
- **Gestion des catégories** : Organisation des articles par catégories
- **Recherche** : Recherche textuelle dans les articles
- **Pagination** : Navigation fluide entre les pages d’articles
- **Prévisualisation** : Aperçu des articles avant publication

### Fonctionnalités Avancées

- **Éditeur Markdown** : Rédaction des articles en Markdown avec prévisualisation en temps réel
- **Système de tags** : Classification fine des articles
- **SEO optimisé** : Meta tags automatiques, URLs propres, sitemap
- **Mode brouillon** : Sauvegarde automatique des articles en cours de rédaction
- **Gestion d’images** : Upload et intégration d’images dans les articles
- **RSS Feed** : Flux RSS pour les abonnés
- **Mode sombre/clair** : Basculement entre les thèmes
- **Commentaires** (optionnel) : Système de commentaires modéré

## 🛠 Stack Technologique

### Frontend - Vue.js 3

- **Vue 3** : Framework JavaScript réactif
- **Vue Router** : Navigation SPA
- **Pinia** : Gestion d’état moderne pour Vue
- **Axios** : Client HTTP pour les appels API
- **Vite** : Build tool rapide et moderne
- **Tailwind CSS** : Framework CSS utility-first pour le design minimaliste
- **Vue-markdown** : Rendu des articles Markdown
- **VueUse** : Collection d’utilitaires Vue

### Backend - Django

- **Django 4.x** : Framework web Python
- **Django REST Framework** : API REST complète
- **Django CORS Headers** : Gestion des CORS pour SPA
- **Pillow** : Traitement d’images
- **django-filter** : Filtrage avancé des données
- **djangorestframework-simplejwt** : Authentification JWT
- **django-environ** : Gestion des variables d’environnement

### Base de données

- **MySQL 8.0+** : Base de données relationnelle
- **django-mysql** : Extensions spécifiques à MySQL

### DevOps & Outils

- **Docker & Docker Compose** : Conteneurisation
- **Nginx** : Serveur web et reverse proxy (production)
- **Gunicorn** : Serveur WSGI (production)
- **GitHub Actions** : CI/CD

## 📋 Prérequis

- **Node.js** 18+ et npm
- **Python** 3.9+
- **MySQL** 8.0+
- **Docker** (optionnel mais recommandé)

## 🚀 Installation

### Développement Local

#### 1. Cloner le repository

```bash
git clone <repository-url>
cd blog-minimaliste
```

#### 2. Configuration Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres MySQL
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

### Déploiement avec Docker

```bash
# Développement
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🔧 Configuration

### Variables d’environnement Backend (.env)

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
```

### Variables d’environnement Frontend (.env.local)

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_MEDIA_BASE_URL=http://localhost:8000/media
```

## 📚 Structure du projet

```
blog-minimaliste/
├── backend/
│   ├── blog/
│   │   ├── models.py          # Modèles de données
│   │   ├── serializers.py     # Sérialiseurs DRF
│   │   ├── views.py           # Vues API
│   │   └── urls.py            # Routes API
│   ├── config/
│   │   ├── settings.py        # Configuration Django
│   │   └── urls.py            # URLs principales
│   ├── requirements.txt       # Dépendances Python
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/        # Composants Vue réutilisables
│   │   ├── views/             # Pages principales
│   │   ├── stores/            # Stores Pinia
│   │   ├── services/          # Services API
│   │   └── router/            # Configuration des routes
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## 🔒 Sécurité - Points d’attention

### Backend Django

- **Variables sensibles** : Utiliser django-environ, jamais de secrets en dur
- **CORS** : Configurer strictement les domaines autorisés
- **Authentification** : Implémenter JWT avec refresh tokens
- **Validation** : Valider toutes les entrées utilisateur
- **Permissions** : Système de permissions granulaire (auteur/admin)
- **Rate Limiting** : Limiter les requêtes API pour éviter les abus
- **Uploads** : Validation stricte des fichiers uploadés (type, taille)
- **SQL Injection** : Utiliser l’ORM Django, éviter les requêtes SQL brutes

### Frontend Vue.js

- **XSS** : Sanitiser le contenu Markdown et HTML
- **Gestion des tokens** : Stocker les JWT de manière sécurisée
- **Validation côté client** : Ne jamais faire confiance uniquement au frontend
- **HTTPS** : Obligatoire en production
- **CSP Headers** : Content Security Policy stricte

### Base de données MySQL

- **Utilisateur dédié** : Créer un utilisateur MySQL spécifique avec permissions limitées
- **Chiffrement** : Chiffrer les connexions (SSL/TLS)
- **Sauvegardes** : Automatiser les sauvegardes régulières
- **Index** : Optimiser les performances avec des index appropriés

## 🎯 Modèles de données

### Article

```python
- title (CharField)
- slug (SlugField, unique)
- content (TextField, Markdown)
- excerpt (TextField)
- status (ChoiceField: draft/published)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- published_at (DateTimeField, nullable)
- author (ForeignKey User)
- category (ForeignKey Category)
- tags (ManyToManyField Tag)
- featured_image (ImageField)
- meta_description (CharField, SEO)
```

### Category & Tag

```python
Category:
- name (CharField)
- slug (SlugField)
- description (TextField)

Tag:
- name (CharField)
- slug (SlugField)
```

## 🚦 API Endpoints

```
GET    /api/articles/          # Liste des articles publiés
GET    /api/articles/{slug}/   # Détail d'un article
POST   /api/articles/          # Créer un article (auth)
PUT    /api/articles/{id}/     # Modifier un article (auth)
DELETE /api/articles/{id}/     # Supprimer un article (auth)

GET    /api/categories/        # Liste des catégories
GET    /api/tags/              # Liste des tags
GET    /api/search/            # Recherche d'articles

POST   /api/auth/login/        # Connexion
POST   /api/auth/refresh/      # Refresh token
POST   /api/auth/logout/       # Déconnexion
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

- **Pagination** : Limiter le nombre d’articles par page
- **Cache** : Redis pour le cache des vues fréquentes
- **Database** : Index sur les champs de recherche et tri
- **Media** : CDN pour servir les images

### Frontend

- **Bundle splitting** : Code splitting par routes
- **Images** : Lazy loading et formats optimisés
- **Cache** : Service Worker pour le cache offline
- **SEO** : Server-side rendering avec Nuxt.js (migration future)

## 🔄 Roadmap

- [ ] Système de commentaires
- [ ] Newsletter/abonnements
- [ ] Analytics intégrées
- [ ] PWA (Progressive Web App)
- [ ] Thèmes personnalisables
- [ ] API GraphQL
- [ ] Migration vers Nuxt.js (SSR)

## 📄 Licence

[Choisir une licence appropriée - MIT, GPL, etc.]

## 👥 Contribution

Les contributions sont les bienvenues ! Voir <CONTRIBUTING.md> pour les guidelines.

## 📞 Support

Pour toute question ou problème :

- Ouvrir une [issue](lien-vers-issues)
- Documentation : [lien-vers-docs]
- Email : [contact@example.com]