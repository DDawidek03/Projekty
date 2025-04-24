import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

available_locales = ['pl_PL', 'en_US', 'en_GB', 'de_DE', 'fr_FR', 'es_ES', 'it_IT', 
                     'ja_JP', 'zh_CN', 'ru_RU', 'pt_BR', 'nl_NL', 'sv_SE', 'tr_TR']
fakers = {locale: Faker(locale) for locale in available_locales}

country_currencies = {
    'pl_PL': 'PLN',
    'en_US': 'USD',
    'en_GB': 'GBP',
    'de_DE': 'EUR',
    'fr_FR': 'EUR',
    'es_ES': 'EUR',
    'it_IT': 'EUR',
    'ja_JP': 'JPY',
    'zh_CN': 'CNY',
    'ru_RU': 'RUB',
    'pt_BR': 'BRL',
    'nl_NL': 'EUR',
    'sv_SE': 'SEK',
    'tr_TR': 'TRY'
}

country_codes = {
    'pl_PL': 'PL',
    'en_US': 'US',
    'en_GB': 'GB',
    'de_DE': 'DE',
    'fr_FR': 'FR',
    'es_ES': 'ES',
    'it_IT': 'IT',
    'ja_JP': 'JP',
    'zh_CN': 'CN',
    'ru_RU': 'RU',
    'pt_BR': 'BR',
    'nl_NL': 'NL',
    'sv_SE': 'SE',
    'tr_TR': 'TR'
}

full_country_names = {
    'PL': 'Poland',
    'US': 'United States',
    'GB': 'United Kingdom',
    'DE': 'Germany',
    'FR': 'France',
    'ES': 'Spain',
    'IT': 'Italy',
    'JP': 'Japan',
    'CN': 'China',
    'RU': 'Russia',
    'BR': 'Brazil',
    'NL': 'Netherlands',
    'SE': 'Sweden',
    'TR': 'Turkey'
}

OUTPUT_DIR = "data"
NUM_CLIENTS = 200
NUM_ACCOUNTS = 300
NUM_TRANSACTIONS = 1100
NUM_LOCATIONS = 200
NUM_ALERTS = 50

START_DATE = datetime.strptime('2010-01-01', '%Y-%m-%d')
END_DATE = datetime.strptime('2025-12-31', '%Y-%m-%d')
TODAY = datetime.today()

os.makedirs(OUTPUT_DIR, exist_ok=True)

clients = []
for i in range(1, NUM_CLIENTS + 1):
    locale = random.choice(available_locales)
    fake = fakers[locale]
    
    registration_date = fake.date_between(start_date=START_DATE, end_date=TODAY).strftime('%Y-%m-%d')
    
    if locale == 'pl_PL':
        identifier = fake.pesel()
    else:
        identifier = fake.ssn()
    
    country_code = locale.split('_')[1]
    country_name = full_country_names.get(country_code, country_code)
    
    # Define Western locales that use Latin alphabet
    western_locales = ['pl_PL', 'en_US', 'en_GB', 'de_DE', 'fr_FR', 'es_ES', 'it_IT', 'nl_NL', 'sv_SE', 'tr_TR', 'pt_BR']
    
    # Use the original locale for most data but pick a Western locale for names
    name_locale = locale if locale in western_locales else random.choice(western_locales)
    name_faker = fakers[name_locale]
    
    clients.append({
        'id': i,
        'first_name': name_faker.first_name(),
        'last_name': name_faker.last_name(),
        'identifier': identifier,
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
        'email': fake.email(),
        'phone': fake.phone_number().replace(" ", ""),
        'gender': random.choice(['M', 'F']),
        'registration_date': registration_date,
        'is_active': random.choice(['Yes', 'No']),
        'country': country_name,
        'locale': locale
    })
clients_df = pd.DataFrame(clients)
clients_df.to_csv(os.path.join(OUTPUT_DIR, 'clients.csv'), index=False)

locations = []
english_faker = fakers['en_US']
english_faker_gb = fakers['en_GB']

for i in range(1, NUM_LOCATIONS + 1):
    client_id = random.randint(1, NUM_CLIENTS)
    client_locale = clients_df[clients_df['id'] == client_id]['locale'].iloc[0]
    client_country_code = client_locale.split('_')[1]
    client_country = full_country_names.get(client_country_code, client_country_code)
    
    if client_country_code in ['GB', 'IE']:
        fake_location = english_faker_gb
    else:
        fake_location = english_faker
    
    address_parts = fake_location.address().split('\n')
    
    if client_country_code == 'US':
        region = fake_location.state()
    elif client_country_code == 'GB':
        region = fake_location.county()
    else:
        region = f"{fake_location.state()} Region"
    
    locations.append({
        'id': i,
        'client_id': client_id,
        'city': fake_location.city(),
        'region': region,
        'country': client_country,
        'postal_code': fakers[client_locale].postcode(),
        'street': fake_location.street_name(),
        'building_number': fake_location.building_number()
    })

locations_df = pd.DataFrame(locations)
locations_df.to_csv(os.path.join(OUTPUT_DIR, 'locations.csv'), index=False)

accounts = []
client_account_counts = {i: 0 for i in range(1, NUM_CLIENTS + 1)}

for i in range(1, NUM_ACCOUNTS + 1):
    if i <= NUM_CLIENTS:
        client_id = i
    else:
        client_id = random.choices(
            list(client_account_counts.keys()),
            weights=[1.0/(count+1) for count in client_account_counts.values()],
            k=1
        )[0]
    
    client_account_counts[client_id] += 1
    
    client = clients_df[clients_df['id'] == client_id].iloc[0]
    client_locale = client['locale']
    client_reg_date = datetime.strptime(client['registration_date'], '%Y-%m-%d')
    
    default_currency = country_currencies.get(client_locale, 'USD')
    
    currency = random.choices(
        [default_currency, 'USD', 'EUR', 'GBP'], 
        weights=[0.7, 0.1, 0.15, 0.05], 
        k=1
    )[0]
    
    opening_date = fakers[client_locale].date_between(
        start_date=client_reg_date, 
        end_date=END_DATE
    ).strftime('%Y-%m-%d')
    
    balance_distribution = [
        lambda: round(random.uniform(0, 1000), 2),
        lambda: round(random.uniform(1000, 10000), 2),
        lambda: round(random.uniform(10000, 100000), 2),
        lambda: round(random.uniform(100000, 1000000), 2),
    ]
    balance_weights = [0.6, 0.25, 0.10, 0.05]
    balance_generator = random.choices(balance_distribution, weights=balance_weights, k=1)[0]
    
    account_type_options = ['personal', 'savings', 'business']
    account_type_weights = [0.7, 0.25, 0.05]
    
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
        'account_type': random.choices(account_type_options, weights=account_type_weights, k=1)[0],
        'opening_date': opening_date,
        'balance': balance_generator(),
        'currency': currency,
        'is_active': random.choices([True, False], weights=[0.9, 0.1], k=1)[0]
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
transaction_types_df = pd.DataFrame(transaction_types)
transaction_types_df.to_csv(os.path.join(OUTPUT_DIR, 'transaction_types.csv'), index=False)

transactions = []
high_value_count = 0
min_high_value_transactions = NUM_ALERTS + 10

for i in range(1, NUM_TRANSACTIONS + 1):
    account_idx = random.randint(0, len(accounts_df) - 1)
    account = accounts_df.iloc[account_idx]
    
    client_id = account['client_id']
    client_locale = clients_df[clients_df['id'] == client_id]['locale'].iloc[0]
    fake = fakers[client_locale]
    
    account_opening_date = datetime.strptime(account['opening_date'], '%Y-%m-%d')
    
    transaction_date = fake.date_time_between(
        start_date=account_opening_date, 
        end_date=END_DATE
    ).strftime('%Y-%m-%d %H:%M:%S')
    
    transaction_type_id = random.randint(1, len(transaction_types))
    transaction_type = transaction_types[transaction_type_id - 1]['type']
    
    if high_value_count < min_high_value_transactions and i % 20 == 0:
        amount = round(random.uniform(20001, 50000), 2)
        high_value_count += 1
    else:
        if transaction_type in ['standing_charge', 'standing_order']:
            amount = round(random.uniform(5, 500), 2)
        elif transaction_type in ['deposit', 'withdrawal', 'atm_withdrawal']:
            amount = round(random.uniform(50, 3000), 2)
        elif transaction_type == 'express_transfer':
            amount = round(random.uniform(1000, 20000), 2)
        else:
            amount = round(random.uniform(10, 5000), 2)
    
    transaction_type_id = random.randint(1, len(transaction_types))
    
    is_deposit = transaction_types[transaction_type_id - 1]['type'] == 'deposit'
    
    title = ""
    if transaction_types[transaction_type_id - 1]['type'] == 'outgoing_transfer' or transaction_types[transaction_type_id - 1]['type'] == 'incoming_transfer':
        categories = {
            "Daily expenses": [
                f"Rent payment - {fake.month_name()} {fake.year()}",
                f"Apartment rent {fake.street_address()} - {fake.month_name()}",
                f"Electricity bill - {fake.month_name()} {fake.year()}",
                f"Gas bill - {fake.month_name()} {fake.year()}",
                f"Water bill - {fake.month_name()} {fake.year()}",
                f"TV/Internet subscription - {fake.month_name()}",
                "Home insurance",
                "Heating payment",
                "Renovation fund",
                "Administrative fee"
            ],
            "Shopping": [
                "Grocery shopping",
                f"Shopping at {random.choice(['Walmart', 'Tesco', 'Carrefour', 'Aldi', 'Home Depot', 'Target', 'IKEA'])}",
                f"Purchase of {random.choice(['clothes', 'electronics', 'books', 'furniture', 'appliances'])}",
                "Online shopping",
                f"Order from {random.choice(['eBay', 'Amazon', 'Etsy', 'Alibaba'])}",
                "Public transport ticket"
            ],
            "Business services": [
                f"Invoice no. {fake.year()}/{random.randint(1, 12):02d}/F{random.randint(100, 999)} - {random.choice(['IT services', 'consulting', 'office supplies', 'transport services', 'marketing services'])}",
                f"VAT Invoice FV/{fake.year()}/{random.randint(1, 12):02d}/{random.randint(100, 999)}",
                f"Invoice for {random.choice(['accounting', 'legal', 'advertising', 'consulting', 'IT', 'training'])} services",
                f"Payment for {random.choice(['programming', 'graphic design', 'analytical', 'marketing'])} services",
                "Contract work payment",
                "Project work payment"
            ],
            "Salaries": [
                f"Salary - {fake.month_name()} {fake.year()}",
                f"Monthly salary {fake.month_name()}",
                f"Salary payment {fake.month_name()} {fake.year()}",
                "Quarterly bonus",
                "Holiday bonus",
                "Performance bonus",
                "13th salary",
                "Seniority bonus"
            ],
            "Finance": [
                f"{random.choice(['Mortgage', 'Personal loan', 'Car loan', 'Consolidation loan'])} payment - {fake.month_name()} installment",
                f"Loan installment {random.randint(1, 240)}/{random.randint(240, 360)}",
                f"Capital investment - {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])}",
                "Transfer to investment account",
                "Dividend payment",
                "Stock investment profit",
                "Bond redemption",
                "Retirement account contribution",
                "Pension plan contribution"
            ],
            "Taxes and official fees": [
                f"{random.choice(['Income tax', 'VAT', 'Property tax', 'Transfer tax', 'Inheritance tax'])}",
                "Stamp duty",
                "Court fee",
                "Document issuance fee",
                "Social security contributions",
                "Health insurance premium",
                "Income tax advance payment"
            ],
            "Insurance": [
                "Car insurance payment",
                "Vehicle liability insurance",
                "Comprehensive auto insurance",
                "Life insurance",
                "Health insurance",
                "Travel insurance",
                "Property insurance"
            ],
            "Transport": [
                "Fuel purchase",
                "Vehicle inspection fee",
                "Vehicle repair cost",
                "Public transport tickets",
                "Train ticket",
                "Flight ticket",
                "Car rental"
            ],
            "Education and development": [
                "University tuition",
                "Course fee",
                "Training fee",
                "Educational books purchase",
                "School tuition",
                "Kindergarten fee",
                "Tutoring"
            ],
            "Entertainment": [
                "Cinema ticket",
                "Concert ticket",
                "Sports event ticket",
                "Streaming service subscription",
                "Gym/fitness membership",
                "Hotel reservation",
                "Trip payment"
            ],
            "Other": [
                "Charity donation",
                "Private loan repayment",
                "Family transfer",
                f"Gift for {random.choice(['birthday', 'name day', 'wedding', 'holidays'])}",
                "Membership fee",
                "Medical service fee",
                "Refund for unused services"
            ]
        }
        
        category = random.choice(list(categories.keys()))
        title = random.choice(categories[category])
    
    recipient_account = ''
    if transaction_types[transaction_type_id - 1]['type'] in ['outgoing_transfer', 'incoming_transfer']:
        recipient_locale = random.choice(available_locales)
        recipient_account = fakers[recipient_locale].iban()
    
    transactions.append({
        'id': i,
        'account_id': account['id'],
        'transaction_type_id': transaction_type_id,
        'date': transaction_date,
        'amount': amount,
        'currency': account['currency'],
        'balance_after': round(account['balance'] + (amount if is_deposit else -amount), 2),
        'recipient_account': recipient_account,
        'status': random.choice(['completed', 'pending', 'cancelled']),
        'title': title
    })
transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv(os.path.join(OUTPUT_DIR, 'transactions.csv'), index=False)

alerts = []
for i in range(1, NUM_ALERTS + 1):
    high_value_txns = transactions_df[transactions_df['amount'] > 20000]
    
    if len(high_value_txns) >= i:
        transaction = high_value_txns.sample(1).iloc[0]
    else:
        transaction = transactions_df.nlargest(NUM_ALERTS, 'amount').iloc[i-1]
    
    alerts.append({
        'id': i,
        'transaction_id': transaction['id'],
        'reason': random.choice(['high amount', 'unusual location', 'rapid transfers']),
        'risk_level': random.choice(['Low', 'Medium', 'High']),
        'alert_date': fake.date_between(start_date=TODAY - timedelta(days=365), end_date=TODAY).strftime('%Y-%m-%d'),
        'flagged_by': random.choice(['system', 'analyst'])
    })
alerts_df = pd.DataFrame(alerts)
alerts_df.to_csv(os.path.join(OUTPUT_DIR, 'alerts.csv'), index=False)

print("Data generated and saved to 'data' folder!")