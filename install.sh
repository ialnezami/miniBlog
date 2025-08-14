#!/bin/bash

echo "🚀 Installation de MiniBlog avec intégration IA"
echo "================================================"

# Vérifier les prérequis
echo "📋 Vérification des prérequis..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Tous les prérequis sont satisfaits"

# Configuration des variables d'environnement
echo "🔧 Configuration des variables d'environnement..."

# Demander la clé API OpenAI
read -p "🔑 Entrez votre clé API OpenAI (ou appuyez sur Entrée pour la configurer plus tard): " openai_key

# Créer le fichier .env pour Docker
if [ ! -z "$openai_key" ]; then
    echo "OPENAI_API_KEY=$openai_key" > .env
    echo "✅ Clé API OpenAI configurée"
else
    echo "⚠️  Clé API OpenAI non configurée. Vous devrez la configurer manuellement."
fi

# Installation du backend
echo "🐍 Installation du backend Django..."

cd backend

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env pour Django
if [ ! -f .env ]; then
    cat > .env << EOF
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
DEBUG=True
DATABASE_NAME=blog_minimaliste
DATABASE_USER=miniblog_user
DATABASE_PASSWORD=miniblog_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
MEDIA_ROOT=./media
OPENAI_API_KEY=${openai_key:-your-openai-api-key-here}
OPENAI_MODEL=gpt-3.5-turbo
EOF
    echo "✅ Fichier .env Django créé"
fi

cd ..

# Installation du frontend
echo "⚛️  Installation du frontend Vue.js..."

cd frontend

# Installer les dépendances
npm install

# Créer le fichier .env.local pour Vue
if [ ! -f .env.local ]; then
    cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:8000/api
VITE_MEDIA_BASE_URL=http://localhost:8000/media
EOF
    echo "✅ Fichier .env.local Vue créé"
fi

cd ..

# Créer le script de démarrage
echo "📝 Création du script de démarrage..."

cat > start.sh << 'EOF'
#!/bin/bash

echo "🚀 Démarrage de MiniBlog..."

# Démarrer les services avec Docker Compose
docker-compose up -d

echo "✅ MiniBlog est en cours de démarrage..."
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "🗄️  Admin Django: http://localhost:8000/admin"
echo "📊 Base de données: localhost:3306"

echo ""
echo "📋 Commandes utiles:"
echo "  - Arrêter: docker-compose down"
echo "  - Logs: docker-compose logs -f"
echo "  - Redémarrer: docker-compose restart"
EOF

chmod +x start.sh

# Créer le script d'arrêt
cat > stop.sh << 'EOF'
#!/bin/bash

echo "🛑 Arrêt de MiniBlog..."

docker-compose down

echo "✅ MiniBlog arrêté"
EOF

chmod +x stop.sh

# Créer le script de mise à jour
cat > update.sh << 'EOF'
#!/bin/bash

echo "🔄 Mise à jour de MiniBlog..."

# Arrêter les services
docker-compose down

# Mettre à jour le code
git pull origin main

# Reconstruire et redémarrer
docker-compose up --build -d

echo "✅ MiniBlog mis à jour et redémarré"
EOF

chmod +x update.sh

echo ""
echo "🎉 Installation terminée avec succès !"
echo ""
echo "📋 Pour démarrer MiniBlog:"
echo "  ./start.sh"
echo ""
echo "📋 Pour arrêter MiniBlog:"
echo "  ./stop.sh"
echo ""
echo "📋 Pour mettre à jour:"
echo "  ./update.sh"
echo ""
echo "🔑 N'oubliez pas de configurer votre clé API OpenAI dans le fichier .env"
echo ""
echo "📚 Documentation: consultez le README.md pour plus d'informations"
