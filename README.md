FlexiCrypto

Bot-Verhalten und Grundlogik

Grundaufbau des Bots Hauptmerkmale:

Hauptmenü Aufbau:

Sprache wählen:
-> Sprachen werden über die in /locales hinterlegten Sprachdateien dynamisch geladen. Sprachdateien beinhalten die Bezeichnung ihres Button
Gruppe wählen:
-> Untermenü enthält die Gruppe -/Kanal in welcher der Bot aktiv und der Nutzer aktuell admin ist. Button beschriftet sich mit dem aktuellen Gruppen -/Kanalname und passt sich bei änderungen entsprechend an. Beim betätigen der jeweiligen Gruppe werden die in /modules hineterlegten Modulebuttons dynamisch erzeugt und über die jeweiligen Module können Einstellungen für die Gruppe -/Kanal welche zuvor ausgewählt wurde.
Bot Owner Menü (Butten nur sichtbar für den Bot Owner. ID wird mit der in der .env hinterlegten verglichen):
-> Untermenü enthält Folgende Menüs:
Ad Modul -> Untermenü lässt die Ad's Für registrierte Gruppe -/Kanal deaktivieren und aktivieren
Module -> hier lassen sich Module aus der /modules aktivieren und deaktivieren. (Module sind stadard mäßig deaktivert) Modulbuttons sollen dennoch in den Gruppe -/Kanal Einstellungen angezeigt werden mit dem hinzweis "Wartung"

Modularität:
Module in /modules und /admin werden automatisch erkannt und geladen, ohne Änderungen am Hauptbot vorzunehmen. Module definieren ihre eigenen Menüstrukturen und Interaktionsmöglichkeiten. Alle Texte, einschließlich Modultexte, werden aus den zentralen Sprachdateien in /locales geladen. Module speichern ihre Einstellungen in einer eigenen SQLite-Datenbank im jeweiligen Modulordner. Sprachunterstützung:

Sprachdateien (/locales/*.json) enthalten alle Texte, einschließlich Modultexte. Texte werden über Namensräume wie module__ eindeutig definiert. Änderungen an Sprachdateien gelten global für den Bot und alle Module. Modulspezifische Speicherung:

Jedes Modul verwaltet eine eigene SQLite-Datenbank (.db), um Einstellungen und Daten unabhängig zu speichern. Der Hauptbot stellt eine Schnittstelle bereit, um Module mit ihrer Datenbank zu verbinden. Menüstruktur mit "Zurück"-Button:

Jedes Menü enthält einen "Zurück"-Button, um eine intuitive Navigation zu gewährleisten. Die Struktur ist dynamisch und passt sich der Hierarchie an. Gruppenspezifische Funktionen:

Gruppennamen werden bei jeder relevanten Interaktion automatisch überprüft und aktualisiert. AD-Funktion: Nur der Owner kann diese aktivieren oder deaktivieren. Linkvorschau: Wird über Module und deren Menüs gesteuert. 2. Verhaltensübersicht des Bots Verhalten in Gruppen/Kanälen: Hinzufügen des Bots zu einer Gruppe/Kanal:

Der Bot registriert die Gruppen-ID und den aktuellen Gruppen-Namen in der Hauptdatenbank. Gruppen-Admins werden erkannt und gespeichert. Ein Begrüßungstext informiert die Admins, dass alle Einstellungen im privaten Chat vorgenommen werden können. Automatische AD-Funktion:

Jeder Post in einer Gruppe, in der der Bot aktiv ist, erhält einen zusätzlichen Text mit einem Hyperlink (AD). Wenn der Hyperlink der einzige Link im Post ist, wird die Linkvorschau automatisch deaktiviert. Der Owner kann die AD-Funktion für jede Gruppe über das Owner Menü aktivieren oder deaktivieren. Verhalten im privaten Chat: Prüfung der Benutzerberechtigung:

Wenn ein Benutzer den Bot anschreibt, überprüft dieser, ob der Benutzer Admin in einer Gruppe ist, in der der Bot aktiv ist. Gruppen, in denen der Benutzer Admin ist, werden mit ihrem aktuellen Namen angezeigt. Startmenü:

Buttons: "Sprache ändern": Öffnet ein Untermenü, um die Sprache zu wechseln. "Gruppen/Kanäle verwalten": Öffnet die Liste der verwaltbaren Gruppen. "Owner Admin Menü": Wird nur angezeigt, wenn der Benutzer die in .env definierte Owner-ID besitzt. Gruppen-/Kanalauswahl und Modulverwaltung:

Nach Auswahl einer Gruppe werden alle Module angezeigt, die für diese Gruppe verfügbar sind.

Modul-Buttons:

Werden dynamisch aus der menu()-Funktion der Module erzeugt. Beschriftungen stammen aus den zentralen Sprachdateien. Modulinteraktion:

Bei Auswahl eines Moduls öffnet sich das vom Modul definierte Menü. Jede Interaktion wird über Callback-Funktionen des Moduls abgewickelt. Sprache ändern:

Die Sprachbuttons werden dynamisch aus den Sprachdateien generiert. Nach Auswahl wird die Sprache sofort übernommen und das Menü aktualisiert. Owner Admin Menü: Zugang:

Nur die in .env definierte Owner-ID hat Zugriff auf dieses Menü. Funktionen:

AD-Funktion:

Der Owner kann die AD-Funktion für jede Gruppe aktivieren oder deaktivieren. Änderungen werden sofort in der Hauptdatenbank gespeichert. Modulverwaltung:

Der Owner sieht eine Liste aller Module im /admin-Ordner. Module können aktiviert/deaktiviert werden, ohne den Bot neu zu starten. Logging:

Der Owner kann Fehlerprotokolle anzeigen lassen. Protokolle können heruntergeladen oder gelöscht werden. Bot-Status:

Der Owner kann den globalen Status des Bots einsehen (z. B. aktive Gruppen, Benutzer, Speicherverbrauch). 3. Datenbankstruktur

Hauptdatenbank (main.db): Speichert globale Informationen über den Bot und die Gruppen:
sql Code kopieren CREATE TABLE IF NOT EXISTS groups ( group_id INTEGER PRIMARY KEY, group_name TEXT, admin_ids TEXT, -- JSON-Array mit Admin-IDs ad_enabled INTEGER DEFAULT 1, -- AD-Funktion aktiviert/deaktiviert settings TEXT -- JSON-String mit weiteren Gruppeneinstellungen ); 2. Modul-spezifische Datenbanken: Jedes Modul verwendet eine eigene SQLite-Datenbank. Beispiel für ein Moderationsmodul:

sql Code kopieren CREATE TABLE IF NOT EXISTS warnings ( user_id INTEGER, reason TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ); 4. Modulaufbau Jedes Modul muss folgende Anforderungen erfüllen:

Konfigurationsdatei (module_config.json):

json Code kopieren { "module_name": "Moderation", "module_description": "Verwaltet Warnungen und Bans.", "entry_point": "main.py", "permissions": ["group_admin", "owner"] } Hauptskript (main.py): Enthält:

menu(): Definiert Buttons und Callback-Funktionen. load_language(key): Lädt Texte aus zentralen Sprachdateien. Beispiel:

python Code kopieren from utils.translation import get_translation

def menu(): return { "buttons": [ {"label": get_translation("module_moderation_warn_button"), "callback": "warn_menu"}, {"label": get_translation("module_moderation_ban_button"), "callback": "ban_menu"} ], "callbacks": { "warn_menu": open_warn_menu, "ban_menu": open_ban_menu } }

def open_warn_menu(): # Logik für das Warn-Menü pass 5. Sprachunterstützung Nutzung zentraler Sprachdateien: Namensräume wie module__ strukturieren Texte. Beispiel für /locales/en.json: json Code kopieren { "module_moderation_warn_button": "Warn User", "module_moderation_ban_button": "Ban User", "owner_menu_ad_toggle": "Toggle AD Function" } 6. Dynamisches Modulmanagement Der Hauptbot registriert Module basierend auf der module_config.json. Module können dynamisch aktiviert oder deaktiviert werden. Änderungen an Modulen erfordern keinen Neustart des Bots.
