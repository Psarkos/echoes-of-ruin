# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ==================================================================
# === Création des templates pour le placement dans le code main ===
# ==================================================================

# ==============
# === IMPORT ===
# ==============
import pygame as pg
import random as rdm
import pandas as pd

from usefull_fonctions import csv_to_list, get_files_in_directory

# ============================
# === DEFINITION DES CLASS ===
# ============================


class Template(pg.sprite.Sprite):
    """Représente les templates placés sur la map"""

    def __init__(self, content: list):
        super().__init__()
        self.origin = None  # x, y; coordonnée 0, 0 du template absolue dans la map
        self.size = self.__size_get(content)  # Contient la largeur et la hauteur
        self.border = self.__get_border(content)  # Liste des coordonnés des bordures en position relative
        self.content = content  # Contenue du template

    def __size_get(self, tab):
        """Renvoie un tuple de la largeur et de la hauteur du template

        Args:
            tab (list): template

        Returns:
            tuple: hauteur et largeur du template
        """
        return len(tab[0]), len(tab)

    def __get_border(self, content):
        """Renvoie la liste des coordonnées relatives des blocs du template qui sont des bords

        Args:
            content (list): template

        Returns:
            list: liste de tuples des coordonnées des blocs du template qui sont des bords
        """
        list_border = []
        for row in range(self.size[1]):
            for column in range(self.size[0]):
                if (
                    content[row][column] != "0"  # Si l'élément n'est pas 0
                    and
                    # Si l'on se trouve à la première ou dernière colonne
                    (
                        column == 0
                        or column == self.size[0] - 1
                        or
                        # Si l'on se trouve à la première ou dernière ligne
                        row == 0
                        or row == self.size[1] - 1
                    )
                ):
                    list_border.append((column, row))  # Ajoute les coordonnées

                elif (
                    content[row][column] != "0"  # Si l'élément n'est pas 0
                    and
                    # Si l'élément au dessus ou au dessus est 0
                    (
                        content[row - 1][column] == "0"
                        or content[row + 1][column] == "0"
                        or
                        # Si l'élément à droite ou à gauche est 0
                        content[row][column - 1] == "0"
                        or content[row][column + 1] == "0"
                    )
                ):
                    list_border.append((column, row))  # Ajoute les coordonnées
        return list_border

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return "Template"


# ================================
# === DEFINITION DES FONCTIONS ===
# ================================


def get_random_list_of_templates(number_of_templates: int):
    # liste des noms des fichiers contenant les templates
    PATH = 'data/templates/'
    templates_link_list = (
        get_files_in_directory(PATH)
    )
    n = len(templates_link_list)  # nombre de templates disponible
    templates_list = []
    for i in range(
        number_of_templates
    ):  # rempli avec le nombre de templates voulu aléatoirement
        templates_list.append(
            Template(
                csv_to_list(
                    (PATH + templates_link_list[rdm.randint(0, n - 1)])
                )
            )
        )
    return templates_list
