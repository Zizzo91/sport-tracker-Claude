# 📺 Eventi Sportivi Italiani - Guida TV Automatica

Web app moderna che traccia automaticamente gli eventi sportivi italiani con aggiornamento giornaliero via GitHub Actions.

## 🎯 Caratteristiche

- ✅ **Aggiornamento automatico** ogni giorno alle 06:00 e 18:00 CET
- ✅ **Scraping intelligente** da OASport e altre fonti sportive
- ✅ **Filtri per giorno**: Ieri, Oggi, Domani
- ✅ **Design responsive** ottimizzato per smartphone
- ✅ **Eventi evidenziati** con squadre/atleti italiani in grassetto rosso
- ✅ **Badge colorati** per distinguere gli sport
- ✅ **Hosting gratuito** su GitHub Pages

## 📋 Sport Tracciati

### ⚽ Calcio
- Serie A (tutte le partite)
- Champions League (solo squadre italiane)
- Europa League (solo squadre italiane)
- Conference League (solo squadre italiane)
- Serie B: Monza e Catanzaro
- Serie D: Reggina (ReggioTV per trasferte)

### 🎾 Tennis
- ATP/WTA con giocatori italiani
- Sinner, Paolini, Berrettini, Musetti, Darderi, etc.

### 🏎️ Formula 1 & MotoGP
- Test, prove, qualifiche, gare

### ⛷️ Sci Alpino
- Federica Brignone e Sofia Goggia

### 🏐 Volley
- Monza (Vero Volley)

## 🚀 Setup su GitHub

### 1. Crea il Repository

```bash
# Crea una nuova cartella
mkdir eventi-sportivi-italiani
cd eventi-sportivi-italiani

# Inizializza Git
git init
git add .
git commit -m "🎉 Setup iniziale web app eventi sportivi"

# Crea il repository su GitHub e collega
git remote add origin https://github.com/TUO-USERNAME/eventi-sportivi-italiani.git
git branch -M main
git push -u origin main
```

### 2. Struttura File

Assicurati di avere questi file nel repository:

```
eventi-sportivi-italiani/
├── .github/
│   └── workflows/
│       └── update-events.yml    # GitHub Actions workflow
├── index.html                    # Web app principale
├── eventi.json                   # Database eventi (auto-generato)
├── scrape_events.py             # Script scraping
├── requirements.txt              # Dipendenze Python
└── README.md                     # Questo file
```

### 3. Attiva GitHub Pages

1. Vai su **Settings** del repository
2. Sezione **Pages** (menu laterale)
3. Source: **Deploy from a branch**
4. Branch: **main** → cartella: **/ (root)**
5. Clicca **Save**

Dopo qualche minuto, la tua app sarà online su:
```
https://TUO-USERNAME.github.io/eventi-sportivi-italiani/
```

### 4. Verifica GitHub Actions

1. Vai alla tab **Actions** del repository
2. Controlla che il workflow "Aggiorna Eventi Sportivi" sia attivo
3. Puoi eseguirlo manualmente con "Run workflow"

## 🔧 Configurazione

### Modifica Orari Aggiornamento

Modifica il file `.github/workflows/update-events.yml`:

```yaml
on:
  schedule:
    # Formato: minuto ora giorno mese giorno-settimana
    # Esempi:
    - cron: '0 5,17 * * *'    # Alle 06:00 e 18:00 CET ogni giorno
    - cron: '0 */6 * * *'     # Ogni 6 ore
    - cron: '0 8 * * *'       # Ogni giorno alle 09:00 CET
```

### Aggiungi Eventi Fissi

Modifica `scrape_events.py`, sezione `add_fixed_events()`:

```python
def add_fixed_events(self):
    # Esempio: Partite Reggina in trasferta
    fixed_events = [
        ('2026-02-15', '14:30', 'Reggina - Avversario', 'ReggioTV'),
        ('2026-03-01', '14:30', 'Reggina - Avversario', 'ReggioTV'),
    ]

    for date, time, event, channel in fixed_events:
        if date not in self.events:
            self.events[date] = []

        self.events[date].append({
            'time': time,
            'event': event,
            'competition': 'Serie D',
            'sport': 'calcio',
            'channel': channel,
            'notes': 'Trasferta Reggina',
            'highlight': True
        })
```

## 🛠️ Sviluppo Locale

### Testa lo Scraper

```bash
# Installa dipendenze
pip install -r requirements.txt

# Esegui lo scraper
python scrape_events.py

# Controlla il file generato
cat eventi.json
```

### Testa la Web App

```bash
# Avvia un server locale
python -m http.server 8000

# Apri nel browser
# http://localhost:8000
```

## 📊 Formato Dati

Il file `eventi.json` ha questa struttura:

```json
{
  "2026-01-29": [
    {
      "time": "21:00",
      "event": "Panathinaikos - Roma",
      "competition": "Europa League",
      "sport": "calcio",
      "channel": "Sky Sport",
      "notes": "Diretta Gol: Sky Sport 251",
      "highlight": true
    }
  ]
}
```

## 🎨 Personalizzazione

### Modifica Colori Sport

In `index.html`, sezione CSS:

```css
.calcio { background: #28a745; }   /* Verde */
.tennis { background: #ffc107; }   /* Giallo */
.f1 { background: #dc3545; }       /* Rosso */
.motogp { background: #fd7e14; }   /* Arancione */
.sci { background: #17a2b8; }      /* Azzurro */
.volley { background: #6f42c1; }   /* Viola */
```

## 🔍 Fonti Dati

Lo scraper raccoglie dati da:
- 📰 OASport.it
- 📺 Guide TV Sky Sport
- 🔔 Canali Telegram sportivi (opzionale)

## 🐛 Troubleshooting

### Gli eventi non si aggiornano
- Verifica che GitHub Actions sia attivo nella tab "Actions"
- Controlla i log dell'ultimo workflow execution
- Esegui manualmente "Run workflow"

### La pagina non si carica
- Verifica che GitHub Pages sia attivato
- Controlla che `index.html` sia nella root del repository
- Aspetta 2-3 minuti dopo ogni commit

### Errori nello scraping
- Alcuni siti potrebbero bloccare i bot
- Aggiungi delay tra le richieste HTTP
- Usa User-Agent realistici

## 📱 Screenshot

![Desktop](https://via.placeholder.com/800x400.png?text=Desktop+View)
![Mobile](https://via.placeholder.com/375x812.png?text=Mobile+View)

## 📝 Licenza

MIT License - Sentiti libero di modificare e condividere!

## 🤝 Contributi

Pull request benvenute! Per modifiche importanti, apri prima una issue.

---

**Fatto con ❤️ per gli appassionati di sport italiano**
