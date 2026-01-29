# 🔧 GUIDA MANUTENZIONE EVENTI

## 📅 Come Aggiungere Eventi Manualmente

### Opzione 1: Modifica scrape_events.py

Apri `scrape_events.py` e cerca la funzione `add_manual_events()`:

```python
def add_manual_events(self):
    """Aggiungi eventi che potrebbero mancare dallo scraping"""

    # Partite Serie B con Catanzaro
    manual_serie_b_catanzaro = [
        ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),
        ('2026-02-07', '15:00', 'Catanzaro', 'Bari'),
        # Aggiungi qui altre partite
    ]

    for date, time, home, away in manual_serie_b_catanzaro:
        if date not in self.events:
            self.events[date] = []

        event = {
            'time': time,
            'event': f'{home} - {away}',
            'competition': 'Serie B',
            'sport': 'calcio',
            'channel': self.channels_by_competition['serie_b'],
            'notes': '',
            'highlight': True
        }

        if not self.is_duplicate(self.events[date], event):
            self.events[date].append(event)
```

**Aggiungi semplicemente una riga:**
```python
('2026-02-14', '15:00', 'Spezia', 'Catanzaro'),
```

### Opzione 2: Usa helper_add_events.py

```bash
# Modifica helper_add_events.py nella sezione quick_add_catanzaro()
# Poi esegui:
python helper_add_events.py
```

### Opzione 3: Modifica eventi.json Direttamente

```json
{
  "2026-02-07": [
    {
      "time": "15:00",
      "event": "Catanzaro - Bari",
      "competition": "Serie B - 24ª giornata",
      "sport": "calcio",
      "channel": "DAZN, LaB Channel (Prime Video)",
      "notes": "",
      "highlight": true
    }
  ]
}
```

---

## 🔄 Workflow Settimanale Consigliato

### Lunedì Mattina:
1. Controlla calendario Serie A su https://www.legaseriea.it
2. Controlla calendario Serie B su https://www.legab.it
3. Verifica partite Catanzaro e Monza in Serie B
4. Se mancano partite, aggiungile in `scrape_events.py`

### Prima di Fare Commit:
```bash
# Test locale
python scrape_events.py

# Verifica il file generato
cat eventi.json | grep -i catanzaro
cat eventi.json | grep -i monza

# Se tutto ok, commit
git add scrape_events.py eventi.json
git commit -m "📅 Aggiornamento calendario settimanale"
git push
```

---

## 📺 Verifica Canali TV

### Serie A - Come Sapere se è DAZN o DAZN+Sky

**Solo DAZN** (7 partite/giornata):
- Venerdì 20:45
- Sabato 15:00
- Domenica 12:30
- Domenica 15:00
- Lunedì 20:45
- Martedì 20:45 (se ci sono turni infrasettimanali)

**DAZN + Sky** (3 partite/giornata):
- Sabato 18:00
- Sabato 20:45
- Domenica 18:00
- Domenica 20:45

⚠️ **ATTENZIONE**: Questi sono slot tipici, ma verificare sempre su:
- https://www.legaseriea.it
- https://sport.sky.it/calcio/serie-a

### Serie B - Sempre Uguale
Tutte le partite: **DAZN, LaB Channel (Prime Video)**

### Coppa Italia
Sky Sport (esclusiva)

### Champions/Europa/Conference
Sky Sport (esclusiva per italiane)

---

## 🐛 Troubleshooting

### "Lo scraper non trova la partita del Catanzaro"

**Soluzione:**
Aggiungi manualmente in `scrape_events.py` → `add_manual_events()`

### "Il canale è sbagliato per Serie A"

**Verifica:**
1. Controlla su https://sport.sky.it/calcio/serie-a/calendario-risultati
2. Se è solo DAZN, non deve comparire Sky
3. Se è co-esclusiva, deve comparire "DAZN, Sky Sport"

**Fix:**
Modifica `eventi.json` manualmente o aspetta il prossimo run dello scraper

### "Mancano partite di Serie D Reggina"

**Le partite in casa non sono trasmesse**
Solo le trasferte su ReggioTV.

**Aggiungi trasferte:**
```python
manual_serie_d = [
    ('2026-02-09', '14:30', 'Acireale', 'Reggina'),
]
```

---

## 📊 Calendario da Monitorare

### Catanzaro (Serie B 2025/26)
Cerca su: https://www.uscatanzaro.net/calendario/

### Monza (Serie B 2025/26)
Cerca su: (verifica se Monza è in Serie A o Serie B nella stagione corrente)

### Reggina (Serie D Girone I)
Cerca su: https://www.reggina1914.it/

---

## ⚡ Quick Reference

```bash
# Test scraper
python scrape_events.py

# Test sistema
python test_system.py

# Aggiungi eventi extra
python helper_add_events.py

# Verifica JSON
python -m json.tool eventi.json

# Deploy
git add .
git commit -m "📅 Aggiornamento eventi"
git push
```

---

**Ultimo aggiornamento: 2026-01-29**
