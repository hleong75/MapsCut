# MapsCut

Application Python complète avec interface graphique PyQt6 pour découper des images géoréférencées destinées à l'impression.

## Fonctionnalités

✅ **Chargement et mosaïquage**
- Sélection d'un dossier contenant des images GeoTIFF
- Génération automatique d'une mosaïque à partir de plusieurs images
- Utilisation de rasterio et GDAL pour le traitement raster

✅ **Interface interactive**
- Affichage de la mosaïque dans une vue zoomable et déplaçable (QGraphicsView)
- Sélection interactive d'une zone via rectangle dessiné à la souris (Ctrl + Clic gauche)
- Navigation: glisser-déposer pour se déplacer, molette pour zoomer

✅ **Paramètres d'impression configurables**
- Format papier: A4, A3, A2, A1, A0, Letter, Legal, Tabloid
- Orientation: Portrait ou Paysage
- DPI: Résolution d'impression (72-600 dpi)
- Overlap: Recouvrement entre pages en mm (pour assemblage manuel)

✅ **Découpage intelligent**
- Découpage automatique de la zone sélectionnée en pages
- Calcul du nombre de pages nécessaires
- Gestion du recouvrement paramétrable
- Préservation de la géoréférence

✅ **Export multi-format**
- Export en GeoTIFF géoréférencés (un fichier par page)
- Export en PDF multi-pages prêt à imprimer
- Conservation des métadonnées de géoréférence

## Structure du projet

```
MapsCut/
├── src/
│   ├── __init__.py           # Package principal
│   ├── interface.py          # Module interface graphique PyQt6
│   ├── raster_processing.py  # Module traitement raster
│   ├── cutting.py            # Module découpage en pages
│   └── export.py             # Module export GeoTIFF/PDF
├── main.py                   # Point d'entrée de l'application
├── requirements.txt          # Dépendances Python
├── run_windows.bat           # Lanceur Windows
├── run_linux.sh              # Lanceur Linux/macOS
├── .gitignore               # Fichiers à ignorer
└── README.md                # Ce fichier
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation sur Windows

1. **Télécharger et installer Python**
   - Télécharger depuis https://www.python.org/downloads/
   - ⚠️ **Important**: Cocher "Add Python to PATH" lors de l'installation

2. **Installer GDAL (optionnel mais recommandé)**
   - Télécharger les wheels GDAL depuis: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
   - Installer avec: `pip install GDAL-3.x.x-cpxxx-cpxxx-win_amd64.whl`

3. **Lancer l'application**
   - Double-cliquer sur `run_windows.bat`
   - Le script créera automatiquement un environnement virtuel et installera les dépendances

### Installation manuelle

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Installation de GDAL

GDAL peut être difficile à installer. Voici quelques solutions:

**Windows:**
```bash
# Option 1: Utiliser conda (recommandé)
conda install -c conda-forge gdal

# Option 2: Utiliser les wheels précompilés
pip install GDAL-3.x.x-cpxxx-cpxxx-win_amd64.whl
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev
pip install GDAL==$(gdal-config --version)
```

**macOS:**
```bash
brew install gdal
pip install GDAL==$(gdal-config --version)
```

## Utilisation

### 1. Lancement de l'application

**Windows:** Double-cliquez sur `run_windows.bat`

**Linux/macOS:** Exécutez `./run_linux.sh` ou `python main.py`

### 2. Chargement des images

1. Cliquez sur **"📁 Charger dossier GeoTIFF"**
2. Sélectionnez un dossier contenant des fichiers GeoTIFF (.tif, .tiff)
3. L'application crée automatiquement une mosaïque et l'affiche

### 3. Navigation dans l'image

- **Zoomer:** Utilisez la molette de la souris
- **Déplacer:** Maintenez le clic gauche et déplacez la souris
- **Réinitialiser la vue:** Rechargez le dossier

### 4. Sélection d'une zone

1. Maintenez **Ctrl** enfoncé
2. Cliquez et glissez pour dessiner un rectangle
3. La sélection s'affiche en rouge transparent
4. Les informations de découpage se mettent à jour automatiquement

### 5. Configuration des paramètres

Dans le panneau de gauche, configurez:
- **Format:** A4, A3, etc.
- **Orientation:** Portrait ou Paysage
- **DPI:** Résolution (300 dpi recommandé pour l'impression)
- **Recouvrement:** Chevauchement entre pages (10 mm par défaut)

Les informations de découpage se mettent à jour en temps réel.

### 6. Export

**Export GeoTIFF:**
1. Cliquez sur **"💾 Exporter GeoTIFF"**
2. Sélectionnez un dossier de destination
3. Les fichiers sont nommés `page_001.tif`, `page_002.tif`, etc.
4. Chaque fichier conserve sa géoréférence

**Export PDF:**
1. Cliquez sur **"📄 Exporter PDF"**
2. Choisissez l'emplacement et le nom du fichier PDF
3. Un PDF multi-pages est créé, prêt à imprimer

### 7. Effacer la sélection

Cliquez sur **"🗑️ Effacer sélection"** pour recommencer

## Architecture modulaire

### Module `raster_processing.py`
- Chargement de fichiers GeoTIFF
- Création de mosaïques
- Conversions pixel ↔ coordonnées géographiques
- Extraction de régions
- Normalisation pour affichage

### Module `cutting.py`
- Gestion des formats de papier
- Calcul des dimensions en pixels selon DPI
- Découpage en grille avec recouvrement
- Génération des informations de page

### Module `export.py`
- Export en GeoTIFF géoréférencés
- Export en PDF multi-pages
- Conversion et normalisation d'images
- Gestion des métadonnées

### Module `interface.py`
- Interface graphique PyQt6
- Vue interactive (zoom, pan, sélection)
- Panneau de configuration
- Gestion des événements utilisateur

## Gestion des erreurs

L'application intègre une gestion complète des erreurs:
- Validation des entrées utilisateur
- Messages d'erreur explicites
- Gestion des formats de fichiers non supportés
- Vérification de l'existence des fichiers/dossiers

## Dépendances

- **PyQt6** (≥6.4.0): Interface graphique
- **rasterio** (≥1.3.0): Traitement raster et GeoTIFF
- **numpy** (≥1.24.0): Calculs numériques
- **Pillow** (≥10.0.0): Traitement d'images
- **reportlab** (≥4.0.0): Génération de PDF
- **GDAL** (≥3.6.0): Outils géospatiaux
- **matplotlib** (≥3.7.0): Visualisation (optionnel)

## Limitations connues

- Les très grandes images peuvent être lentes à charger et afficher
- GDAL peut être difficile à installer sur certains systèmes
- Le format PDF ne conserve pas la géoréférence (utiliser GeoTIFF pour cela)

## Dépannage

### Erreur "No module named 'rasterio'" ou "GDAL"
Installez manuellement: `pip install rasterio GDAL`

### L'application ne se lance pas sur Windows
Vérifiez que Python est bien dans le PATH système

### Erreur de mémoire avec de grandes images
- Réduisez la zone de sélection
- Diminuez le DPI
- Utilisez moins d'images dans le dossier source

### Les GeoTIFF ne se chargent pas
Vérifiez que les fichiers ont bien l'extension .tif ou .tiff et contiennent des données géoréférencées

## Développement

### Exécution en mode développement
```bash
python main.py
```

### Structure de développement
Le projet est organisé de manière modulaire pour faciliter la maintenance et les évolutions:
- Séparation claire des responsabilités
- Code commenté et documenté
- Gestion des exceptions
- Interface découplée de la logique métier

## Licence

Ce projet est fourni tel quel, sans garantie.

## Auteur

MapsCut Development Team

## Support

Pour toute question ou problème, veuillez créer une issue sur le dépôt GitHub.
