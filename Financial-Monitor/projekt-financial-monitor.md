# 💼 **Projekt: Financial Monitor - System Analityczny**

## 🎯 **Opis projektu**

Celem projektu jest stworzenie systemu bankowego opartego na relacyjnej bazie danych, który umożliwia:

- analizę danych klientów, kont i transakcji,
- oznaczanie podejrzanych operacji,
- prezentację danych w postaci interaktywnego dashboardu Power BI,
- automatyczne tworzenie kopii zapasowych bazy danych,
- wykrywanie anomalii w transakcjach bankowych.

---

## 🧰 **Technologie użyte w projekcie**

| Obszar              | Technologia                            | Opis                                                              |
| ------------------- | -------------------------------------- | ----------------------------------------------------------------- |
| Baza danych         | **MySQL**                              | Relacyjna baza danych z tabelami klientów, kont, transakcji itp.  |
| Backend (ETL)       | **Python (pandas, faker, sqlalchemy)** | Generowanie i przetwarzanie danych, zasymulowanie działania banku |
| Wykrywanie anomalii | **Python (pandas, numpy)**             | System wykrywania podejrzanych transakcji i alertów               |
| Backup danych       | **Python + mysqldump**                 | Automatyczne tworzenie i rotacja kopii zapasowych bazy danych     |
| SQL                 | **MySQL**                              | Tworzenie tabel, kwerendy analityczne, wykrywanie wzorców         |
| Wizualizacja        | **Power BI**                           | Dashboard z KPI, wykresami, relacjami                             |
| Dokumentacja        | **README.md + ERD**                    | Diagramy relacji, opisy funkcji i logiki                          |
| Analizy             | **Jupyter Notebook**                   | Eksploracja danych, statystyki, podsumowania                      |
| GitHub              | **Repozytorium publiczne**             | Kod, dane, dashboard, dokumentacja do wglądu                      |

---

## 🧱 **Struktura bazy danych (ERD)**

![Diagram ERD bazy danych prism.db](../zdjecia/prism-erd.png)

### 📊 **Tabele w bazie danych**

#### 🧍‍♂️ `clients` – dane klientów

| Column              | Data Type    | Description                      |
| ------------------- | ------------ | -------------------------------- |
| `id`                | INTEGER (PK) | ID klienta                       |
| `first_name`        | TEXT         | Imię                             |
| `last_name`         | TEXT         | Nazwisko                         |
| `identifier`        | TEXT         | Numer identyfikacyjny/PESEL/SSN  |
| `birth_date`        | DATE         | Data urodzenia                   |
| `email`             | TEXT         | Email                            |
| `phone`             | TEXT         | Telefon                          |
| `gender`            | TEXT         | Płeć (M / F)                     |
| `registration_date` | DATE         | Data rejestracji klienta         |
| `is_active`         | TEXT         | Czy klient jest aktywny (Yes/No) |
| `country`           | TEXT         | Kraj pochodzenia                 |
| `locale`            | TEXT         | Ustawienia regionalne klienta    |

---

#### 🌍 `locations` – lokalizacja klienta

| Column            | Data Type    | Description              |
| ----------------- | ------------ | ------------------------ |
| `id`              | INTEGER (PK) | ID lokalizacji           |
| `client_id`       | INTEGER (FK) | Klient                   |
| `city`            | TEXT         | Miasto                   |
| `region`          | TEXT         | Region                   |
| `country`         | TEXT         | Kraj                     |
| `postal_code`     | TEXT         | Kod pocztowy             |
| `street`          | TEXT         | Ulica                    |
| `building_number` | TEXT         | Numer budynku/mieszkania |

---

#### 💳 `accounts` – konta bankowe

| Column           | Data Type     | Description                                 |
| ---------------- | ------------- | ------------------------------------------- |
| `id`             | INTEGER (PK)  | ID konta                                    |
| `client_id`      | INTEGER (FK)  | Właściciel konta                            |
| `account_number` | TEXT          | Numer konta IBAN                            |
| `account_type`   | TEXT          | Typ konta (personal, savings, business)     |
| `opening_date`   | DATE          | Data otwarcia konta                         |
| `balance`        | DECIMAL(12,2) | Saldo                                       |
| `currency`       | TEXT          | Waluta (EUR, USD, PLN itp.)                 |
| `is_active`      | INTEGER/TEXT  | Czy konto jest aktywne (1/0 lub True/False) |

---

#### 🔄 `transaction_types` – typy transakcji

| Column        | Data Type    | Description                              |
| ------------- | ------------ | ---------------------------------------- |
| `id`          | INTEGER (PK) | ID typu transakcji                       |
| `type`        | TEXT         | Nazwa (deposit, withdrawal, transfer...) |
| `description` | TEXT         | Opis                                     |

---

#### 💸 `transactions` – transakcje

| Column                | Data Type     | Description                           |
| --------------------- | ------------- | ------------------------------------- |
| `id`                  | INTEGER (PK)  | ID transakcji                         |
| `account_id`          | INTEGER (FK)  | Konto źródłowe                        |
| `transaction_type_id` | INTEGER (FK)  | Typ transakcji                        |
| `date`                | DATETIME      | Data i czas transakcji                |
| `amount`              | DECIMAL(12,2) | Kwota transakcji                      |
| `currency`            | TEXT          | Waluta transakcji                     |
| `balance_after`       | DECIMAL(12,2) | Saldo po transakcji                   |
| `recipient_account`   | TEXT          | Konto odbiorcy (IBAN)                 |
| `status`              | TEXT          | Status: completed, pending, cancelled |
| `title`               | TEXT          | Tytuł przelewu/opis transakcji        |

---

#### 🚨 `alerts` – podejrzane transakcje

| Column           | Data Type    | Description                                                   |
| ---------------- | ------------ | ------------------------------------------------------------- |
| `id`             | INTEGER (PK) | ID alertu                                                     |
| `transaction_id` | INTEGER (FK) | Powiązana transakcja                                          |
| `reason`         | TEXT         | Powód alertu (high amount, unusual location, rapid transfers) |
| `risk_level`     | TEXT         | Low / Medium / High                                           |
| `alert_date`     | DATE         | Data oznaczenia                                               |
| `flagged_by`     | TEXT         | analyst / system                                              |

---

## 🔍 **System wykrywania anomalii (w trakcie pracy)**

Projekt zawiera system wykrywania anomalii ([`anomaly_alert.py`](../Financial-Monitor/skrypty/anomaly_alert.py)), który jest obecnie w trakcie implementacji. System powinien:

1. **Analizować transakcje** pod kątem podejrzanych wzorców
2. **Wykrywać anomalie** oparte na następujących kryteriach:
   - Transakcje o nietypowo wysokich kwotach (powyżej 95 percentyla)
   - Nietypowe wzorce transakcji (np. wiele przelewów w krótkim czasie)
   - Serie szybkich transferów z jednego konta
3. **Przypisywać poziom ryzyka** każdej wykrytej anomalii
4. **Generować alerty** dla zespołów bezpieczeństwa
5. **Raportować statystyki** związane z wykrytymi anomaliami

System powinien wykorzystywać:

- Metody statystyczne do określania progów dla nietypowych transakcji
- Analizę historyczną zachowań klientów jako punkt odniesienia
- Reguły biznesowe dla specyficznych scenariuszy

---

## 📊 **ETL - Generator danych**

Projekt wykorzystuje generator danych ([`data_generator.py`](../Financial-Monitor/skrypty/data_generator.py)) do symulacji działania banku i zasilania bazy danych:

- Generowanie realistycznych danych klientów, kont i transakcji
- Symulacja historii transakcji z różnymi wzorcami użytkowania
- Tworzenie danych z odpowiednią dystrybucją i relacjami
- Obsługa różnych typów kont, walut i transakcji
- Zasilanie bazy danych w kontrolowany sposób z możliwością ustawienia parametrów

Ten komponent ETL (Extract, Transform, Load) pozwala na:

- Kontrolowane generowanie zestawów testowych
- Symulację normalnych i anomalnych zachowań klientów
- Tworzenie różnorodnych scenariuszy transakcyjnych
- Skalowanie liczby rekordów według potrzeb

---

## 💾 **Backup bazy danych**

System kopii zapasowych ([`backup.py`](../Financial-Monitor/skrypty/backup.py)) automatyzujący proces tworzenia i zarządzania backupami bazy danych:

- Automatyczne tworzenie kopii zapasowych przy użyciu narzędzia `mysqldump`
- Konfigurowalny system z możliwością ustawień w pliku konfiguracyjnym `db_config.ini`
- Dynamiczne generowanie nazw plików kopii zapasowych zawierających datę i czas
- Rotacja starych kopii zapasowych (usuwanie po określonym czasie - domyślnie 7 dni)
- Szczegółowe logi wykonywanych operacji z informacją o błędach zapisywane w pliku `backup.log`
- Obsługa wszystkich obiektów bazy danych (procedury, wyzwalacze, widoki, zdarzenia)
- Możliwość uruchamiania ręcznego lub przez harmonogram zadań (cron, Task Scheduler)
- Zabezpieczenia przed błędami z obsługą wyjątków i raportowaniem problemów

---

## 📊 **Dashboard Power BI**

**Docelowo dashboard zawierać będzie:**

- KPI: liczba klientów, kont, łączna suma transakcji
- Wykresy transakcji w czasie z możliwością filtrowania po okresie
- Top klienci wg sumy przelewów i liczby transakcji
- Wykryte alerty z podziałem na poziom ryzyka i powód
- Mapa lokalizacji klientów z oznaczeniem koncentracji
- Analizy transakcji podejrzanych z możliwością drążenia danych
- Rozkład wartości transakcji z oznaczeniem anomalii statystycznych
