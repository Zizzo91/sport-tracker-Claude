import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re

class SportEventScraper:
    def __init__(self):
        self.events = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.today = datetime.now()

        # Mapping canali corretti per competizione
        self.channels_by_competition = {
            'serie_a': 'DAZN',  # Default, poi verifichiamo se anche Sky
            'serie_b': 'DAZN, LaB Channel (Prime Video)',
            'serie_c': 'Sky Sport',
            'serie_d': 'ReggioTV',
            'champions': 'Sky Sport',
            'europa': 'Sky Sport',
            'conference': 'Sky Sport',
            'tennis': 'Eurosport, discovery+',
            'sci': 'Eurosport 2, RaiSport',
            'f1': 'Sky Sport F1',
            'motogp': 'Sky Sport MotoGP',
            'volley': 'DAZN'
        }

    def scrape_oasport(self):
        """Scrape da OASport.it"""
        try:
            for i in range(-1, 5):  # Da ieri a +4 giorni
                date = self.today + timedelta(days=i)
                day_name = self.get_italian_day_name(date.weekday())
                month_name = self.get_italian_month_name(date.month)

                url = f'https://www.oasport.it/{date.year}/{date.month:02d}/sport-in-tv-{day_name}-{date.day}-{month_name}-orari-e-programma-completo/'

                print(f"🔍 Cerco eventi per {date.strftime('%Y-%m-%d')}")

                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        self.parse_oasport_content(soup, date)
                except Exception as e:
                    print(f"  ⚠️  Errore: {e}")
                    continue

        except Exception as e:
            print(f"Errore scraping OASport: {e}")

    def scrape_serie_a_calendar(self):
        """Integra con calendario Serie A per avere orari e canali precisi"""
        print("\n🔍 Integro con fonti Serie A...")

        # Qui potresti aggiungere scraping da:
        # - https://www.legaseriea.it
        # - https://sport.sky.it/calcio/serie-a
        # Per ora uso logica intelligente

    def scrape_serie_b_calendar(self):
        """Integra calendario Serie B"""
        print("\n🔍 Cerco partite Serie B...")

        # Lista partite Serie B con Catanzaro (da aggiornare manualmente o via API)
        # Per automazione futura, si potrebbe scrapare da:
        # - https://www.legab.it
        # - https://www.dazn.com/it-IT/l/calcio/serie-b/

    def parse_oasport_content(self, soup, target_date):
        """Analizza contenuto OASport con logica migliorata"""
        date_str = target_date.strftime('%Y-%m-%d')

        if date_str not in self.events:
            self.events[date_str] = []

        content = soup.find('div', class_='post-content') or soup.find('article')
        if not content:
            print(f"  ⚠️  Contenuto non trovato")
            return

        text = content.get_text()
        lines = text.split('\n')

        # Keyword italiane
        italian_keywords = [
            'italia', 'italiano', 'italiana',
            'inter', 'milan', 'juventus', 'juve', 'roma', 'napoli', 'lazio',
            'atalanta', 'bologna', 'fiorentina', 'torino', 'udinese', 'genoa',
            'cagliari', 'verona', 'como', 'lecce', 'parma', 'cremonese',
            'sinner', 'paolini', 'berrettini', 'musetti', 'darderi', 'sonego', 'arnaldi',
            'brignone', 'goggia', 'paris', 'de aliprandini',
            'monza', 'catanzaro', 'reggina', 'pisa', 'sassuolo'
        ]

        time_pattern = r'(?:ore\s+)?(\d{1,2})[:\.](\d{2})'

        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean:
                continue

            line_lower = line_clean.lower()

            # Cerca orari
            time_match = re.search(time_pattern, line_clean)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                time = f"{hour:02d}:{minute:02d}"

                # Verifica se contiene italiani
                is_italian = any(keyword in line_lower for keyword in italian_keywords)

                # Determina sport e competizione
                sport_type = self.detect_sport(line_lower)
                competition_key = self.detect_competition_key(line_lower, sport_type)

                if sport_type and (is_italian or sport_type in ['f1', 'motogp']):
                    # Determina data corretta
                    actual_date = date_str
                    if hour < 6 and self.today.hour >= 18:
                        context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)])
                        if 'domani' in context.lower():
                            next_day = target_date + timedelta(days=1)
                            actual_date = next_day.strftime('%Y-%m-%d')
                            if actual_date not in self.events:
                                self.events[actual_date] = []

                    # Estrai nome evento
                    event_name = self.clean_event_name(line_clean, time)

                    # Determina canale corretto
                    channel = self.get_correct_channel(sport_type, competition_key, line_clean, event_name)

                    # Crea evento
                    event = {
                        'time': time,
                        'event': event_name,
                        'competition': self.get_competition_name(line_lower, sport_type),
                        'sport': sport_type,
                        'channel': channel,
                        'notes': self.extract_notes(line_lower, line_clean),
                        'highlight': is_italian
                    }

                    # Evita duplicati
                    if not self.is_duplicate(self.events[actual_date], event):
                        self.events[actual_date].append(event)
                        print(f"  ✅ {actual_date} {time} - {event_name[:50]}")

    def detect_competition_key(self, text, sport):
        """Rileva la chiave della competizione per assegnare il canale corretto"""
        if sport == 'calcio':
            if 'serie a' in text and 'serie b' not in text:
                return 'serie_a'
            elif 'serie b' in text:
                return 'serie_b'
            elif 'serie c' in text:
                return 'serie_c'
            elif 'serie d' in text:
                return 'serie_d'
            elif 'champions' in text:
                return 'champions'
            elif 'europa league' in text:
                return 'europa'
            elif 'conference' in text:
                return 'conference'
        elif sport == 'tennis':
            return 'tennis'
        elif sport == 'sci':
            return 'sci'
        elif sport == 'f1':
            return 'f1'
        elif sport == 'motogp':
            return 'motogp'
        elif sport == 'volley':
            return 'volley'

        return None

    def get_correct_channel(self, sport, competition_key, text_original, event_name):
        """Determina il canale TV corretto basandosi su competizione e logica"""

        # Serie B: sempre DAZN + Prime Video
        if competition_key == 'serie_b':
            return self.channels_by_competition['serie_b']

        # Serie D: ReggioTV per Reggina
        if competition_key == 'serie_d':
            if 'reggina' in event_name.lower():
                return 'ReggioTV'

        # Champions, Europa, Conference: Sky
        if competition_key in ['champions', 'europa', 'conference']:
            # Cerca numero canale Sky
            sky_match = re.search(r'sky sport\s*(uno|calcio|\d{3})', text_original.lower())
            if sky_match:
                num = sky_match.group(1)
                if num.isdigit():
                    base_channel = f'Sky Sport {num}'
                elif num == 'uno':
                    base_channel = 'Sky Sport Uno'
                else:
                    base_channel = 'Sky Sport'
            else:
                base_channel = 'Sky Sport'

            # Aggiungi diretta gol se menzionata
            if 'diretta gol' in text_original.lower():
                dg_match = re.search(r'diretta gol.*?(\d{3})', text_original.lower())
                if dg_match:
                    return base_channel
                else:
                    return base_channel
            return base_channel

        # Serie A: logica DAZN vs DAZN+Sky
        if competition_key == 'serie_a':
            # Verifica se esplicitamente menziona Sky
            has_sky = 'sky' in text_original.lower()
            has_dazn = 'dazn' in text_original.lower()

            if has_sky and has_dazn:
                return 'DAZN, Sky Sport'
            elif has_sky:
                return 'DAZN, Sky Sport'  # Probabile co-esclusiva
            else:
                return 'DAZN'  # Default per Serie A

        # Fallback al mapping standard
        if competition_key and competition_key in self.channels_by_competition:
            return self.channels_by_competition[competition_key]

        # Ultima risorsa: estrai dal testo
        return self.extract_channel_from_text(text_original) or 'Da verificare'

    def extract_channel_from_text(self, text):
        """Estrae canale dal testo (fallback)"""
        text_lower = text.lower()

        # Priorità a canali specifici
        if 'sky sport uno' in text_lower:
            return 'Sky Sport Uno'
        elif 'sky sport calcio' in text_lower:
            return 'Sky Sport Calcio'
        elif re.search(r'sky sport\s*\d{3}', text_lower):
            match = re.search(r'sky sport\s*(\d{3})', text_lower)
            return f'Sky Sport {match.group(1)}'
        elif 'sky sport' in text_lower:
            return 'Sky Sport'
        elif 'dazn' in text_lower:
            return 'DAZN'
        elif 'prime video' in text_lower:
            return 'Prime Video'
        elif 'eurosport 2' in text_lower:
            return 'Eurosport 2'
        elif 'eurosport' in text_lower:
            return 'Eurosport'
        elif 'discovery+' in text_lower or 'discovery plus' in text_lower:
            return 'discovery+'
        elif 'raisport' in text_lower or 'rai sport' in text_lower:
            return 'RaiSport'
        elif 'tv8' in text_lower:
            return 'TV8'

        return ''

    def add_manual_events(self):
        """Aggiungi eventi che potrebbero mancare dallo scraping"""
        print("\n📝 Aggiungo eventi manuali di sicurezza...")

        # Partite Serie A conosciute (aggiorna settimanalmente)
        manual_serie_a = [
            # Formato: (data, ora, squadra1, squadra2, canale)
            # Lascia vuoto o aggiorna manualmente
        ]

        # Partite Serie B con Catanzaro
        manual_serie_b_catanzaro = [
            # ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),
            # Aggiungi qui le prossime partite del Catanzaro
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
                print(f"  ✅ Aggiunto: {date} {time} - {home} - {away}")

    def is_duplicate(self, events_list, new_event):
        """Controlla duplicati"""
        for existing in events_list:
            if (existing['time'] == new_event['time'] and 
                self.similar_events(existing['event'], new_event['event'])):
                return True
        return False

    def similar_events(self, event1, event2):
        """Verifica se due eventi sono simili"""
        # Normalizza
        e1 = event1.lower().replace('-', '').replace('vs', '').strip()[:40]
        e2 = event2.lower().replace('-', '').replace('vs', '').strip()[:40]

        # Calcola similarità semplice
        return e1 == e2 or e1 in e2 or e2 in e1

    def get_italian_day_name(self, weekday):
        days = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
        return days[weekday]

    def get_italian_month_name(self, month):
        months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        return months[month - 1]

    def detect_sport(self, text):
        if any(word in text for word in ['calcio', 'serie a', 'serie b', 'champions', 'europa league', 'conference']):
            return 'calcio'
        elif any(word in text for word in ['tennis', 'atp', 'wta', 'australian open', 'roland garros', 'wimbledon', 'us open']):
            return 'tennis'
        elif 'formula 1' in text or 'f1' in text or 'formula1' in text:
            return 'f1'
        elif 'motogp' in text or 'moto gp' in text:
            return 'motogp'
        elif any(word in text for word in ['sci', 'slalom', 'discesa', 'super-g', 'gigante']):
            return 'sci'
        elif 'volley' in text or 'pallavolo' in text:
            return 'volley'
        return None

    def get_competition_name(self, text, sport):
        if sport == 'calcio':
            if 'champions' in text:
                return 'Champions League'
            elif 'europa league' in text:
                return 'Europa League'
            elif 'conference' in text:
                return 'Conference League'
            elif 'serie a' in text and 'serie b' not in text:
                # Prova a estrarre giornata
                giornata_match = re.search(r'(\d+)[ªa°]\s*giornata', text)
                if giornata_match:
                    return f'Serie A - {giornata_match.group(1)}ª giornata'
                return 'Serie A'
            elif 'serie b' in text:
                giornata_match = re.search(r'(\d+)[ªa°]\s*giornata', text)
                if giornata_match:
                    return f'Serie B - {giornata_match.group(1)}ª giornata'
                return 'Serie B'
            elif 'serie d' in text:
                return 'Serie D - Girone I'
            return 'Calcio'
        elif sport == 'tennis':
            if 'australian open' in text:
                return 'Australian Open'
            elif 'semifinale' in text or 'semifinali' in text:
                return 'Australian Open'
            elif 'finale' in text:
                return 'Australian Open'
            return 'Tennis ATP/WTA'
        elif sport == 'sci':
            return 'Sci Alpino - Coppa del Mondo'
        elif sport == 'f1':
            if 'test' in text:
                return 'Formula 1 - Test'
            elif 'prove' in text:
                return 'Formula 1 - Prove'
            elif 'qualifiche' in text:
                return 'Formula 1 - Qualifiche'
            elif 'gara' in text or 'gran premio' in text:
                return 'Formula 1 - Gara'
            return 'Formula 1'
        elif sport == 'motogp':
            if 'test' in text:
                return 'MotoGP - Test'
            return 'MotoGP'
        elif sport == 'volley':
            return 'Volley'
        return sport.title()

    def extract_notes(self, text_lower, text_original):
        notes = []

        # Diretta gol
        dg_match = re.search(r'diretta gol.*?(?:sky sport\s*)?(\d{3})', text_lower)
        if dg_match:
            notes.append(f'Diretta Gol: Sky Sport {dg_match.group(1)}')
        elif 'diretta gol' in text_lower:
            notes.append('Diretta Gol disponibile')

        # Semifinale/Finale
        if 'semifinale' in text_lower:
            notes.append('Semifinale')
        elif 'finale' in text_lower and 'semifinale' not in text_lower:
            notes.append('Finale')

        # Prova sci
        prova_match = re.search(r'(\d+)[ªa°]\s*prova', text_lower)
        if prova_match:
            notes.append(f'{prova_match.group(1)}ª prova')

        # Differita
        if 'differita' in text_lower:
            notes.append('In differita')

        # Luogo per eventi fuori casa
        if 'trasferta' in text_lower:
            notes.append('Trasferta')

        return ', '.join(notes) if notes else ''

    def clean_event_name(self, text, time_str):
        # Rimuovi orario
        text = re.sub(r'\d{1,2}[:\.\s]\d{2}', '', text)
        text = re.sub(r'ore\s+', '', text, flags=re.IGNORECASE)

        # Rimuovi canali
        text = re.sub(r'Sky Sport.*?(?=\s|$)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'DAZN|Prime Video|Eurosport|RaiSport|TV8|discovery\+|LaB Channel', '', text, flags=re.IGNORECASE)

        # Rimuovi parole comuni
        text = re.sub(r'\b(diretta|streaming|live|gratis|differita)\b', '', text, flags=re.IGNORECASE)

        # Pulisci spazi
        text = re.sub(r'\s+', ' ', text)

        return text.strip()[:100]

    def filter_relevant_events(self):
        """Filtra eventi rilevanti"""
        filtered = {}

        for date, events in self.events.items():
            filtered[date] = []

            for event in events:
                should_include = False
                sport = event['sport']
                comp = event['competition'].lower()
                ev_name = event['event'].lower()

                # Calcio
                if sport == 'calcio':
                    if 'serie a' in comp:
                        should_include = True
                    elif 'champions' in comp or 'europa' in comp or 'conference' in comp:
                        italian_teams = ['inter', 'milan', 'juventus', 'juve', 'roma', 'napoli', 
                                       'lazio', 'atalanta', 'bologna', 'fiorentina']
                        should_include = any(team in ev_name for team in italian_teams)
                    elif 'serie b' in comp:
                        should_include = 'monza' in ev_name or 'catanzaro' in ev_name
                    elif 'serie d' in comp:
                        should_include = 'reggina' in ev_name

                # Tennis
                elif sport == 'tennis':
                    italian_players = ['sinner', 'paolini', 'berrettini', 'musetti', 
                                     'darderi', 'sonego', 'arnaldi', 'italia']
                    should_include = any(player in ev_name for player in italian_players)

                # F1 e MotoGP
                elif sport in ['f1', 'motogp']:
                    should_include = True

                # Sci
                elif sport == 'sci':
                    should_include = 'brignone' in ev_name or 'goggia' in ev_name

                # Volley
                elif sport == 'volley':
                    should_include = 'monza' in ev_name or 'vero volley' in ev_name

                if should_include:
                    filtered[date].append(event)

            if not filtered[date]:
                del filtered[date]

        return filtered

    def save_to_json(self, filename='eventi.json'):
        filtered_events = self.filter_relevant_events()
        sorted_events = dict(sorted(filtered_events.items()))

        for date in sorted_events:
            sorted_events[date] = sorted(sorted_events[date], key=lambda x: x['time'])

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_events, f, ensure_ascii=False, indent=2)

        total_events = sum(len(v) for v in sorted_events.values())
        print(f"\n✅ Salvati {total_events} eventi rilevanti in {filename}")
        return sorted_events

def main():
    print("🔄 Inizio scraping eventi sportivi...")
    print(f"📅 Data corrente: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    scraper = SportEventScraper()

    # Scraping
    scraper.scrape_oasport()
    scraper.add_manual_events()

    # Salva
    events = scraper.save_to_json('eventi.json')

    print(f"\n📊 Riepilogo:")
    for date, evs in events.items():
        print(f"\n  {date} ({len(evs)} eventi):")
        for ev in evs[:5]:  # Primi 5
            highlight = "⭐" if ev['highlight'] else "  "
            print(f"    {highlight} {ev['time']} - {ev['event'][:45]:45} | {ev['channel']}")

    print("\n✅ Scraping completato!")

if __name__ == '__main__':
    main()
