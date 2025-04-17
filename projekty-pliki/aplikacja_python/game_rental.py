import re
import random
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
import sqlite3
from kivy.core.window import Window
from kivymd.uix.list import IconLeftWidget

with open("game_rental.kv", "r", encoding="utf-8") as kv_file:
    KV = kv_file.read()

class EditProfileScreen(Screen):
    pass

class RentScreen(Screen):
    pass

class AccountScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class HelpScreen(Screen):
    pass

class NavigationDrawer(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.create_nav_menu())

    def create_nav_menu(self):
        """Create navigation menu content."""
        layout = MDBoxLayout(orientation="vertical", spacing="8dp", padding="8dp")

        options = [
            ("Settings", lambda x: MDApp.get_running_app().show_settings()),
            ("Help", lambda x: MDApp.get_running_app().show_help()),
            ("Log Out", lambda x: MDApp.get_running_app().log_out())
        ]

        for text, callback in options:
            item = OneLineIconListItem(text=text, on_release=callback)
            layout.add_widget(item)

        return layout

class GameRentalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"
        Window.size = (460, 720)
        self.current_user = None
        self.nav_drawer = NavigationDrawer()
        return Builder.load_string(KV)

    def on_start(self):
        self.initialize_database()
        self.initialize_sample_games()  # Add sample games if none exist
        dashboard_screen = self.root.get_screen('dashboard')
        if not dashboard_screen.children:
            dashboard_screen.add_widget(self.nav_drawer)
        self.display_rental_history()

    def initialize_database(self):
        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()

            # Tworzenie tabeli użytkowników
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Uzytkownicy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT NOT NULL,
                nazwisko TEXT NOT NULL,
                email TEXT UNIQUE,
                haslo TEXT
            )
            ''')

            # Tworzenie tabeli gier
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Gry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tytul TEXT NOT NULL,
                gatunek TEXT,
                dostepnosc INTEGER DEFAULT 1,
                opis TEXT
            )
            ''')

            # Tworzenie tabeli wypożyczeń
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Wypozyczenia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uzytkownik_id INTEGER,
                gra_id INTEGER,
                data_wypozyczenia TEXT DEFAULT CURRENT_TIMESTAMP,
                data_zwrotu TEXT DEFAULT NULL,
                FOREIGN KEY (uzytkownik_id) REFERENCES Uzytkownicy (id),
                FOREIGN KEY (gra_id) REFERENCES Gry (id)
            )
            ''')

            
            connection.commit()
            connection.close()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")

    def initialize_sample_games(self):
        """Initialize sample games in database if no games exist."""
        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            
            # Check if there are any games in the database
            cursor.execute("SELECT COUNT(*) FROM Gry")
            count = cursor.fetchone()[0]
            
            # If no games exist, add some sample games
            if count == 0:
                sample_games = [
                    ("The Last of Us", "Action-Adventure", "A post-apocalyptic action-adventure game."),
                    ("FIFA 24", "Sports", "Football simulation game."),
                    ("Minecraft", "Sandbox", "Block building and adventure game."),
                    ("Call of Duty: Modern Warfare", "FPS", "First-person shooter game."),
                    ("The Legend of Zelda: Breath of the Wild", "Adventure", "Action-adventure game."),
                    ("Grand Theft Auto V", "Action", "Action-adventure game."),
                    ("Fortnite", "Battle Royale", "Online multiplayer battle royale game."),
                    ("Cyberpunk 2077", "RPG", "Action role-playing game."),
                    ("Assassin's Creed Valhalla", "Action RPG", "Action role-playing game.")
                ]
                
                for title, genre, description in sample_games:
                    cursor.execute(
                        "INSERT INTO Gry (tytul, gatunek, dostepnosc, opis) VALUES (?, ?, 1, ?)",
                        (title, genre, description)
                    )
                
                connection.commit()
                print("Sample games added to the database.")
            
            connection.close()
        except Exception as e:
            print(f"Error initializing sample games: {e}")

    def validate_login(self):
        username = self.root.get_screen('login').ids.username.text
        password = self.root.get_screen('login').ids.password.text
        
        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Uzytkownicy WHERE email=? AND haslo=?", (username, password))
            user = cursor.fetchone()
            connection.close()

            if user:
                self.current_user = user
                self.root.current = 'dashboard'
                self.show_dialog("Success", "You have logged in successfully!")
                self.display_rental_history()
            else:
                self.show_dialog("Login Failed", "Invalid username or password.")
        except Exception as e:
            print(f"Error during login: {e}")
            self.show_dialog("Error", f"Error during login: {e}")

    def show_dialog(self, title, text):
        if not hasattr(self, 'dialog'):
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=self.close_dialog
                    ),
                ],
            )
        else:
            self.dialog.title = title
            self.dialog.text = text
        
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_register_screen(self):
        self.root.current = 'register'

    def show_rent_screen(self):
        """Show rent screen and load available games."""
        self.root.current = 'rent'
        self.load_available_games()

    def load_available_games(self):
        """Load and display available games in the rent screen."""
        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            
            cursor.execute('''
            SELECT id, tytul, gatunek, opis FROM Gry 
            WHERE dostepnosc = 1
            ORDER BY tytul ASC
            ''')
            
            games = cursor.fetchall()
            connection.close()
            
            games_list = self.root.get_screen('rent').ids.available_games_list
            games_list.clear_widgets()
            
            if not games:
                no_games_item = OneLineIconListItem(
                    text="No games available for rent."
                )
                games_list.add_widget(no_games_item)
            else:
                for game in games:
                    game_id, title, genre, description = game
                    item = TwoLineAvatarIconListItem(
                        text=f"{title}",
                        secondary_text=f"Genre: {genre}",
                        on_release=lambda x, title=title: self.select_game(title)
                    )
                    icon = IconLeftWidget(
                        icon="gamepad-variant"
                    )
                    item.add_widget(icon)
                    games_list.add_widget(item)
                    
        except Exception as e:
            print(f"Error loading available games: {e}")
            self.show_dialog("Error", f"Error loading available games: {e}")

    def select_game(self, game_title):
        """Select a game to rent from the list."""
        self.root.get_screen('rent').ids.game_title.text = game_title

    def rent_game(self):
        game_title = self.root.get_screen('rent').ids.game_title.text

        if not game_title:
            self.show_dialog("Rental Error", "Please enter a game title.")
            return

        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()

            cursor.execute('SELECT id, dostepnosc FROM Gry WHERE tytul=?', (game_title,))
            game = cursor.fetchone()
            if not game or game[1] == 0:
                self.show_dialog("Rental Error", "Game not available or does not exist.")
                connection.close()
                return

            game_id = game[0]

            cursor.execute('UPDATE Gry SET dostepnosc = 0 WHERE id = ?', (game_id,))
            cursor.execute('''
            INSERT INTO Wypozyczenia (uzytkownik_id, gra_id, data_wypozyczenia)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (self.current_user[0], game_id))

            connection.commit()
            connection.close()

            self.show_dialog("Success", f"Game '{game_title}' rented successfully!")
            self.display_rental_history()
            self.load_available_games()  # Refresh the games list
        except Exception as e:
            print(f"Error during rental: {e}")
            self.show_dialog("Error", f"Error during rental: {e}")

    def return_game(self):
        game_title = self.root.get_screen('dashboard').ids.return_game_title.text

        if not game_title:
            self.show_dialog("Return Error", "Please enter a game title.")
            return

        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()

            cursor.execute('''
            SELECT W.id, G.id
            FROM Wypozyczenia W
            JOIN Gry G ON W.gra_id = G.id
            WHERE W.uzytkownik_id = ? AND G.tytul = ? AND W.data_zwrotu IS NULL
            ''', (self.current_user[0], game_title))
            rental = cursor.fetchone()

            if not rental:
                self.show_dialog("Return Error", "You haven't rented this game or it was already returned.")
                connection.close()
                return

            rental_id, game_id = rental

            cursor.execute('UPDATE Wypozyczenia SET data_zwrotu = CURRENT_TIMESTAMP WHERE id = ?', (rental_id,))
            cursor.execute('UPDATE Gry SET dostepnosc = 1 WHERE id = ?', (game_id,))

            connection.commit()
            connection.close()

            self.show_dialog("Success", f"Game '{game_title}' returned successfully!")
            self.display_rental_history()
            # If we're on the rent screen, refresh the games list
            if self.root.current == 'rent':
                self.load_available_games()
        except Exception as e:
            print(f"Error during return: {e}")
            self.show_dialog("Error", f"Error during return: {e}")

    def log_out(self):
        self.root.current = 'login'
        self.root.get_screen('login').ids.username.text = ""
        self.root.get_screen('login').ids.password.text = ""
        self.clear_registration_fields()
        self.clear_dashboard()

    def clear_dashboard(self):
        dashboard_screen = self.root.get_screen('dashboard')
        dashboard_screen.ids.rental_history.clear_widgets()
        dashboard_screen.ids.return_game_title.text = ""

    def clear_registration_fields(self):
        register_screen = self.root.get_screen('register')
        register_screen.ids.name.text = ""
        register_screen.ids.last_name.text = ""
        register_screen.ids.email.text = ""
        register_screen.ids.password.text = ""
        register_screen.ids.confirm_password.text = ""

    def contains_inappropriate_words(self, text):
        inappropriate_words = ["badword1", "badword2", "badword3"]
        return any(word in text.lower() for word in inappropriate_words)

    def is_valid_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit."
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter."
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter."
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`" for char in password):
            return False, "Password must contain at least one special character."
        return True, ""

    def generate_password(self):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`"
        password = "".join(random.choice(characters) for _ in range(12))
        return password

    def register_user(self):
        name = self.root.get_screen('register').ids.name.text
        last_name = self.root.get_screen('register').ids.last_name.text
        email = self.root.get_screen('register').ids.email.text
        password = self.root.get_screen('register').ids.password.text
        confirm_password = self.root.get_screen('register').ids.confirm_password.text

        if not all([name, last_name, email, password, confirm_password]):
            self.show_dialog("Registration Error", "All fields must be filled out.")
            return

        if self.contains_inappropriate_words(email) or self.contains_inappropriate_words(password):
            self.show_dialog("Registration Error", "Email or password contains inappropriate words.")
            return

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            self.show_dialog("Registration Error", "Invalid email format.")
            return

        is_valid, message = self.is_valid_password(password)
        if not is_valid:
            self.show_dialog("Registration Error", message)
            return

        if password == confirm_password:
            try:
                connection = sqlite3.connect('game_rental.db')
                cursor = connection.cursor()
                cursor.execute('''
                INSERT INTO Uzytkownicy (imie, nazwisko, email, haslo)
                VALUES (?, ?, ?, ?)
                ''', (name, last_name, email, password))
                
                connection.commit()
                connection.close()
                self.show_dialog("Success", f"User {name} {last_name} registered successfully!")
                self.root.current = 'login'
            except sqlite3.IntegrityError:
                self.show_dialog("Error", "Email already exists.")
            except Exception as e:
                print(f"Error during registration: {e}")
                self.show_dialog("Error", f"Error during registration: {e}")
        else:
            self.show_dialog("Error", "Passwords do not match.")

    def show_account_screen(self):
        try:
            self.root.current = 'account'
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            
            cursor.execute('SELECT imie, nazwisko, email FROM Uzytkownicy WHERE id=?', (self.current_user[0],))
            account_info = cursor.fetchone()
            connection.close()
            
            if account_info:
                account_screen = self.root.get_screen('account')
                account_screen.ids.user_name.text = account_info[0]
                account_screen.ids.user_last_name.text = account_info[1]
                account_screen.ids.user_email.text = account_info[2]
            else:
                print("No account information found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_settings(self):
        self.root.current = 'settings'

    def show_help(self):
        self.root.current = 'help'

    def display_rental_history(self):
        if not self.current_user:
            return
        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            cursor.execute('''
            SELECT G.tytul, W.data_wypozyczenia, W.data_zwrotu
            FROM Wypozyczenia W
            JOIN Gry G ON W.gra_id = G.id
            WHERE W.uzytkownik_id = ?
            ORDER BY W.data_wypozyczenia DESC
            LIMIT 10
            ''', (self.current_user[0],))
            rentals = cursor.fetchall()
            connection.close()

            rental_history = self.root.get_screen('dashboard').ids.rental_history
            rental_history.clear_widgets()

            for rental in rentals:
                game_title = rental[0]
                
                # Format dates to be more compact
                try:
                    rental_date = rental[1][:10] if rental[1] else ""
                    return_date = rental[2][:10] if rental[2] else ""
                except:
                    rental_date = str(rental[1])
                    return_date = str(rental[2]) if rental[2] else ""
                    
                # Determine status and date to show
                if rental[2]:  # If returned
                    status = "Returned"
                    date_to_show = return_date
                else:  # If still rented
                    status = "Rented"
                    date_to_show = rental_date
                    
                # First line: Game title only
                primary_text = game_title
                
                # Second line: Status with date
                secondary_text = f"{status} ({date_to_show})"
                    
                # Create the two-line list item with an icon
                item = TwoLineAvatarIconListItem(
                    text=primary_text,
                    secondary_text=secondary_text
                )
                
                # Add a gamepad icon
                icon = IconLeftWidget(
                    icon="gamepad-variant"
                )
                item.add_widget(icon)
                rental_history.add_widget(item)
                
        except Exception as e:
            self.show_dialog("Error", f"Error displaying rental history: {e}")

    def show_login_screen(self):
        self.root.current = 'login'

    def save_profile_changes(self):
        name = self.root.get_screen('edit_profile').ids.name.text
        last_name = self.root.get_screen('edit_profile').ids.last_name.text
        email = self.root.get_screen('edit_profile').ids.email.text
        password = self.root.get_screen('edit_profile').ids.password.text

        if not all([name, last_name, email, password]):
            self.show_dialog("Error", "All fields must be filled out.")
            return

        try:
            connection = sqlite3.connect('game_rental.db')
            cursor = connection.cursor()
            cursor.execute('''
            UPDATE Uzytkownicy
            SET imie=?, nazwisko=?, email=?, haslo=?
            WHERE id=?
            ''', (name, last_name, email, password, self.current_user[0]))
            connection.commit()
            connection.close()

            self.show_dialog("Success", "Profile updated successfully.")
            self.show_account_screen()
        except Exception as e:
            self.show_dialog("Error", f"Error updating profile: {e}")

    def toggle_dark_mode(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def toggle_password_visibility(self, icon_button, text_field):
        if text_field.password:
            text_field.password = False
            icon_button.icon = "eye"
        else:
            text_field.password = True
            icon_button.icon = "eye-off"

    def show_edit_profile(self):
        """Show edit profile screen."""
        self.root.current = 'edit_profile'

if __name__ == '__main__':
    GameRentalApp().run()