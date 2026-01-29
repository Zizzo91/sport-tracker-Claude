# 📖 GUIDA COMPLETA - Gestione Eventi Automatici

## 🎯 RISPOSTA ALLE TUE DOMANDE

### 1. Come trova Monza e Catanzaro automaticamente?

**Automatico:**
- Lo scraper cerca su OASport le keyword "monza" e "catanzaro"
- Se menzionate in articoli Serie B, vengono aggiunte automaticamente
- Canale assegnato: "DAZN, LaB Channel (Prime Video)"

**Se non le trova (backup manuale):**

1. Apri `scrape_events.py`
2. Cerca la funzione `add_manual_events()`
3. Trova la sezione `manual_serie_b_catanzaro`:

```python
manual_serie_b_catanzaro = [
    ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),
    ('2026-02-07', '15:00', 'Catanzaro', 'Bari'),  # ← Aggiungi qui
    ('2026-02-14', '20:30', 'Spezia', 'Catanzaro'),  # ← E qui
]
```

4. Salva, commit e push:
```bash
git add scrape_events.py
git commit -m "📅 Aggiunte partite Catanzaro"
git push
```

5. GitHub Actions eseguirà lo scraper alla prossima run (o esegui manualmente)

**Dove trovare il calendario Catanzaro:**
- Sito ufficiale: https://www.uscatanzaro.net/calendario/
- Lega Serie B: https://www.legab.it
- DAZN app/sito: sezione calendario Serie B

---

### 2. Canale Sky specifico (Uno, Calcio, 251, 252...)

**✅ IMPLEMENTATO AUTOMATICAMENTE!**

Lo scraper ora riconosce:

**Canali nominati:**
- Sky Sport Uno
- Sky Sport Calcio
- Sky Sport Arena
- Sky Sport 24

**Canali numerati:**
- Sky Sport 251, 252, 253, ecc.

**Come funziona:**

Lo scraper analizza il testo OASport e cerca pattern come:
- "Sky Sport Uno" → Canale: "Sky Sport Uno"
- "Sky Sport 251" → Canale: "Sky Sport 251"
- "Diretta Gol su Sky Sport 251" → Note: "Diretta Gol: Sky Sport 251"

**Esempio output:**

```json
{
  "time": "18:45",
  "event": "Maccabi Tel Aviv - Bologna",
  "channel": "Sky Sport Uno",
  "notes": "Diretta Gol: Sky Sport 251"
}
```

**Se il canale non è specifico:**
- Default: "Sky Sport" (generico)
- Puoi correggere manualmente in `eventi.json` dopo la generazione

---

### 3. Test F1 e Shakedown MotoGP (non in TV)

**✅ IMPLEMENTATO!**

**Eventi inclusi anche se NON trasmessi:**
- Test F1 (Barcellona, Bahrain, ecc.)
- Shakedown MotoGP
- Filming days
- Prove a porte chiuse

**Come vengono tracciati:**

```json
{
  "time": "10:00",
  "event": "Test F1 Barcellona - Giorno 1",
  "competition": "Formula 1 - Test",
  "channel": "Non trasmesso",
  "notes": "Test a porte chiuse, Non in TV"
}
```

**Aggiungere manualmente test futuri:**

1. Apri `scrape_events.py`
2. Cerca `add_special_events()`
3. Aggiungi nella lista:

```python
special_events = [
    # Test F1
    ('2026-02-05', '10:00', 'Test F1 Barcellona - Giorno 1', 
     'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),

    # Shakedown MotoGP
    ('2026-02-01', '09:00', 'Shakedown MotoGP Sepang', 
     'MotoGP - Shakedown', 'Non trasmesso', 'Shakedown'),
]
```

**Perché includerli se non sono in TV?**
- Utile per seguire il calendario completo
- Ti ricorda quando ci sono test importanti
- Puoi seguire aggiornamenti online (live timing, social)

---

### 4. Sorteggi Champions, Europa e Conference League

**✅ IMPLEMENTATO!**

**Eventi riconosciuti automaticamente:**
- Sorteggi Champions League
- Sorteggi Europa League
- Sorteggi Conference League
- Altri eventi UEFA (SuperCoppa, ecc.)

**Come aggiungere sorteggi futuri:**

1. Apri `scrape_events.py`
2. Cerca `add_special_events()`
3. Aggiungi:

```python
special_events = [
    # Sorteggi UEFA
    ('2026-01-30', '12:00', 'Sorteggio Playoff Champions League', 
     'Champions League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),

    ('2026-01-30', '13:00', 'Sorteggio Playoff Europa League', 
     'Europa League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),

    ('2026-01-30', '14:00', 'Sorteggio Playoff Conference League', 
     'Conference League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),
]
```

**Date tipiche dei sorteggi UEFA:**
- Playoff (gennaio/febbraio)
- Ottavi di finale (febbraio)
- Quarti di finale (marzo)
- Semifinali (aprile)

**Dove trovare le date:**
- Sito UEFA: https://www.uefa.com/
- Sky Sport: calendario eventi
- Articoli OASport (lo scraper li trova automaticamente se menzionati)

---

## 🔄 WORKFLOW SETTIMANALE AGGIORNATO

### Lunedì Mattina (5 minuti)

**1. Verifica calendario Serie B (Catanzaro/Monza)**
- Vai su https://www.legab.it
- Controlla prossime 2 partite di Catanzaro e Monza
- Se non le vedi su `eventi.json`:
  - Apri `scrape_events.py`
  - Aggiungi in `manual_serie_b_catanzaro`
  - Commit e push

**2. Verifica eventi speciali prossima settimana**
- Sorteggi UEFA? → Aggiungi in `add_special_events()`
- Test F1/MotoGP? → Aggiungi in `add_special_events()`
- Altri eventi speciali? → Aggiungi in `add_special_events()`

**3. Trigger manuale GitHub Actions**
- Vai su GitHub → Actions
- "Run workflow"
- Verifica che completi con successo

**Tempo totale: 5-10 minuti**

---

## 📝 ESEMPIO PRATICO: Aggiungere Partita Catanzaro

**Scenario:** È lunedì 3 febbraio 2026, devi aggiungere la prossima partita del Catanzaro.

**1. Trova info partita:**
- Vai su https://www.uscatanzaro.net/calendario/
- Trovi: Catanzaro - Bari, sabato 7 febbraio ore 15:00

**2. Apri scrape_events.py:**
```bash
# Sul tuo computer
nano scrape_events.py
# oppure via GitHub web editor
```

**3. Cerca `manual_serie_b_catanzaro`:**
```python
manual_serie_b_catanzaro = [
    ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),  # Passata
    # Aggiungi qui ↓
]
```

**4. Aggiungi la nuova partita:**
```python
manual_serie_b_catanzaro = [
    ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),
    ('2026-02-07', '15:00', 'Catanzaro', 'Bari'),  # ← NUOVA
]
```

**5. Salva e commit:**
```bash
git add scrape_events.py
git commit -m "📅 Aggiunta Catanzaro-Bari del 7/2"
git push
```

**6. Trigger GitHub Actions:**
- Vai su GitHub → Actions
- "Run workflow"
- Aspetta 2 minuti
- Verifica su web app: la partita deve comparire!

---

## 🔍 VERIFICA CHE TUTTO FUNZIONI

### Test Locale (opzionale):

```bash
# Esegui lo scraper localmente
python scrape_events.py

# Controlla il file generato
cat eventi.json | grep -i catanzaro
cat eventi.json | grep -i "sorteggio"
cat eventi.json | grep -i "test f1"

# Se tutto ok, puoi fare push
git add eventi.json scrape_events.py
git commit -m "✅ Test locale: tutto funziona"
git push
```

### Test su GitHub Actions:

1. Vai su repository GitHub → tab "Actions"
2. Click su "Aggiorna Eventi Sportivi" (menu laterale)
3. Click "Run workflow" → "Run workflow"
4. Guarda i log in tempo reale:
   - ✅ "Cerco eventi per 2026-01-30"
   - ✅ "Serie B: 2026-01-31 15:00 - Südtirol - Catanzaro"
   - ✅ "Salvati X eventi rilevanti in eventi.json"
5. Se vedi ✅ verde → tutto ok!

---

## 🎯 CHECKLIST SETTIMANALE

**Ogni Lunedì:**
- [ ] Controlla calendario Serie B (Catanzaro/Monza)
- [ ] Aggiungi partite mancanti in `add_manual_events()`
- [ ] Controlla eventi speciali settimana (sorteggi, test)
- [ ] Aggiungi eventi speciali in `add_special_events()`
- [ ] Commit e push modifiche
- [ ] Trigger GitHub Actions manualmente
- [ ] Verifica web app mostra eventi corretti

**Una volta fatto, il sistema è automatico per tutta la settimana! 🚀**

---

## 💡 TIPS & TRICKS

### Tip 1: Usa commenti nel codice
```python
manual_serie_b_catanzaro = [
    # Gennaio
    ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),

    # Febbraio
    ('2026-02-07', '15:00', 'Catanzaro', 'Bari'),
    ('2026-02-14', '20:30', 'Spezia', 'Catanzaro'),

    # Marzo
    # ('2026-03-01', '15:00', 'Catanzaro', 'Palermo'),  # Da confermare
]
```

### Tip 2: Eventi ricorrenti
Per eventi che si ripetono (es. sorteggi ogni mese), crea un reminder:
```python
# REMINDER: Ultimo venerdì del mese → sorteggio Champions
# Controlla https://www.uefa.com/draws/
```

### Tip 3: Verifica rapida web app
Dopo ogni modifica:
1. Ctrl+F5 sulla web app
2. Cerca evento appena aggiunto
3. Verifica canale corretto

---

## 🆘 TROUBLESHOOTING

### "Non vedo la partita del Catanzaro sulla web app"

**Possibili cause:**
1. Non aggiunta in `add_manual_events()` → Aggiungi e push
2. GitHub Actions non eseguito → Esegui manualmente
3. Cache browser → Ctrl+F5
4. Data sbagliata → Verifica formato: 'YYYY-MM-DD'

**Soluzione rapida:**
```bash
# Verifica che sia in eventi.json
cat eventi.json | grep -i catanzaro

# Se non c'è, aggiungi manualmente e push
git add eventi.json
git commit -m "Fix: aggiungi Catanzaro"
git push
```

### "Il canale Sky è generico invece che specifico"

**Causa:** OASport non menziona il canale specifico.

**Soluzione:**
1. Modifica `eventi.json` direttamente:
```json
"channel": "Sky Sport Uno"  // invece di "Sky Sport"
```
2. Commit e push
3. Ctrl+F5 sulla web app

### "Test F1 non compare"

**Causa:** Non aggiunto in `add_special_events()`.

**Soluzione:**
1. Apri `scrape_events.py`
2. Aggiungi in `add_special_events()`:
```python
('2026-02-05', '10:00', 'Test F1 Barcellona', 'Formula 1 - Test', 'Non trasmesso', 'Test'),
```
3. Commit, push, run workflow

---

**Questo è tutto! Il sistema è ora COMPLETO e FLESSIBILE! 🎉**
