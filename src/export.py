"""
Module d'export
Gère l'export des pages découpées en GeoTIFF et PDF
"""

import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from reportlab.lib.pagesizes import A4, A3, A2, A1, A0, letter, legal
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image
from typing import List, Tuple
from pathlib import Path

from .cutting import PageInfo


class Exporter:
    """Classe pour exporter les pages découpées"""
    
    # Correspondance entre noms de formats et tailles ReportLab
    REPORTLAB_FORMATS = {
        'A4': A4,
        'A3': A3,
        'A2': A2,
        'A1': A1,
        'A0': A0,
        'Letter': letter,
        'Legal': legal,
    }
    
    def __init__(self):
        self.output_folder = None
        
    def set_output_folder(self, folder_path: str):
        """
        Définit le dossier de sortie
        
        Args:
            folder_path: Chemin du dossier de sortie
        """
        self.output_folder = Path(folder_path)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
    def export_geotiff(self, data: np.ndarray, metadata: dict, 
                      page_info: PageInfo, base_name: str = "page") -> str:
        """
        Exporte une page en GeoTIFF
        
        Args:
            data: Données raster
            metadata: Métadonnées incluant CRS et transform
            page_info: Informations sur la page
            base_name: Nom de base pour le fichier
            
        Returns:
            Chemin du fichier créé
            
        Raises:
            ValueError: Si le dossier de sortie n'est pas défini
        """
        if self.output_folder is None:
            raise ValueError("Le dossier de sortie n'est pas défini")
            
        # Créer le nom de fichier
        filename = f"{base_name}_page_{page_info.page_number:03d}.tif"
        output_path = self.output_folder / filename
        
        # Écrire le fichier GeoTIFF
        with rasterio.open(output_path, 'w', **metadata) as dst:
            dst.write(data)
            
        return str(output_path)
        
    def export_all_geotiffs(self, mosaic_data: np.ndarray, mosaic_crs,
                           mosaic_transform, pages: List[PageInfo],
                           region_offset_x: int = 0, region_offset_y: int = 0,
                           base_name: str = "page") -> List[str]:
        """
        Exporte toutes les pages en GeoTIFF
        
        Args:
            mosaic_data: Données de la mosaïque complète
            mosaic_crs: CRS de la mosaïque
            mosaic_transform: Transformation de la mosaïque
            pages: Liste des pages à exporter
            region_offset_x: Décalage X de la région dans la mosaïque
            region_offset_y: Décalage Y de la région dans la mosaïque
            base_name: Nom de base pour les fichiers
            
        Returns:
            Liste des chemins des fichiers créés
        """
        if self.output_folder is None:
            raise ValueError("Le dossier de sortie n'est pas défini")
            
        exported_files = []
        
        for page in pages:
            # Calculer les coordonnées absolues dans la mosaïque
            abs_x_start = region_offset_x + page.x_start_px
            abs_y_start = region_offset_y + page.y_start_px
            abs_x_end = region_offset_x + page.x_end_px
            abs_y_end = region_offset_y + page.y_end_px
            
            # Extraire les données de la page
            page_data = mosaic_data[:, abs_y_start:abs_y_end, abs_x_start:abs_x_end]
            
            # Calculer la transformation pour cette page
            geo_x, geo_y = rasterio.transform.xy(mosaic_transform, abs_y_start, abs_x_start)
            res_x = mosaic_transform.a
            res_y = mosaic_transform.e
            
            page_transform = rasterio.transform.from_origin(
                geo_x, geo_y, abs(res_x), abs(res_y)
            )
            
            # Créer les métadonnées
            metadata = {
                'driver': 'GTiff',
                'height': page_data.shape[1],
                'width': page_data.shape[2],
                'count': page_data.shape[0],
                'dtype': page_data.dtype,
                'crs': mosaic_crs,
                'transform': page_transform,
                'compress': 'lzw'
            }
            
            # Exporter la page
            output_path = self.export_geotiff(page_data, metadata, page, base_name)
            exported_files.append(output_path)
            
        return exported_files
        
    def export_pdf(self, mosaic_data: np.ndarray, pages: List[PageInfo],
                   region_offset_x: int, region_offset_y: int,
                   paper_format: str, orientation: str,
                   output_name: str = "output.pdf") -> str:
        """
        Exporte toutes les pages en PDF multi-pages
        
        Args:
            mosaic_data: Données de la mosaïque complète
            pages: Liste des pages à exporter
            region_offset_x: Décalage X de la région dans la mosaïque
            region_offset_y: Décalage Y de la région dans la mosaïque
            paper_format: Format de papier
            orientation: Orientation ('portrait' ou 'landscape')
            output_name: Nom du fichier PDF
            
        Returns:
            Chemin du fichier PDF créé
            
        Raises:
            ValueError: Si le dossier de sortie n'est pas défini ou format invalide
        """
        if self.output_folder is None:
            raise ValueError("Le dossier de sortie n'est pas défini")
            
        if paper_format not in self.REPORTLAB_FORMATS:
            raise ValueError(f"Format {paper_format} non reconnu")
            
        output_path = self.output_folder / output_name
        
        # Obtenir la taille de page
        page_size = self.REPORTLAB_FORMATS[paper_format]
        if orientation == 'landscape':
            page_size = (page_size[1], page_size[0])
            
        # Créer le canvas PDF
        c = canvas.Canvas(str(output_path), pagesize=page_size)
        
        # Convertir les données en RGB si nécessaire
        if mosaic_data.shape[0] >= 3:
            rgb_data = np.dstack((mosaic_data[0], mosaic_data[1], mosaic_data[2]))
        elif mosaic_data.shape[0] == 1:
            rgb_data = np.dstack((mosaic_data[0], mosaic_data[0], mosaic_data[0]))
        else:
            raise ValueError("Format de données non supporté")
            
        # Normaliser pour l'affichage
        rgb_normalized = self._normalize_for_display(rgb_data).astype(np.uint8)
        
        # Créer un dossier temporaire pour les images
        temp_folder = self.output_folder / "temp_pdf_images"
        temp_folder.mkdir(exist_ok=True)
        
        try:
            for page in pages:
                # Calculer les coordonnées absolues
                abs_x_start = region_offset_x + page.x_start_px
                abs_y_start = region_offset_y + page.y_start_px
                abs_x_end = region_offset_x + page.x_end_px
                abs_y_end = region_offset_y + page.y_end_px
                
                # Extraire les données de la page
                page_rgb = rgb_normalized[abs_y_start:abs_y_end, abs_x_start:abs_x_end, :]
                
                # Créer une image PIL
                img = Image.fromarray(page_rgb, mode='RGB')
                
                # Sauvegarder temporairement
                temp_img_path = temp_folder / f"temp_page_{page.page_number}.png"
                img.save(temp_img_path, 'PNG')
                
                # Ajouter l'image au PDF
                # Ajuster l'image pour remplir la page
                c.drawImage(str(temp_img_path), 0, 0, 
                          width=page_size[0], height=page_size[1],
                          preserveAspectRatio=True)
                
                # Ajouter le numéro de page
                c.setFont("Helvetica", 10)
                c.drawString(10, 10, f"Page {page.page_number}/{len(pages)}")
                
                # Nouvelle page (sauf pour la dernière)
                if page.page_number < len(pages):
                    c.showPage()
                    
        finally:
            # Nettoyer les fichiers temporaires
            for temp_file in temp_folder.glob("*.png"):
                temp_file.unlink()
            temp_folder.rmdir()
            
        # Sauvegarder le PDF
        c.save()
        
        return str(output_path)
        
    @staticmethod
    def _normalize_for_display(data: np.ndarray) -> np.ndarray:
        """
        Normalise les données pour l'affichage (0-255)
        
        Args:
            data: Tableau numpy à normaliser
            
        Returns:
            Tableau normalisé
        """
        valid_data = data[data > 0]
        if len(valid_data) == 0:
            return data
            
        p2, p98 = np.percentile(valid_data, (2, 98))
        normalized = np.clip((data - p2) / (p98 - p2) * 255, 0, 255)
        
        return normalized
