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

    def scrape_oasport(self):
        """Scrape da OASport.it per eventi sportivi italiani"""
        try:
            # Ottieni eventi di oggi
            today = datetime.now()
            for i in range(-1, 3):  # Ieri, oggi, domani, dopodomani
                date = today + timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')

                url = f'https://www.oasport.it/{date.year}/{date.month:02d}/sport-in-tv-{date.strftime("%A-%d-%B").lower()}-orari-e-programma-completo/'

                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        self.parse_oasport_content(soup, date_str)
                except:
                    continue

        except Exception as e:
            print(f"Errore scraping OASport: {e}")

    def parse_oasport_content(self, soup, date_str):
        """Analizza il contenuto HTML di OASport"""
        if date_str not in self.events:
            self.events[date_str] = []

        # Cerca sezioni con orari e eventi
        content = soup.find('div', class_='post-content')
        if not content:
            return

        text = content.get_text()

        # Pattern per trovare eventi con orari
        time_pattern = r'(\d{1,2}[:\.]\d{2})'

        # Cerca menzioni di eventi italiani
        italian_keywords = [
            'italia', 'inter', 'milan', 'juventus', 'roma', 'napoli', 'lazio',
            'atalanta', 'bologna', 'fiorentina', 'sinner', 'paolini', 'berrettini',
            'musetti', 'brignone', 'goggia', 'monza', 'catanzaro', 'reggina'
        ]

        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()

            # Controlla se la riga contiene un orario
            time_match = re.search(time_pattern, line)
            if time_match:
                time = time_match.group(1).replace('.', ':')

                # Verifica se contiene keyword italiane
                is_italian = any(keyword in line_lower for keyword in italian_keywords)

                # Determina il tipo di sport e canale
                sport_type = self.detect_sport(line_lower)
                channel = self.extract_channel(line)

                if sport_type and (is_italian or sport_type in ['f1', 'motogp']):
                    event = {
                        'time': time,
                        'event': self.clean_event_name(line),
                        'competition': self.get_competition_name(line_lower, sport_type),
                        'sport': sport_type,
                        'channel': channel if channel else 'Da verificare',
                        'notes': self.extract_notes(line_lower),
                        'highlight': is_italian
                    }
                    self.events[date_str].append(event)

    def detect_sport(self, text):
        """Rileva il tipo di sport dal testo"""
        if any(word in text for word in ['calcio', 'serie a', 'champions', 'europa league', 'conference']):
            return 'calcio'
        elif any(word in text for word in ['tennis', 'atp', 'wta', 'australian open', 'roland garros']):
            return 'tennis'
        elif 'formula 1' in text or 'f1' in text:
            return 'f1'
        elif 'motogp' in text or 'moto gp' in text:
            return 'motogp'
        elif any(word in text for word in ['sci', 'slalom', 'discesa', 'super-g']):
            return 'sci'
        elif 'volley' in text or 'pallavolo' in text:
            return 'volley'
        return None

    def extract_channel(self, text):
        """Estrae il nome del canale TV"""
        channels = ['sky sport', 'dazn', 'prime video', 'eurosport', 'rai', 'tv8', 
                   'discovery+', 'reggiotv', 'sky sport uno', 'sky sport calcio']

        text_lower = text.lower()
        for channel in channels:
            if channel in text_lower:
                # Cerca anche numeri di canale Sky
                if 'sky sport' in channel:
                    sky_num = re.search(r'sky sport (\d{3})', text_lower)
                    if sky_num:
                        return f'Sky Sport {sky_num.group(1)}'
                return channel.title()
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
            return 'Tennis ATP/WTA'
        elif sport == 'sci':
            return 'Sci Alpino - Coppa del Mondo'
        elif sport == 'f1':
            return 'Formula 1'
        elif sport == 'motogp':
            return 'MotoGP'
        elif sport == 'volley':
            return 'Volley'
        return sport.title()

    def extract_notes(self, text):
        """Estrae note aggiuntive"""
        notes = []
        if 'diretta gol' in text:
            match = re.search(r'diretta gol.*?(\d{3})', text)
            if match:
                notes.append(f'Diretta Gol: Sky Sport {match.group(1)}')
        if 'differita' in text:
            notes.append('In differita')
        return ', '.join(notes) if notes else ''

    def clean_event_name(self, text):
        """Pulisce il nome dell'evento"""
        # Rimuovi orari e canali
        text = re.sub(r'\d{1,2}[:\.]\d{2}', '', text)
        text = re.sub(r'Sky Sport.*?\d{3}', '', text, flags=re.IGNORECASE)
        text = re.sub(r'DAZN|Prime Video|Eurosport|RaiSport', '', text, flags=re.IGNORECASE)
        return text.strip()[:100]  # Limita lunghezza

    def add_fixed_events(self):
        """Aggiungi eventi fissi conosciuti (es. Serie D Reggina in trasferta)"""
        # Date campionato Serie D - Reggina trasferta
        reggina_away_dates = [
            ('2026-02-02', '14:30', 'Reggina - Avversario (Trasferta)'),
            ('2026-02-16', '14:30', 'Reggina - Avversario (Trasferta)'),
            # Aggiungi altre date...
        ]

        for date, time, event in reggina_away_dates:
            if date not in self.events:
                self.events[date] = []

            self.events[date].append({
                'time': time,
                'event': event,
                'competition': 'Serie D',
                'sport': 'calcio',
                'channel': 'ReggioTV',
                'notes': 'Trasferta Reggina',
                'highlight': True
            })

    def save_to_json(self, filename='eventi.json'):
        """Salva gli eventi in JSON"""
        # Ordina per data
        sorted_events = dict(sorted(self.events.items()))

        # Ordina eventi per orario dentro ogni giorno
        for date in sorted_events:
            sorted_events[date] = sorted(sorted_events[date], 
                                        key=lambda x: x['time'])

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_events, f, ensure_ascii=False, indent=2)

        print(f"✅ Salvati {sum(len(v) for v in sorted_events.values())} eventi in {filename}")
        return sorted_events

def main():
    print("🔄 Inizio scraping eventi sportivi...")

    scraper = SportEventScraper()

    # Scraping da varie fonti
    scraper.scrape_oasport()

    # Aggiungi eventi fissi
    scraper.add_fixed_events()

    # Salva in JSON
    events = scraper.save_to_json('eventi.json')

    print(f"📊 Eventi trovati per {len(events)} giorni")
    for date, evs in events.items():
        print(f"  {date}: {len(evs)} eventi")

    print("\n✅ Scraping completato!")

if __name__ == '__main__':
    main()
