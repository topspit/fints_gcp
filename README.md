# FinTS Google Cloud Demo

## Einleitung
Dieses Projekt zeigt, wie man Google Cloud Technologien mit FinTS (Financial Transaction Services) kombiniert, um ein sicheres und cloudbasiertes Online-Banking-Dashboard zu erstellen.

Nach dem Durchlaufen dieses Projekts wirst du gelernt haben:
- Wie man Google OAuth für die Authentifizierung nutzt.
- Wie man eine verschlüsselte API-Anbindung mit FinTS implementiert.
- Wie man Firebase Firestore als Datenbank für Nutzeranmeldungen nutzt.
- Wie man eine Webanwendung mit Flask in einer Google Cloud Umgebung bereitstellt.

Das Ziel ist es, eine funktionale Webanwendung zu erstellen, die sich mit einem Bankkonto verbindet, Authentifizierungsmechanismen nutzt und Daten sicher in der Cloud speichert.

## Projektübersicht
Diese Anwendung ermöglicht es Nutzern, sich mit ihrem Google-Konto anzumelden, ihre Bankdaten über das FinTS-Protokoll zu verbinden und ihren Kontostand über eine Web-Oberfläche anzuzeigen.

### Hauptfunktionen
- **Google OAuth 2.0 Authentifizierung**: Nutzer melden sich mit ihrem Google-Konto an.
- **FinTS Integration**: Verbindung zu Bankkonten mit PIN/TAN-Authentifizierung.
- **Firestore Datenbank**: Sicheres Speichern der Nutzerbankdaten in Firebase Firestore.
- **Dynamisches Dashboard**: Zeigt aktuelle Bankinformationen des Nutzers an.
- **Verschlüsselung**: Sensible Daten werden mit Verschlüsselung gespeichert und entschlüsselt.

## Projektdateien

### 1. `app.py`
Die Hauptapplikation, die folgende Aufgaben übernimmt:
- Startet den Flask Webserver
- Verarbeitet OAuth-Authentifizierung mit Google
- Verbindet sich mit Firestore zur Speicherung von Benutzerdaten
- Implementiert die FinTS-Schnittstelle für Online-Banking
- Stellt die Web-Oberfläche zur Verfügung

### 2. `decrypt_sub.py`
Dieses Skript entschlüsselt die `client_secret.json.enc` und `service-account.json.enc`, um Zugriff auf die Google API und Firebase zu erhalten.

### 3. `decrypt_enc_PIN.py`
Bietet Funktionen zur Verschlüsselung und Entschlüsselung von PINs, um sensible Daten sicher zu speichern.

### 4. `templates/index.html`
Die Startseite der Anwendung, die Login-Optionen bietet.

### 5. `templates/dashboard.html`
Das Hauptdashboard, das den Bankkontostand des Nutzers anzeigt.

### 6. `templates/fints_login.html`
Ein Formular für Nutzer, um ihre Bankdaten einzugeben und mit FinTS zu verbinden.

### 7. `templates/tan.html`
Falls eine TAN erforderlich ist, wird diese Seite zur Eingabe einer TAN verwendet.

## Einrichtung und Nutzung

### Voraussetzungen
- Ein Google Cloud Projekt mit OAuth 2.0 Credentials
- Ein Firebase Firestore Projekt
- Eine Bank, die FinTS unterstützt
- Python 3 und Flask

### Installation
1. Klone dieses Repository:
   ```sh
   git clone https://github.com/dein-username/dein-repository.git
   cd dein-repository
   ```

2. Installiere die benötigten Abhängigkeiten:
   ```sh
   pip install -r requirements.txt
   ```

3. Setze die Umgebungsvariablen für die Entschlüsselung:
   ```sh
   export DECRYPTION_PASSWORD='dein_passwort'
   ```

4. Starte die Anwendung:
   ```sh
   python app.py
   ```

5. Öffne die Anwendung im Browser unter `http://localhost:5000`

## Deployment auf Google Cloud
Das Projekt kann in einer Google Cloud Umgebung bereitgestellt werden. Hierfür kannst du Google Cloud Run oder eine VM auf Google Compute Engine nutzen.

### Deployment mit Cloud Run
1. Erstelle ein Dockerfile für die Anwendung.
2. Baue das Docker-Image und pushe es in die Google Container Registry.
3. Starte das Deployment mit Cloud Run.

Weitere Details findest du in der Google Cloud Dokumentation.

## Sicherheitshinweise
- Speichere keine sensiblen Daten im Quellcode.
- Verwende Umgebungsvariablen für Passwörter und API-Keys.
- Stelle sicher, dass Firestore-Datenbankregeln korrekt konfiguriert sind.

## Fazit
Diese Anwendung ist eine gute Einführung für Google Cloud Nutzer, die lernen möchten, wie man eine sichere Webanwendung mit Google OAuth, Firebase Firestore und FinTS erstellt. Viel Erfolg beim Ausprobieren!

