#!/usr/bin/env python3
"""
MapsCut - Application de découpage d'images géoréférencées
Point d'entrée principal de l'application
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.interface import MainWindow


def main():
    """Point d'entrée principal de l'application"""
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Définir des informations sur l'application
    app.setApplicationName("MapsCut")
    app.setOrganizationName("MapsCut")
    app.setApplicationVersion("1.0.0")
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Lancer la boucle d'événements
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
