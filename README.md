Hier ist eine überarbeitete und strukturierte Version der README-Datei, die die hinzugefügten Details berücksichtigt:

---

# FlexiCrypto Bot

## Übersicht

FlexiCrypto ist ein modularer Telegram-Bot, der verschiedene Funktionen zur Verwaltung und Moderation von Gruppen bietet. Die Module sind so konzipiert, dass sie unabhängig arbeiten und einfach hinzugefügt oder entfernt werden können, ohne den Hauptbot zu verändern.

## Hauptmerkmale

### Hauptmenü Aufbau

- **Sprache wählen:** 
  - Sprachen werden dynamisch über die in `/locales` hinterlegten Sprachdateien geladen. Die Sprachdateien beinhalten die Bezeichnung ihres Buttons.
- **Gruppe wählen:** 
  - Untermenü enthält die Gruppe/Kanal, in welcher der Bot aktiv ist und der Nutzer aktuell Admin ist. Der Button beschriftet sich mit dem aktuellen Gruppen-/Kanalnamen und passt sich bei Änderungen automatisch an.
- **Bot Owner Menü:** 
  - Nur sichtbar für den Bot Owner. Die ID wird mit der in der `.env` hinterlegten verglichen. Das Untermenü enthält:
    - **Ad Modul:** Ermöglicht das Aktivieren/Deaktivieren der Ads für registrierte Gruppen/Kanäle.
    - **Module:** Aktivierung und Deaktivierung von Modulen aus dem `/modules` Ordner. Module sind standardmäßig deaktiviert, Modulbuttons werden dennoch in den Gruppen-/Kanaleinstellungen angezeigt.

### Modularität

- **Automatische Modul-Erkennung:** Module in `/modules` und `/admin` werden automatisch erkannt und geladen.
- **Eigene Menüstrukturen:** Module definieren ihre eigenen Menüstrukturen und Interaktionsmöglichkeiten.
- **Sprachdateien:** Alle Texte, einschließlich Modultexte, werden über Sprachdateien in `/locales/*.json` verwaltet. Änderungen gelten global.
- **Eigene SQLite-Datenbanken:** Jedes Modul verwaltet eine eigene SQLite-Datenbank zur Speicherung von Einstellungen und Daten.

### Gruppenspezifische Funktionen

- **Automatische Aktualisierung:** Gruppennamen und Gruppen-IDs werden bei jeder relevanten Interaktion automatisch überprüft und aktualisiert.
- **AD-Funktion:** Kann vom Owner aktiviert oder deaktiviert werden.
- **Linkvorschau:** Kann über Module und deren Einstellungen gesteuert werden.
- **Admin-Erkennung:** Gruppen-Admins werden erkannt und gespeichert.

### Benutzerinteraktionen

- **Admin-Menü:** Spezielles Menü für Gruppen-Admins und den Owner.
- **Dynamische Menüs:** Menüs und Buttons werden dynamisch aus den Sprachdateien generiert.
- **Sprachwechsel:** Benutzer können die Sprache des Bots ändern, die sofort übernommen wird.

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

## Owner Admin Menü

### Zugang

Nur die in `.env` definierte Owner-ID hat Zugriff auf dieses Menü.

### Funktionen

- **AD-Funktion:** Aktivierung/Deaktivierung für jede Gruppe.
- **Modulverwaltung:** Aktivierung/Deaktivierung von Modulen.
- **Logging:** Anzeige und Verwaltung von Fehlerprotokollen.
- **Bot-Status:** Übersicht über aktive Gruppen, Benutzer und Speicherverbrauch.

---

Diese Strukturierung sorgt für eine klare und verständliche Dokumentation, die es einfacher macht, den Bot zu entwickeln und zu verwalten. Lass mich wissen, ob du weitere Anpassungen oder Ergänzungen benötigst.
