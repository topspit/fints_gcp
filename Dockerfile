# Basis-Image für Python
FROM python:3.10

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere Code und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopiere den gesamten App-Code
COPY . .

# Exponiere den Port für den Webserver
EXPOSE 8080

# Flask-App starten
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app
