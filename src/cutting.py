"""
Module de découpage
Gère le découpage des images en pages pour l'impression
"""

import math
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class PageInfo:
    """Informations sur une page découpée"""
    page_number: int
    x_start_px: int
    y_start_px: int
    x_end_px: int
    y_end_px: int
    width_px: int
    height_px: int
    row: int
    col: int


class PageCutter:
    """Classe pour découper une image en pages imprimables"""
    
    # Formats de papier en mm (largeur x hauteur en portrait)
    PAPER_FORMATS = {
        'A4': (210, 297),
        'A3': (297, 420),
        'A2': (420, 594),
        'A1': (594, 841),
        'A0': (841, 1189),
        'Letter': (216, 279),
        'Legal': (216, 356),
        'Tabloid': (279, 432),
    }
    
    def __init__(self):
        self.paper_format = 'A4'
        self.orientation = 'portrait'  # 'portrait' ou 'landscape'
        self.dpi = 300
        self.overlap_mm = 10
        self.pages = []
        
    def set_paper_format(self, format_name: str):
        """
        Définit le format de papier
        
        Args:
            format_name: Nom du format (A4, A3, etc.)
            
        Raises:
            ValueError: Si le format n'est pas reconnu
        """
        if format_name not in self.PAPER_FORMATS:
            raise ValueError(f"Format {format_name} non reconnu. Formats disponibles: {list(self.PAPER_FORMATS.keys())}")
        self.paper_format = format_name
        
    def set_orientation(self, orientation: str):
        """
        Définit l'orientation du papier
        
        Args:
            orientation: 'portrait' ou 'landscape'
            
        Raises:
            ValueError: Si l'orientation n'est pas valide
        """
        if orientation not in ['portrait', 'landscape']:
            raise ValueError("L'orientation doit être 'portrait' ou 'landscape'")
        self.orientation = orientation
        
    def set_dpi(self, dpi: int):
        """
        Définit la résolution DPI
        
        Args:
            dpi: Résolution en DPI (points par pouce)
            
        Raises:
            ValueError: Si le DPI est invalide
        """
        if dpi <= 0:
            raise ValueError("Le DPI doit être positif")
        self.dpi = dpi
        
    def set_overlap(self, overlap_mm: float):
        """
        Définit le recouvrement entre les pages
        
        Args:
            overlap_mm: Recouvrement en millimètres
            
        Raises:
            ValueError: Si le recouvrement est négatif
        """
        if overlap_mm < 0:
            raise ValueError("Le recouvrement ne peut pas être négatif")
        self.overlap_mm = overlap_mm
        
    def get_page_size_px(self) -> Tuple[int, int]:
        """
        Calcule la taille d'une page en pixels
        
        Returns:
            Tuple (largeur_px, hauteur_px)
        """
        # Récupérer les dimensions du papier en mm
        width_mm, height_mm = self.PAPER_FORMATS[self.paper_format]
        
        # Inverser si paysage
        if self.orientation == 'landscape':
            width_mm, height_mm = height_mm, width_mm
            
        # Convertir mm en pouces (1 pouce = 25.4 mm)
        width_inch = width_mm / 25.4
        height_inch = height_mm / 25.4
        
        # Convertir en pixels
        width_px = int(width_inch * self.dpi)
        height_px = int(height_inch * self.dpi)
        
        return width_px, height_px
        
    def get_overlap_px(self) -> int:
        """
        Calcule le recouvrement en pixels
        
        Returns:
            Recouvrement en pixels
        """
        # Convertir mm en pouces puis en pixels
        overlap_inch = self.overlap_mm / 25.4
        overlap_px = int(overlap_inch * self.dpi)
        return overlap_px
        
    def calculate_pages(self, region_width_px: int, region_height_px: int) -> List[PageInfo]:
        """
        Calcule le découpage en pages pour une région donnée
        
        Args:
            region_width_px: Largeur de la région en pixels
            region_height_px: Hauteur de la région en pixels
            
        Returns:
            Liste des informations de page
            
        Raises:
            ValueError: Si les dimensions sont invalides
        """
        if region_width_px <= 0 or region_height_px <= 0:
            raise ValueError("Les dimensions doivent être positives")
            
        # Taille d'une page en pixels
        page_width_px, page_height_px = self.get_page_size_px()
        
        # Recouvrement en pixels
        overlap_px = self.get_overlap_px()
        
        # Taille effective d'une page (en retirant le recouvrement)
        effective_width_px = page_width_px - overlap_px
        effective_height_px = page_height_px - overlap_px
        
        if effective_width_px <= 0 or effective_height_px <= 0:
            raise ValueError("Le recouvrement est trop grand par rapport à la taille de la page")
            
        # Calculer le nombre de pages nécessaires
        num_cols = math.ceil(region_width_px / effective_width_px)
        num_rows = math.ceil(region_height_px / effective_height_px)
        
        # Générer les informations pour chaque page
        pages = []
        page_number = 1
        
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculer les coordonnées de début
                x_start = col * effective_width_px
                y_start = row * effective_height_px
                
                # Calculer les coordonnées de fin
                x_end = min(x_start + page_width_px, region_width_px)
                y_end = min(y_start + page_height_px, region_height_px)
                
                # Créer les informations de page
                page = PageInfo(
                    page_number=page_number,
                    x_start_px=x_start,
                    y_start_px=y_start,
                    x_end_px=x_end,
                    y_end_px=y_end,
                    width_px=x_end - x_start,
                    height_px=y_end - y_start,
                    row=row,
                    col=col
                )
                
                pages.append(page)
                page_number += 1
                
        self.pages = pages
        return pages
        
    def get_grid_info(self) -> Dict[str, int]:
        """
        Retourne des informations sur la grille de découpage
        
        Returns:
            Dictionnaire avec le nombre de lignes et colonnes
        """
        if not self.pages:
            return {'rows': 0, 'cols': 0, 'total': 0}
            
        max_row = max(p.row for p in self.pages)
        max_col = max(p.col for p in self.pages)
        
        return {
            'rows': max_row + 1,
            'cols': max_col + 1,
            'total': len(self.pages)
        }
        
    def get_page_info_text(self) -> str:
        """
        Génère un texte descriptif du découpage
        
        Returns:
            Texte descriptif
        """
        if not self.pages:
            return "Aucune page calculée"
            
        grid_info = self.get_grid_info()
        page_width_px, page_height_px = self.get_page_size_px()
        overlap_px = self.get_overlap_px()
        
        text = f"Format: {self.paper_format} ({self.orientation})\n"
        text += f"DPI: {self.dpi}\n"
        text += f"Taille page: {page_width_px} x {page_height_px} px\n"
        text += f"Recouvrement: {self.overlap_mm} mm ({overlap_px} px)\n"
        text += f"Grille: {grid_info['rows']} x {grid_info['cols']} = {grid_info['total']} pages"
        
        return text
