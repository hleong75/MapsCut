# Guide de l'utilisateur MapsCut

## Table des matières
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Premiers pas](#premiers-pas)
4. [Fonctionnalités détaillées](#fonctionnalités-détaillées)
5. [Cas d'usage](#cas-dusage)
6. [FAQ](#faq)
7. [Dépannage](#dépannage)

## Introduction

MapsCut est une application de découpage d'images géoréférencées pour l'impression. Elle permet de:
- Charger plusieurs images GeoTIFF et les assembler en mosaïque
- Sélectionner interactivement une zone à imprimer
- Découper cette zone en pages imprimables avec recouvrement
- Exporter les résultats en GeoTIFF ou PDF

### Pourquoi MapsCut?

Lorsque vous avez de grandes cartes géoréférencées et que vous souhaitez les imprimer sur plusieurs pages pour les assembler ensuite, MapsCut automatise tout le processus:
- Calcul automatique du nombre de pages nécessaires
- Gestion du recouvrement pour faciliter l'assemblage
- Conservation de la géoréférence pour chaque page
- Export direct en PDF prêt à imprimer

## Installation

### Prérequis système

- **Système d'exploitation:** Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python:** 3.8 ou supérieur
- **Mémoire RAM:** 4 GB minimum, 8 GB recommandé pour les grandes images
- **Espace disque:** 1 GB pour l'application + espace pour vos données

### Installation rapide (Windows)

1. Téléchargez le projet MapsCut
2. Double-cliquez sur `run_windows.bat`
3. L'installation des dépendances se fait automatiquement

### Installation manuelle

```bash
# 1. Cloner ou télécharger le projet
cd MapsCut

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/macOS:
source venv/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 5. Lancer l'application
python main.py
```

### Installation de GDAL

GDAL est nécessaire pour le traitement des GeoTIFF. Voici comment l'installer:

#### Windows
```bash
# Option 1: Utiliser conda (recommandé)
conda install -c conda-forge gdal

# Option 2: Utiliser les wheels précompilés
# Télécharger depuis: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
pip install GDAL-3.x.x-cpxxx-cpxxx-win_amd64.whl
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal
pip install GDAL==$(gdal-config --version)
```

#### macOS
```bash
brew install gdal
pip install GDAL==$(gdal-config --version)
```

## Premiers pas

### 1. Lancement de l'application

**Windows:**
```
Double-cliquez sur run_windows.bat
```

**Linux/macOS:**
```bash
./run_linux.sh
```

Ou directement:
```bash
python main.py
```

### 2. Interface de l'application

L'interface se compose de deux parties:

**Panneau de gauche (contrôles):**
- Bouton de chargement de dossier
- Paramètres d'impression
- Informations de découpage
- Boutons d'export

**Zone principale (droite):**
- Vue de la mosaïque d'images
- Zone de sélection interactive

### 3. Workflow de base

1. **Charger des images**
   - Cliquez sur "📁 Charger dossier GeoTIFF"
   - Sélectionnez un dossier contenant des fichiers .tif ou .tiff
   - Attendez la création de la mosaïque

2. **Explorer la carte**
   - Utilisez la molette pour zoomer
   - Cliquez-glissez pour vous déplacer

3. **Sélectionner une zone**
   - Maintenez **Ctrl** enfoncé
   - Cliquez et glissez pour dessiner un rectangle
   - La zone apparaît en rouge

4. **Configurer l'impression**
   - Format: Choisissez A4, A3, etc.
   - Orientation: Portrait ou Paysage
   - DPI: 300 recommandé pour l'impression
   - Recouvrement: 10 mm par défaut

5. **Exporter**
   - Cliquez sur "💾 Exporter GeoTIFF" ou "📄 Exporter PDF"
   - Choisissez le dossier/fichier de destination

## Fonctionnalités détaillées

### Navigation dans l'image

| Action | Méthode |
|--------|---------|
| Zoomer | Molette de la souris |
| Dézoomer | Molette de la souris (sens inverse) |
| Se déplacer | Cliquer-glisser avec le bouton gauche |
| Sélectionner | Ctrl + Cliquer-glisser |

### Formats de papier supportés

| Format | Dimensions (mm) | Usage typique |
|--------|----------------|---------------|
| A4 | 210 × 297 | Documents standard |
| A3 | 297 × 420 | Petites affiches |
| A2 | 420 × 594 | Affiches moyennes |
| A1 | 594 × 841 | Grandes affiches |
| A0 | 841 × 1189 | Très grandes affiches |
| Letter | 216 × 279 | Standard US |
| Legal | 216 × 356 | Documents légaux US |
| Tabloid | 279 × 432 | Tabloid US |

### Paramètres DPI

| DPI | Qualité | Usage |
|-----|---------|-------|
| 72-150 | Basse | Prévisualisation, brouillons |
| 200-300 | Standard | Impression normale |
| 400-600 | Haute | Impression professionnelle |

**Recommandation:** 300 DPI pour un bon compromis qualité/taille de fichier

### Recouvrement (Overlap)

Le recouvrement permet de faciliter l'assemblage manuel des pages imprimées.

- **0 mm:** Pas de recouvrement (assemblage difficile)
- **5-10 mm:** Recouvrement minimal
- **10-20 mm:** Recouvrement standard (recommandé)
- **20-30 mm:** Recouvrement important (facilite l'assemblage mais augmente le nombre de pages)

### Export GeoTIFF

**Avantages:**
- Conserve la géoréférence exacte
- Peut être réutilisé dans des SIG
- Format standard pour les données géospatiales

**Sortie:**
- Un fichier .tif par page
- Nommage: `page_001.tif`, `page_002.tif`, etc.
- Métadonnées de géoréférence conservées

### Export PDF

**Avantages:**
- Fichier unique multi-pages
- Prêt à imprimer directement
- Compact et facile à partager

**Sortie:**
- Un fichier .pdf contenant toutes les pages
- Numéro de page sur chaque feuille
- Taille adaptée au format choisi

**Note:** Le PDF ne conserve pas la géoréférence

## Cas d'usage

### 1. Impression d'une carte topographique

**Contexte:** Vous avez une carte topographique IGN en GeoTIFF et voulez l'imprimer sur plusieurs pages A4.

**Procédure:**
1. Chargez le fichier GeoTIFF
2. Sélectionnez la zone d'intérêt
3. Configurez: A4, Portrait, 300 DPI, 10 mm overlap
4. Exportez en PDF
5. Imprimez le PDF
6. Assemblez les pages en suivant le recouvrement

### 2. Préparation de dalles pour un SIG

**Contexte:** Vous voulez découper une grande image en dalles géoréférencées pour un SIG.

**Procédure:**
1. Chargez vos images
2. Sélectionnez toute la zone ou une région
3. Configurez les paramètres selon vos besoins
4. Exportez en GeoTIFF
5. Importez les dalles dans votre SIG

### 3. Création d'un atlas papier

**Contexte:** Créer un atlas avec plusieurs pages de cartes.

**Procédure:**
1. Chargez vos images de base
2. Pour chaque région:
   - Sélectionnez la zone
   - Exportez en PDF
3. Combinez les PDF en un seul document
4. Ajoutez une page de titre et un index

## FAQ

### Comment charger plusieurs images en même temps?

Placez tous vos fichiers GeoTIFF dans un seul dossier, puis chargez ce dossier. L'application créera automatiquement une mosaïque.

### Mes images ne se chargent pas, pourquoi?

Vérifiez que:
- Les fichiers ont l'extension .tif ou .tiff
- Les fichiers sont des GeoTIFF valides (avec géoréférence)
- Vous avez les droits de lecture sur les fichiers

### Comment savoir combien de pages seront générées?

Après avoir sélectionné une zone, regardez "Info découpage" dans le panneau de gauche. Vous verrez le nombre de pages et la grille (ex: 3 x 2 = 6 pages).

### Puis-je modifier la sélection?

Oui, refaites une sélection (Ctrl + Cliquer-glisser). La nouvelle sélection remplace l'ancienne.

### Comment annuler une sélection?

Cliquez sur "🗑️ Effacer sélection" dans le panneau de gauche.

### Le PDF est-il géoréférencé?

Non, seuls les GeoTIFF exportés conservent la géoréférence. Le PDF est optimisé pour l'impression.

### Quelle est la taille maximale d'image supportée?

Cela dépend de votre mémoire RAM. Pour de très grandes images (>10 GB), il peut être nécessaire de les prétraiter.

### Comment assembler les pages imprimées?

1. Imprimez toutes les pages
2. Découpez les bords selon le recouvrement
3. Alignez les pages en superposant les zones de recouvrement
4. Collez ou scotchez les pages ensemble

## Dépannage

### Problème: "No module named 'rasterio'"

**Solution:**
```bash
pip install rasterio
```

Si cela échoue, installez GDAL d'abord (voir section Installation).

### Problème: "ImportError: DLL load failed" (Windows)

**Solution:**
Installez GDAL avec conda:
```bash
conda install -c conda-forge gdal rasterio
```

### Problème: L'application est lente

**Solutions possibles:**
- Réduisez la zone de sélection
- Diminuez le DPI
- Fermez d'autres applications
- Utilisez moins d'images sources

### Problème: Erreur de mémoire

**Solutions:**
- Augmentez la RAM disponible
- Traitez les images par portions
- Réduisez la résolution des images sources

### Problème: Les couleurs sont étranges

C'est normal pour certaines images (infrarouge, etc.). L'application utilise les 3 premières bandes comme RGB. Pour de meilleures couleurs, préparez vos images avec les bonnes bandes.

### Problème: Le PDF est trop volumineux

**Solutions:**
- Réduisez le DPI (essayez 200 au lieu de 300)
- Réduisez la taille de la sélection
- Exportez en GeoTIFF et convertissez en PDF avec compression

### Besoin d'aide supplémentaire?

Créez une issue sur le dépôt GitHub avec:
- Description du problème
- Message d'erreur exact
- Version de Python
- Système d'exploitation
- Captures d'écran si pertinent

## Conseils et astuces

### Optimiser la qualité d'impression

1. Utilisez 300 DPI minimum
2. Vérifiez la résolution de vos images sources
3. Utilisez un recouvrement de 10-15 mm

### Économiser du papier

1. Optimisez votre sélection pour éviter les pages partiellement vides
2. Utilisez le format de papier le plus adapté
3. Vérifiez le nombre de pages avant d'exporter

### Gagner du temps

1. Préparez vos images GeoTIFF à l'avance
2. Testez avec un petit DPI d'abord (150)
3. Utilisez des raccourcis clavier (quand disponibles)

### Meilleurs résultats

1. Utilisez des images de bonne qualité
2. Assurez-vous que les images sont correctement géoréférencées
3. Testez avec une petite zone d'abord

---

**Version du guide:** 1.0.0  
**Dernière mise à jour:** 2026  
**Application:** MapsCut
