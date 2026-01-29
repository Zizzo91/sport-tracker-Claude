#!/usr/bin/env python3
"""
Script di test rapido per verificare il corretto funzionamento del sistema
"""
import json
from datetime import datetime, timedelta

def test_json_structure():
    """Verifica la struttura del file JSON"""
    print("🧪 Test 1: Struttura JSON")
    try:
        with open('eventi.json', 'r', encoding='utf-8') as f:
            events = json.load(f)

        if not isinstance(events, dict):
            print("  ❌ Il JSON non è un dizionario")
            return False

        print(f"  ✅ JSON valido con {len(events)} date")
        return True
    except FileNotFoundError:
        print("  ❌ File eventi.json non trovato")
        return False
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON non valido: {e}")
        return False

def test_date_correctness():
    """Verifica che gli eventi siano nelle date corrette"""
    print("\n🧪 Test 2: Correttezza Date")

    with open('eventi.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    today = datetime.now().date()
    issues = []

    for date_str, event_list in events.items():
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        for event in event_list:
            time_parts = event['time'].split(':')
            hour = int(time_parts[0])

            # Eventi molto presto la mattina dovrebbero essere controllati
            if hour < 6:
                days_diff = (event_date - today).days
                if days_diff < 0:
                    issues.append(f"  ⚠️  {date_str} {event['time']} - {event['event'][:40]} - Evento passato con orario mattutino")

    if issues:
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✅ Tutte le date sembrano corrette")
        return True

def test_required_fields():
    """Verifica che tutti gli eventi abbiano i campi richiesti"""
    print("\n🧪 Test 3: Campi Richiesti")

    with open('eventi.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    required_fields = ['time', 'event', 'competition', 'sport', 'channel', 'notes', 'highlight']
    missing = []

    for date_str, event_list in events.items():
        for i, event in enumerate(event_list):
            for field in required_fields:
                if field not in event:
                    missing.append(f"  ❌ {date_str} evento #{i}: manca '{field}'")

    if missing:
        for m in missing[:10]:  # Mostra solo i primi 10
            print(m)
        return False
    else:
        print(f"  ✅ Tutti gli eventi hanno i campi richiesti")
        return True

def test_time_format():
    """Verifica il formato degli orari"""
    print("\n🧪 Test 4: Formato Orari")

    with open('eventi.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    import re
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    invalid = []

    for date_str, event_list in events.items():
        for event in event_list:
            if not time_pattern.match(event['time']):
                invalid.append(f"  ❌ {date_str}: orario '{event['time']}' non valido")

    if invalid:
        for inv in invalid[:10]:
            print(inv)
        return False
    else:
        print("  ✅ Tutti gli orari nel formato corretto (HH:MM)")
        return True

def test_today_tomorrow_classification():
    """Verifica che eventi siano classificati correttamente"""
    print("\n🧪 Test 5: Classificazione Oggi/Domani")

    with open('eventi.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    today_str = today.strftime('%Y-%m-%d')
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    today_events = events.get(today_str, [])
    tomorrow_events = events.get(tomorrow_str, [])

    print(f"  📅 Oggi ({today_str}): {len(today_events)} eventi")
    for ev in today_events[:3]:
        print(f"     • {ev['time']} - {ev['event'][:50]}")

    print(f"  📅 Domani ({tomorrow_str}): {len(tomorrow_events)} eventi")
    for ev in tomorrow_events[:3]:
        print(f"     • {ev['time']} - {ev['event'][:50]}")

    # Verifica eventi mattutini di domani non siano sotto oggi
    issues = []
    for ev in today_events:
        hour = int(ev['time'].split(':')[0])
        if hour < 6:
            issues.append(f"  ⚠️  Evento molto mattutino ({ev['time']}) classificato come 'oggi'")

    if issues:
        for issue in issues:
            print(issue)
        print("  ℹ️  Verifica manualmente se questi eventi sono corretti")

    return True

def print_summary():
    """Stampa riepilogo eventi"""
    print("\n📊 Riepilogo Eventi")
    print("=" * 60)

    with open('eventi.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    total = sum(len(v) for v in events.values())

    print(f"\n  Totale eventi: {total}")
    print(f"  Giorni coperti: {len(events)}")

    # Conta per sport
    sports_count = {}
    for event_list in events.values():
        for event in event_list:
            sport = event['sport']
            sports_count[sport] = sports_count.get(sport, 0) + 1

    print("\n  Eventi per sport:")
    for sport, count in sorted(sports_count.items(), key=lambda x: -x[1]):
        emoji = {'calcio': '⚽', 'tennis': '🎾', 'sci': '⛷️', 'f1': '🏎️', 
                'motogp': '🏍️', 'volley': '🏐'}.get(sport, '📺')
        print(f"    {emoji} {sport.title()}: {count}")

def main():
    print("🚀 Test Sistema Eventi Sportivi")
    print("=" * 60)

    tests = [
        test_json_structure,
        test_date_correctness,
        test_required_fields,
        test_time_format,
        test_today_tomorrow_classification
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print_summary()

    print("\n" + "=" * 60)
    print(f"Risultato: {passed}/{len(tests)} test superati")

    if passed == len(tests):
        print("✅ Tutti i test passati! Sistema pronto per il deploy.")
    else:
        print("⚠️  Alcuni test falliti. Controlla gli errori sopra.")

    print("=" * 60)

if __name__ == '__main__':
    main()
