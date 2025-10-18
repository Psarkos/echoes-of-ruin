# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# =============================
# === Création des couloirs ===
# =============================


# ==============
# === IMPORT ===
# ==============

import pygame as pg
import random as rdm

from pathfinder import aStar
from tile import Ground, Wall
from usefull_fonctions import is_tile_neighbor


# ============================
# === DEFINITION DES CLASS ===
# ============================


class Corridor(pg.sprite.Sprite):
    """Représente les couloirs entre les templates"""

    def __init__(self, map, information: tuple):
        super().__init__()
        self.distance_beetween_templates = information[0]
        self.template1 = information[1]
        self.template2 = information[2]
        self.template1_relative_pos = information[3]

        self.is_templates_near = self.determine_is_template_near()
        
        # boucle de sécurité qui regenère le couloir s'il n'est pas possible
        attemp = 50
        counter = 0
        loop = True
        while loop:
            self.corridor_absolute_pos_start_end_in_template = (
                self.define_corridor_abs_pos_start_end_in_template()
            )
            
            if not self.is_templates_near:
                self.corridor_absolute_pos_start_end_out_template = (
                    self.start_end_aStar_pos_founder(map)
                )
                if len(self.corridor_absolute_pos_start_end_out_template) == 2:
                    self.succesive_position = self.found_succesive_position(map)
                    loop = False
                    
            else:
                loop = False
            
            if counter == attemp:
                loop = False
                self.distance_beetween_templates = -1
                
            counter += 1

    def determine_is_template_near(self):
        """Renvoi True si les templates sont coller, False sinon

        Returns:
            bool: proche ou non
        """
        return self.distance_beetween_templates <= 1

    def define_corridor_abs_pos_start_end_in_template(self):
        """En fonction de si le template et proche ou non, créer soit une ouverture droite,
            soit un couloir utilisant le aStar

        Returns:
            tupple: positions dans les deux templates du départ et de l'arrivé du couloir
        """
        if self.is_templates_near:
            opening = self.found_opening_beetween_two_templates()

            if self.verify_opening(opening):
                return opening
            else:
                self.is_templates_near = False
        return self.start_end_absolute_pos_founder()

    def start_end_absolute_pos_founder(self):
        """Détermine la case du bord de chaque template dans une certaines zone en fonction de leur position
            relative, puis en appelant random_choice_border()

        Returns:
            tupple: tupple de tupple, chacun contenant les coordonnées d'une des extrémités du couloir
        """

        # Les x1, x2, y1, y2 sont les limites internes des templates, pour qu'il n'y est plus qu'a préciser un bord du template

        if self.template1_relative_pos[0] == "left":

            if self.template1_relative_pos[1] == "above":
                return self.pos_founder_left_above()

            elif self.template1_relative_pos[1] == "under":
                return self.pos_founder_left_under()

            else:  # a gauche au meme niveau
                return self.pos_founder_left_same()

        elif self.template1_relative_pos[0] == "right":

            if self.template1_relative_pos[1] == "above":
                return self.pos_founder_right_above()

            elif self.template1_relative_pos[1] == "under":
                return self.pos_founder_right_under()

            else:  # a droite au meme niveau
                return self.pos_founder_right_same()

        else:  # sur la meme verticale
            if self.template1_relative_pos[1] == "above":
                return self.pos_founder_same_above()

            else:  # en-dessous
                return self.pos_founder_same_under()

    def random_choice_border(self, template, x1: int, x2: int, y1: int, y2: int):
        """Choisi aléatoirement un bord du template qui est entre les coordonnées données
            Et si elle n'en trouve, la fonction se rappelle récursivement avec un plus grand
            encadrement jusqu'à trouver un bord

        Args:
            template (Template): template sur lequel on veut choisir un bord
            x1 (int): une extrémité horizontale
            x2 (int): l'autre extrémité horizontale
            y1 (int): une extrémité verticale
            y2 (int): l'autre extrémité vertical

        Returns:
            tupple: coordonné absolu de la case dans la map
        """

        # Tri les coordonnées pour connaître les plus grandes et les plus petites
        x_min, x_max = min([x1, x2]), max([x1, x2])
        y_min, y_max = min([y1, y2]), max([y1, y2])

        possible_position = []  # initialise les positions possibles

        for pos in template.border:  # on parcours tous les bords du templates
            # Si le bord se trouve dans l'intervalle alors on l'ajoute à la liste des positions possibles
            if (
                x_min <= (pos[0] + template.origin[0]) <= x_max
                and y_min <= (pos[1] + template.origin[1]) <= y_max
            ):
                possible_position.append(
                    (pos[0] + template.origin[0], (pos[1] + template.origin[1]))
                )

        # Si il n'y a aucune positions possible on rappelle la fonction mais avec un plus grand intervalle
        if possible_position == []:
            return self.random_choice_border(
                template, x_min - 1, x_max + 1, y_min - 1, y_max + 1
            )

        # On retourne une position aléatoire
        return rdm.choice(possible_position)

    def start_end_aStar_pos_founder(self, map):
        """Trouve le bloc adjacent au bord du template se trouvant à l'extérieur du template
            pour éxécuter le aStar entre les deux templates

        Args:
            map (list): map du jeu contenant contenant les templates

        Returns:
            tupple: position du départ et de l'arrivé du couloir en dehors du template, pour pouvoir éxécuter le aStar
        """
        pos_for_Astar = []
        pos = self.corridor_absolute_pos_start_end_in_template

        for i in range(2):
            current_template_pos = pos[i]

            if (
                type(map[current_template_pos[1]][current_template_pos[0] - 1])
                == Ground
            ):  # au-dessus
                pos_for_Astar.append(
                    (current_template_pos[0] - 1, current_template_pos[1])
                )

            elif (
                type(map[current_template_pos[1] + 1][current_template_pos[0]])
                == Ground
            ):  # à droite
                pos_for_Astar.append(
                    (current_template_pos[0], current_template_pos[1] + 1)
                )

            elif (
                type(map[current_template_pos[1]][current_template_pos[0] + 1])
                == Ground
            ):  # au-dessous
                pos_for_Astar.append(
                    (current_template_pos[0] + 1, current_template_pos[1])
                )

            elif (
                type(map[current_template_pos[1] - 1][current_template_pos[0]])
                == Ground
            ):  # à gauche
                pos_for_Astar.append(
                    (current_template_pos[0], current_template_pos[1] - 1)
                )

        return tuple(pos_for_Astar)

    def found_succesive_position(self, map):
        """Détermine le tracé du couloir en utilisant la distance de manathan, entre les deux case du template

        Args:
            map (list): map du jeu où les templates sont deja placés

        Returns:
            list: liste des positions des bloc qui constitues le couloir, trouvé par le aStar
        """
        start_end = self.corridor_absolute_pos_start_end_out_template
        passages_points = self.found_passages_points(map)
        
        aStar_beetween_start_passage_point = aStar(map, start_end[0], passages_points[0])
        aStar_beetween_passage_point = aStar(map, passages_points[0], passages_points[1])
        aStar_beetween_end_passage_point = aStar(map, passages_points[1], start_end[1])
        
        if not (
            aStar_beetween_start_passage_point is None or
            aStar_beetween_passage_point is None or
            aStar_beetween_end_passage_point is None
        ):
            return (
                aStar_beetween_start_passage_point
                + aStar_beetween_passage_point[1:-1]
                + aStar_beetween_end_passage_point
            )
        else:
            return aStar(map, start_end[0], start_end[1])

    def found_passages_points(self, map):
        """Return les deux points de passage du couloir

        Args:
            map (list): map avec les templates

        Returns:
            list: liste des 2 points de passage
        """
        all_passages_points = []  # Initialise la liste des points de passage
        pos_out_temp = self.corridor_absolute_pos_start_end_out_template

        # Si le couloir est plus haut que large
        if max([pos_out_temp[0][0], pos_out_temp[1][0]]) - min(
            [pos_out_temp[0][0], pos_out_temp[1][0]]
        ) < max([pos_out_temp[0][1], pos_out_temp[1][1]]) - min(
            [pos_out_temp[0][1], pos_out_temp[1][1]]
        ):

            # On initialise la position de l'intersection
            pos_x_inter = (pos_out_temp[0][0] + pos_out_temp[1][0]) // 2

            # On ajoute le point de passage si il n'y a pas de mur
            for i in range(2):
                if not type(map[pos_out_temp[i][1]][pos_x_inter]) == Wall:
                    all_passages_points.append((pos_x_inter, pos_out_temp[i][1]))
                else:
                    # Si il y a un mur alors le point de passage est l'extrémitée correspondante du couloir
                    all_passages_points.append(pos_out_temp[i])

        # Si le couloir est plus large que haut
        else:
            # On initialise la position de l'intersection
            pos_y_inter = (pos_out_temp[0][1] + pos_out_temp[1][1]) // 2

            # On ajoute le point de passage si il n'y a pas de mur
            for i in range(2):
                if not type(map[pos_y_inter][pos_out_temp[i][0]]) == Wall:
                    all_passages_points.append((pos_out_temp[i][0], pos_y_inter))
                else:
                    # Si il y a un mur alors le point de passage est l'extrémitée correspondante du couloir
                    all_passages_points.append(pos_out_temp[i])

        return all_passages_points

    def found_opening_beetween_two_templates(self):
        """Trouve les deux positions des murs à ouvrir pour créer un passage entre les deux templates

        Returns:
            tuple: positions des deux murs à ouvrir pour créer un passage entre les deux templates
        """
        if self.template1_relative_pos[0] == "left":
            x1 = self.template1.origin[0] + self.template1.size[0] - 1
            y1 = self.template1.origin[1] + self.template1.size[1] - 1

            x2 = self.template2.origin[0]
            y2 = self.template2.origin[1] + self.template2.size[1] - 1

            opening_template1 = self.random_choice_border(
                self.template1,
                x1,
                x1,
                max([self.template1.origin[1], self.template2.origin[1]]),
                min([y1, y2]),
            )

            return (opening_template1, (x2, opening_template1[1]))

        elif self.template1_relative_pos[0] == "right":
            x1 = self.template1.origin[0]
            y1 = self.template1.origin[1] + self.template1.size[1] - 1

            x2 = self.template2.origin[0] + self.template2.size[0] - 1
            y2 = self.template2.origin[1] + self.template2.size[1] - 1

            opening_template1 = self.random_choice_border(
                self.template1,
                x1,
                x1,
                max([self.template1.origin[1], self.template2.origin[1]]),
                min([y1, y2]),
            )

            return (opening_template1, (x2, opening_template1[1]))

        elif self.template1_relative_pos[1] == "above":
            x1 = self.template1.origin[0] + self.template1.size[0] - 1
            y1 = self.template1.origin[1] + self.template1.size[1] - 1

            x2 = self.template2.origin[0] + self.template2.size[0] - 1
            y2 = self.template2.origin[1]

            opening_template1 = self.random_choice_border(
                self.template1,
                min([x1, x2]),
                max([self.template1.origin[0], self.template2.origin[0]]),
                y1,
                y1,
            )

            return (opening_template1, (opening_template1[0], y2))

        elif self.template1_relative_pos[1] == "under":
            x1 = self.template1.origin[0] + self.template1.size[0] - 1
            y1 = self.template1.origin[1]

            x2 = self.template2.origin[0] + self.template2.size[0] - 1
            y2 = self.template2.origin[1] + self.template2.size[1] - 1

            opening_template1 = self.random_choice_border(
                self.template1,
                min([x1, x2]),
                max([self.template1.origin[0], self.template2.origin[0]]),
                y1,
                y1,
            )

            return (opening_template1, (opening_template1[0], y2))

    def verify_opening(self, opening:tuple):
        """ Vérifie si l'ouverture est correct, c'est-à-dire si elle est bien dans les deux templates
            et si les deux cases sont bien collées

        Args:
            opening (tuple): tuple de 2 tuples des 2 positions des ouvertures 
        Returns:
            bool: True si les coordonnées sont correct sinon False
        """
        relative_opening_pos = (
            (
                opening[0][0] - self.template1.origin[0],
                opening[0][1] - self.template1.origin[1]
            ),
            (
                opening[1][0] - self.template2.origin[0],
                opening[1][1] - self.template2.origin[1]
            )
        )
        if (
            relative_opening_pos[0] in self.template1.border and 
            relative_opening_pos[1] in self.template2.border and 
            is_tile_neighbor(opening[0], opening[1])
        ):
            return True
        return False

    def __str__(self):
        return str(self.corridor_absolute_pos_start_end_in_template)

    def __repr__(self):
        return str(self.corridor_absolute_pos_start_end_in_template)

    # Sous fonctions pour simplifier la fonction start_end_absolute_pos_founder
    def pos_founder_left_above(self):
        
        x1 = self.template1.origin[0] + (3 * (self.template1.size[0] - 1)) // 4
        y1 = self.template1.origin[1] + (3 * (self.template1.size[1] - 1)) // 4

        x2 = self.template2.origin[0] + (self.template2.size[0] - 1) // 4
        y2 = self.template2.origin[1] + (self.template2.size[1] - 1) // 4

        return (
            self.random_choice_border(
                self.template1,
                x1,
                self.template1.origin[0] + self.template1.size[0] - 1,
                y1,
                self.template1.origin[1] + self.template1.size[1] - 1,
            ),
            self.random_choice_border(
                self.template2,
                x2,
                self.template2.origin[0],
                y2,
                self.template2.origin[1],
            ),
        )
    
    def pos_founder_left_under(self):
        x1 = self.template1.origin[0] + int((3 * (self.template1.size[0] - 1)) / 4)
        y1 = self.template1.origin[1] + int((self.template1.size[1] - 1) / 4)

        x2 = self.template2.origin[0] + int((self.template2.size[1] - 1) / 4)
        y2 = self.template2.origin[1] + int((3 * (self.template2.size[1] - 1)) / 4)

        return (
            self.random_choice_border(
                self.template1,
                x1,
                self.template1.origin[0] + self.template1.size[0] - 1,
                y1,
                self.template1.origin[1],
            ),
            self.random_choice_border(
                self.template2,
                x2,
                self.template2.origin[0],
                y2,
                self.template2.origin[1] + self.template2.size[1] - 1,
            ),
        )
    
    def pos_founder_left_same(self):
        x1 = self.template1.origin[0] + self.template1.size[0] - 1
        y1 = self.template2.origin[1] + self.template2.size[1] - 1

        x2 = self.template2.origin[0]
        y2 = self.template1.origin[1] + self.template1.size[1] - 1

        return (
            self.random_choice_border(
                self.template1, x1, x1, y1, self.template2.origin[1]
            ),
            self.random_choice_border(
                self.template2, x2, x2, y2, self.template1.origin[1]
            ),
        )
    
    def pos_founder_right_above(self):
        x1 = self.template1.origin[0] + int((self.template1.size[0] - 1) / 4)
        y1 = self.template1.origin[1] + int((3 * (self.template1.size[1] - 1)) / 4)

        x2 = self.template2.origin[0] + int((3 * (self.template2.size[0] - 1)) / 4)
        y2 = self.template2.origin[1] + int((self.template2.size[1] - 1) / 4)

        return (
            self.random_choice_border(
                self.template1,
                x1,
                self.template1.origin[0],
                y1,
                self.template1.origin[1] + self.template1.size[1] - 1,
            ),
            self.random_choice_border(
                self.template2,
                x2,
                self.template2.origin[0] + self.template2.size[0] - 1,
                y2,
                self.template2.origin[1],
            ),
        )
    
    def pos_founder_right_same(self):
        x1 = self.template1.origin[0]
        y1 = self.template2.origin[1] + self.template2.size[1] - 1

        x2 = self.template2.origin[0] + self.template2.size[0] - 1
        y2 = self.template1.origin[1] + self.template1.size[1] - 1

        return (
            self.random_choice_border(
                self.template1, x1, x1, y1, self.template1.origin[1]
            ),
            self.random_choice_border(
                self.template2, x2, x2, y2, self.template2.origin[1]
            ),
        )
    
    def pos_founder_right_under(self):
        x1 = self.template1.origin[0] + int((self.template1.size[0] - 1) / 4)
        y1 = self.template1.origin[1] + int((self.template1.size[1] - 1) / 4)

        x2 = self.template2.origin[0] + ((3 * (self.template2.size[0] - 1)) / 4)
        y2 = self.template2.origin[1] + ((3 * (self.template2.size[1] - 1)) / 4)

        return (
            self.random_choice_border(
                self.template1,
                x1,
                self.template1.origin[0],
                y1,
                self.template1.origin[1],
            ),
            self.random_choice_border(
                self.template2,
                x2,
                self.template2.origin[0] + self.template2.size[0] - 1,
                y2,
                self.template2.origin[1] + self.template2.size[1] - 1,
            ),
        )
    
    def pos_founder_same_above(self):
        x1 = self.template2.origin[0] + self.template2.size[0] - 1
        y1 = self.template1.origin[1] + self.template1.size[1] - 1

        x2 = self.template1.origin[0] + self.template1.size[0] - 1
        y2 = self.template2.origin[1]

        return (
            self.random_choice_border(
                self.template1, x1, self.template1.origin[0], y1, y1
            ),
            self.random_choice_border(
                self.template2, x2, self.template2.origin[0], y2, y2
            ),
        )
    
    def pos_founder_same_under(self):
        x1 = self.template2.origin[0] + self.template2.size[0] - 1
        y1 = self.template1.origin[1]

        x2 = self.template1.origin[0] + self.template1.size[0] - 1
        y2 = self.template2.origin[1] + self.template2.size[1] - 1

        return (
            self.random_choice_border(
                self.template1, x1, self.template1.origin[0], y1, y1
            ),
            self.random_choice_border(
                self.template2, x2, self.template2.origin[0], y2, y2
            ),
        )
    
    
# ================================
# === DEFINITION DES FONCTIONS ===
# ================================

# === Fonctions pour calculer les distances entre tous les templates ===


def all_template_distance_founder(template_list):
    """Renvoie une liste de tupple contenant les distances entre les templates

    Args:
        template_list (list): liste des templates placés sur la map

    Returns:
        list: liste de tupple étant de la forme (distance, template1, template2, position_template1)
    """
    all_template_distance_list = []

    for current_template_id in range(
        len(template_list) - 1
    ):  # On parcours les id des templates jusqu'à l'avant dernier

        # On parcours les id des templates jusqu'au dernier et le current_template exclus
        for other_template_id in range(current_template_id + 1, len(template_list)):
            # On détermine position relative de l'origin du current_template par rapprort à l'autre
            current_position = (
                determine_horizontal_position_of_two_templates(
                    template_list[current_template_id], template_list[other_template_id]
                ),
                determine_vertical_position_of_two_templates(
                    template_list[current_template_id], template_list[other_template_id]
                ),
            )

            # On ajoute à la liste des distances le tupple (distance, current_template, other_template, current_template_position) trié dans l'ordre croissant
            all_template_distance_list = insertion_sort(
                all_template_distance_list,
                distance_caltulator_beetween_two_template(
                    template_list[current_template_id],
                    template_list[other_template_id],
                    current_position,
                ),
            )
    return all_template_distance_list


def determine_vertical_position_of_two_templates(current_template, other_template):
    """ Renvoie une chaîne de charactère présisant où se trouve le premier template
        verticalement par rapport à l'autre en comparant les origines des templates

    Args:
        current_template (Template): template de référence, c'est de lui dont on présisera la position par rapport à l'autre
        other_template (Template): deuxième template

    Returns:
        str: présice où se trouve le premier template par rapport à l'autre
    """
    if current_template.origin[1] < other_template.origin[1]:  # S'il est au dessus
        return "above"
    elif current_template.origin[1] > other_template.origin[1]:  # S'il est en-desous
        return "under"
    else:  # S'il est au même niveau
        return "same"


def determine_horizontal_position_of_two_templates(current_template, other_template):
    """ Renvoie une chaîne de charactère présisant où se trouve le premier template
        horizontalement par rapport à l'autre en comparant les origines des templates

    Args:
        current_template (Template): template de référence, c'est de lui dont on présisera la position par rapport à l'autre
        other_template (Template): deuxième template

    Returns:
        str: présice où se trouve le premier template par rapport à l'autre
    """
    if current_template.origin[0] > other_template.origin[0]:  # S'il est à droite
        return "right"
    elif current_template.origin[0] < other_template.origin[0]:  # S'il est à gauche
        return "left"
    else:  # S'il est au même niveau
        return "same"


def distance_caltulator_beetween_two_template(template1, template2, template1_position):
    """ Renvoi la distance entre deux templates en fonction de leurs bords les plus proche
        qui sont déterminés à partir de leurs positions relatives

    Args:
        template1 (Template): template dont on dira la position
        template2 (Template): template de conparaison
        template1_position (tupple): position (horizontal, vertical) du template1 par rapport au template2

    Returns:
        tupple: tupple a ajouter a la liste des distance entre tous les templates de la forme
                (distance, template1, template2, position_template1)
    """
    if template1_position[0] == "left":

        if template1_position[1] == "above":
            return distance_left_above(template1, template2, template1_position)

        elif template1_position[1] == "same":
            return (
                template2.origin[0] - (template1.origin[0] + template1.size[0] - 1),
                template1,
                template2,
                template1_position,
            )

        else:
            return distance_left_under(template1, template2, template1_position)

    elif template1_position[0] == "right":

        if template1_position[1] == "above":
            return distance_right_above(template1, template2, template1_position)

        elif template1_position[1] == "same":
            return (
                template1.origin[0] - (template2.origin[0] + template2.size[0] - 1),
                template1,
                template2,
                template1_position,
            )

        else:
            return distance_right_under(template1, template2, template1_position)

    elif template1_position[0] == "same":

        if template1_position[1] == "above":
            return (
                template2.origin[1] - (template1.origin[1] + template1.size[1] - 1),
                template1,
                template2,
                template1_position,
            )

        else:
            return (
                template1.origin[1] - (template2.origin[1] + template2.size[1] - 1),
                template1,
                template2,
                template1_position,
            )


# L'origine du template1 se trouve à gauche de celle du template2 
def distance_left_above(template1, template2, template1_position):
    # Calcul de la différence entre les coordonnées des bords
    horizontal_soustraction = template2.origin[0] - (
        template1.origin[0] + template1.size[0] - 1
    )
    vertical_soustraction = template2.origin[1] - (
        template1.origin[1] + template1.size[1] - 1
    )

    # Si aucune des droites passant par les bords du template1 ne passe par template2
    if horizontal_soustraction >= 1 and vertical_soustraction >= 1:
        # On renvoi la distance de manathan entre les deux templates
        return (
            horizontal_soustraction + vertical_soustraction,
            template1,
            template2,
            template1_position,
        )
    else:
        # Sinon la distance entre deux qui n'est pas négative
        if horizontal_soustraction > vertical_soustraction:
            return (
                horizontal_soustraction,
                template1,
                template2,
                (template1_position[0], None),
            )
        else:
            return (
                vertical_soustraction,
                template1,
                template2,
                (None, template1_position[1]),
            )


def distance_left_under(template1, template2, template1_position):
    # Calcul de la différence entre les coordonnées des bords
    horizontal_soustraction = template2.origin[0] - (
        template1.origin[0] + template1.size[0] - 1
    )
    vertical_soustraction = template1.origin[1] - (
        template2.origin[1] + template2.size[1] - 1
    )

    # Si aucune des droites passant par les bords du template1 ne passe par template2
    if horizontal_soustraction >= 1 and vertical_soustraction >= 1:
        # On renvoi la distance de manathan entre les deux templates
        return (
            horizontal_soustraction + vertical_soustraction,
            template1,
            template2,
            template1_position,
        )
    else:
        # Sinon la distance entre deux qui n'est pas négative
        if horizontal_soustraction > vertical_soustraction:
            return (
                horizontal_soustraction,
                template1,
                template2,
                (template1_position[0], None),
            )
        else:
            return (
                vertical_soustraction,
                template1,
                template2,
                (None, template1_position[1]),
            )


# L'origine du template1 se trouve à droite de celle du template2
def distance_right_above(template1, template2, template1_position):
    # Calcul de la différence entre les coordonnées des bords
    horizontal_soustraction = template1.origin[0] - (
        template2.origin[0] + template2.size[0] - 1
    )
    vertical_soustraction = template2.origin[1] - (
        template1.origin[1] + template1.size[1] - 1
    )

    # Si aucune des droites passant par les bords du template1 ne passe par template2
    if horizontal_soustraction >= 1 and vertical_soustraction >= 1:
        # On renvoi la distance de manathan entre les deux templates
        return (
            horizontal_soustraction + vertical_soustraction,
            template1,
            template2,
            template1_position,
        )
    else:
        # Sinon la distance entre deux qui n'est pas négative
        if horizontal_soustraction > vertical_soustraction:
            return (
                horizontal_soustraction,
                template1,
                template2,
                (template1_position[0], None),
            )
        else:
            return (
                vertical_soustraction,
                template1,
                template2,
                (None, template1_position[1]),
            )


def distance_right_under(template1, template2, template1_position):
    # Calcul de la différence entre les coordonnées des bords
    horizontal_soustraction = template1.origin[0] - (
        template2.origin[0] + template2.size[0] - 1
    )
    vertical_soustraction = template1.origin[1] - (
        template2.origin[1] + template2.size[1] - 1
    )

    # Si aucune des droites passant par les bords du template1 ne passe par template2
    if horizontal_soustraction >= 1 and vertical_soustraction >= 1:
        # On renvoi la distance de manathan entre les deux templates
        return (
            horizontal_soustraction + vertical_soustraction,
            template1,
            template2,
            template1_position,
        )
    else:
        # Sinon la distance entre deux qui n'est pas négative
        if horizontal_soustraction > vertical_soustraction:
            return (
                horizontal_soustraction,
                template1,
                template2,
                (template1_position[0], None),
            )
        else:
            return (
                vertical_soustraction,
                template1,
                template2,
                (None, template1_position[1]),
            )


def insertion_sort(list, elt):
    """ Tri récusivement les distances entre les templates au moment de les ajouters à la liste
        pour que les templates soient triés dans l'ordre croissant

    Args:
        list (list): list des distances entre les templates
        elt (tupple): tupple distance, template1 et template2

    Returns:
        list: la liste contenant l'élément ajouter au bon endroit
    """
    if list == []:
        return [elt]
    elif list[0][0] >= elt[0]:
        return [elt] + list
    return list[:1] + insertion_sort(list[1:], elt)
