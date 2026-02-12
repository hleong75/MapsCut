"""
Script de validation de la structure du code
Vérifie que tous les fichiers sont présents et bien formés
"""

import os
import ast
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} manquant: {filepath}")
        return False


def check_python_syntax(filepath):
    """Vérifie la syntaxe Python d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"  ✗ Erreur de syntaxe: {e}")
        return False


def check_module_structure():
    """Vérifie la structure des modules"""
    print("=== Vérification de la structure du projet ===\n")
    
    all_ok = True
    
    # Fichiers principaux
    files = {
        'README.md': 'Documentation',
        'requirements.txt': 'Dépendances',
        'main.py': 'Point d\'entrée',
        '.gitignore': 'Git ignore',
        'run_windows.bat': 'Lanceur Windows',
        'run_linux.sh': 'Lanceur Linux',
    }
    
    for file, desc in files.items():
        if not check_file_exists(file, desc):
            all_ok = False
    
    print("\n=== Vérification des modules Python ===\n")
    
    # Modules Python
    modules = {
        'src/__init__.py': 'Package src',
        'src/raster_processing.py': 'Module traitement raster',
        'src/cutting.py': 'Module découpage',
        'src/export.py': 'Module export',
        'src/interface.py': 'Module interface',
    }
    
    for module, desc in modules.items():
        if check_file_exists(module, desc):
            if not check_python_syntax(module):
                all_ok = False
        else:
            all_ok = False
    
    return all_ok


def check_module_content():
    """Vérifie le contenu des modules"""
    print("\n=== Vérification du contenu des modules ===\n")
    
    checks = {
        'src/raster_processing.py': [
            'class RasterProcessor',
            'def load_geotiffs',
            'def create_mosaic',
            'def pixel_to_geo',
            'def geo_to_pixel',
        ],
        'src/cutting.py': [
            'class PageCutter',
            'PAPER_FORMATS',
            'def calculate_pages',
            'def get_page_size_px',
        ],
        'src/export.py': [
            'class Exporter',
            'def export_geotiff',
            'def export_pdf',
        ],
        'src/interface.py': [
            'class MainWindow',
            'class ImageView',
            'def load_folder',
            'def export_geotiff',
            'def export_pdf',
        ],
    }
    
    all_ok = True
    
    for module, expected_content in checks.items():
        print(f"Module {module}:")
        with open(module, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for item in expected_content:
            if item in content:
                print(f"  ✓ {item}")
            else:
                print(f"  ✗ {item} manquant")
                all_ok = False
        print()
    
    return all_ok


def check_documentation():
    """Vérifie la documentation"""
    print("=== Vérification de la documentation ===\n")
    
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    
    sections = [
        '## Fonctionnalités',
        '## Structure du projet',
        '## Installation',
        '## Utilisation',
        '## Architecture modulaire',
    ]
    
    all_ok = True
    for section in sections:
        if section in readme:
            print(f"✓ Section '{section}'")
        else:
            print(f"✗ Section '{section}' manquante")
            all_ok = False
    
    return all_ok


def count_lines_of_code():
    """Compte les lignes de code"""
    print("\n=== Statistiques du code ===\n")
    
    total_lines = 0
    total_code = 0
    total_comments = 0
    
    modules = [
        'main.py',
        'src/__init__.py',
        'src/raster_processing.py',
        'src/cutting.py',
        'src/export.py',
        'src/interface.py',
    ]
    
    for module in modules:
        with open(module, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines += len(lines)
        code = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        comments = sum(1 for line in lines if line.strip().startswith('#'))
        
        total_code += code
        total_comments += comments
        
        print(f"{module:30s}: {len(lines):4d} lignes ({code:4d} code, {comments:3d} commentaires)")
    
    print(f"\n{'Total:':30s}: {total_lines:4d} lignes ({total_code:4d} code, {total_comments:3d} commentaires)")


def main():
    """Fonction principale"""
    print("MapsCut - Validation de la structure du projet\n")
    print("="*60 + "\n")
    
    all_ok = True
    
    if not check_module_structure():
        all_ok = False
    
    if not check_module_content():
        all_ok = False
    
    if not check_documentation():
        all_ok = False
    
    count_lines_of_code()
    
    print("\n" + "="*60)
    if all_ok:
        print("✓ Tous les contrôles sont passés avec succès!")
        print("\nLe projet est correctement structuré et prêt à être utilisé.")
        print("\nProchaines étapes:")
        print("1. Installer les dépendances: pip install -r requirements.txt")
        print("2. Lancer l'application: python main.py")
        return 0
    else:
        print("✗ Certains contrôles ont échoué")
        return 1


if __name__ == '__main__':
    sys.exit(main())
