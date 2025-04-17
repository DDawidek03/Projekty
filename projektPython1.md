# 📱 Game Rental - Aplikacja Desktopowa w Python i Kivy

## 📋 Opis projektu

Aplikacja **Game Rental** to interaktywny system obsługi wypożyczalni gier, zbudowany przy użyciu Pythona oraz frameworka Kivy/KivyMD. Aplikacja umożliwia zarządzanie wypożyczeniami gier, obsługę kont użytkowników oraz przechowywanie danych w lokalnej bazie SQLite.

## 🛠️ Technologie

- **Python** - język programowania
- **Kivy/KivyMD** - framework do tworzenia interfejsów użytkownika na wiele platform
- **SQLite** - lekka, wbudowana baza danych
- **UI/UX Design** - nowoczesny, responsywny interfejs

## ✨ Główne funkcje

### 👤 Zarządzanie użytkownikami

- Rejestracja nowych użytkowników
- Logowanie do systemu
- Edycja profilu użytkownika
- Bezpieczne przechowywanie haseł

### 🎮 Zarządzanie grami

- Przeglądanie dostępnych gier
- Wypożyczanie gier
- Zwracanie wypożyczonych gier
- Historia wypożyczeń

### ⚙️ Ustawienia i personalizacja

- Tryb ciemny/jasny
- Ustawienia konta
- Pomoc i wsparcie

## 🗄️ Struktura bazy danych

Aplikacja korzysta z bazy danych SQLite z następującymi tabelami:

- **Uzytkownicy** - dane użytkowników systemu
- **Gry** - informacje o dostępnych grach
- **Wypozyczenia** - historia wypożyczeń

## 📊 Diagram przejść między ekranami

```
Login Screen → Register Screen
      ↓
Dashboard Screen ←→ Account Screen
      ↓
 Rent Screen     ←→ Edit Profile Screen
      ↓
Settings Screen  ←→ Help Screen
```

## 📂 Struktura projektu

Projekt składa się z następujących plików:

- **game_rental.py** - główny plik aplikacji z logiką biznesową
- **game_rental.kv** - definicja interfejsu użytkownika w języku Kivy
- **game_rental.db** - plik bazy danych SQLite

## 🔒 Bezpieczeństwo

Aplikacja implementuje następujące mechanizmy bezpieczeństwa:

- Walidacja danych wejściowych
- Weryfikacja haseł (minimalna długość, znaki specjalne)
- Zabezpieczenia przed SQL Injection
- Generator bezpiecznych haseł

## 📱 Zrzuty ekranu

![Ekran logowania](./zdjecia/game_rental_login.png)
![Panel główny](./zdjecia/game_rental_dashboard.png)
![Wypożyczanie gier](./zdjecia/game_rental_rent.png)

## 🚀 Rozwój projektu

Planowane są następujące rozszerzenia aplikacji:

- Synchronizacja danych z chmurą
- System rekomendacji gier
- Wersja mobilna na Android i iOS
- Integracja z API zewnętrznych baz gier

---

> Autor: Damian Dawidek
