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

    def scrape_oasport(self):
        """Scrape da OASport.it per eventi sportivi italiani"""
        try:
            # Ottieni eventi per più giorni
            for i in range(-1, 4):  # Da ieri a +3 giorni
                date = self.today + timedelta(days=i)

                # OASport usa formato: sport-in-tv-oggi-giovedi-29-gennaio
                day_name = self.get_italian_day_name(date.weekday())
                url = f'https://www.oasport.it/{date.year}/{date.month:02d}/sport-in-tv-{day_name}-{date.day}-{self.get_italian_month_name(date.month)}-orari-e-programma-completo/'

                print(f"🔍 Cerco eventi per {date.strftime('%Y-%m-%d')} su {url}")

                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        self.parse_oasport_content(soup, date)
                    else:
                        print(f"  ⚠️  Status code: {response.status_code}")
                except Exception as e:
                    print(f"  ❌ Errore: {e}")
                    continue

        except Exception as e:
            print(f"Errore generale scraping OASport: {e}")

    def parse_oasport_content(self, soup, target_date):
        """Analizza il contenuto HTML di OASport con migliore gestione date"""
        date_str = target_date.strftime('%Y-%m-%d')

        if date_str not in self.events:
            self.events[date_str] = []

        # Cerca il contenuto principale dell'articolo
        content = soup.find('div', class_='post-content') or soup.find('article')
        if not content:
            print(f"  ⚠️  Contenuto non trovato")
            return

        text = content.get_text()

        # Pattern per trovare eventi con orari (formato italiano)
        # Esempi: 09:30, 21.00, ore 18:45
        time_pattern = r'(?:ore\s+)?(\d{1,2})[:\.](\d{2})'

        # Cerca menzioni di eventi italiani
        italian_keywords = [
            'italia', 'italiano', 'italiana',
            'inter', 'milan', 'juventus', 'juve', 'roma', 'napoli', 'lazio',
            'atalanta', 'bologna', 'fiorentina', 'torino', 'udinese',
            'sinner', 'paolini', 'berrettini', 'musetti', 'darderi', 'sonego',
            'brignone', 'goggia', 'paris', 'de aliprandini',
            'monza', 'catanzaro', 'reggina'
        ]

        lines = text.split('\n')
        current_section = None

        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean:
                continue

            line_lower = line_clean.lower()

            # Rileva sezione sport
            if any(sport in line_lower for sport in ['calcio', 'tennis', 'sci', 'formula 1', 'motogp', 'volley']):
                current_section = self.detect_sport(line_lower)

            # Controlla se la riga contiene un orario
            time_match = re.search(time_pattern, line_clean)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                time = f"{hour:02d}:{minute:02d}"

                # Verifica se contiene keyword italiane
                is_italian = any(keyword in line_lower for keyword in italian_keywords)

                # Determina il tipo di sport
                sport_type = current_section or self.detect_sport(line_lower)

                # Se è uno sport che seguiamo sempre (F1, MotoGP) o contiene italiani
                if sport_type and (is_italian or sport_type in ['f1', 'motogp']):
                    # Estrai informazioni
                    channel = self.extract_channel(line_clean)
                    competition = self.get_competition_name(line_lower, sport_type)
                    event_name = self.clean_event_name(line_clean, time)

                    # Controlla se l'evento è effettivamente in questa data
                    # Eventi molto presto la mattina (prima delle 7) potrebbero riferirsi al giorno dopo
                    actual_date = date_str

                    # Se l'evento è prima delle 06:00 e siamo a tarda sera, potrebbe essere il giorno dopo
                    if hour < 6 and self.today.hour >= 18:
                        # Controlla nel contesto se c'è scritto "domani"
                        context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)])
                        if 'domani' in context.lower():
                            next_day = target_date + timedelta(days=1)
                            actual_date = next_day.strftime('%Y-%m-%d')
                            if actual_date not in self.events:
                                self.events[actual_date] = []

                    event = {
                        'time': time,
                        'event': event_name,
                        'competition': competition,
                        'sport': sport_type,
                        'channel': channel if channel else 'Da verificare',
                        'notes': self.extract_notes(line_lower, line_clean),
                        'highlight': is_italian
                    }

                    # Evita duplicati
                    if not self.is_duplicate(self.events[actual_date], event):
                        self.events[actual_date].append(event)
                        print(f"  ✅ {actual_date} {time} - {event_name[:50]}")

    def is_duplicate(self, events_list, new_event):
        """Controlla se l'evento è un duplicato"""
        for existing in events_list:
            if (existing['time'] == new_event['time'] and 
                existing['event'][:30] == new_event['event'][:30]):
                return True
        return False

    def get_italian_day_name(self, weekday):
        """Restituisce il nome del giorno in italiano"""
        days = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
        return days[weekday]

    def get_italian_month_name(self, month):
        """Restituisce il nome del mese in italiano"""
        months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        return months[month - 1]

    def detect_sport(self, text):
        """Rileva il tipo di sport dal testo"""
        if any(word in text for word in ['calcio', 'serie a', 'champions', 'europa league', 'conference']):
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

    def extract_channel(self, text):
        """Estrae il nome del canale TV"""
        channels_map = {
            'sky sport uno': 'Sky Sport Uno',
            'sky sport calcio': 'Sky Sport Calcio',
            'sky sport': 'Sky Sport',
            'dazn': 'DAZN',
            'prime video': 'Prime Video',
            'amazon prime': 'Prime Video',
            'eurosport 1': 'Eurosport 1',
            'eurosport 2': 'Eurosport 2',
            'eurosport': 'Eurosport',
            'discovery+': 'discovery+',
            'rai sport': 'RaiSport',
            'raisport': 'RaiSport',
            'rai 2': 'Rai 2',
            'tv8': 'TV8',
            'reggiotv': 'ReggioTV'
        }

        text_lower = text.lower()

        # Cerca canali Sky con numero
        sky_match = re.search(r'sky sport (uno|calcio|\d{3})', text_lower)
        if sky_match:
            num_or_name = sky_match.group(1)
            if num_or_name.isdigit():
                return f'Sky Sport {num_or_name}'
            else:
                return f'Sky Sport {num_or_name.capitalize()}'

        # Cerca altri canali
        for key, value in channels_map.items():
            if key in text_lower:
                return value

        return ''

    def get_competition_name(self, text, sport):
        """Determina il nome della competizione"""
        if sport == 'calcio':
            if 'champions' in text:
                return 'Champions League'
            elif 'europa league' in text:
                return 'Europa League'
            elif 'conference' in text:
                return 'Conference League'
            elif 'serie a' in text:
                return 'Serie A'
            elif 'serie b' in text:
                return 'Serie B'
            elif 'serie d' in text:
                return 'Serie D'
            return 'Calcio'
        elif sport == 'tennis':
            if 'australian open' in text:
                return 'Australian Open'
            elif 'roland garros' in text or 'french open' in text:
                return 'Roland Garros'
            elif 'wimbledon' in text:
                return 'Wimbledon'
            elif 'us open' in text:
                return 'US Open'
            return 'Tennis ATP/WTA'
        elif sport == 'sci':
            if 'mondiali' in text:
                return 'Sci Alpino - Mondiali'
            return 'Sci Alpino - Coppa del Mondo'
        elif sport == 'f1':
            if 'test' in text:
                return 'Formula 1 - Test'
            elif 'prove' in text or 'libere' in text:
                return 'Formula 1 - Prove'
            elif 'qualifiche' in text:
                return 'Formula 1 - Qualifiche'
            elif 'gara' in text or 'gran premio' in text:
                return 'Formula 1 - Gara'
            return 'Formula 1'
        elif sport == 'motogp':
            if 'test' in text:
                return 'MotoGP - Test'
            elif 'prove' in text:
                return 'MotoGP - Prove'
            elif 'qualifiche' in text:
                return 'MotoGP - Qualifiche'
            elif 'gara' in text:
                return 'MotoGP - Gara'
            return 'MotoGP'
        elif sport == 'volley':
            if 'champions' in text:
                return 'Volley - Champions League'
            return 'Volley'
        return sport.title()

    def extract_notes(self, text_lower, text_original):
        """Estrae note aggiuntive"""
        notes = []

        # Cerca diretta gol
        diretta_gol_match = re.search(r'diretta gol.*?(?:sky sport\s*)?(\d{3})', text_lower)
        if diretta_gol_match:
            notes.append(f'Diretta Gol: Sky Sport {diretta_gol_match.group(1)}')
        elif 'diretta gol' in text_lower:
            notes.append('Diretta Gol disponibile')

        # Altre note
        if 'differita' in text_lower:
            notes.append('In differita')
        if 'semifinale' in text_lower:
            notes.append('Semifinale')
        elif 'finale' in text_lower:
            notes.append('Finale')
        if 'prova' in text_lower:
            prova_match = re.search(r'(\d+)[ªa°]\s*prova', text_lower)
            if prova_match:
                notes.append(f'{prova_match.group(1)}ª prova')

        return ', '.join(notes) if notes else ''

    def clean_event_name(self, text, time_str):
        """Pulisce il nome dell'evento"""
        # Rimuovi orario
        text = re.sub(r'\d{1,2}[:\.\s]\d{2}', '', text)
        text = re.sub(r'ore\s+', '', text, flags=re.IGNORECASE)

        # Rimuovi canali TV comuni
        text = re.sub(r'Sky Sport.*?(?=\s|$)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'DAZN|Prime Video|Eurosport|RaiSport|TV8|discovery\+', '', text, flags=re.IGNORECASE)

        # Rimuovi parole comuni inutili
        text = re.sub(r'\b(diretta|streaming|live|gratis)\b', '', text, flags=re.IGNORECASE)

        # Pulisci spazi multipli
        text = re.sub(r'\s+', ' ', text)

        return text.strip()[:100]

    def add_fixed_events(self):
        """Aggiungi eventi fissi conosciuti"""
        # Serie D - Reggina trasferte (esempio - aggiungere date reali)
        reggina_away = [
            ('2026-02-02', '14:30', 'Reggina - Vibonese (Trasferta)'),
            ('2026-02-09', '14:30', 'Reggina - Scafatese (Trasferta)'),
        ]

        for date, time, event in reggina_away:
            if date not in self.events:
                self.events[date] = []

            self.events[date].append({
                'time': time,
                'event': event,
                'competition': 'Serie D - Girone I',
                'sport': 'calcio',
                'channel': 'ReggioTV',
                'notes': 'Trasferta Reggina',
                'highlight': True
            })

    def filter_relevant_events(self):
        """Filtra solo gli eventi rilevanti secondo i criteri specificati"""
        filtered = {}

        for date, events in self.events.items():
            filtered[date] = []

            for event in events:
                should_include = False
                sport = event['sport']
                comp = event['competition'].lower()
                ev_name = event['event'].lower()

                # Calcio: regole specifiche
                if sport == 'calcio':
                    if 'serie a' in comp:
                        should_include = True
                    elif 'champions' in comp or 'europa' in comp or 'conference' in comp:
                        # Solo con squadre italiane
                        italian_teams = ['inter', 'milan', 'juventus', 'juve', 'roma', 'napoli', 
                                       'lazio', 'atalanta', 'bologna', 'fiorentina']
                        should_include = any(team in ev_name for team in italian_teams)
                    elif 'serie b' in comp:
                        should_include = 'monza' in ev_name or 'catanzaro' in ev_name
                    elif 'serie d' in comp:
                        should_include = 'reggina' in ev_name

                # Tennis: solo italiani
                elif sport == 'tennis':
                    italian_players = ['sinner', 'paolini', 'berrettini', 'musetti', 
                                     'darderi', 'sonego', 'arnaldi', 'italia']
                    should_include = any(player in ev_name for player in italian_players)

                # F1 e MotoGP: sempre
                elif sport in ['f1', 'motogp']:
                    should_include = True

                # Sci: solo Brignone e Goggia
                elif sport == 'sci':
                    should_include = 'brignone' in ev_name or 'goggia' in ev_name

                # Volley: solo Monza
                elif sport == 'volley':
                    should_include = 'monza' in ev_name or 'vero volley' in ev_name

                if should_include:
                    filtered[date].append(event)

            # Rimuovi date senza eventi
            if not filtered[date]:
                del filtered[date]

        return filtered

    def save_to_json(self, filename='eventi.json'):
        """Salva gli eventi in JSON"""
        # Filtra eventi rilevanti
        filtered_events = self.filter_relevant_events()

        # Ordina per data
        sorted_events = dict(sorted(filtered_events.items()))

        # Ordina eventi per orario dentro ogni giorno
        for date in sorted_events:
            sorted_events[date] = sorted(sorted_events[date], 
                                        key=lambda x: x['time'])

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

    # Scraping da OASport
    scraper.scrape_oasport()

    # Aggiungi eventi fissi
    scraper.add_fixed_events()

    # Salva in JSON
    events = scraper.save_to_json('eventi.json')

    print(f"\n📊 Riepilogo eventi per giorno:")
    for date, evs in events.items():
        print(f"\n  {date}:")
        for ev in evs:
            highlight = "⭐" if ev['highlight'] else "  "
            print(f"    {highlight} {ev['time']} - {ev['event'][:60]}")

    print("\n✅ Scraping completato!")

if __name__ == '__main__':
    main()
