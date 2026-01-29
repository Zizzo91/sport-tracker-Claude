# 📝 CHANGELOG

## [1.1.0] - 2026-01-29

### 🔧 Fixed
- **Date classification**: Eventi ora correttamente classificati in oggi/domani/dopodomani
- Eventi mattutini (< 06:00) non più erroneamente classificati come "oggi"
- Gestione corretta fusi orari per eventi internazionali (Australian Open, ecc.)

### ✨ Added
- Logica intelligente per rilevamento "oggi/domani" nel contesto articoli
- Filtro automatico eventi rilevanti secondo criteri specificati
- Prevenzione duplicati nel database eventi
- Script di test automatico (`test_system.py`)
- Documentazione troubleshooting completa (`TEST_E_DEBUG.md`)

### 🔄 Improved
- Parsing più accurato di canali TV (Sky Sport 251, 252, etc.)
- Estrazione automatica competizioni e note
- Gestione migliore delle sezioni sport negli articoli
- Riconoscimento eventi con italiani (squadre/atleti)

### 📚 Documentation
- Aggiunta guida test e debug
- Aggiornato README con changelog fix
- Creato riepilogo miglioramenti

---

## [1.0.0] - 2026-01-28

### 🎉 Initial Release
- Web app responsive per eventi sportivi
- Scraping automatico da OASport
- GitHub Actions per aggiornamento giornaliero
- Filtri per giorno (Ieri/Oggi/Domani)
- Design moderno con badge colorati per sport
- Hosting su GitHub Pages

---

*Versionamento: [Major.Minor.Patch]*
- Major: Cambiamenti breaking o ristrutturazioni importanti
- Minor: Nuove funzionalità compatibili
- Patch: Bug fix e piccoli miglioramenti
