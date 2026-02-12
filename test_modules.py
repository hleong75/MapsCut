#!/usr/bin/env python3
"""
Script de test pour vérifier les modules MapsCut
"""

import sys
import traceback


def test_imports():
    """Test des imports de modules"""
    print("=== Test des imports ===")
    
    try:
        print("Import de numpy...", end=" ")
        import numpy as np
        print(f"✓ (version {np.__version__})")
    except ImportError as e:
        print(f"✗ {e}")
        return False
    
    try:
        print("Import de PyQt6...", end=" ")
        from PyQt6.QtWidgets import QApplication
        print("✓")
    except ImportError as e:
        print(f"✗ {e}")
        return False
        
    try:
        print("Import de rasterio...", end=" ")
        import rasterio
        print(f"✓ (version {rasterio.__version__})")
    except ImportError as e:
        print(f"✗ {e}")
        return False
        
    try:
        print("Import de PIL...", end=" ")
        from PIL import Image
        print("✓")
    except ImportError as e:
        print(f"✗ {e}")
        return False
        
    try:
        print("Import de reportlab...", end=" ")
        from reportlab.pdfgen import canvas
        print("✓")
    except ImportError as e:
        print(f"✗ {e}")
        return False
        
    return True


def test_modules():
    """Test des modules MapsCut"""
    print("\n=== Test des modules MapsCut ===")
    
    try:
        print("Import du module raster_processing...", end=" ")
        from src.raster_processing import RasterProcessor
        print("✓")
        
        print("Import du module cutting...", end=" ")
        from src.cutting import PageCutter
        print("✓")
        
        print("Import du module export...", end=" ")
        from src.export import Exporter
        print("✓")
        
        print("Import du module interface...", end=" ")
        from src.interface import MainWindow
        print("✓")
        
    except ImportError as e:
        print(f"✗ {e}")
        traceback.print_exc()
        return False
        
    return True


def test_cutting_module():
    """Test du module de découpage"""
    print("\n=== Test du module cutting ===")
    
    try:
        from src.cutting import PageCutter
        
        cutter = PageCutter()
        print(f"Format par défaut: {cutter.paper_format}")
        print(f"Orientation par défaut: {cutter.orientation}")
        print(f"DPI par défaut: {cutter.dpi}")
        print(f"Overlap par défaut: {cutter.overlap_mm} mm")
        
        # Test de calcul de pages
        cutter.set_paper_format('A4')
        cutter.set_orientation('portrait')
        cutter.set_dpi(300)
        cutter.set_overlap(10)
        
        # Taille de page en pixels
        page_w, page_h = cutter.get_page_size_px()
        print(f"\nTaille page A4 à 300 DPI: {page_w} x {page_h} px")
        
        # Calculer des pages pour une région de test
        pages = cutter.calculate_pages(5000, 3000)
        grid_info = cutter.get_grid_info()
        print(f"Pages calculées pour 5000x3000 px: {grid_info['total']} pages ({grid_info['rows']}x{grid_info['cols']})")
        
        print("✓ Module cutting fonctionne correctement")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        traceback.print_exc()
        return False


def test_raster_module():
    """Test du module raster (sans fichiers)"""
    print("\n=== Test du module raster_processing ===")
    
    try:
        from src.raster_processing import RasterProcessor
        import numpy as np
        
        processor = RasterProcessor()
        print("RasterProcessor créé")
        
        # Test de normalisation
        test_data = np.random.randint(0, 1000, (100, 100))
        normalized = processor.normalize_for_display(test_data)
        print(f"Normalisation testée: {normalized.min()}-{normalized.max()}")
        
        print("✓ Module raster_processing fonctionne correctement")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    print("MapsCut - Tests des modules\n")
    
    all_ok = True
    
    # Test des imports
    if not test_imports():
        print("\n⚠️  Certaines dépendances ne sont pas installées.")
        print("Installez-les avec: pip install -r requirements.txt")
        all_ok = False
    
    # Test des modules
    if not test_modules():
        print("\n✗ Erreur lors de l'import des modules MapsCut")
        all_ok = False
    else:
        # Tests fonctionnels
        if not test_cutting_module():
            all_ok = False
            
        if not test_raster_module():
            all_ok = False
    
    print("\n" + "="*50)
    if all_ok:
        print("✓ Tous les tests sont passés avec succès!")
        return 0
    else:
        print("✗ Certains tests ont échoué")
        return 1


if __name__ == '__main__':
    sys.exit(main())
