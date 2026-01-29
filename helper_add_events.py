#!/usr/bin/env python3
"""
Helper per aggiungere rapidamente eventi al database
"""
import json
from datetime import datetime

def add_serie_b_match(date, time, home, away, output_file='eventi_extra.json'):
    """Aggiungi una partita di Serie B"""
    event = {
        "date": date,
        "time": time,
        "home": home,
        "away": away,
        "competition": "Serie B",
        "channel": "DAZN, LaB Channel (Prime Video)"
    }

    print(f"✅ Aggiunto: {date} {time} - {home} vs {away}")
    return event

def add_serie_d_match(date, time, home, away, output_file='eventi_extra.json'):
    """Aggiungi una partita di Serie D Reggina"""
    event = {
        "date": date,
        "time": time,
        "home": home,
        "away": away,
        "competition": "Serie D - Girone I",
        "channel": "ReggioTV",
        "notes": "Trasferta Reggina" if away.lower() == "reggina" else ""
    }

    print(f"✅ Aggiunto: {date} {time} - {home} vs {away}")
    return event

def quick_add_catanzaro():
    """Aggiungi rapidamente le prossime partite del Catanzaro"""
    # MODIFICA QUI le prossime partite del Catanzaro
    matches = [
        ("2026-01-31", "15:00", "Südtirol", "Catanzaro"),
        ("2026-02-07", "15:00", "Catanzaro", "Bari"),
        ("2026-02-14", "15:00", "Spezia", "Catanzaro"),
        # Aggiungi altre partite...
    ]

    events = []
    for date, time, home, away in matches:
        events.append(add_serie_b_match(date, time, home, away))

    return events

def merge_with_main_events(extra_events, main_file='eventi.json'):
    """Unisci eventi extra con il file principale"""
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            main_events = json.load(f)
    except FileNotFoundError:
        main_events = {}

    # Aggiungi eventi extra
    for event in extra_events:
        date = event['date']
        if date not in main_events:
            main_events[date] = []

        # Converti in formato standard
        std_event = {
            'time': event['time'],
            'event': f"{event['home']} - {event['away']}",
            'competition': event['competition'],
            'sport': 'calcio',
            'channel': event['channel'],
            'notes': event.get('notes', ''),
            'highlight': True
        }

        # Verifica duplicati
        is_duplicate = False
        for existing in main_events[date]:
            if existing['time'] == std_event['time'] and existing['event'] == std_event['event']:
                is_duplicate = True
                break

        if not is_duplicate:
            main_events[date].append(std_event)

    # Ordina per data e orario
    sorted_events = dict(sorted(main_events.items()))
    for date in sorted_events:
        sorted_events[date] = sorted(sorted_events[date], key=lambda x: x['time'])

    # Salva
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_events, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Eventi aggiornati in {main_file}")

if __name__ == '__main__':
    print("🔧 Helper Aggiunta Eventi\n")

    # Aggiungi partite Catanzaro
    extra = quick_add_catanzaro()

    # Unisci con eventi principali
    merge_with_main_events(extra)

    print("\n✨ Completato!")
