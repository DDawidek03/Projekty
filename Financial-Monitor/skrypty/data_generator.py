import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import numpy as np
import calendar
from collections import defaultdict

# Lista lokalizacji - tylko kraje europejskie
available_locales = ['pl_PL', 'en_GB', 'de_DE', 'fr_FR', 'es_ES', 'it_IT', 
                    'nl_NL', 'sv_SE', 'de_AT']  # Zamieniono 'tr_TR' na 'de_AT'
fakers = {locale: Faker(locale) for locale in available_locales}

# Mapowanie krajów na waluty
country_currencies = {
    'pl_PL': 'PLN',  # Polska - złotówki
    'en_GB': 'GBP',  # Wielka Brytania - funty
    'de_DE': 'EUR',  # Niemcy - euro
    'fr_FR': 'EUR',  # Francja - euro
    'es_ES': 'EUR',  # Hiszpania - euro
    'it_IT': 'EUR',  # Włochy - euro
    'nl_NL': 'EUR',  # Holandia - euro
    'sv_SE': 'SEK',  # Szwecja - korony szwedzkie
    'de_AT': 'EUR'   # Austria - euro 
}

# Mapowanie krajów na kody
country_codes = {
    'pl_PL': 'PL',  # Polska
    'en_GB': 'GB',  # Wielka Brytania
    'de_DE': 'DE',  # Niemcy
    'fr_FR': 'FR',  # Francja
    'es_ES': 'ES',  # Hiszpania
    'it_IT': 'IT',  # Włochy
    'nl_NL': 'NL',  # Holandia
    'sv_SE': 'SE',  # Szwecja
    'de_AT': 'AT'   # Austria 
}

full_country_names = {
    'PL': 'Poland',
    'GB': 'United Kingdom',
    'DE': 'Germany',
    'FR': 'France',
    'ES': 'Spain',
    'IT': 'Italy',
    'NL': 'Netherlands',
    'SE': 'Sweden',
    'TR': 'Turkey',
    'AT': 'Austria',
    'BE': 'Belgium',
    'DK': 'Denmark',
    'FI': 'Finland',
    'GR': 'Greece',
    'IE': 'Ireland',
    'PT': 'Portugal',
    'CZ': 'Czech Republic',
    'HU': 'Hungary',
    'CH': 'Switzerland',
    'BG': 'Bulgaria',
    'RO': 'Romania',
    'RS': 'Serbia',
    'HR': 'Croatia',
    'SK': 'Slovakia',
    'LT': 'Lithuania',
    'LV': 'Latvia',
    'EE': 'Estonia',
    'NO': 'Norway'
}

european_cities = {
    'PL': ['Warsaw', 'Krakow', 'Gdansk', 'Wroclaw', 'Poznan', 'Lodz', 'Szczecin', 'Katowice', 'Lublin', 'Bydgoszcz'],
    'GB': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Glasgow', 'Edinburgh', 'Bristol', 'Leeds', 'Sheffield', 'Cardiff'],
    'DE': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Dresden', 'Leipzig', 'Hannover', 'Stuttgart', 'Düsseldorf'],
    'FR': ['Paris', 'Marseille', 'Lyon', 'Nice', 'Toulouse', 'Bordeaux', 'Strasbourg', 'Nantes', 'Montpellier', 'Lille'],
    'ES': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Malaga', 'Bilbao', 'Zaragoza', 'Palma', 'Granada', 'Vigo'],
    'IT': ['Rome', 'Milan', 'Naples', 'Turin', 'Florence', 'Bologna', 'Venice', 'Genoa', 'Palermo', 'Verona'],
    'NL': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven', 'Groningen', 'Tilburg', 'Almere', 'Breda', 'Nijmegen'],
    'SE': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Linköping', 'Örebro', 'Helsingborg', 'Norrköping', 'Västerås', 'Umeå'],
    'AT': ['Vienna', 'Salzburg', 'Graz', 'Linz', 'Innsbruck']  
}

other_european_cities = [
    'Vienna', 'Salzburg', 'Brussels', 'Antwerp', 'Copenhagen', 'Aarhus', 
    'Helsinki', 'Tampere', 'Athens', 'Thessaloniki', 'Dublin', 'Cork', 
    'Lisbon', 'Porto', 'Prague', 'Brno', 'Budapest', 'Debrecen', 
    'Zurich', 'Geneva', 'Sofia', 'Plovdiv', 'Bucharest', 'Cluj-Napoca',
    'Belgrade', 'Novi Sad', 'Zagreb', 'Split', 'Bratislava', 'Kosice',
    'Vilnius', 'Kaunas', 'Riga', 'Tallinn', 'Oslo', 'Bergen',
    'Gothenburg', 'Malmö', 'Lyon', 'Toulouse', 'Munich', 'Frankfurt',
    'Milan', 'Naples', 'Barcelona', 'Valencia', 'Rotterdam', 'Utrecht'

]
# Dodanie mapowania miast do ich województw/regionów dla większej spójności danych
city_to_region = {
    # Polska - miasta do województw
    'Warsaw': 'Mazowieckie',
    'Krakow': 'Małopolskie',
    'Gdansk': 'Pomorskie',
    'Wroclaw': 'Dolnośląskie',
    'Poznan': 'Wielkopolskie',
    'Lodz': 'Łódzkie',
    'Szczecin': 'Zachodniopomorskie',
    'Katowice': 'Śląskie',
    'Lublin': 'Lubelskie',
    'Bydgoszcz': 'Kujawsko-pomorskie',
    
    # Niemcy - miasta do landów
    'Berlin': 'Berlin',
    'Munich': 'Bayern',
    'Hamburg': 'Hamburg',
    'Frankfurt': 'Hessen',
    'Cologne': 'Nordrhein-Westfalen',
    'Dresden': 'Sachsen',
    'Leipzig': 'Sachsen',
    'Hannover': 'Niedersachsen',
    'Stuttgart': 'Baden-Württemberg',
    'Düsseldorf': 'Nordrhein-Westfalen',
    
    # UK - miasta do hrabstw
    'London': 'Greater London',
    'Manchester': 'Greater Manchester',
    'Birmingham': 'West Midlands',
    'Liverpool': 'Merseyside',
    'Glasgow': 'Scotland',
    'Edinburgh': 'Scotland',
    'Bristol': 'Bristol',
    'Leeds': 'West Yorkshire',
    'Sheffield': 'South Yorkshire',
    'Cardiff': 'Wales',
    
    # Hiszpania - miasta do wspólnot autonomicznych
    'Madrid': 'Madrid',
    'Barcelona': 'Cataluña',
    'Valencia': 'Comunidad Valenciana',
    'Seville': 'Andalucía',
    'Malaga': 'Andalucía',
    'Bilbao': 'País Vasco',
    'Zaragoza': 'Aragón',
    'Palma': 'Baleares',
    'Granada': 'Andalucía',
    'Vigo': 'Galicia',
    
    # Francja - miasta do regionów
    'Paris': 'Île-de-France',
    'Marseille': 'Provence-Alpes-Côte d\'Azur',
    'Lyon': 'Auvergne-Rhône-Alpes',
    'Nice': 'Provence-Alpes-Côte d\'Azur',
    'Toulouse': 'Occitanie',
    'Bordeaux': 'Nouvelle-Aquitaine',
    'Strasbourg': 'Grand Est',
    'Nantes': 'Pays de la Loire',
    'Montpellier': 'Occitanie',
    'Lille': 'Hauts-de-France',
    
    # Włochy - miasta do regionów
    'Rome': 'Lazio',
    'Milan': 'Lombardia',
    'Naples': 'Campania',
    'Turin': 'Piemonte',
    'Florence': 'Toscana',
    'Bologna': 'Emilia-Romagna',
    'Venice': 'Veneto',
    'Genoa': 'Liguria',
    'Palermo': 'Sicilia',
    'Verona': 'Veneto',
    
    # Holandia - miasta do prowincji
    'Amsterdam': 'Noord-Holland',
    'Rotterdam': 'Zuid-Holland',
    'The Hague': 'Zuid-Holland',
    'Utrecht': 'Utrecht',
    'Eindhoven': 'Noord-Brabant',
    'Groningen': 'Groningen',
    'Tilburg': 'Noord-Brabant',
    'Almere': 'Flevoland',
    'Breda': 'Noord-Brabant',
    'Nijmegen': 'Gelderland',
    
    # Szwecja - miasta do regionów
    'Stockholm': 'Stockholm',
    'Gothenburg': 'Västra Götaland',
    'Malmö': 'Skåne',
    'Uppsala': 'Uppsala',
    'Linköping': 'Östergötland',
    'Örebro': 'Örebro',
    'Helsingborg': 'Skåne',
    'Norrköping': 'Östergötland',
    'Västerås': 'Västmanland',
    'Umeå': 'Västerbotten',
    
    # Austria - miasta do krajów związkowych
    'Vienna': 'Vienna',
    'Salzburg': 'Salzburg',
    'Graz': 'Styria',
    'Linz': 'Upper Austria',
    'Innsbruck': 'Tyrol'
    # Usunięto mapowanie miast z Turcji
}

OUTPUT_DIR = "data"
NUM_CLIENTS = 200
NUM_ACCOUNTS = 300
NUM_TRANSACTIONS = 3000  
NUM_LOCATIONS = 200
NUM_ALERTS = 0  

START_DATE = datetime.strptime('2017-01-01', '%Y-%m-%d')
END_DATE = datetime.strptime('2023-12-31', '%Y-%m-%d')
TODAY = datetime.today()

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_age():

    age_distribution = [
        (18, 25, 0.15),  # Młodzi dorośli
        (26, 35, 0.25),  # Wczesna kariera
        (36, 50, 0.30),  # Środkowa kariera
        (51, 65, 0.20),  # Późna kariera
        (66, 80, 0.10)   # Emerytura
    ]

    age_range = random.choices(age_distribution, weights=[w for _, _, w in age_distribution], k=1)[0]
    return random.randint(age_range[0], age_range[1])


clients = []
for i in range(1, NUM_CLIENTS + 1):
    locale = random.choice(available_locales)
    fake = fakers[locale]

    # Bardziej realistyczne rozłożenie dat rejestracji
    years_back = random.randint(1, 5)
    registration_date = fake.date_between(start_date=TODAY - timedelta(days=365 * years_back),
                                          end_date=TODAY).strftime('%Y-%m-%d')

    if (locale == 'pl_PL'):
        identifier = fake.pesel()
    else:
        identifier = fake.ssn()

    country_code = country_codes.get(locale, 'US')  # Domyślnie UK zamiast US
    country_name = full_country_names.get(country_code, country_code)

    # Zdefiniuj zachodnie lokalizacje używające alfabetu łacińskiego - tylko dostępne europejskie
    western_locales = ['pl_PL', 'en_GB', 'de_DE', 'fr_FR', 'es_ES', 'it_IT', 'nl_NL', 'sv_SE', 'de_AT']
    
    # Użyj oryginalnej lokalizacji dla większości danych, ale wybierz zachodnią lokalizację dla imion
    name_locale = locale if locale in western_locales else random.choice(western_locales)
    name_faker = fakers[name_locale]
    
    # Wygeneruj bardziej realistyczny wiek
    age = generate_age()
    birth_date = (TODAY - timedelta(days=age * 365)).strftime('%Y-%m-%d')
    # Bardziej realistyczny stosunek aktywnych/nieaktywnych klientów z 85% aktywnych klientów
    is_active = random.choices(['Yes', 'No'], weights=[0.85, 0.15], k=1)[0]
    clients.append({
        'id': i,
        'first_name': name_faker.first_name(),
        'last_name': name_faker.last_name(),
        'identifier': identifier,
        'birth_date': birth_date,
        'email': fake.email(),
        'phone': fake.phone_number().replace(" ", ""),
        'gender': random.choice(['M', 'F']),
        'registration_date': registration_date,
        'is_active': is_active,
        'country': country_name,
        'locale': locale,
        'age_group': f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"  # Dodaj grupę wiekową dla łatwiejszej wizualizacji
    })

clients_df = pd.DataFrame(clients)
clients_df.to_csv(os.path.join(OUTPUT_DIR, 'clients.csv'), index=False)

locations = []
for i in range(1, NUM_LOCATIONS + 1):
    client_id = random.randint(1, NUM_CLIENTS)
    client_locale = clients_df[clients_df['id'] == client_id]['locale'].iloc[0]
    client_country_code = country_codes.get(client_locale, 'GB')  # Zmieniono domyślny kraj na GB
    client_country = full_country_names.get(client_country_code, client_country_code)
    fake_location = fakers[client_locale]
    
    # Wybierz europejskie miasto zamiast generowanych przez faker
    if client_country_code in european_cities:
        city = random.choice(european_cities[client_country_code])
        # Użyj odpowiedniego regionu dla wybranego miasta, jeśli istnieje w mapowaniu
        if city in city_to_region:
            region = city_to_region[city]
        else:
            # Dla miast bez mapowania, wybierz region jak wcześniej
            if client_locale == 'pl_PL':
                region = random.choice(polish_voivodeships)
            elif client_locale == 'en_GB':
                region = fake_location.county()
            elif client_locale == 'de_DE':
                # German states (Bundesländer)
                german_states = [
                    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen",
                    "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
                    "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
                    "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
                ]
                region = random.choice(german_states)
            elif client_locale == 'fr_FR':
                # Use a generic region for France since department() doesn't exist
                french_regions = [
                    "Île-de-France", "Grand Est", "Hauts-de-France", "Normandie",
                    "Bretagne", "Pays de la Loire", "Centre-Val de Loire",
                    "Bourgogne-Franche-Comté", "Nouvelle-Aquitaine", "Occitanie",
                    "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur", "Corse"
                ]
                region = random.choice(french_regions)
            elif client_locale == 'es_ES':
                # Spanish autonomous communities
                spanish_communities = [
                    "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias",
                    "Cantabria", "Castilla-La Mancha", "Castilla y León", "Cataluña",
                    "Extremadura", "Galicia", "La Rioja", "Madrid", "Murcia",
                    "Navarra", "País Vasco", "Comunidad Valenciana"
                ]
                region = random.choice(spanish_communities)
            elif client_locale == 'it_IT':
                # Italian regions
                italian_regions = [
                    "Valle d'Aosta", "Piemonte", "Lombardia", "Trentino-Alto Adige",
                    "Veneto", "Friuli-Venezia Giulia", "Liguria", "Emilia-Romagna",
                    "Toscana", "Umbria", "Marche", "Lazio", "Abruzzo", "Molise",
                    "Campania", "Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"
                ]
                region = random.choice(italian_regions)
            elif client_locale == 'nl_NL':
                # Dutch provinces
                dutch_provinces = [
                    "Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen",
                    "Limburg", "Noord-Brabant", "Noord-Holland", "Overijssel",
                    "Utrecht", "Zeeland", "Zuid-Holland"
                ]
                region = random.choice(dutch_provinces)
            elif client_locale == 'sv_SE':
                # Swedish counties
                swedish_counties = [
                    "Stockholm", "Uppsala", "Södermanland", "Östergötland", "Jönköping",
                    "Kronoberg", "Kalmar", "Gotland", "Blekinge", "Skåne", "Halland",
                    "Västra Götaland", "Värmland", "Örebro", "Västmanland", "Dalarna",
                    "Gävleborg", "Västernorrland", "Jämtland", "Västerbotten", "Norrbotten"
                ]
                region = random.choice(swedish_counties)
            elif client_locale == 'de_AT':
                # Austrian states
                austrian_states = [
                    "Burgenland", "Carinthia", "Lower Austria", "Upper Austria", "Salzburg",
                    "Styria", "Tyrol", "Vorarlberg", "Vienna"
                ]
                region = random.choice(austrian_states)
            else:
                # Fallback for other locales
                region = f"Region in {client_country}"
    else:
        # Dla krajów nieeuropejskich, wybierz losowe miasto z other_european_cities
        city = random.choice(other_european_cities)
        # Próba znalezienia regionu dla wybranego miasta
        if city in city_to_region:
            region = city_to_region[city]
        else:
            region = f"Region in {client_country}"
    
    # Generuj kody pocztowe i adresy przy użyciu Faker
    postal_code = fake_location.postcode()
    street = fake_location.street_name()
    building_number = fake_location.building_number()
    
    locations.append({
        'id': i,
        'client_id': client_id,
        'city': city,
        'region': region,
        'country': client_country,
        'postal_code': postal_code,
        'street': street,
        'building_number': building_number
    })

locations_df = pd.DataFrame(locations)
locations_df.to_csv(os.path.join(OUTPUT_DIR, 'locations.csv'), index=False)

# Ulepszone generowanie kont dla lepszej wizualizacji
accounts = []
client_account_counts = {i: 0 for i in range(1, NUM_CLIENTS + 1)}

# Stwórz rozkład liczby kont na klienta
def get_num_accounts_for_client():
    return random.choices([1, 2, 3, 4], weights=[0.6, 0.25, 0.1, 0.05], k=1)[0]

# Najpierw określ, ile kont powinien mieć każdy klient
target_accounts_per_client = {i: get_num_accounts_for_client() for i in range(1, NUM_CLIENTS + 1)}
remaining_accounts = NUM_ACCOUNTS - NUM_CLIENTS

# Upewnij się, że każdy klient ma co najmniej jedno konto
for i in range(1, NUM_CLIENTS + 1):
    client_account_counts[i] = 1

# Rozdziel pozostałe konta zgodnie z celem
clients_for_additional = [c for c, target in target_accounts_per_client.items()
                          if client_account_counts[c] < target]
while remaining_accounts > 0 and clients_for_additional:
    client_id = random.choice(clients_for_additional)
    client_account_counts[client_id] += 1
    remaining_accounts -= 1
    # Zaktualizuj listę klientów, którzy mogą otrzymać więcej kont
    if client_account_counts[client_id] >= target_accounts_per_client[client_id]:
        clients_for_additional.remove(client_id)

for i in range(1, NUM_ACCOUNTS + 1):
    if i <= NUM_CLIENTS:
        client_id = i
    else:
        client_id = i - NUM_CLIENTS
        while client_account_counts[client_id] <= 0:
            client_id = (client_id % NUM_CLIENTS) + 1
        client_account_counts[client_id] -= 1

    client = clients_df[clients_df['id'] == client_id].iloc[0]
    client_locale = client['locale']
    client_reg_date = datetime.strptime(client['registration_date'], '%Y-%m-%d')
    default_currency = country_currencies.get(client_locale, 'EUR')  # Zmieniono domyślną walutę na EUR zamiast USD
    # Bardziej realistyczny rozkład walut (większa waga dla lokalnej waluty)
    currency = random.choices(
        [default_currency, 'EUR', 'GBP'],  # Usunięto USD jako opcję dla europejskich danych
        weights=[0.85, 0.1, 0.05],  # Dostosowane wagi
        k=1
    )[0]

    # Naprawiony kod generowania daty otwarcia - sprawdzenie poprawności zakresu dat
    account_end_date = min(END_DATE, TODAY)
    if client_reg_date <= account_end_date:
        opening_date = fakers[client_locale].date_between(
            start_date=client_reg_date,
            end_date=account_end_date
        ).strftime('%Y-%m-%d')
    else:
        # Jeśli zakres jest nieprawidłowy, użyj daty rejestracji klienta
        opening_date = client_reg_date.strftime('%Y-%m-%d')

    account_type_options = ['personal', 'savings', 'business']
    account_type_weights = [0.7, 0.25, 0.05]
    account_type = random.choices(account_type_options, weights=account_type_weights, k=1)[0]
    is_active = random.choices([True, False], weights=[0.92, 0.08], k=1)[0]

    # Stwórz realistyczny rozkład salda na podstawie wieku i typu konta
    def get_balance_generator(client_age):
        if client_age < 25:
            return lambda: round(random.uniform(0, 10000) * random.betavariate(1, 3), 2)
        elif client_age < 40:
            return lambda: round(random.uniform(0, 50000) * random.betavariate(1.5, 3), 2)
        elif client_age < 60:
            return lambda: round(random.uniform(0, 100000) * random.betavariate(2, 3), 2)
        else:
            return lambda: round(random.uniform(0, 80000) * random.betavariate(1.8, 2), 2)

    client_age = (TODAY - datetime.strptime(client['birth_date'], '%Y-%m-%d')).days // 365
    balance_generator = get_balance_generator(client_age)

    country_code = country_codes.get(client_locale, 'US')
    if country_code == 'PL':
        check_digits = f"{random.randint(0, 99):02d}"
        bank_code = random.choice(["10201", "11402", "10901", "10501", "16001"])
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        iban = f"{country_code}{check_digits}{bank_code}{account_number}"
    else:
        iban = fakers[client_locale].iban()

    accounts.append({
        'id': i,
        'client_id': client_id,
        'account_number': iban,
        'account_type': account_type,
        'opening_date': opening_date,
        'balance': balance_generator(),
        'currency': currency,
        'is_active': is_active
    })

accounts_df = pd.DataFrame(accounts)
accounts_df.to_csv(os.path.join(OUTPUT_DIR, 'accounts.csv'), index=False)

transaction_types = [
    {'id': 1, 'type': 'deposit', 'description': 'Cash deposit'},
    {'id': 2, 'type': 'withdrawal', 'description': 'Cash withdrawal'},
    {'id': 3, 'type': 'outgoing_transfer', 'description': 'Outgoing transfer'},
    {'id': 4, 'type': 'incoming_transfer', 'description': 'Incoming transfer'},
    {'id': 5, 'type': 'card_payment', 'description': 'Debit/credit card payment'},
    {'id': 6, 'type': 'standing_charge', 'description': 'Account maintenance fee'},
    {'id': 7, 'type': 'standing_order', 'description': 'Standing order'},
    {'id': 8, 'type': 'atm_withdrawal', 'description': 'ATM withdrawal'},
    {'id': 9, 'type': 'express_transfer', 'description': 'Express transfer'},
    {'id': 10, 'type': 'mobile_payment', 'description': 'Mobile payment'}
]

# Dodaj kategorie transakcji dla lepszego grupowania wizualizacji
transaction_categories = [
    {'id': 1, 'category': 'Housing', 'description': 'Rent, mortgage, utilities'},
    {'id': 2, 'category': 'Food', 'description': 'Groceries and dining'},
    {'id': 3, 'category': 'Transportation', 'description': 'Public transit, car expenses'},
    {'id': 4, 'category': 'Shopping', 'description': 'Retail purchases'},
    {'id': 5, 'category': 'Entertainment', 'description': 'Movies, events, subscriptions'},
    {'id': 6, 'category': 'Health', 'description': 'Medical expenses'},
    {'id': 7, 'category': 'Education', 'description': 'Tuition, courses, books'},
    {'id': 8, 'category': 'Travel', 'description': 'Vacations, hotels, flights'},
    {'id': 9, 'category': 'Income', 'description': 'Salary, investments'},
    {'id': 10, 'category': 'Financial', 'description': 'Banking fees, loans'},
    {'id': 11, 'category': 'Other', 'description': 'Miscellaneous'}
]

transaction_types_df = pd.DataFrame(transaction_types)
transaction_types_df.to_csv(os.path.join(OUTPUT_DIR, 'transaction_types.csv'), index=False)
pd.DataFrame(transaction_categories).to_csv(os.path.join(OUTPUT_DIR, 'transaction_categories.csv'), index=False)

# Stwórz wzorce oparte na czasie dla lepszej wizualizacji
def generate_transaction_date(start_date, end_date):
    # Sprawdź, czy mamy prawidłowy zakres dat
    if start_date > end_date:
        # Jeśli data początkowa jest po dacie końcowej, zwróć datę początkową jako zapasowe rozwiązanie
        return start_date

    days_range = (end_date - start_date).days
    if days_range <= 0:
        return start_date  # Unikaj błędu pustego zakresu

    # Stwórz wzorzec dni tygodnia (więcej transakcji w dni robocze, mniej w weekendy)
    weekday_weights = [0.15, 0.18, 0.18, 0.17, 0.20, 0.07, 0.05]  # Pon-Ndz

    # Stwórz wzorzec miesięczny (więcej transakcji na początku/końcu miesiąca)
    day_of_month_weights = [0.05] * 31
    for i in range(31):
        if i < 5:  # Pierwsze 5 dni miesiąca
            day_of_month_weights[i] = 0.06
        elif i > 25:  # Ostatnie 5 dni miesiąca
            day_of_month_weights[i] = 0.07

    # Teraz wiemy, że days_range jest dodatni
    random_day = random.randint(0, days_range)
    potential_date = start_date + timedelta(days=random_day)

    # Zastosuj prawdopodobieństwo dnia tygodnia
    weekday = potential_date.weekday()
    if random.random() <= weekday_weights[weekday]:
        # Zastosuj prawdopodobieństwo dnia miesiąca
        day_of_month = potential_date.day - 1  # 0-indeksowane
        if day_of_month < len(day_of_month_weights) and random.random() <= day_of_month_weights[day_of_month]:
            # Dodaj wzorzec godzinowy (więcej transakcji w godzinach pracy)
            if potential_date.date() == datetime.today().date():
                hour = random.randint(8, datetime.now().hour)
            else:
                hour_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.05,
                                0.08, 0.10, 0.10, 0.12, 0.10, 0.08, 0.08, 0.08,
                                0.06, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01]
                hour = random.choices(range(24), weights=hour_weights, k=1)[0]
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            return potential_date.replace(hour=hour, minute=minute, second=second)

    # Jeśli nie znajdziemy pasującego wzorca, zwróć podstawową datę z losowym czasem
    hour = random.randint(8, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return potential_date.replace(hour=hour, minute=minute, second=second)

# Przechowuj salda kont dla spójnej historii transakcji
account_balances = {}
for _, account in accounts_df.iterrows():
    account_balances[account['id']] = account['balance']

# Generuj transakcje z bardziej realistycznymi wzorcami
transactions = []
high_value_count = 0
min_high_value_transactions = NUM_ALERTS + 10

# Stwórz mapowanie kategorii transakcji dla tytułów
transaction_title_categories = {
    'Housing': [
        'Rent payment', 'Mortgage payment', 'Electricity bill', 'Gas bill',
        'Water bill', 'Internet bill', 'Home insurance', 'Property tax',
        'Home repairs', 'Furniture purchase'
    ],
    'Food': [
        'Grocery shopping', 'Restaurant bill', 'Coffee shop', 'Food delivery',
        'Cafeteria lunch', 'Bakery', 'Supermarket purchase'
    ],
    'Transportation': [
        'Fuel purchase', 'Car repair', 'Public transport', 'Parking fee',
        'Car insurance', 'Car loan payment', 'Taxi/Uber ride', 'Airline ticket'
    ],
    'Shopping': [
        'Clothing purchase', 'Electronics store', 'Online shopping', 'Department store',
        'Bookstore purchase', 'Gift shop', 'Hardware store', 'Mobile phone purchase'
    ],
    'Entertainment': [
        'Movie tickets', 'Concert tickets', 'Theater show', 'Streaming service',
        'Gaming subscription', 'Sport event', 'Museum entry', 'Amusement park'
    ],
    'Health': [
        'Doctor visit', 'Pharmacy purchase', 'Health insurance', 'Dental care',
        'Eye care', 'Hospital bill', 'Medical test', 'Fitness membership'
    ],
    'Education': [
        'Tuition payment', 'School supplies', 'Textbook purchase', 'Course fee',
        'Student loan payment', 'Educational software', 'Training program', 'Workshop fee'
    ],
    'Travel': [
        'Hotel booking', 'Flight ticket', 'Train ticket', 'Car rental',
        'Travel insurance', 'Vacation package', 'Cruise payment', 'Tour booking'
    ],
    'Income': [
        'Salary deposit', 'Freelance payment', 'Investment return', 'Dividend payment',
        'Rental income', 'Bonus payment', 'Commission payment', 'Royalty payment'
    ],
    'Financial': [
        'Account fee', 'Loan payment', 'Credit card bill', 'Investment deposit',
        'Brokerage fee', 'Exchange fee', 'Safe deposit box fee', 'Financial advisory fee'
    ],
    'Other': [
        'Charity donation', 'Gift payment', 'Subscription renewal', 'Membership fee',
        'Legal service', 'Tax payment', 'Government fee', 'Miscellaneous expense'
    ]
}

# Generuj transakcje dostosowane do sezonowości
account_transactions = defaultdict(list)
for i in range(1, NUM_TRANSACTIONS + 1):
    account_idx = random.randint(0, len(accounts_df) - 1)
    account = accounts_df.iloc[account_idx]
    client_id = account['client_id']
    client_locale = clients_df[clients_df['id'] == client_id]['locale'].iloc[0]
    fake = fakers[client_locale]
    account_opening_date = datetime.strptime(account['opening_date'], '%Y-%m-%d')
    transaction_date = generate_transaction_date(
        max(account_opening_date, START_DATE),
        min(END_DATE, TODAY)
    )

    transaction_type_id = random.randint(1, len(transaction_types))
    transaction_type = transaction_types[transaction_type_id - 1]['type']

    # Dodaj wzorce sezonowe (święta, wakacje letnie itp.)
    month = transaction_date.month
    day = transaction_date.day
    # Wzmacniacze sezonowe dla kwoty transakcji
    seasonal_multiplier = 1.0
    # Sezon świąteczny (grudzień)
    if month == 12 and day > 10:
        seasonal_multiplier = 1.5
    # Wakacje letnie (lipiec-sierpień)
    elif month in [7, 8]:
        seasonal_multiplier = 1.2
    # Black Friday (koniec listopada)
    elif month == 11 and day > 20 and day < 30:
        seasonal_multiplier = 1.4
    # Wyprzedaże styczniowe
    elif month == 1 and day < 15:
        seasonal_multiplier = 1.2

    # Generuj realistyczne kwoty transakcji na podstawie typu i wzorców sezonowych
    if high_value_count < min_high_value_transactions and i % 60 == 0:
        amount = round(random.uniform(20000, 50000), 2)
        high_value_count += 1
    else:
        if transaction_type in ['standing_charge', 'standing_order']:
            amount = round(random.uniform(5, 500) * seasonal_multiplier, 2)
        elif transaction_type in ['deposit', 'withdrawal', 'atm_withdrawal']:
            amount = round(random.uniform(50, 2000) * seasonal_multiplier, 2)
        elif transaction_type == 'express_transfer':
            amount = round(random.uniform(1000, 10000) * seasonal_multiplier, 2)
        else:
            amount = round(random.uniform(10, 2000) * seasonal_multiplier, 2)

    # Przypisz kategorię transakcji dla lepszego grupowania wizualizacji
    category_id = random.randint(1, len(transaction_categories))
    category = transaction_categories[category_id - 1]['category']

    # Generuj znaczące tytuły transakcji
    is_deposit = transaction_type in ['deposit', 'incoming_transfer']
    title = ""
    if category in transaction_title_categories:
        title = random.choice(transaction_title_categories[category])
        # Dodaj daty lub numery faktur, aby tytuły były bardziej realistyczne
        if 'bill' in title.lower() or 'payment' in title.lower():
            title += f" - {transaction_date.strftime('%b %Y')}"
        elif 'shopping' in title.lower() or 'purchase' in title.lower():
            store_names = ['Walmart', 'Target', 'Amazon', 'Tesco', 'Carrefour', 'IKEA', 'H&M', 'Zara']
            title += f" at {random.choice(store_names)}"

    recipient_account = ''
    if transaction_type in ['outgoing_transfer', 'incoming_transfer']:
        recipient_locale = random.choice(available_locales)
        recipient_account = fakers[recipient_locale].iban()

    # Oblicz bieżące saldo dla tego konta
    if account['id'] not in account_balances:
        account_balances[account['id']] = account['balance']
    if is_deposit:
        new_balance = account_balances[account['id']] + amount
    else:
        new_balance = max(0, account_balances[account['id']] - amount)

    # Przechowuj transakcję z bieżącym saldem
    transaction_data = {
        'id': i,
        'account_id': account['id'],
        'transaction_type_id': transaction_type_id,
        'category_id': category_id,
        'date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
        'amount': amount,
        'currency': account['currency'],
        'balance_after': round(new_balance, 2),
        'recipient_account': recipient_account,
        'status': random.choices(['completed', 'pending', 'cancelled'], weights=[0.95, 0.03, 0.02], k=1)[0],
        'title': title,
        'year': transaction_date.year,
        'month': transaction_date.month,
        'day_of_week': transaction_date.weekday(),
        'hour': transaction_date.hour
    }
    account_transactions[account['id']].append((transaction_date, transaction_data))

# Sortuj transakcje według daty dla każdego konta i aktualizuj bieżące salda
all_transactions = []
for account_id, txns in account_transactions.items():
    # Sortuj według daty
    sorted_txns = sorted(txns, key=lambda x: x[0])
    running_balance = accounts_df[accounts_df['id'] == account_id]['balance'].iloc[0]
    for _, txn in sorted_txns:
        is_deposit = transaction_types[txn['transaction_type_id'] - 1]['type'] in ['deposit', 'incoming_transfer']
        if is_deposit:
            running_balance += txn['amount']
        else:
            running_balance = max(0, running_balance - txn['amount'])
        txn['balance_after'] = round(running_balance, 2)
        all_transactions.append(txn)
        # Zaktualizuj saldo konta do przyszłego odniesienia
        account_balances[account_id] = running_balance

# Sortuj wszystkie transakcje według daty dla końcowej ramki danych
all_transactions.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))
transactions_df = pd.DataFrame(all_transactions)
transactions_df.to_csv(os.path.join(OUTPUT_DIR, 'transactions.csv'), index=False)

alerts = []
for i in range(1, NUM_ALERTS + 1):
    high_value_txns = transactions_df[transactions_df['amount'] > 20000]
    if len(high_value_txns) >= i:
        transaction = high_value_txns.sample(1).iloc[0]
    else:
        transaction = transactions_df.nlargest(NUM_ALERTS, 'amount').iloc[i - 1]
    alerts.append({
        'id': i,
        'transaction_id': transaction['id'],
        'reason': random.choice(['high amount', 'unusual location', 'rapid transfers']),
        'risk_level': random.choice(['Low', 'Medium', 'High']),
        'alert_date': fake.date_between(start_date=TODAY - timedelta(days=365), end_date=TODAY).strftime('%Y-%m-%d'),
        'flagged_by': random.choice(['system', 'analyst'])
    })

alerts_df = pd.DataFrame(alerts)  # Dodano tę linię, aby utworzyć DataFrame
alerts_df.to_csv(os.path.join(OUTPUT_DIR, 'alerts.csv'), index=False)

print("Dane wygenerowane i zapisane w folderze 'data'!")
print("Ten zestaw danych zawiera teraz realistyczne wzorce odpowiednie do wizualizacji!")

print("Łączenie wszystkich danych do jednego pliku CSV...")

# Utworzenie podkatalogu na złączone dane
MERGED_DIR = os.path.join(OUTPUT_DIR, "merged")
os.makedirs(MERGED_DIR, exist_ok=True)

# Sprawdzenie struktury ramek danych przed próbą łączenia
print("Kolumny w clients_df:", clients_df.columns.tolist())
print("Kolumny w locations_df:", locations_df.columns.tolist())
print("Kolumny w accounts_df:", accounts_df.columns.tolist())

# Łączenie danych z wykorzystaniem bezpieczniejszego podejścia
# Transakcje z informacjami o typach i kategoriach
transactions_enriched = transactions_df.merge(
    transaction_types_df, 
    left_on='transaction_type_id', 
    right_on='id', 
    how='left',
    suffixes=('', '_type')
).merge(
    pd.DataFrame(transaction_categories), 
    left_on='category_id', 
    right_on='id', 
    how='left',
    suffixes=('', '_category')
)

# Łączenie klientów i ich kont
clients_with_accounts = clients_df.merge(
    accounts_df,
    left_on='id',
    right_on='client_id',
    how='left',
    suffixes=('', '_account')
)

# Łączenie klientów i ich lokalizacji
clients_with_locations = clients_df.merge(
    locations_df,
    left_on='id',
    right_on='client_id',
    how='left',
    suffixes=('', '_location')
)

# Pełne łączenie klientów, lokalizacji i kont
clients_locations_accounts = clients_df.merge(
    locations_df,
    left_on='id',
    right_on='client_id',
    how='left',
    suffixes=('', '_location')
).merge(
    accounts_df,
    left_on='id',
    right_on='client_id',
    how='left',
    suffixes=('', '_account')
)

# Łączenie klientów, kont i transakcji
all_data = transactions_enriched.merge(
    accounts_df[['id', 'client_id']],
    left_on='account_id',
    right_on='id',
    how='left',
    suffixes=('', '_account')
).merge(
    clients_df,
    left_on='client_id',
    right_on='id',
    how='left',
    suffixes=('', '_client')
)

# Zapisanie połączonych danych
all_data_file = os.path.join(MERGED_DIR, 'all_data.csv')
all_data.to_csv(all_data_file, index=False)

clients_locations_accounts_file = os.path.join(MERGED_DIR, 'clients_accounts_locations.csv')
clients_locations_accounts.to_csv(clients_locations_accounts_file, index=False)

print(f"Wszystkie dane zostały zapisane do {all_data_file}")
print(f"Uproszczony zestaw danych klientów z kontami zapisano w {clients_locations_accounts_file}")