 FinTS Web App auf Google Cloud

Dieses Projekt bietet eine vollständige Implementierung einer FinTS-gestützten Webanwendung, die in der Google Cloud läuft. Es beinhaltet eine Flask-Webanwendung zur Authentifizierung über Google OAuth, zur Speicherung von Benutzerdaten in Firestore sowie zur Abfrage von Bankkontodaten über das FinTS-Protokoll.

## Lernziele
Durch das Durcharbeiten dieses Projekts lernen Sie:
- **Google OAuth 2.0**: Wie man eine sichere Anmeldung mit Google realisiert.
- **Google Firestore**: Speicherung und Verwaltung von Nutzerdaten in einer NoSQL-Datenbank.
- **FinTS-Integration**: Abrufen von Bankkontodaten über das FinTS-Protokoll.
- **Google Cloud Run**: Deployment einer containerisierten Anwendung in der Google Cloud.
- **Terraform**: Automatisierte Bereitstellung der Cloud-Infrastruktur.
- **Google Cloud Build Trigger**: Automatisierung des Build- und Deployment-Prozesses.

## Projektübersicht
Das Projekt besteht aus mehreren Komponenten:
- **Flask-Webanwendung (`app.py`)**: Kern der Anwendung mit Authentifizierung, Firestore-Datenbankzugriff und FinTS-Abfragen.
- **Terraform-Konfigurationsdateien (`main.tf`, `service-account.tf`)**: Automatisierte Bereitstellung der Firestore-Datenbank und der benötigten Google Cloud Ressourcen.
- **Cloud Build-Konfiguration (`cloudbuild-dev.yaml`)**: Automatisiertes Deployment auf Google Cloud Run mit Google Cloud Build.

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

## Installation und Einrichtung
### Voraussetzungen
- Ein Google Cloud-Projekt mit aktivierten APIs:
  - Cloud Run
  - Firestore
  - IAM
- Ein Service-Account mit den entsprechenden Berechtigungen.
- Terraform installiert.
- Docker installiert.

### Schritte zur Einrichtung
1. **Google Cloud Authentifizierung einrichten**
   ```sh
   gcloud auth login
   gcloud config set project fints-web
   ```
2. **Terraform ausführen** (erstellt Firestore und Service-Accounts):
   ```sh
   terraform init
   terraform apply
   ```
3. **Docker-Image erstellen und in Google Container Registry hochladen:**
   ```sh
   docker build -t gcr.io/fints-web/fints-app:latest .
   docker push gcr.io/fints-web/fints-app:latest
   ```
4. **Cloud Run Deployment starten:**
   ```sh
   gcloud run deploy fints-dev --image gcr.io/fints-web/fints-app:latest --region europe-west3 --allow-unauthenticated
   ```

### Automatisches Deployment mit Cloud Build
Google Cloud Build kann automatisch Änderungen aus GitHub übernehmen und die Anwendung neu deployen. Der `cloudbuild-dev.yaml` definiert diesen Prozess.

**Trigger erstellen:**
```sh
gcloud beta builds triggers create cloud-source-repositories \
  --repo=fints-web \
  --branch-pattern=".*" \
  --build-config=cloudbuild-dev.yaml
```

Nach dem Einrichten wird bei jedem Push in das Repository automatisch ein neuer Build und ein Deployment ausgelöst.

## Fazit
Dieses Projekt bietet eine praxisnahe Einführung in die Kombination von Google Cloud Technologien mit Python-basierten Webanwendungen. Es automatisiert die Infrastrukturbereitstellung mit Terraform und nutzt Google Cloud Build für Continuous Deployment.

Viel Erfolg beim Ausprobieren! 🚀

## Sicherheitshinweise
- Speichere keine sensiblen Daten im Quellcode.
- Verwende Umgebungsvariablen für Passwörter und API-Keys.
- Stelle sicher, dass Firestore-Datenbankregeln korrekt konfiguriert sind.

