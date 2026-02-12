"""
Module d'interface graphique
Interface PyQt6 pour l'application MapsCut
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGroupBox, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox,
    QMessageBox, QProgressDialog, QGraphicsRectItem, QTextEdit
)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPen, QColor, QBrush
import numpy as np
from typing import Optional, Tuple
from pathlib import Path

from .raster_processing import RasterProcessor
from .cutting import PageCutter
from .export import Exporter


class SelectionRectItem(QGraphicsRectItem):
    """Rectangle de sélection interactif"""
    
    def __init__(self):
        super().__init__()
        self.setPen(QPen(QColor(255, 0, 0, 255), 2, Qt.PenStyle.DashLine))
        self.setBrush(QBrush(QColor(255, 0, 0, 50)))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setVisible(False)


class ImageView(QGraphicsView):
    """Vue graphique pour afficher et interagir avec l'image"""
    
    selection_changed = pyqtSignal(QRectF)
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Activer le déplacement et le zoom
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Variables pour la sélection
        self.selecting = False
        self.selection_start = None
        self.selection_rect = SelectionRectItem()
        self.scene.addItem(self.selection_rect)
        
        # Image pixmap
        self.pixmap_item = None
        
    def set_image(self, image_array: np.ndarray):
        """
        Affiche une image numpy dans la vue
        
        Args:
            image_array: Tableau numpy RGB (height, width, 3)
        """
        # Convertir numpy array en QImage
        height, width, channel = image_array.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_array.data, width, height, bytes_per_line, 
                        QImage.Format.Format_RGB888)
        
        # Créer un pixmap
        pixmap = QPixmap.fromImage(q_image)
        
        # Ajouter à la scène
        self.scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        self.selection_rect = SelectionRectItem()
        self.scene.addItem(self.selection_rect)
        
        # Ajuster la vue
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        
    def wheelEvent(self, event):
        """Gérer le zoom avec la molette"""
        # Facteur de zoom
        zoom_factor = 1.15
        
        if event.angleDelta().y() > 0:
            # Zoom avant
            self.scale(zoom_factor, zoom_factor)
        else:
            # Zoom arrière
            self.scale(1 / zoom_factor, 1 / zoom_factor)
            
    def mousePressEvent(self, event):
        """Début de sélection"""
        if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Mode sélection avec Ctrl+Click
            self.selecting = True
            self.selection_start = self.mapToScene(event.pos())
            self.selection_rect.setRect(QRectF(self.selection_start, self.selection_start))
            self.selection_rect.setVisible(True)
            event.accept()
        else:
            super().mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        """Mise à jour de la sélection"""
        if self.selecting:
            current_pos = self.mapToScene(event.pos())
            rect = QRectF(self.selection_start, current_pos).normalized()
            self.selection_rect.setRect(rect)
            event.accept()
        else:
            super().mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        """Fin de sélection"""
        if self.selecting and event.button() == Qt.MouseButton.LeftButton:
            self.selecting = False
            current_pos = self.mapToScene(event.pos())
            rect = QRectF(self.selection_start, current_pos).normalized()
            self.selection_rect.setRect(rect)
            self.selection_changed.emit(rect)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
            
    def get_selection_rect(self) -> Optional[QRectF]:
        """Retourne le rectangle de sélection actuel"""
        if self.selection_rect.isVisible():
            return self.selection_rect.rect()
        return None
        
    def clear_selection(self):
        """Efface la sélection"""
        self.selection_rect.setVisible(False)


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MapsCut - Découpage d'images géoréférencées")
        self.setGeometry(100, 100, 1400, 900)
        
        # Modules
        self.raster_processor = RasterProcessor()
        self.page_cutter = PageCutter()
        self.exporter = Exporter()
        
        # Variables
        self.current_folder = None
        self.selection_rect_px = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panneau gauche (contrôles)
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Vue de l'image
        self.image_view = ImageView()
        self.image_view.selection_changed.connect(self.on_selection_changed)
        main_layout.addWidget(self.image_view, stretch=1)
        
    def create_control_panel(self) -> QWidget:
        """Crée le panneau de contrôle"""
        panel = QWidget()
        panel.setMaximumWidth(350)
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Titre
        title = QLabel("<h2>MapsCut</h2>")
        layout.addWidget(title)
        
        # Bouton chargement
        self.btn_load = QPushButton("📁 Charger dossier GeoTIFF")
        self.btn_load.clicked.connect(self.load_folder)
        layout.addWidget(self.btn_load)
        
        # Info dossier
        self.lbl_folder = QLabel("Aucun dossier chargé")
        self.lbl_folder.setWordWrap(True)
        layout.addWidget(self.lbl_folder)
        
        # Instructions
        instructions = QLabel(
            "<b>Instructions:</b><br>"
            "1. Chargez un dossier GeoTIFF<br>"
            "2. Maintenez Ctrl + clic gauche pour sélectionner une zone<br>"
            "3. Configurez les paramètres<br>"
            "4. Exportez"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Paramètres d'impression
        print_group = QGroupBox("Paramètres d'impression")
        print_layout = QFormLayout()
        print_group.setLayout(print_layout)
        
        # Format papier
        self.cmb_format = QComboBox()
        self.cmb_format.addItems(list(PageCutter.PAPER_FORMATS.keys()))
        self.cmb_format.setCurrentText('A4')
        self.cmb_format.currentTextChanged.connect(self.on_params_changed)
        print_layout.addRow("Format:", self.cmb_format)
        
        # Orientation
        self.cmb_orientation = QComboBox()
        self.cmb_orientation.addItems(['portrait', 'landscape'])
        self.cmb_orientation.currentTextChanged.connect(self.on_params_changed)
        print_layout.addRow("Orientation:", self.cmb_orientation)
        
        # DPI
        self.spn_dpi = QSpinBox()
        self.spn_dpi.setRange(72, 600)
        self.spn_dpi.setValue(300)
        self.spn_dpi.setSuffix(" dpi")
        self.spn_dpi.valueChanged.connect(self.on_params_changed)
        print_layout.addRow("DPI:", self.spn_dpi)
        
        # Overlap
        self.spn_overlap = QDoubleSpinBox()
        self.spn_overlap.setRange(0, 50)
        self.spn_overlap.setValue(10)
        self.spn_overlap.setSuffix(" mm")
        self.spn_overlap.valueChanged.connect(self.on_params_changed)
        print_layout.addRow("Recouvrement:", self.spn_overlap)
        
        layout.addWidget(print_group)
        
        # Info découpage
        self.txt_cut_info = QTextEdit()
        self.txt_cut_info.setReadOnly(True)
        self.txt_cut_info.setMaximumHeight(120)
        layout.addWidget(QLabel("<b>Info découpage:</b>"))
        layout.addWidget(self.txt_cut_info)
        
        # Boutons export
        self.btn_export_tiff = QPushButton("💾 Exporter GeoTIFF")
        self.btn_export_tiff.clicked.connect(self.export_geotiff)
        self.btn_export_tiff.setEnabled(False)
        layout.addWidget(self.btn_export_tiff)
        
        self.btn_export_pdf = QPushButton("📄 Exporter PDF")
        self.btn_export_pdf.clicked.connect(self.export_pdf)
        self.btn_export_pdf.setEnabled(False)
        layout.addWidget(self.btn_export_pdf)
        
        # Bouton effacer sélection
        self.btn_clear = QPushButton("🗑️ Effacer sélection")
        self.btn_clear.clicked.connect(self.clear_selection)
        self.btn_clear.setEnabled(False)
        layout.addWidget(self.btn_clear)
        
        # Spacer
        layout.addStretch()
        
        return panel
        
    def load_folder(self):
        """Charge un dossier contenant des GeoTIFF"""
        folder = QFileDialog.getExistingDirectory(
            self, "Sélectionner un dossier contenant des GeoTIFF"
        )
        
        if not folder:
            return
            
        try:
            # Afficher une boîte de progression
            progress = QProgressDialog("Chargement des images...", "Annuler", 0, 0, self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.show()
            
            # Charger les fichiers
            files = self.raster_processor.load_geotiffs(folder)
            
            # Créer la mosaïque
            progress.setLabelText("Création de la mosaïque...")
            self.raster_processor.create_mosaic()
            
            # Afficher l'image
            progress.setLabelText("Affichage...")
            rgb_array = self.raster_processor.get_rgb_array()
            self.image_view.set_image(rgb_array)
            
            progress.close()
            
            # Mettre à jour l'interface
            self.current_folder = folder
            self.lbl_folder.setText(f"Chargé: {len(files)} fichier(s)\n{folder}")
            
            QMessageBox.information(
                self, "Succès",
                f"{len(files)} fichier(s) GeoTIFF chargé(s) et mosaïqué(s)"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Erreur",
                f"Erreur lors du chargement:\n{str(e)}"
            )
            
    def on_selection_changed(self, rect: QRectF):
        """Appelé quand la sélection change"""
        if rect.width() < 5 or rect.height() < 5:
            return
            
        # Stocker la sélection en pixels
        self.selection_rect_px = (
            int(rect.x()), int(rect.y()),
            int(rect.x() + rect.width()), int(rect.y() + rect.height())
        )
        
        # Mettre à jour les infos de découpage
        self.update_cutting_info()
        
        # Activer les boutons
        self.btn_export_tiff.setEnabled(True)
        self.btn_export_pdf.setEnabled(True)
        self.btn_clear.setEnabled(True)
        
    def on_params_changed(self):
        """Appelé quand les paramètres d'impression changent"""
        if self.selection_rect_px:
            self.update_cutting_info()
            
    def update_cutting_info(self):
        """Met à jour les informations de découpage"""
        if not self.selection_rect_px:
            self.txt_cut_info.setText("Aucune sélection")
            return
            
        try:
            # Appliquer les paramètres
            self.page_cutter.set_paper_format(self.cmb_format.currentText())
            self.page_cutter.set_orientation(self.cmb_orientation.currentText())
            self.page_cutter.set_dpi(self.spn_dpi.value())
            self.page_cutter.set_overlap(self.spn_overlap.value())
            
            # Calculer les pages
            x1, y1, x2, y2 = self.selection_rect_px
            width = x2 - x1
            height = y2 - y1
            
            pages = self.page_cutter.calculate_pages(width, height)
            
            # Afficher les infos
            info_text = f"Zone sélectionnée: {width} x {height} px\n\n"
            info_text += self.page_cutter.get_page_info_text()
            
            self.txt_cut_info.setText(info_text)
            
        except Exception as e:
            self.txt_cut_info.setText(f"Erreur: {str(e)}")
            
    def export_geotiff(self):
        """Exporte en GeoTIFF"""
        if not self.selection_rect_px:
            QMessageBox.warning(self, "Avertissement", "Aucune zone sélectionnée")
            return
            
        # Choisir le dossier de sortie
        output_folder = QFileDialog.getExistingDirectory(
            self, "Sélectionner le dossier de sortie"
        )
        
        if not output_folder:
            return
            
        try:
            progress = QProgressDialog("Export en cours...", "Annuler", 0, len(self.page_cutter.pages), self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            
            self.exporter.set_output_folder(output_folder)
            
            x1, y1, x2, y2 = self.selection_rect_px
            
            files = self.exporter.export_all_geotiffs(
                self.raster_processor.mosaic_data,
                self.raster_processor.mosaic_crs,
                self.raster_processor.mosaic_transform,
                self.page_cutter.pages,
                x1, y1,
                "page"
            )
            
            progress.setValue(len(files))
            
            QMessageBox.information(
                self, "Succès",
                f"{len(files)} fichier(s) GeoTIFF exporté(s) dans:\n{output_folder}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export:\n{str(e)}")
            
    def export_pdf(self):
        """Exporte en PDF"""
        if not self.selection_rect_px:
            QMessageBox.warning(self, "Avertissement", "Aucune zone sélectionnée")
            return
            
        # Choisir le fichier de sortie
        output_file, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder le PDF", "output.pdf", "PDF Files (*.pdf)"
        )
        
        if not output_file:
            return
            
        try:
            progress = QProgressDialog("Création du PDF...", "Annuler", 0, 0, self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.show()
            
            output_folder = str(Path(output_file).parent)
            output_name = Path(output_file).name
            
            self.exporter.set_output_folder(output_folder)
            
            x1, y1, x2, y2 = self.selection_rect_px
            
            pdf_path = self.exporter.export_pdf(
                self.raster_processor.mosaic_data,
                self.page_cutter.pages,
                x1, y1,
                self.cmb_format.currentText(),
                self.cmb_orientation.currentText(),
                output_name
            )
            
            progress.close()
            
            QMessageBox.information(
                self, "Succès",
                f"PDF exporté:\n{pdf_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export:\n{str(e)}")
            
    def clear_selection(self):
        """Efface la sélection"""
        self.image_view.clear_selection()
        self.selection_rect_px = None
        self.btn_export_tiff.setEnabled(False)
        self.btn_export_pdf.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.txt_cut_info.setText("Sélection effacée")
