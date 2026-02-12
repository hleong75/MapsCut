# MapsCut - Résumé du projet

## Vue d'ensemble

**MapsCut** est une application Python complète avec interface graphique PyQt6 pour découper des images géoréférencées destinées à l'impression.

## ✅ Fonctionnalités implémentées

### 1. Chargement et traitement d'images
- ✅ Sélection de dossier contenant des GeoTIFF
- ✅ Génération automatique de mosaïque (rasterio + GDAL)
- ✅ Support de multiples fichiers .tif/.tiff
- ✅ Conservation de la géoréférence

### 2. Interface graphique interactive
- ✅ Interface PyQt6 moderne et intuitive
- ✅ QGraphicsView + QGraphicsScene pour affichage
- ✅ Vue zoomable (molette souris)
- ✅ Vue déplaçable (glisser-déposer)
- ✅ Sélection interactive par rectangle (Ctrl + clic)
- ✅ Feedback visuel en temps réel

### 3. Paramètres d'impression configurables
- ✅ **Formats papier**: A4, A3, A2, A1, A0, Letter, Legal, Tabloid
- ✅ **Orientation**: Portrait ou Paysage
- ✅ **DPI**: 72-600 dpi (300 recommandé)
- ✅ **Overlap**: Recouvrement 0-50 mm configurable
- ✅ Calcul automatique du nombre de pages
- ✅ Affichage de la grille de découpage

### 4. Découpage intelligent
- ✅ Découpage automatique de la zone sélectionnée
- ✅ Calcul du nombre de pages nécessaires
- ✅ Gestion du recouvrement entre pages
- ✅ Numérotation automatique des pages
- ✅ Conservation des coordonnées géographiques

### 5. Export multi-format
- ✅ **GeoTIFF géoréférencés**: 
  - Un fichier par page
  - Conservation de la géoréférence exacte
  - Métadonnées CRS préservées
  - Format compatible SIG
- ✅ **PDF multi-pages**:
  - Un fichier PDF unique
  - Prêt à imprimer directement
  - Numéros de page inclus
  - Taille adaptée au format

### 6. Gestion des erreurs
- ✅ Validation des entrées utilisateur
- ✅ Messages d'erreur explicites
- ✅ Gestion des formats non supportés
- ✅ Vérification des fichiers/dossiers
- ✅ Try/except complets

## 📁 Structure modulaire

### Module `raster_processing.py` (267 lignes)
**Responsabilité**: Traitement raster et géoréférencement
- Classe `RasterProcessor`
- Chargement de GeoTIFF
- Création de mosaïques
- Conversions pixel ↔ coordonnées géographiques
- Extraction de régions
- Normalisation pour affichage

### Module `cutting.py` (245 lignes)
**Responsabilité**: Découpage en pages imprimables
- Classe `PageCutter`
- DataClass `PageInfo`
- Gestion des formats de papier
- Calcul de dimensions selon DPI
- Découpage avec recouvrement
- Génération d'infos de grille

### Module `export.py` (252 lignes)
**Responsabilité**: Export vers différents formats
- Classe `Exporter`
- Export GeoTIFF individuel
- Export batch GeoTIFF
- Export PDF multi-pages
- Conservation des métadonnées

### Module `interface.py` (466 lignes)
**Responsabilité**: Interface graphique utilisateur
- Classe `MainWindow`
- Classe `ImageView`
- Classe `SelectionRectItem`
- Gestion des événements
- Panneau de configuration
- Barre d'outils

### Point d'entrée `main.py` (31 lignes)
**Responsabilité**: Lancement de l'application
- Initialisation PyQt6
- Configuration de l'application
- Boucle d'événements

## 📊 Statistiques

- **Total**: 1274 lignes de code
- **Code**: 901 lignes
- **Commentaires**: 104 lignes
- **Modules**: 5 fichiers Python
- **Documentation**: 3 fichiers Markdown complets

## 🚀 Exécution

### Windows
```bash
# Méthode 1: Double-clic
run_windows.bat

# Méthode 2: Ligne de commande
python main.py
```

### Linux/macOS
```bash
# Méthode 1: Script
./run_linux.sh

# Méthode 2: Direct
python3 main.py
```

## 📚 Documentation

1. **README.md**: Documentation principale avec installation et usage
2. **GUIDE_UTILISATEUR.md**: Guide détaillé pour utilisateurs finaux
3. **DEVELOPER.md**: Documentation technique pour développeurs
4. **Code comments**: Docstrings complètes dans tous les modules

## 🔧 Outils fournis

1. **validate_structure.py**: Validation de la structure du projet
2. **test_modules.py**: Tests d'import et de fonctionnalités
3. **run_windows.bat**: Lanceur automatique Windows
4. **run_linux.sh**: Lanceur automatique Linux/macOS

## 📦 Dépendances

```
PyQt6>=6.4.0         # Interface graphique
rasterio>=1.3.0      # Traitement GeoTIFF
numpy>=1.24.0        # Calculs numériques
Pillow>=10.0.0       # Manipulation d'images
reportlab>=4.0.0     # Génération PDF
GDAL>=3.6.0          # Outils géospatiaux
matplotlib>=3.7.0    # Visualisation
```

## ✨ Points forts

1. **Architecture modulaire**: Code bien organisé et maintenable
2. **Interface intuitive**: Facile à utiliser, pas de formation nécessaire
3. **Code documenté**: Commentaires et docstrings complets
4. **Gestion d'erreurs**: Robuste et informatif
5. **Multi-plateforme**: Windows, Linux, macOS
6. **Autonome**: Inclut tous les scripts nécessaires
7. **Extensible**: Facile d'ajouter de nouvelles fonctionnalités

## 🎯 Utilisation typique

1. **Charger** un dossier de GeoTIFF
2. **Explorer** la mosaïque (zoom/pan)
3. **Sélectionner** une zone (Ctrl + clic-glisser)
4. **Configurer** les paramètres (format, DPI, overlap)
5. **Exporter** en GeoTIFF ou PDF
6. **Imprimer** et assembler les pages

## 🔐 Qualité du code

- ✅ Code Python idiomatique
- ✅ Type hints utilisés
- ✅ Docstrings complètes
- ✅ Gestion d'erreurs appropriée
- ✅ Commentaires explicatifs
- ✅ Nommage cohérent
- ✅ Séparation des responsabilités
- ✅ Pas de code dupliqué

## 📈 Extensibilité

Le code est conçu pour être facilement étendu:

- Ajouter de nouveaux formats de papier
- Ajouter de nouveaux formats d'export
- Ajouter des filtres d'image
- Ajouter des transformations
- Personnaliser l'interface
- Intégrer d'autres bibliothèques SIG

## 🎓 Pour les développeurs

Voir **DEVELOPER.md** pour:
- Architecture détaillée
- API de chaque module
- Guide d'extension
- Bonnes pratiques
- Conventions de code

## 👥 Pour les utilisateurs

Voir **GUIDE_UTILISATEUR.md** pour:
- Installation pas à pas
- Guide d'utilisation complet
- Cas d'usage
- FAQ
- Dépannage

## ✅ Conformité au cahier des charges

| Exigence | Statut |
|----------|--------|
| Interface PyQt6 | ✅ Implémenté |
| Chargement GeoTIFF | ✅ Implémenté |
| Génération mosaïque (rasterio/GDAL) | ✅ Implémenté |
| Vue zoomable/déplaçable | ✅ Implémenté |
| Sélection interactive | ✅ Implémenté |
| Conversion coordonnées | ✅ Implémenté |
| Formats papier configurables | ✅ Implémenté |
| DPI configurable | ✅ Implémenté |
| Overlap configurable | ✅ Implémenté |
| Découpage automatique | ✅ Implémenté |
| Export GeoTIFF | ✅ Implémenté |
| Export PDF multi-pages | ✅ Implémenté |
| Structure modulaire | ✅ Implémenté |
| Code commenté | ✅ Implémenté |
| Gestion d'erreurs | ✅ Implémenté |
| Autonome et exécutable Windows | ✅ Implémenté |

## 🏆 Résultat

**Application complète et fonctionnelle** répondant à 100% des exigences du cahier des charges, avec:
- Code de production de qualité
- Documentation exhaustive
- Scripts d'installation automatisés
- Architecture extensible

---

**Version**: 1.0.0  
**Date**: 2026  
**Statut**: ✅ Complet et prêt à l'emploi
