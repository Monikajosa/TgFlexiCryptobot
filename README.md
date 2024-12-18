# FlexiCrypto Bot

## Übersicht

FlexiCrypto ist ein modularer Telegram-Bot, der verschiedene Funktionen im Bereich Crypto zur Verwaltung und Moderation von Gruppen und Kanälen bietet. Die Module sind so konzipiert, dass sie unabhängig voneinander arbeiten und leicht hinzugefügt oder entfernt werden können.

## Ordnerstruktur

Die folgende Ordnerstruktur zeigt die grundlegende Organisation des Projekts:

```
TgFlexiCryptobot/
├── admin/
│   ├── __init__.py               # Lädt alle Admin-Module
│   ├── owner_admin_module.py     # Owner-spezifisches Menü
├── modules/
│   ├── __init__.py               # Lädt alle Benutzer-Module
│   ├── moderation_module.py      # Beispiel: Moderationsmodul
│   ├── welcome_module.py         # Beispiel: Begrüßungsmodul
├── data/
│   ├── persistent_storage.py     # Datenbankinteraktionen
│   ├── migrations.py             # Datenbank-Migrations-Handler
├── locales/
│   ├── en.json                   # Englische Übersetzungen
│   ├── de.json                   # Deutsche Übersetzungen
├── utils/
│   ├── translation.py            # Übersetzungsfunktionen
│   ├── helpers.py                # Allgemeine Hilfsfunktionen
├── .env                          # Token, Owner-ID, Log-Level
├── requirements.txt              # Abhängigkeiten
├── bot.py                        # Hauptdatei
├── config.py                     # Konfigurationen (Konstanten)
```

## Hauptmerkmale

### Hauptmenü Aufbau

- **Sprache wählen:**
  - Das Modul "Sprache ändern" liegt in `/modules` und gehört zum Grundgerüst und stellt folgende Funktion zur Verfügung:
    - Sprachen werden dynamisch über die in `/locales` hinterlegten Sprachdateien geladen. Die Sprachdateien beinhalten die Bezeichnung ihres Buttons.
    - Die gewählte Sprache wird global für den Bot gesetzt.

- **Gruppe wählen:** 
  - Untermenü enthält die Gruppe/Kanal, in welcher der Bot aktiv ist und der Nutzer aktuell Admin ist. Der Button beschriftet sich mit dem aktuellen Gruppen-/Kanalnamen und passt sich bei Änderungen automatisch an.

- **Owner Admin Menü:**
  - Zugang:
    - Nur die in `.env` definierte Owner-ID hat Zugriff auf dieses Menü.
  - Funktionen:
    - Module hierzu liegen in `/admin`. Folgende Grundmodule stellt das Grundgerüst bereits zur Verfügung:
      - AD-Funktion: Aktivierung/Deaktivierung für jede Gruppe.
      - Modulverwaltung: Aktivierung/Deaktivierung von Modulen.
      - Bot-Status: Übersicht über aktive Gruppen und Benutzer.

### Botaktionen

- **Reaktion in Gruppe/Kanal:**
  - Nachdem der Bot einer Gruppe/Kanal hinzugefügt wurde, reagiert er einmalig mit "Bot aktiv. Einstellungen können PRIVAT vorgenommen werden". Nach der ersten Reaktion keine weiteren Reaktionen mehr.

- **Reaktion in privater Konversation:**
  - Nachdem der Bot privat gestartet wurde, zeigt er das Hauptmenü an. Jegliche zuvor gesetzte Einstellung wird geladen.

### Modularität

- **Automatische Modul-Erkennung:** Module in `/modules` und `/admin` werden automatisch erkannt und geladen.
- **Eigene Menüstrukturen:** Module definieren ihre eigenen Menüstrukturen und Interaktionsmöglichkeiten.
- **Sprachdateien:** Alle Texte, einschließlich Modultexte, werden über Sprachdateien in `/locales/*.json` verwaltet. Änderungen gelten global. Standardsprache sollte die der Nutzerapp sein.
- **Eigene SQLite-Datenbanken:** Jedes Modul verwaltet eine eigene SQLite-Datenbank zur Speicherung von Einstellungen und Daten. Diese müssen so aufgebaut sein, dass Daten bei Anpassungen, Bot-Abstürzen etc. nicht verloren gehen.
- **Modul-Hooks und Events:** Module können auf bestimmte Ereignisse im Bot reagieren und eigene Aktionen ausführen.

### Gruppenspezifische Funktionen

- **Automatische Aktualisierung:** Gruppennamen und Gruppen-IDs werden bei jeder relevanten Interaktion automatisch überprüft und aktualisiert.
- **AD-Funktion:** Kann vom Owner aktiviert oder deaktiviert werden.
- **Linkvorschau:** Kann über Module und deren Einstellungen gesteuert werden.
- **Admin-Erkennung:** Gruppen-Admins werden erkannt und gespeichert.

### Benutzerinteraktionen

- **Owner Admin Menü:** Spezielles Menü für den Owner.
- **Dynamische Menüs:** Menüs und Buttons werden dynamisch aus den jeweiligen Dateien generiert.
- **Sprachwechsel:** Benutzer können die Sprache des Bots ändern, die sofort übernommen wird und auch bei einer erneuten Interaktion bestehen bleibt.

### Sicherheitsmaßnahmen

- **Eingabeverifizierung:** Alle Benutzereingaben werden verifiziert und validiert, um Sicherheitslücken wie SQL-Injection zu verhindern.
- **Zugriffskontrollen:** Zugriffskontrollen und Berechtigungen werden strikt verwaltet, um unbefugten Zugriff zu verhindern.
- **Interaktion mit dem Bot:** Interagiert ein Nutzer privat mit dem Bot, wird geprüft, ob der Nutzer in einer Gruppe/Kanal Admin ist, in welcher der Bot aktiv ist.

### Fehlerbehandlung und Logging

- **Erweiterte Fehlerprotokollierung:** Fehler werden ausführlich protokolliert, um die Wartung zu erleichtern.
- **Benachrichtigungen:** Kritische Fehler lösen Benachrichtigungen an den Bot-Owner aus.
