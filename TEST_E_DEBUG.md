# 🧪 Guida Test e Risoluzione Problemi

## 🔍 Come Testare Localmente

### Test 1: Verifica lo Scraper

```bash
# Esegui lo scraper manualmente
python scrape_events.py
```

**Output atteso:**
```
🔄 Inizio scraping eventi sportivi...
📅 Data corrente: 2026-01-29 18:30:00

🔍 Cerco eventi per 2026-01-28 su https://...
  ✅ 2026-01-28 21:00 - Monaco - Juventus
  ✅ 2026-01-29 18:45 - Maccabi Tel Aviv - Bologna

📊 Riepilogo eventi per giorno:
  2026-01-29:
    ⭐ 18:45 - Maccabi Tel Aviv - Bologna
    ⭐ 21:00 - Panathinaikos - Roma
  2026-01-30:
    ⭐ 09:30 - Sinner vs Avversario - Semifinale

✅ Salvati 15 eventi rilevanti in eventi.json
```

### Test 2: Verifica il JSON Generato

```bash
# Visualizza il file JSON in formato leggibile
python -m json.tool eventi.json
```

**Controlla che:**
- ✅ Le date siano corrette (eventi di domani non sotto oggi)
- ✅ Gli orari siano in formato HH:MM
- ✅ I canali TV siano presenti
- ✅ Solo eventi rilevanti siano inclusi

### Test 3: Verifica la Web App

```bash
# Avvia server locale
python -m http.server 8000

# Apri nel browser
# http://localhost:8000
```

**Test nel browser:**
1. ✅ Clicca "Ricarica" - dovrebbe animarsi
2. ✅ Filtra per "Oggi" - vedi solo eventi di oggi
3. ✅ Filtra per "Domani" - vedi solo eventi di domani
4. ✅ Su mobile (F12 → device toolbar) - tabella responsive

---

## 🐛 Risoluzione Problemi Comuni

### Problema: Eventi nella data sbagliata

**Causa:** Lo scraper non ha identificato correttamente quando un evento è "domani"

**Soluzione:**
1. Controlla l'articolo OASport manualmente
2. Se l'articolo dice "domani" ma l'evento è classificato oggi:
   - Aggiungi debug in `parse_oasport_content()`
   ```python
   print(f"  DEBUG: Orario {hour}:{minute}, Ora corrente: {self.today.hour}")
   print(f"  DEBUG: Contesto: {context[:100]}")
   ```

3. Regola la logica nella sezione:
   ```python
   if hour < 6 and self.today.hour >= 18:
       # Potrebbe essere domani
   ```

**Fix manuale rapido:**
Modifica direttamente `eventi.json` spostando l'evento alla data corretta.

### Problema: Canale TV non rilevato

**Causa:** Nome canale non in `channels_map`

**Soluzione:**
Aggiungi il canale in `extract_channel()`:
```python
channels_map = {
    'sky sport uno': 'Sky Sport Uno',
    'nuovo_canale': 'Nuovo Canale',  # ← Aggiungi qui
}
```

### Problema: Eventi duplicati

**Causa:** Stesso evento trovato più volte nello stesso articolo

**Soluzione:**
La funzione `is_duplicate()` dovrebbe prevederlo. Verifica con:
```python
print(f"  Controllo duplicati per: {event_name}")
```

Se persiste, aumenta i caratteri di confronto:
```python
existing['event'][:50] == new_event['event'][:50]  # da 30 a 50
```

### Problema: GitHub Actions fallisce

**Errori comuni:**

**1. "Module not found: bs4"**
```yaml
# Verifica in .github/workflows/update-events.yml
- name: Install dependencies
  run: |
    pip install requests beautifulsoup4 lxml  # ✅ Corretto
```

**2. "Permission denied"**
```yaml
# Aggiungi permessi al workflow
permissions:
  contents: write
```

**3. "Nothing to commit"**
- Normale se non ci sono nuovi eventi
- Il workflow non fa push se `eventi.json` è invariato

### Problema: Scraping non trova eventi

**Possibili cause:**
1. OASport ha cambiato struttura HTML
2. URL non corretto (giorno/mese in italiano)
3. Richiesta bloccata (rate limiting)

**Debug:**
```python
# In scrape_oasport(), aggiungi:
print(f"URL: {url}")
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)}")

# Salva HTML per ispezionarlo
with open(f'debug_{date_str}.html', 'wb') as f:
    f.write(response.content)
```

---

## ✅ Checklist Pre-Deploy

Prima di fare push su GitHub:

- [ ] `python scrape_events.py` funziona senza errori
- [ ] `eventi.json` contiene eventi con date corrette
- [ ] Web app si carica correttamente in locale
- [ ] File in `.github/workflows/update-events.yml` (non nella root)
- [ ] `requirements.txt` contiene: requests, beautifulsoup4, lxml
- [ ] `.gitignore` esclude `__pycache__` e file di test

---

## 🔧 Test Manuale GitHub Actions

Dopo il push:

1. **Vai su GitHub** → tab **Actions**
2. **Seleziona** "Aggiorna Eventi Sportivi"
3. **Click** su "Run workflow" → "Run workflow"
4. **Aspetta** 1-2 minuti
5. **Controlla** i log:
   ```
   ✅ Run scraper
   ✅ Check for changes  
   ✅ Commit and push if changed
   ```

Se fallisce:
- Leggi l'errore nel log
- Correggi localmente
- Fai push della correzione
- Riprova

---

## 📊 Monitoraggio Continuo

### Verifica settimanale:

```bash
# Ogni lunedì, controlla:
git pull  # Scarica ultimi aggiornamenti
cat eventi.json | grep "$(date +%Y-%m)" | wc -l  # Conta eventi del mese
```

### Log GitHub Actions:

Controlla ogni giorno che il workflow:
- ✅ Si esegue alle 06:00 e 18:00
- ✅ Completa senza errori
- ✅ Trova almeno qualche evento

Se per 2+ giorni consecutivi non trova eventi:
→ Possibile cambio struttura OASport
→ Verifica manualmente e aggiorna lo scraper

---

## 🆘 Supporto

**Errori persistenti?**

1. Controlla [Issue su GitHub del progetto]
2. Crea un nuovo Issue con:
   - Output completo del comando
   - File `eventi.json` generato
   - Screenshot dell'errore

**Fonti alternative:**

Se OASport non funziona, considera:
- API sportive (The Sports DB, API-Football)
- RSS feed di Sky Sport / DAZN
- Scraping da Gazzetta.it o Corriere Sport

---

**Buon debugging! 🚀**
