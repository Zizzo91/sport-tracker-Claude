# 🚀 GUIDA RAPIDA: Deploy su GitHub

## ⚡ Setup in 5 minuti

### STEP 1: Scarica i file
Scarica tutti i file generati e organizzali così:

```
eventi-sportivi-italiani/
├── .github/
│   └── workflows/
│       └── update-events.yml    ← Rinomina github_workflow.yml
├── index.html
├── eventi.json
├── scrape_events.py
├── requirements.txt
├── README.md
└── .gitignore
```

**IMPORTANTE**: Crea la cartella `.github/workflows/` e rinomina `github_workflow.yml` in `update-events.yml`

### STEP 2: Crea il repository GitHub

1. Vai su https://github.com/new
2. Nome repository: `eventi-sportivi-italiani`
3. ✅ Public (per GitHub Pages gratuito)
4. ❌ NON aggiungere README, .gitignore o license
5. Clicca "Create repository"

### STEP 3: Carica i file

```bash
# Nella cartella eventi-sportivi-italiani
git init
git add .
git commit -m "🎉 Setup iniziale guida TV eventi sportivi"

# Sostituisci TUO-USERNAME con il tuo username GitHub
git remote add origin https://github.com/TUO-USERNAME/eventi-sportivi-italiani.git
git branch -M main
git push -u origin main
```

### STEP 4: Attiva GitHub Pages

1. Vai nel repository → **Settings**
2. Menu laterale → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** → Folder: **/ (root)**
5. **Save**

⏱️ Aspetta 2-3 minuti

### STEP 5: Verifica

La tua app sarà online su:
```
https://TUO-USERNAME.github.io/eventi-sportivi-italiani/
```

GitHub Actions aggiornerà automaticamente gli eventi ogni giorno alle 06:00 e 18:00 CET!

---

## 🔧 Test Locale (Opzionale)

```bash
# Installa dipendenze
pip install requests beautifulsoup4 lxml

# Testa lo scraper
python scrape_events.py

# Avvia server locale
python -m http.server 8000

# Apri http://localhost:8000
```

---

## ✅ Checklist Finale

- [ ] Repository GitHub creato e pubblico
- [ ] Cartella `.github/workflows/` creata correttamente
- [ ] File `update-events.yml` dentro workflows
- [ ] Tutti i file caricati su GitHub
- [ ] GitHub Pages attivato
- [ ] URL funzionante dopo 2-3 minuti
- [ ] Tab "Actions" mostra il workflow attivo

---

## 🆘 Problemi Comuni

**"Workflow non si esegue"**
→ Controlla che il file sia in `.github/workflows/update-events.yml`

**"Pagina 404"**
→ Aspetta qualche minuto, poi controlla Settings → Pages

**"Eventi non si aggiornano"**
→ Vai su Actions → Run workflow manualmente per testare

---

**Fatto! 🎉 La tua guida TV è online e si aggiorna automaticamente!**
