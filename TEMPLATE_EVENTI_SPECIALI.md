# 🗓️ TEMPLATE EVENTI SPECIALI DA AGGIUNGERE

## Copia e incolla in scrape_events.py → add_special_events()

### Sorteggi UEFA 2025/26

```python
# SORTEGGI CHAMPIONS LEAGUE
('2026-01-31', '12:00', 'Sorteggio Playoff Champions League', 
 'Champions League', 'Sky Sport, UEFA.com', 'Sorteggio'),

('2026-02-21', '12:00', 'Sorteggio Ottavi Champions League', 
 'Champions League', 'Sky Sport, UEFA.com', 'Sorteggio'),

# SORTEGGI EUROPA LEAGUE
('2026-01-31', '13:00', 'Sorteggio Playoff Europa League', 
 'Europa League', 'Sky Sport, UEFA.com', 'Sorteggio'),

# SORTEGGI CONFERENCE LEAGUE
('2026-01-31', '14:00', 'Sorteggio Playoff Conference League', 
 'Conference League', 'Sky Sport, UEFA.com', 'Sorteggio'),
```

### Test F1 2026

```python
# TEST BARCELLONA (Febbraio)
('2026-02-05', '09:00', 'Test F1 Barcellona - Giorno 1', 
 'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),

('2026-02-06', '09:00', 'Test F1 Barcellona - Giorno 2', 
 'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),

('2026-02-07', '09:00', 'Test F1 Barcellona - Giorno 3', 
 'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),

# TEST BAHRAIN (Marzo - se previsti)
# ('2026-03-12', '09:00', 'Test F1 Bahrain - Giorno 1', 
#  'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),
```

### Shakedown / Test MotoGP 2026

```python
# SHAKEDOWN SEPANG
('2026-01-31', '03:00', 'Shakedown MotoGP Sepang - Giorno 1', 
 'MotoGP - Shakedown', 'Non trasmesso', 'Shakedown'),

# TEST UFFICIALI SEPANG
('2026-02-05', '03:00', 'Test MotoGP Sepang - Giorno 1', 
 'MotoGP - Test', 'Non trasmesso', 'Test ufficiali'),

('2026-02-06', '03:00', 'Test MotoGP Sepang - Giorno 2', 
 'MotoGP - Test', 'Non trasmesso', 'Test ufficiali'),
```

### Altri Eventi Speciali

```python
# SUPERCOPPA UEFA
('2026-08-12', '21:00', 'Supercoppa UEFA', 
 'Supercoppa UEFA', 'Sky Sport Uno, TV8', 'Finale'),

# MONDIALE PER CLUB FIFA
# ('2026-06-15', '20:00', 'Sorteggio Mondiale per Club', 
#  'Mondiale per Club', 'Sky Sport', 'Sorteggio'),
```

---

## 📅 CALENDARIO SORTEGGI UEFA 2025/26 (Date Indicative)

| Evento | Data Approssimativa | Ora |
|--------|---------------------|-----|
| Sorteggio Playoff CL/EL/UECL | Fine gennaio | 12:00-14:00 |
| Sorteggio Ottavi CL/EL/UECL | Fine febbraio | 12:00-14:00 |
| Sorteggio Quarti CL/EL/UECL | Metà marzo | 12:00-14:00 |
| Sorteggio Semifinali CL/EL/UECL | Metà marzo | Dopo quarti |

**Verifica sempre su:** https://www.uefa.com/draws/

---

## 🏎️ CALENDARIO TEST F1 2026 (Date Indicative)

| Circuito | Date | Giorni |
|----------|------|--------|
| Barcellona | 5-7 febbraio | 3 giorni |
| Bahrain | 26-28 febbraio | 3 giorni |

**Verifica sempre su:** https://www.formula1.com/

---

## 🏍️ CALENDARIO TEST MOTOGP 2026 (Date Indicative)

| Circuito | Date | Tipo |
|----------|------|------|
| Sepang | 31 gen - 2 feb | Shakedown + Test |
| Qatar | 20-23 febbraio | Test ufficiali |

**Verifica sempre su:** https://www.motogp.com/

---

## ✏️ COME USARE QUESTO TEMPLATE

1. Copia gli eventi che ti interessano
2. Apri `scrape_events.py`
3. Cerca la funzione `add_special_events()`
4. Incolla nella lista `special_events`
5. Salva, commit e push
6. Run workflow su GitHub Actions

**Fatto! Gli eventi compariranno sulla web app! 🎉**
