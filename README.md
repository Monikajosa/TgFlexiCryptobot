# FlexiCrypto Bot

## Übersicht

FlexiCrypto ist ein modularer Telegram-Bot, der verschiedene Funktionen zur Verwaltung und Moderation von Gruppen und Kanälen bietet. Die Module sind so konzipiert, dass sie unabhängig arbeiten und einfach hinzugefügt oder entfernt werden können, ohne den Hauptbot zu verändern.

## Hauptmerkmale

### Hauptmenü Aufbau

- **Sprache wählen:** 
  - Sprachen werden dynamisch über die in `/locales` hinterlegten Sprachdateien geladen. Die Sprachdateien beinhalten die Bezeichnung ihres Buttons.
- **Gruppe wählen:** 
  - Untermenü enthält die Gruppe/Kanal, in welcher der Bot aktiv ist und der Nutzer aktuell Admin ist. Der Button beschriftet sich mit dem aktuellen Gruppen-/Kanalnamen und passt sich bei Änderungen automatisch an.
- **Owner Admin Menü**
  - Zugang
    - Nur die in `.env` definierte Owner-ID hat Zugriff auf dieses Menü.
  - Funktionen
    - **AD-Funktion:** Aktivierung/Deaktivierung für jede Gruppe.
    - **Modulverwaltung:** Aktivierung/Deaktivierung von Modulen.
    - **Logging:** Anzeige und Verwaltung von Fehlerprotokollen.
    - **Bot-Status:** Übersicht über aktive Gruppen, Benutzer und Speicherverbrauch.

### Modularität

- **Automatische Modul-Erkennung:** Module in `/modules` und `/admin` werden automatisch erkannt und geladen.
- **Eigene Menüstrukturen:** Module definieren ihre eigenen Menüstrukturen und Interaktionsmöglichkeiten.
- **Sprachdateien:** Alle Texte, einschließlich Modultexte, werden über Sprachdateien in `/locales/*.json` verwaltet. Änderungen gelten global.
- **Eigene SQLite-Datenbanken:** Jedes Modul verwaltet eine eigene SQLite-Datenbank zur Speicherung von Einstellungen und Daten.
- **Modul-Hooks und Events:** Module können auf bestimmte Events reagieren und eigene Hooks definieren.

### Gruppenspezifische Funktionen

- **Automatische Aktualisierung:** Gruppennamen und Gruppen-IDs werden bei jeder relevanten Interaktion automatisch überprüft und aktualisiert.
- **AD-Funktion:** Kann vom Owner aktiviert oder deaktiviert werden.
- **Linkvorschau:** Kann über Module und deren Einstellungen gesteuert werden.
- **Admin-Erkennung:** Gruppen-Admins werden erkannt und gespeichert.

### Benutzerinteraktionen

- **Admin-Menü:** Spezielles Menü für Gruppen-Admins und den Owner.
- **Dynamische Menüs:** Menüs und Buttons werden dynamisch aus den Sprachdateien generiert.
- **Sprachwechsel:** Benutzer können die Sprache des Bots ändern, die sofort übernommen wird.

### Sicherheitsmaßnahmen

- **Eingabeverifizierung:** Alle Benutzereingaben werden verifiziert und validiert, um Sicherheitslücken wie SQL-Injection zu verhindern.
- **Zugriffskontrollen:** Zugriffskontrollen und Berechtigungen werden strikt verwaltet, um unbefugten Zugriff zu verhindern.

### Fehlerbehandlung und Logging

- **Erweiterte Fehlerprotokollierung:** Fehler werden ausführlich protokolliert, um die Wartung zu erleichtern.
- **Benachrichtigungen:** Kritische Fehler lösen Benachrichtigungen an den Bot-Owner aus.

## Datenbankstruktur

### Hauptdatenbank (`main.db`)

Speichert globale Informationen über den Bot und die Gruppen.

```sql
CREATE TABLE IF NOT EXISTS groups (
  group_id INTEGER PRIMARY KEY,
  group_name TEXT,
  admin_ids TEXT, -- JSON-Array mit Admin-IDs
  ad_enabled INTEGER DEFAULT 1 -- AD-Funktion aktiviert/deaktiviert
);

CREATE TABLE IF NOT EXISTS warnings (
  user_id INTEGER,
  reason TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Modulaufbau

Jedes Modul muss folgende Anforderungen erfüllen:

### Konfigurationsdatei (`module_config.json`)

Definiert grundlegende Modul-Informationen und Berechtigungen.

```json
{
  "module_name": "Moderation",
  "module_description": "Verwaltet Warnungen und Bans.",
  "entry_point": "main.py",
  "permissions": ["group_admin", "owner"]
}
```

### Hauptskript (`main.py`)

Enthält die Logik des Moduls und definiert die Menüstruktur.

```python
from utils.translation import get_translation

def menu():
    return {
        "buttons": [
            {"label": get_translation("module_moderation_warn_button"), "callback": "warn_menu"},
            {"label": get_translation("module_moderation_ban_button"), "callback": "ban_menu"}
        ]
    }

def open_warn_menu():
    # Logik für das Warn-Menü
    pass
```

## Sprachunterstützung

Alle Texte werden zentral in Sprachdateien verwaltet. Die Texte sind durch Namensräume wie `module__` strukturiert.

### Beispiel für `/locales/en.json`

```json
{
  "module_moderation_warn_button": "Warn User",
  "module_moderation_ban_button": "Ban User"
}
```
