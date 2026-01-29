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

        # Mapping canali per competizione
        self.channels_by_competition = {
            'serie_a': 'DAZN',
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
            for i in range(-1, 7):  # Da ieri a +6 giorni (per coprire più eventi)
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

    def scrape_serie_b_calendar(self):
        """
        INTEGRAZIONE SERIE B - Cerca partite specifiche
        Questo metodo cerca attivamente le partite di Monza e Catanzaro
        """
        print("\n🔍 Cerco partite Serie B (Monza e Catanzaro)...")

        # URL calendario Serie B (può essere scrapato da legab.it o altri siti)
        # Per ora uso logica manuale + cerca su OASport

        teams_to_track = ['monza', 'catanzaro']

        # Cerca nelle prossime 2 settimane
        for i in range(0, 14):
            date = self.today + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')

            # Logica: ogni weekend ci sono partite di Serie B
            # Sabato e domenica ore 15:00, 17:15, 20:30
            if date.weekday() in [5, 6]:  # Sabato=5, Domenica=6
                # Qui potresti fare scraping specifico da altri siti
                # oppure usare una API se disponibile
                pass

        print("  ℹ️  Per partite Serie B non trovate automaticamente,")
        print("      aggiungile manualmente in add_manual_events()")

    def add_special_events(self):
        """
        NUOVA FUNZIONE: Eventi speciali (sorteggi, test, shakedown)
        """
        print("\n📅 Aggiungo eventi speciali...")

        # SORTEGGI Champions/Europa/Conference League
        special_events = [
            # Formato: (data, ora, evento, competizione, canale, note)
            ('2026-01-30', '12:00', 'Sorteggio Playoff Champions League', 'Champions League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),
            ('2026-01-30', '13:00', 'Sorteggio Playoff Europa League', 'Europa League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),
            ('2026-01-30', '14:00', 'Sorteggio Playoff Conference League', 'Conference League', 'Sky Sport, streaming UEFA.com', 'Sorteggio'),

            # TEST F1/MotoGP (anche se non in TV, li tracciamo)
            # ('2026-02-05', '10:00', 'Test F1 Barcellona - Giorno 1', 'Formula 1 - Test', 'Non trasmesso', 'Test a porte chiuse'),
        ]

        for date, time, event, competition, channel, notes in special_events:
            if date not in self.events:
                self.events[date] = []

            evt = {
                'time': time,
                'event': event,
                'competition': competition,
                'sport': self.detect_sport_from_competition(competition),
                'channel': channel,
                'notes': notes,
                'highlight': True  # Eventi speciali sempre evidenziati
            }

            if not self.is_duplicate(self.events[date], evt):
                self.events[date].append(evt)
                print(f"  ✅ {date} {time} - {event}")

    def detect_sport_from_competition(self, competition):
        """Rileva sport dalla competizione"""
        comp_lower = competition.lower()
        if 'champions' in comp_lower or 'europa' in comp_lower or 'conference' in comp_lower or 'calcio' in comp_lower:
            return 'calcio'
        elif 'formula 1' in comp_lower or 'f1' in comp_lower:
            return 'f1'
        elif 'motogp' in comp_lower:
            return 'motogp'
        elif 'tennis' in comp_lower:
            return 'tennis'
        elif 'sci' in comp_lower:
            return 'sci'
        return 'altro'

    def parse_oasport_content(self, soup, target_date):
        """Analizza contenuto OASport con riconoscimento canali specifici"""
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
            'monza', 'catanzaro', 'reggina', 'pisa', 'sassuolo',
            # Aggiungi altri nomi se necessario
        ]

        # NUOVA KEYWORD per eventi speciali
        special_keywords = ['sorteggio', 'sorteggi', 'test', 'shakedown', 'prove libere']

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

                # Verifica se contiene italiani o eventi speciali
                is_italian = any(keyword in line_lower for keyword in italian_keywords)
                is_special = any(keyword in line_lower for keyword in special_keywords)

                # Determina sport e competizione
                sport_type = self.detect_sport(line_lower)
                competition_key = self.detect_competition_key(line_lower, sport_type)

                if sport_type and (is_italian or is_special or sport_type in ['f1', 'motogp']):
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

                    # *** MODIFICA CHIAVE: Estrai canale SPECIFICO ***
                    channel = self.extract_specific_channel(line_clean, sport_type, competition_key, event_name)

                    # Determina se è un evento non in TV
                    is_not_on_tv = 'non trasmesso' in line_lower or 'porte chiuse' in line_lower or 'non in tv' in line_lower

                    # Crea evento
                    event = {
                        'time': time,
                        'event': event_name,
                        'competition': self.get_competition_name(line_lower, sport_type),
                        'sport': sport_type,
                        'channel': channel if not is_not_on_tv else 'Non trasmesso',
                        'notes': self.extract_notes(line_lower, line_clean),
                        'highlight': is_italian or is_special
                    }

                    # Evita duplicati
                    if not self.is_duplicate(self.events[actual_date], event):
                        self.events[actual_date].append(event)
                        print(f"  ✅ {actual_date} {time} - {event_name[:50]}")

    def extract_specific_channel(self, text, sport, competition_key, event_name):
        """
        NUOVA FUNZIONE: Estrae canale TV SPECIFICO
        Cerca Sky Sport Uno, Sky Sport Calcio, Sky Sport 251, ecc.
        """
        text_lower = text.lower()

        # Serie B: sempre uguale
        if competition_key == 'serie_b':
            return 'DAZN, LaB Channel (Prime Video)'

        # Serie D Reggina
        if competition_key == 'serie_d' and 'reggina' in event_name.lower():
            return 'ReggioTV'

        # Champions/Europa/Conference: cerca canale Sky specifico
        if competition_key in ['champions', 'europa', 'conference']:
            # Cerca pattern: "Sky Sport Uno", "Sky Sport 251", ecc.

            # Pattern 1: Sky Sport Uno/Calcio/Arena/ecc.
            sky_named = re.search(r'sky sport\s+(uno|calcio|arena|24|serie a|football)', text_lower)
            if sky_named:
                name = sky_named.group(1).capitalize()
                if name == 'Uno':
                    base_channel = 'Sky Sport Uno'
                elif name == 'Calcio':
                    base_channel = 'Sky Sport Calcio'
                elif name == 'Arena':
                    base_channel = 'Sky Sport Arena'
                elif name == '24':
                    base_channel = 'Sky Sport 24'
                else:
                    base_channel = f'Sky Sport {name.title()}'
            else:
                base_channel = 'Sky Sport'

            # Pattern 2: Sky Sport + numero (251, 252, ecc.)
            sky_numbered = re.search(r'sky sport\s+(\d{3})', text_lower)
            if sky_numbered:
                num = sky_numbered.group(1)
                base_channel = f'Sky Sport {num}'

            # Cerca Diretta Gol
            diretta_gol = re.search(r'diretta gol.*?sky sport\s*(\d{3})', text_lower)
            if diretta_gol:
                # Non sovrascrivere base_channel, lo aggiungiamo nelle note
                pass

            return base_channel

        # Serie A: DAZN vs DAZN+Sky
        if competition_key == 'serie_a':
            has_sky = 'sky' in text_lower
            has_dazn = 'dazn' in text_lower

            if has_sky:
                # Cerca canale Sky specifico
                sky_named = re.search(r'sky sport\s+(uno|calcio|arena)', text_lower)
                if sky_named:
                    name = sky_named.group(1)
                    if name == 'uno':
                        return 'DAZN, Sky Sport Uno'
                    elif name == 'calcio':
                        return 'DAZN, Sky Sport Calcio'
                    else:
                        return f'DAZN, Sky Sport {name.title()}'
                else:
                    return 'DAZN, Sky Sport'
            else:
                return 'DAZN'

        # F1
        if sport == 'f1':
            return 'Sky Sport F1'

        # MotoGP
        if sport == 'motogp':
            return 'Sky Sport MotoGP'

        # Tennis
        if sport == 'tennis':
            has_eurosport = 'eurosport' in text_lower
            has_discovery = 'discovery' in text_lower
            if has_eurosport and has_discovery:
                return 'Eurosport, discovery+'
            elif has_eurosport:
                if 'eurosport 2' in text_lower:
                    return 'Eurosport 2'
                elif 'eurosport 1' in text_lower:
                    return 'Eurosport 1'
                return 'Eurosport'
            return 'Eurosport, discovery+'

        # Sci
        if sport == 'sci':
            has_eurosport = 'eurosport' in text_lower
            has_rai = 'rai' in text_lower
            if has_eurosport and has_rai:
                if 'eurosport 2' in text_lower:
                    return 'Eurosport 2, RaiSport'
                return 'Eurosport, RaiSport'
            elif has_eurosport:
                return 'Eurosport 2'
            elif has_rai:
                return 'RaiSport'
            return 'Eurosport 2, RaiSport'

        # Fallback: estrai dal testo
        return self.extract_channel_from_text(text) or 'Da verificare'

    def extract_channel_from_text(self, text):
        """Estrae canale dal testo (fallback)"""
        text_lower = text.lower()

        # Cerca canali specifici con priorità
        patterns = [
            (r'sky sport uno', 'Sky Sport Uno'),
            (r'sky sport calcio', 'Sky Sport Calcio'),
            (r'sky sport arena', 'Sky Sport Arena'),
            (r'sky sport (\d{3})', lambda m: f'Sky Sport {m.group(1)}'),
            (r'sky sport 24', 'Sky Sport 24'),
            (r'sky sport f1', 'Sky Sport F1'),
            (r'sky sport motogp', 'Sky Sport MotoGP'),
            (r'sky sport', 'Sky Sport'),
            (r'dazn', 'DAZN'),
            (r'prime video', 'Prime Video'),
            (r'eurosport 2', 'Eurosport 2'),
            (r'eurosport 1', 'Eurosport 1'),
            (r'eurosport', 'Eurosport'),
            (r'discovery\+|discovery plus', 'discovery+'),
            (r'raisport|rai sport', 'RaiSport'),
            (r'tv8', 'TV8'),
        ]

        for pattern, replacement in patterns:
            match = re.search(pattern, text_lower)
            if match:
                if callable(replacement):
                    return replacement(match)
                return replacement

        return ''

    def add_manual_events(self):
        """
        EVENTI MANUALI - Qui aggiungi partite che lo scraper potrebbe non trovare
        """
        print("\n📝 Aggiungo eventi manuali...")

        # *** PARTITE SERIE B CATANZARO ***
        # Aggiorna questa lista ogni settimana con le prossime partite
        manual_serie_b_catanzaro = [
            ('2026-01-31', '15:00', 'Südtirol', 'Catanzaro'),
            # ('2026-02-07', '15:00', 'Catanzaro', 'Bari'),
            # ('2026-02-14', '20:30', 'Spezia', 'Catanzaro'),
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
                print(f"  ✅ Serie B: {date} {time} - {home} - {away}")

        # *** PARTITE SERIE B MONZA *** (se Monza è in Serie B)
        manual_serie_b_monza = [
            # ('2026-02-08', '15:00', 'Monza', 'Palermo'),
            # Aggiungi qui se necessario
        ]

        for date, time, home, away in manual_serie_b_monza:
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
                print(f"  ✅ Serie B: {date} {time} - {home} - {away}")

        # *** SERIE D REGGINA TRASFERTE ***
        manual_serie_d_reggina = [
            # ('2026-02-09', '14:30', 'Acireale', 'Reggina'),
            # Aggiungi qui le prossime trasferte
        ]

        for date, time, home, away in manual_serie_d_reggina:
            if date not in self.events:
                self.events[date] = []

            event = {
                'time': time,
                'event': f'{home} - {away}',
                'competition': 'Serie D - Girone I',
                'sport': 'calcio',
                'channel': 'ReggioTV',
                'notes': 'Trasferta Reggina',
                'highlight': True
            }

            if not self.is_duplicate(self.events[date], event):
                self.events[date].append(event)
                print(f"  ✅ Serie D: {date} {time} - {home} - {away}")

    def detect_competition_key(self, text, sport):
        """Rileva la chiave della competizione"""
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

    def is_duplicate(self, events_list, new_event):
        """Controlla duplicati"""
        for existing in events_list:
            if (existing['time'] == new_event['time'] and 
                self.similar_events(existing['event'], new_event['event'])):
                return True
        return False

    def similar_events(self, event1, event2):
        """Verifica se due eventi sono simili"""
        e1 = event1.lower().replace('-', '').replace('vs', '').strip()[:40]
        e2 = event2.lower().replace('-', '').replace('vs', '').strip()[:40]
        return e1 == e2 or e1 in e2 or e2 in e1

    def get_italian_day_name(self, weekday):
        days = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
        return days[weekday]

    def get_italian_month_name(self, month):
        months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        return months[month - 1]

    def detect_sport(self, text):
        if any(word in text for word in ['calcio', 'serie a', 'serie b', 'champions', 'europa league', 'conference', 'sorteggio']):
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
            if 'sorteggio' in text:
                if 'champions' in text:
                    return 'Champions League - Sorteggio'
                elif 'europa league' in text:
                    return 'Europa League - Sorteggio'
                elif 'conference' in text:
                    return 'Conference League - Sorteggio'
            if 'champions' in text:
                return 'Champions League'
            elif 'europa league' in text:
                return 'Europa League'
            elif 'conference' in text:
                return 'Conference League'
            elif 'serie a' in text and 'serie b' not in text:
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
            return 'Tennis ATP/WTA'
        elif sport == 'sci':
            return 'Sci Alpino - Coppa del Mondo'
        elif sport == 'f1':
            if 'test' in text:
                return 'Formula 1 - Test'
            elif 'shakedown' in text or 'filming day' in text:
                return 'Formula 1 - Shakedown'
            elif 'prove libere' in text or 'prove' in text:
                return 'Formula 1 - Prove Libere'
            elif 'qualifiche' in text:
                return 'Formula 1 - Qualifiche'
            elif 'gara' in text or 'gran premio' in text:
                return 'Formula 1 - Gara'
            return 'Formula 1'
        elif sport == 'motogp':
            if 'test' in text:
                return 'MotoGP - Test'
            elif 'shakedown' in text:
                return 'MotoGP - Shakedown'
            return 'MotoGP'
        elif sport == 'volley':
            return 'Volley'
        return sport.title()

    def extract_notes(self, text_lower, text_original):
        notes = []

        # Diretta gol con numero canale
        dg_match = re.search(r'diretta gol.*?sky sport\s*(\d{3})', text_lower)
        if dg_match:
            notes.append(f'Diretta Gol: Sky Sport {dg_match.group(1)}')
        elif 'diretta gol' in text_lower:
            notes.append('Diretta Gol disponibile')

        # Sorteggio
        if 'sorteggio' in text_lower:
            notes.append('Sorteggio')

        # Semifinale/Finale
        if 'semifinale' in text_lower or 'semifinali' in text_lower:
            notes.append('Semifinale')
        elif 'finale' in text_lower and 'semifinale' not in text_lower:
            notes.append('Finale')

        # Prova sci
        prova_match = re.search(r'(\d+)[ªa°]\s*prova', text_lower)
        if prova_match:
            notes.append(f'{prova_match.group(1)}ª prova')

        # Test/Shakedown
        if 'test' in text_lower and 'contest' not in text_lower:
            notes.append('Test')
        if 'shakedown' in text_lower:
            notes.append('Shakedown')
        if 'porte chiuse' in text_lower or 'non trasmesso' in text_lower:
            notes.append('Non in TV')

        # Differita
        if 'differita' in text_lower:
            notes.append('In differita')

        # Trasferta
        if 'trasferta' in text_lower:
            notes.append('Trasferta')

        return ', '.join(notes) if notes else ''

    def clean_event_name(self, text, time_str):
        # Rimuovi orario
        text = re.sub(r'\d{1,2}[:\.\s]\d{2}', '', text)
        text = re.sub(r'ore\s+', '', text, flags=re.IGNORECASE)

        # Rimuovi canali
        text = re.sub(r'Sky Sport.*?(?=\s|\||$)', '', text, flags=re.IGNORECASE)
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
                    # Sorteggi: sempre inclusi
                    if 'sorteggio' in comp or 'sorteggio' in ev_name:
                        should_include = True
                    elif 'serie a' in comp:
                        should_include = True
                    elif 'champions' in comp or 'europa' in comp or 'conference' in comp:
                        italian_teams = ['inter', 'milan', 'juventus', 'juve', 'roma', 'napoli', 
                                       'lazio', 'atalanta', 'bologna', 'fiorentina']
                        should_include = any(team in ev_name for team in italian_teams) or 'sorteggio' in ev_name
                    elif 'serie b' in comp:
                        should_include = 'monza' in ev_name or 'catanzaro' in ev_name
                    elif 'serie d' in comp:
                        should_include = 'reggina' in ev_name

                # Tennis
                elif sport == 'tennis':
                    italian_players = ['sinner', 'paolini', 'berrettini', 'musetti', 
                                     'darderi', 'sonego', 'arnaldi', 'italia']
                    should_include = any(player in ev_name for player in italian_players)

                # F1 e MotoGP: SEMPRE inclusi (anche test/shakedown)
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
    scraper.scrape_serie_b_calendar()
    scraper.add_special_events()  # NUOVO: eventi speciali (sorteggi, test, ecc.)
    scraper.add_manual_events()    # Eventi manuali (Catanzaro, Monza, Reggina)

    # Salva
    events = scraper.save_to_json('eventi.json')

    print(f"\n📊 Riepilogo:")
    for date, evs in events.items():
        print(f"\n  {date} ({len(evs)} eventi):")
        for ev in evs[:5]:
            highlight = "⭐" if ev['highlight'] else "  "
            print(f"    {highlight} {ev['time']} - {ev['event'][:45]:45} | {ev['channel']}")

    print("\n✅ Scraping completato!")

if __name__ == '__main__':
    main()
