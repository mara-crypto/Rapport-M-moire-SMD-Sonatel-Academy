# Utiliser une image Python officielle comme image de base
FROM python:3.9-slim

# Définir le répertoire de travail dans l'image
WORKDIR /

# Copier les fichiers nécessaires dans l'image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers dans l'image
COPY . .

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Définir la commande par défaut pour exécuter l'application
CMD ["python", "app.py"]
