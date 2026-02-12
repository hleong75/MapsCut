# MapsCut - Architecture visuelle

## Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION MAPSCUT                           │
│                     Point d'entrée: main.py                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    COUCHE INTERFACE (interface.py)                   │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │  MainWindow   │  │   ImageView    │  │ SelectionRectItem   │  │
│  │               │  │                │  │                      │  │
│  │ - Contrôles   │  │ - QGraphicsView│  │ - Rectangle rouge    │  │
│  │ - Paramètres  │  │ - Zoom/Pan     │  │ - Interaction        │  │
│  │ - Export      │  │ - Sélection    │  │                      │  │
│  └───────────────┘  └────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
          │                    │                         │
          ▼                    ▼                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  COUCHE LOGIQUE MÉTIER                               │
│  ┌────────────────────┐              ┌────────────────────────┐    │
│  │  PageCutter        │              │    Exporter            │    │
│  │  (cutting.py)      │              │    (export.py)         │    │
│  │                    │              │                        │    │
│  │ - Formats papier   │              │ - Export GeoTIFF       │    │
│  │ - Calcul pages     │              │ - Export PDF           │    │
│  │ - Grille découpage │              │ - Conservation CRS     │    │
│  │ - Overlap          │              │                        │    │
│  └────────────────────┘              └────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
          │                                        │
          ▼                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│              COUCHE ACCÈS DONNÉES (raster_processing.py)             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    RasterProcessor                            │  │
│  │                                                                │  │
│  │ - load_geotiffs()      : Charge les fichiers                 │  │
│  │ - create_mosaic()      : Crée la mosaïque                     │  │
│  │ - get_rgb_array()      : Convertit pour affichage             │  │
│  │ - pixel_to_geo()       : Conversion pixel → géo               │  │
│  │ - geo_to_pixel()       : Conversion géo → pixel               │  │
│  │ - extract_region()     : Extrait une région                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  COUCHE INFRASTRUCTURE                               │
│  ┌─────────┐  ┌─────────┐  ┌──────┐  ┌─────────┐  ┌──────────┐   │
│  │ PyQt6   │  │rasterio │  │ GDAL │  │  numpy  │  │reportlab │   │
│  │         │  │         │  │      │  │         │  │          │   │
│  │ GUI     │  │ GeoTIFF │  │ GIS  │  │ Calculs │  │   PDF    │   │
│  └─────────┘  └─────────┘  └──────┘  └─────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Flux de données

```
1. CHARGEMENT
   ┌────────────┐
   │ Utilisateur│
   │ sélectionne│──┐
   │  dossier   │  │
   └────────────┘  │
                   ▼
           ┌───────────────┐
           │load_geotiffs()│
           └───────────────┘
                   │
                   ▼
           ┌───────────────┐
           │create_mosaic()│
           └───────────────┘
                   │
                   ▼
           ┌───────────────┐
           │get_rgb_array()│
           └───────────────┘
                   │
                   ▼
           ┌───────────────┐
           │   Affichage   │
           │   dans Vue    │
           └───────────────┘

2. SÉLECTION
   ┌─────────────┐
   │ Ctrl + Clic │
   │   + Glisser │──┐
   └─────────────┘  │
                    ▼
            ┌──────────────┐
            │ Coordonnées  │
            │   rectangle  │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │ Paramètres   │
            │  d'impression│
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │ calculate_   │
            │   pages()    │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │ Affichage    │
            │ info grille  │
            └──────────────┘

3. EXPORT
   ┌──────────────┐
   │ Bouton Export│──┐
   └──────────────┘  │
                     ▼
           ┌──────────────────┐
           │  Export GeoTIFF  │
           │   ou PDF ?       │
           └──────────────────┘
              │            │
              ▼            ▼
     ┌─────────────┐  ┌─────────────┐
     │export_all_  │  │ export_pdf()│
     │geotiffs()   │  │             │
     └─────────────┘  └─────────────┘
              │            │
              ▼            ▼
     ┌─────────────┐  ┌─────────────┐
     │N fichiers   │  │1 fichier    │
     │.tif         │  │.pdf         │
     └─────────────┘  └─────────────┘
```

## Structure des fichiers

```
MapsCut/
├── 📄 Documentation (39 KB total)
│   ├── README.md              (7.7 KB) - Doc principale
│   ├── GUIDE_UTILISATEUR.md   (11 KB)  - Guide utilisateur
│   ├── DEVELOPER.md           (13 KB)  - Doc développeur
│   └── PROJECT_SUMMARY.md     (7.1 KB) - Résumé projet
│
├── 🐍 Code Python (44 KB total)
│   ├── main.py                (0.7 KB) - Point d'entrée
│   └── src/
│       ├── __init__.py        (0.4 KB) - Package
│       ├── raster_processing.py (9.0 KB) - Traitement raster
│       ├── cutting.py         (7.7 KB) - Découpage
│       ├── export.py          (9.1 KB) - Export
│       └── interface.py       (17 KB)  - Interface GUI
│
├── 🔧 Scripts utilitaires (11 KB total)
│   ├── validate_structure.py (5.7 KB) - Validation
│   ├── test_modules.py       (5.0 KB) - Tests
│   ├── run_windows.bat       (1.3 KB) - Lanceur Windows
│   └── run_linux.sh          (1.2 KB) - Lanceur Linux
│
└── 📋 Configuration
    ├── requirements.txt      (0.1 KB) - Dépendances
    └── .gitignore           (0.3 KB) - Git ignore
```

## Interaction utilisateur

```
┌──────────────────────────────────────────────────────────────┐
│                     FENÊTRE PRINCIPALE                        │
│                                                               │
│  ┌──────────────┐  ┌────────────────────────────────────┐   │
│  │   PANNEAU    │  │        VUE IMAGE                   │   │
│  │   CONTRÔLE   │  │                                    │   │
│  │              │  │  ┌──────────────────────────────┐  │   │
│  │ MapsCut      │  │  │                              │  │   │
│  │              │  │  │     Mosaïque GeoTIFF         │  │   │
│  │ [📁 Charger] │  │  │                              │  │   │
│  │              │  │  │  ┌────────────────┐          │  │   │
│  │ Dossier:     │  │  │  │  Sélection     │          │  │   │
│  │ /path/...    │  │  │  │  (rectangle    │          │  │   │
│  │              │  │  │  │   rouge)       │          │  │   │
│  │ Instructions │  │  │  └────────────────┘          │  │   │
│  │ 1. Chargez   │  │  │                              │  │   │
│  │ 2. Ctrl+Clic │  │  │     Molette = Zoom           │  │   │
│  │ 3. Configurez│  │  │     Glisser = Pan            │  │   │
│  │ 4. Exportez  │  │  │                              │  │   │
│  │              │  │  └──────────────────────────────┘  │   │
│  │ ┌──────────┐ │  │                                    │   │
│  │ │Paramètres│ │  └────────────────────────────────────┘   │
│  │ │          │ │                                           │
│  │ │Format: A4│ │                                           │
│  │ │Ori: Port │ │                                           │
│  │ │DPI: 300  │ │                                           │
│  │ │Over: 10mm│ │                                           │
│  │ └──────────┘ │                                           │
│  │              │                                           │
│  │ Info:        │                                           │
│  │ 5000x3000 px │                                           │
│  │ A4 300 DPI   │                                           │
│  │ 3x2 = 6 pages│                                           │
│  │              │                                           │
│  │[💾 GeoTIFF]  │                                           │
│  │[📄 PDF]      │                                           │
│  │[🗑️ Effacer]  │                                           │
│  └──────────────┘                                           │
└──────────────────────────────────────────────────────────────┘
```

## Points clés de l'architecture

### 1. Séparation des responsabilités
- **Interface**: Gère uniquement l'affichage et les interactions
- **Logique métier**: Calculs et découpage
- **Accès données**: Lecture/écriture des rasters

### 2. Communication entre modules
```
Interface → RasterProcessor: Charger/Afficher
Interface → PageCutter: Calculer pages
Interface → Exporter: Exporter résultats
```

### 3. Gestion des données
```
Fichiers GeoTIFF → Mosaïque (numpy array) → Affichage (QImage)
                                          → Export (GeoTIFF/PDF)
```

### 4. Flux de contrôle
```
main.py → MainWindow → ImageView
                    → RasterProcessor
                    → PageCutter
                    → Exporter
```

## Performance et optimisation

### Gestion mémoire
- Utilisation de numpy pour efficacité
- Libération mémoire après traitement
- Normalisation optimisée avec percentiles

### Affichage
- QGraphicsScene pour performance
- Cache d'images pour rapidité
- Zoom/Pan matériel-accéléré

### Calculs
- Vectorisation avec numpy
- Pas de boucles Python inutiles
- Calculs optimisés pour grandes images

---

**Version**: 1.0.0
**Architecture**: Modulaire, extensible, maintenable
