#!/bin/bash

echo "🚀 Setup automatico Eventi Sportivi Italiani"
echo "=============================================="
echo ""

# Chiedi username GitHub
read -p "Inserisci il tuo username GitHub: " github_username

# Verifica che la cartella .github/workflows esista
mkdir -p .github/workflows

# Rinomina il file workflow se necessario
if [ -f "github_workflow.yml" ]; then
    mv github_workflow.yml .github/workflows/update-events.yml
    echo "✅ Workflow spostato in .github/workflows/"
fi

# Inizializza Git
echo ""
echo "📦 Inizializzazione Git..."
git init
git add .
git commit -m "🎉 Setup iniziale guida TV eventi sportivi"

# Aggiungi remote
echo ""
echo "🔗 Collegamento a GitHub..."
git remote add origin https://github.com/$github_username/eventi-sportivi-italiani.git
git branch -M main

# Push
echo ""
echo "⬆️  Upload su GitHub..."
git push -u origin main

echo ""
echo "✅ COMPLETATO!"
echo ""
echo "📝 Prossimi passi:"
echo "1. Vai su https://github.com/$github_username/eventi-sportivi-italiani"
echo "2. Settings → Pages"
echo "3. Source: Deploy from a branch → main → / (root) → Save"
echo ""
echo "🌐 La tua app sarà online su:"
echo "   https://$github_username.github.io/eventi-sportivi-italiani/"
echo ""
echo "⏰ Aggiornamento automatico attivo alle 06:00 e 18:00 CET"
echo ""
