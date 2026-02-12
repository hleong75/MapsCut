# Documentation Développeur - MapsCut

## Table des matières
1. [Architecture](#architecture)
2. [Structure du code](#structure-du-code)
3. [Modules détaillés](#modules-détaillés)
4. [Extension de l'application](#extension-de-lapplication)
5. [Bonnes pratiques](#bonnes-pratiques)

## Architecture

### Vue d'ensemble

MapsCut suit une architecture modulaire en 4 couches:

```
┌─────────────────────────────────────┐
│      Interface (interface.py)       │  ← Couche présentation
├─────────────────────────────────────┤
│  Cutting (cutting.py)                │  ← Couche logique métier
│  Export (export.py)                  │
├─────────────────────────────────────┤
│  Raster (raster_processing.py)      │  ← Couche accès données
├─────────────────────────────────────┤
│  Bibliothèques (rasterio, PyQt6)    │  ← Couche infrastructure
└─────────────────────────────────────┘
```

### Principes de conception

1. **Séparation des responsabilités**: Chaque module a une responsabilité unique
2. **Découplage**: Les modules communiquent via des interfaces claires
3. **Réutilisabilité**: Les classes peuvent être utilisées indépendamment
4. **Extensibilité**: Facile d'ajouter de nouvelles fonctionnalités

## Structure du code

### Arborescence

```
MapsCut/
├── src/                        # Code source principal
│   ├── __init__.py            # Package principal
│   ├── raster_processing.py   # Traitement raster
│   ├── cutting.py             # Découpage en pages
│   ├── export.py              # Export GeoTIFF/PDF
│   └── interface.py           # Interface PyQt6
├── main.py                    # Point d'entrée
├── requirements.txt           # Dépendances
├── README.md                  # Documentation principale
├── GUIDE_UTILISATEUR.md       # Guide utilisateur
├── run_windows.bat            # Lanceur Windows
├── run_linux.sh               # Lanceur Linux
├── validate_structure.py      # Script de validation
└── .gitignore                # Fichiers ignorés
```

### Dépendances

```
PyQt6        → Interface graphique
rasterio     → Lecture/écriture GeoTIFF
numpy        → Calculs numériques
Pillow       → Manipulation d'images
reportlab    → Génération PDF
GDAL         → Opérations géospatiales
```

## Modules détaillés

### 1. raster_processing.py

**Responsabilité**: Gestion des opérations sur les rasters géoréférencés

#### Classe: RasterProcessor

**Attributs principaux:**
```python
mosaic_data: np.ndarray        # Données de la mosaïque
mosaic_transform: Affine       # Transformation géographique
mosaic_crs: CRS               # Système de coordonnées
mosaic_bounds: tuple          # Limites géographiques
source_files: List[str]       # Fichiers sources
```

**Méthodes principales:**

```python
def load_geotiffs(folder_path: str) -> List[str]:
    """Charge tous les GeoTIFF d'un dossier"""
    
def create_mosaic(file_paths: List[str]) -> Tuple[np.ndarray, dict]:
    """Crée une mosaïque à partir de plusieurs fichiers"""
    
def get_rgb_array() -> np.ndarray:
    """Convertit la mosaïque en tableau RGB pour affichage"""
    
def pixel_to_geo(pixel_x: int, pixel_y: int) -> Tuple[float, float]:
    """Convertit coordonnées pixel → géographiques"""
    
def geo_to_pixel(geo_x: float, geo_y: float) -> Tuple[int, int]:
    """Convertit coordonnées géographiques → pixel"""
    
def extract_region(x1, y1, x2, y2) -> Tuple[np.ndarray, dict]:
    """Extrait une région de la mosaïque"""
```

**Utilisation:**
```python
processor = RasterProcessor()
files = processor.load_geotiffs("/path/to/folder")
mosaic, meta = processor.create_mosaic()
rgb = processor.get_rgb_array()
```

### 2. cutting.py

**Responsabilité**: Calcul du découpage en pages imprimables

#### Classe: PageCutter

**Attributs principaux:**
```python
paper_format: str             # Format papier (A4, A3, etc.)
orientation: str              # Portrait ou landscape
dpi: int                     # Résolution
overlap_mm: float            # Recouvrement en mm
pages: List[PageInfo]        # Liste des pages calculées
```

**Méthodes principales:**

```python
def set_paper_format(format_name: str):
    """Définit le format de papier"""
    
def set_orientation(orientation: str):
    """Définit l'orientation"""
    
def set_dpi(dpi: int):
    """Définit la résolution"""
    
def set_overlap(overlap_mm: float):
    """Définit le recouvrement"""
    
def get_page_size_px() -> Tuple[int, int]:
    """Calcule la taille d'une page en pixels"""
    
def calculate_pages(region_width_px, region_height_px) -> List[PageInfo]:
    """Calcule les pages nécessaires"""
    
def get_grid_info() -> Dict[str, int]:
    """Retourne infos sur la grille (rows, cols, total)"""
```

**Utilisation:**
```python
cutter = PageCutter()
cutter.set_paper_format('A4')
cutter.set_dpi(300)
pages = cutter.calculate_pages(5000, 3000)
```

#### DataClass: PageInfo

```python
@dataclass
class PageInfo:
    page_number: int          # Numéro de page
    x_start_px: int          # Début X (pixels)
    y_start_px: int          # Début Y (pixels)
    x_end_px: int            # Fin X (pixels)
    y_end_px: int            # Fin Y (pixels)
    width_px: int            # Largeur (pixels)
    height_px: int           # Hauteur (pixels)
    row: int                 # Ligne dans la grille
    col: int                 # Colonne dans la grille
```

### 3. export.py

**Responsabilité**: Export des pages en GeoTIFF et PDF

#### Classe: Exporter

**Méthodes principales:**

```python
def set_output_folder(folder_path: str):
    """Définit le dossier de sortie"""
    
def export_geotiff(data, metadata, page_info, base_name) -> str:
    """Exporte une page en GeoTIFF"""
    
def export_all_geotiffs(mosaic_data, mosaic_crs, mosaic_transform,
                       pages, region_offset_x, region_offset_y) -> List[str]:
    """Exporte toutes les pages en GeoTIFF"""
    
def export_pdf(mosaic_data, pages, region_offset_x, region_offset_y,
              paper_format, orientation, output_name) -> str:
    """Exporte toutes les pages en PDF multi-pages"""
```

**Utilisation:**
```python
exporter = Exporter()
exporter.set_output_folder("/output")
files = exporter.export_all_geotiffs(data, crs, transform, pages, 0, 0)
pdf = exporter.export_pdf(data, pages, 0, 0, 'A4', 'portrait')
```

### 4. interface.py

**Responsabilité**: Interface graphique PyQt6

#### Classe: MainWindow

Fenêtre principale de l'application

**Méthodes principales:**
```python
def init_ui():
    """Initialise l'interface"""
    
def load_folder():
    """Charge un dossier de GeoTIFF"""
    
def on_selection_changed(rect):
    """Appelé quand la sélection change"""
    
def update_cutting_info():
    """Met à jour les infos de découpage"""
    
def export_geotiff():
    """Exporte en GeoTIFF"""
    
def export_pdf():
    """Exporte en PDF"""
```

#### Classe: ImageView

Vue graphique interactive

**Méthodes principales:**
```python
def set_image(image_array):
    """Affiche une image"""
    
def wheelEvent(event):
    """Gère le zoom"""
    
def mousePressEvent(event):
    """Début de sélection"""
    
def mouseMoveEvent(event):
    """Mise à jour de sélection"""
    
def mouseReleaseEvent(event):
    """Fin de sélection"""
```

## Extension de l'application

### Ajouter un nouveau format de papier

**Fichier:** `src/cutting.py`

```python
# Dans la classe PageCutter
PAPER_FORMATS = {
    # ... formats existants ...
    'Custom': (largeur_mm, hauteur_mm),  # Nouveau format
}
```

### Ajouter un format d'export

**Créer un nouveau module:** `src/export_custom.py`

```python
from .export import Exporter

class CustomExporter(Exporter):
    def export_custom_format(self, data, pages, ...):
        """Exporte dans un format personnalisé"""
        # Votre code ici
        pass
```

**Intégrer dans l'interface:** `src/interface.py`

```python
# Dans MainWindow.__init__
self.custom_exporter = CustomExporter()

# Ajouter un bouton
self.btn_export_custom = QPushButton("Export Custom")
self.btn_export_custom.clicked.connect(self.export_custom)

def export_custom(self):
    """Exporte dans le format personnalisé"""
    # Votre code ici
```

### Ajouter une transformation d'image

**Fichier:** `src/raster_processing.py`

```python
# Dans la classe RasterProcessor
def apply_transformation(self, transformation_type: str):
    """Applique une transformation à la mosaïque"""
    if transformation_type == 'rotate':
        self.mosaic_data = np.rot90(self.mosaic_data, axes=(1, 2))
    elif transformation_type == 'flip':
        self.mosaic_data = np.flip(self.mosaic_data, axis=1)
    # Etc.
```

### Ajouter des filtres d'image

```python
def apply_filter(self, filter_type: str):
    """Applique un filtre à l'image"""
    if filter_type == 'brightness':
        # Augmenter la luminosité
        self.mosaic_data = np.clip(self.mosaic_data * 1.2, 0, 255)
    elif filter_type == 'contrast':
        # Augmenter le contraste
        # Votre code ici
```

## Bonnes pratiques

### 1. Gestion des erreurs

Toujours utiliser des try/except appropriés:

```python
try:
    result = operation_risquee()
except ValueError as e:
    # Erreur de validation
    logger.error(f"Validation error: {e}")
    raise
except Exception as e:
    # Erreur inattendue
    logger.error(f"Unexpected error: {e}")
    raise RuntimeError(f"Operation failed: {e}")
```

### 2. Documentation

Documenter toutes les fonctions publiques:

```python
def ma_fonction(param1: str, param2: int) -> bool:
    """
    Description courte de la fonction
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description du retour
        
    Raises:
        ValueError: Quand param2 est négatif
    """
    pass
```

### 3. Types hints

Utiliser les type hints pour la clarté:

```python
from typing import List, Tuple, Optional

def process_data(data: np.ndarray, 
                options: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, dict]:
    """..."""
    pass
```

### 4. Tests

Écrire des tests pour les fonctions critiques:

```python
def test_page_calculation():
    """Test du calcul de pages"""
    cutter = PageCutter()
    cutter.set_paper_format('A4')
    cutter.set_dpi(300)
    pages = cutter.calculate_pages(5000, 3000)
    
    assert len(pages) > 0
    assert pages[0].page_number == 1
```

### 5. Gestion de la mémoire

Pour les grandes images:

```python
# Libérer la mémoire après utilisation
del large_array
import gc
gc.collect()
```

### 6. Performance

Utiliser numpy pour les opérations sur les arrays:

```python
# Bon
result = np.where(data > threshold, data, 0)

# Mauvais
result = [[v if v > threshold else 0 for v in row] for row in data]
```

## Workflow de développement

1. **Branching**
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. **Développement**
   - Écrire le code
   - Ajouter des docstrings
   - Ajouter des tests si applicable

3. **Validation**
   ```bash
   python validate_structure.py
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "Description claire du changement"
   ```

5. **Push & Pull Request**
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```

## Conventions de code

### Nommage

- **Classes**: `PascalCase` (ex: `RasterProcessor`)
- **Fonctions/méthodes**: `snake_case` (ex: `load_geotiffs`)
- **Constantes**: `UPPER_CASE` (ex: `PAPER_FORMATS`)
- **Variables privées**: `_prefixe` (ex: `_internal_data`)

### Imports

Ordre des imports:
```python
# 1. Bibliothèque standard
import os
import sys

# 2. Bibliothèques tierces
import numpy as np
from PyQt6.QtWidgets import QMainWindow

# 3. Imports locaux
from .raster_processing import RasterProcessor
```

### Ligne de code

- Maximum 100 caractères par ligne
- Utiliser des continuations pour les longues lignes

## Ressources

### Documentation externe

- **PyQt6**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **rasterio**: https://rasterio.readthedocs.io/
- **numpy**: https://numpy.org/doc/
- **reportlab**: https://www.reportlab.com/docs/

### Outils utiles

- **Black**: Formateur de code Python
- **pylint**: Linter Python
- **mypy**: Vérification des types

---

**Version:** 1.0.0  
**Dernière mise à jour:** 2026
