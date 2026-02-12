"""
Module de traitement raster
Gère le chargement et la création de mosaïques à partir d'images GeoTIFF
"""

import os
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.transform import from_bounds
from typing import List, Tuple, Optional
from pathlib import Path


class RasterProcessor:
    """Classe pour traiter les images raster géoréférencées"""
    
    def __init__(self):
        self.mosaic_data = None
        self.mosaic_transform = None
        self.mosaic_crs = None
        self.mosaic_bounds = None
        self.source_files = []
        
    def load_geotiffs(self, folder_path: str) -> List[str]:
        """
        Charge tous les fichiers GeoTIFF d'un dossier
        
        Args:
            folder_path: Chemin du dossier contenant les GeoTIFF
            
        Returns:
            Liste des chemins des fichiers GeoTIFF trouvés
            
        Raises:
            ValueError: Si aucun fichier GeoTIFF n'est trouvé
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise ValueError(f"Le dossier {folder_path} n'existe pas")
            
        # Rechercher les fichiers .tif et .tiff
        geotiff_files = []
        for ext in ['*.tif', '*.tiff', '*.TIF', '*.TIFF']:
            geotiff_files.extend(folder.glob(ext))
            
        if not geotiff_files:
            raise ValueError(f"Aucun fichier GeoTIFF trouvé dans {folder_path}")
            
        self.source_files = [str(f) for f in geotiff_files]
        return self.source_files
        
    def create_mosaic(self, file_paths: Optional[List[str]] = None) -> Tuple[np.ndarray, dict]:
        """
        Crée une mosaïque à partir de plusieurs fichiers GeoTIFF
        
        Args:
            file_paths: Liste des chemins des fichiers à mosaïquer (optionnel, utilise source_files si None)
            
        Returns:
            Tuple (données mosaïque, métadonnées)
            
        Raises:
            ValueError: Si aucun fichier n'est fourni
            RuntimeError: Si la création de la mosaïque échoue
        """
        if file_paths is None:
            file_paths = self.source_files
            
        if not file_paths:
            raise ValueError("Aucun fichier à mosaïquer")
            
        try:
            # Ouvrir tous les fichiers
            src_files_to_mosaic = []
            for fp in file_paths:
                src = rasterio.open(fp)
                src_files_to_mosaic.append(src)
                
            # Créer la mosaïque
            mosaic, out_trans = merge(src_files_to_mosaic)
            
            # Récupérer les métadonnées du premier fichier
            out_meta = src_files_to_mosaic[0].meta.copy()
            
            # Mettre à jour les métadonnées
            out_meta.update({
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_trans
            })
            
            # Stocker les informations
            self.mosaic_data = mosaic
            self.mosaic_transform = out_trans
            self.mosaic_crs = out_meta['crs']
            
            # Calculer les limites
            self.mosaic_bounds = rasterio.transform.array_bounds(
                mosaic.shape[1], mosaic.shape[2], out_trans
            )
            
            # Fermer les fichiers sources
            for src in src_files_to_mosaic:
                src.close()
                
            return mosaic, out_meta
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la création de la mosaïque: {str(e)}")
            
    def get_rgb_array(self) -> np.ndarray:
        """
        Convertit les données de la mosaïque en tableau RGB pour l'affichage
        
        Returns:
            Tableau numpy RGB (height, width, 3)
            
        Raises:
            ValueError: Si la mosaïque n'a pas été créée
        """
        if self.mosaic_data is None:
            raise ValueError("Aucune mosaïque n'a été créée")
            
        # Si l'image a au moins 3 bandes, utiliser les 3 premières comme RGB
        if self.mosaic_data.shape[0] >= 3:
            rgb = np.dstack((
                self.mosaic_data[0],
                self.mosaic_data[1],
                self.mosaic_data[2]
            ))
        # Si une seule bande, créer une image en niveaux de gris
        elif self.mosaic_data.shape[0] == 1:
            rgb = np.dstack((
                self.mosaic_data[0],
                self.mosaic_data[0],
                self.mosaic_data[0]
            ))
        else:
            raise ValueError("Format de données non supporté")
            
        # Normaliser les valeurs pour l'affichage (0-255)
        rgb_normalized = self.normalize_for_display(rgb)
        
        return rgb_normalized.astype(np.uint8)
        
    @staticmethod
    def normalize_for_display(data: np.ndarray) -> np.ndarray:
        """
        Normalise les données pour l'affichage (0-255)
        
        Args:
            data: Tableau numpy à normaliser
            
        Returns:
            Tableau normalisé
        """
        # Ignorer les valeurs nodata (généralement 0 ou très grandes)
        valid_data = data[data > 0]
        if len(valid_data) == 0:
            return data
            
        # Calculer les percentiles pour un meilleur contraste
        p2, p98 = np.percentile(valid_data, (2, 98))
        
        # Normaliser
        normalized = np.clip((data - p2) / (p98 - p2) * 255, 0, 255)
        
        return normalized
        
    def pixel_to_geo(self, pixel_x: int, pixel_y: int) -> Tuple[float, float]:
        """
        Convertit des coordonnées pixel en coordonnées géographiques
        
        Args:
            pixel_x: Coordonnée X en pixels
            pixel_y: Coordonnée Y en pixels
            
        Returns:
            Tuple (longitude, latitude) ou (x, y) en coordonnées projetées
            
        Raises:
            ValueError: Si la mosaïque n'a pas été créée
        """
        if self.mosaic_transform is None:
            raise ValueError("Aucune mosaïque n'a été créée")
            
        geo_x, geo_y = rasterio.transform.xy(self.mosaic_transform, pixel_y, pixel_x)
        return geo_x, geo_y
        
    def geo_to_pixel(self, geo_x: float, geo_y: float) -> Tuple[int, int]:
        """
        Convertit des coordonnées géographiques en coordonnées pixel
        
        Args:
            geo_x: Coordonnée X géographique
            geo_y: Coordonnée Y géographique
            
        Returns:
            Tuple (pixel_x, pixel_y)
            
        Raises:
            ValueError: Si la mosaïque n'a pas été créée
        """
        if self.mosaic_transform is None:
            raise ValueError("Aucune mosaïque n'a été créée")
            
        row, col = rasterio.transform.rowcol(self.mosaic_transform, geo_x, geo_y)
        return col, row
        
    def extract_region(self, x1: int, y1: int, x2: int, y2: int) -> Tuple[np.ndarray, dict]:
        """
        Extrait une région de la mosaïque
        
        Args:
            x1, y1: Coordonnées du coin supérieur gauche (pixels)
            x2, y2: Coordonnées du coin inférieur droit (pixels)
            
        Returns:
            Tuple (données extraites, métadonnées avec nouvelle transformation)
            
        Raises:
            ValueError: Si la mosaïque n'a pas été créée ou si les coordonnées sont invalides
        """
        if self.mosaic_data is None:
            raise ValueError("Aucune mosaïque n'a été créée")
            
        # S'assurer que les coordonnées sont dans le bon ordre
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        
        # S'assurer que les coordonnées sont dans les limites
        height, width = self.mosaic_data.shape[1], self.mosaic_data.shape[2]
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))
        
        if x1 >= x2 or y1 >= y2:
            raise ValueError("Coordonnées invalides")
            
        # Extraire les données
        extracted_data = self.mosaic_data[:, y1:y2, x1:x2]
        
        # Calculer la nouvelle transformation
        geo_x1, geo_y1 = self.pixel_to_geo(x1, y1)
        
        # Calculer la résolution
        res_x = self.mosaic_transform.a
        res_y = self.mosaic_transform.e
        
        new_transform = rasterio.transform.from_origin(
            geo_x1, geo_y1, abs(res_x), abs(res_y)
        )
        
        metadata = {
            'driver': 'GTiff',
            'height': extracted_data.shape[1],
            'width': extracted_data.shape[2],
            'count': extracted_data.shape[0],
            'dtype': extracted_data.dtype,
            'crs': self.mosaic_crs,
            'transform': new_transform
        }
        
        return extracted_data, metadata
