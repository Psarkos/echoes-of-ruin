# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Importation de toutes les bibliotheques
import pygame as pg
from math import sqrt

from usefull_fonctions import image_loader

from tile import *
from corridor import *


# ================================
# === DEFINITION DES FONCTIONS ===
# ================================


# Génération de toute la map
def map_generator(
    templates_list: list,
    tilegroup: pg.sprite.Group,
    tile_style: str = "stone",
    biome: str = "basic",
) -> list:
    """Genere une carte avec les templates en fonction du nombre et de la taille des templates"""
    is_exit_accesible = False

    # Sécurité qui regénère la map jusqu'à ce que toutes les pièces soient liées entre elles
    while not is_exit_accesible:
        # Création de la map
        map = empty_map_generator(templates_list)  # Genere une map vide

        modifiable_templates_list = templates_list.copy()

        add_templates_to_map(
            map, modifiable_templates_list
        )  # Ajoute les templates a la map
        map = add_entities_to_map(
            map, tile_style, biome
        )  # Transforme str et int de la map en objet de type Ground et Wall

        # Ajout des couloirs
        corridor_list = create_all_corridor(
            map, modifiable_templates_list
        )  # Défini les couloirs qui vont être créés

        if is_all_corridor_placed(corridor_list):
            add_corridor_to_map(
                map, corridor_list, tile_style, biome
            )  # Ajoute ces derniers à la map en objet de type Wall

            is_exit_accesible = verify_is_map_possible(map, modifiable_templates_list)

    templates_list = modifiable_templates_list.copy()

    # Ajoute les Wall au tilegroup qu'une fois que la map est possible
    remove_ground_from_map_and_add_to_tilegroup(
        map, tilegroup
    )  # Retire tous les Ground de la map
    return map


# Ajout des blocs au groupe
def add_entities_to_map(map: list, tile_style: str, biome: str):
    """Ajoute des entitees dans les groupes en fonction des donnees de la map"""
    map_with_object = []

    debug_img = image_loader("assets/images/debug/debug_tile/alert_tile_debug.png")

    # On parcours chaque elmt de la map
    for y in range(len(map)):
        new_row_for_map_object = []
        for x in range(len(map[0])):
            elmt = map[y][x]
            var = Block(
                (x, y),
                debug_img,
            )  # <- Block qui indique une erreur
            # Si l'elmt est un entier, on l'ajoute au group
            if type(elmt) is int:  # <- Check si elmt est un entier
                var = Ground((x, y))

            # Si l'elmt est une str ET que son code et correct, on l'ajoute au group

            elif type(elmt) is str:  # <- Verifie que c'est une str
                if elmt == "0":  # Quand les template ne sont pas  carré, 0 sont des str
                    var = Ground((x, y))
                else:
                    var = Wall(
                        (x, y),
                        f"assets/images/{biome}/{tile_style}/{elmt}.png",
                        N=elmt[-4] == "w",
                        E=elmt[-3] == "w",
                        S=elmt[-2] == "w",
                        O=elmt[-1] == "w",
                    )

            new_row_for_map_object.append(var)
        # Des qu'on arrive au bout de la ligne, on vas au debut de la suivante
        map_with_object.append(new_row_for_map_object[:])
    return map_with_object


# === Ajout des couloirs entre les templates


def create_all_corridor(map, templates_list):
    """Créer la liste contenant tous les couloirs à placer sur la map

    Args:
        map (list): map avec les templates placée
        templates_list (list): liste des templates

    Returns:
        list: liste des couloirs
    """
    # === Définition des variables ===
    corridor_list = (
        []
    )  # Liste des couloirs sous forme d'objet Corridor, utilisé pour les ajouter à la map plus tard
    template_graph = (
        {}
    )  # Dictionnaire d'adjacences pour connaître les liens entre les templates
    template_distance_list = all_template_distance_founder(
        templates_list
    )  # Liste des toutes les distances entre les templates
    all_templates_linked = (
        False  # booléen qui passe à vrai si tous les templates sont liées
    )
    max_attempts = (
        len(templates_list) ** 2
    )  # Nombre d'essais max pour placer les couloirs
    counter = 0  # Compteur d'essais
    max_size_corridor = (
        sqrt((len(map) ** 2 + len(map[0]) ** 2)) // 5
    )  # Taille max des couloirs en fonction de la taille de la map

    # Ajoutes les templates au dico d'adjacence
    for template in templates_list:
        template_graph[template] = []

    # === Boucle ===
    while not all_templates_linked and counter < max_attempts:
        if template_distance_list != []:
            information_of_2_templates = template_distance_list.pop(
                0
            )  # Récupère les informations des 2 templates les plus proches
        else:
            break

        if (
            template_graph[information_of_2_templates[1]] == []
            or template_graph[information_of_2_templates[2]] == []
            or information_of_2_templates[0] < max_size_corridor
        ):

            # Ajoute l'arc au dico d'adjacences
            template_graph[information_of_2_templates[1]].append(
                information_of_2_templates[2]
            )
            template_graph[information_of_2_templates[2]].append(
                information_of_2_templates[1]
            )

            # Ajoute le couloir à la liste des couloirs
            corridor_list.append(Corridor(map, information_of_2_templates))

        all_templates_linked = verify_all_template_linked(
            template_graph,
            len(corridor_list),
            len(templates_list) + len(templates_list) // 5,
        )
        counter += 1

    return corridor_list


def verify_all_template_linked(
    template_graphe: dict, nb_corridor: int, min_nb_of_corridor: int
):
    """Fonction qui vérifie dans le dico d'adjacences des templates si ils sont tous liés

    Args:
        template_graphe (dict): dico d'adjacences
        nb_corridor (int): taille de la liste des couloirs existant au moment de la vérification
        min_nb_of_corridor (int): nombre minimum de templtes à placer si l'on veut être sûr que tous les templates sont relier

    Returns:
        bool: True s'ils sont tous liés, False sinon
    """
    if nb_corridor < min_nb_of_corridor:
        return False
    else:
        for elt in template_graphe.values():
            if elt == []:
                return False
    return True


def add_corridor_to_map(map, corridor_list, tile_style: str, biome: str):
    """Ajoute les couloirs fonctionnels à la map

    Args:
        map (list): map avec les templates
        corridor_list (list): liste des couloirs à placer
        tilegroup (pg.sprite.Group): groupe des tiles pygame
        tile_style (str): style des tiles (ex: stone, sand, etc...)
        biome (str): biome des images (pour les variantes)
    """
    # On ajoute les couloirs mais sous forme de Wall avec 4 murs à la map
    add_brut_corridor_to_map(map, corridor_list, tile_style, biome)

    # On parcours la liste des couloirs
    for corridor in corridor_list:
        # Si les templates sont coller
        if corridor.is_templates_near:

            # On créer une ouverture dans chaque template vers l'autres templates templates
            open_tile(
                map,
                corridor.corridor_absolute_pos_start_end_in_template[0],
                corridor.corridor_absolute_pos_start_end_in_template[1],
            )
            open_tile(
                map,
                corridor.corridor_absolute_pos_start_end_in_template[1],
                corridor.corridor_absolute_pos_start_end_in_template[0],
            )

        # Si les templates ne sont pas proche
        elif not corridor.is_templates_near:

            # On créer une liste contenant toutes les positions du couloirs + les positions dans les templates
            all_positions = (
                [corridor.corridor_absolute_pos_start_end_in_template[0]]
                + corridor.succesive_position
                + [corridor.corridor_absolute_pos_start_end_in_template[1]]
            )

            # On ouvre les templates
            open_tile(map, all_positions[0], all_positions[1])
            open_tile(map, all_positions[-1], all_positions[-2])

            # Puis on ouvre chaque case du couloir une par une
            for index_pos in range(1, len(all_positions) - 1):
                # Ouverture avec la case suivante
                open_tile(map, all_positions[index_pos], all_positions[index_pos + 1])
                # Ouverture avec la case precedante
                open_tile(map, all_positions[index_pos], all_positions[index_pos - 1])


def open_tile(map: list, pos: tuple, next_pos: tuple):
    """Modifie le Wall au coordonné pos qui mène sur le Wall au coordonné next_pos

    Args:
        map (list): map avec les templates de placés
        pos (tuple): position de la case que l'on veut modifier
        next_pos (tuple): position de la case vers laquelle on veut qu'il y est un passage
    """
    tile_pos = map[pos[1]][
        pos[0]
    ]  # Récupère la case que l'on veut modifier pour plus de facilité
    if type(tile_pos) is Wall:
        if pos[0] == next_pos[0]:  # Les cases sont sur la même ligne
            if pos[1] > next_pos[1]:  # Si la case d'après est au dessus
                tile_pos.walls["N"] = False
                tile_pos.image_setter(
                    tile_pos.img_link[:-8] + "0" + tile_pos.img_link[-7:]
                )

            else:  # Si la case d'après est au dessous
                tile_pos.walls["S"] = False
                tile_pos.image_setter(
                    tile_pos.img_link[:-6] + "0" + tile_pos.img_link[-5:]
                )

        else:  # Les cases sont sur la même colonne
            if pos[0] > next_pos[0]:  # Si la case d'après est à gauche
                tile_pos.walls["O"] = False
                tile_pos.image_setter(
                    tile_pos.img_link[:-5] + "0" + tile_pos.img_link[-4:]
                )

            else:  # Si la case d'après est à droite
                tile_pos.walls["E"] = False
                tile_pos.image_setter(
                    tile_pos.img_link[:-7] + "0" + tile_pos.img_link[-6:]
                )


def add_brut_corridor_to_map(map, corridor_list, tile_style: str, biome: str):
    """Ajoute les couloirs mais sous forme de Wall avec 4 murs

    Args:
        map (list): map avec les templates
        corridor_list (list): liste des couloirs à placer
        tilegroup (pg.sprite.Group): groupe des tiles pygame
        tile_style (str): style des tiles (ex: stone, sand, etc...)
        biome (str): biome des images (pour les variantes)
    """
    # On parcours laliste des couloirs
    for corridor in corridor_list:

        # Si les templates sont à plus de 1 de distance
        if not corridor.is_templates_near:

            # On parcours les positions successives du couloirs et on remplace dans la map par un Wall complet (4 murs)
            for x, y in corridor.succesive_position:
                var = Wall(
                    (x, y),
                    f"assets/images/{biome}/{tile_style}/{tile_style}wwww.png",
                    N=True,
                    E=True,
                    S=True,
                    O=True,
                )

                map[y][x] = var


def is_all_corridor_placed(corridor_list):
    """Vérifie que tout les couloirs sont placés en regardant leur
    distance car une distance de -1 signifie qu'un couloirs n'est pas placé"""
    for corridor in corridor_list:
        if corridor.distance_beetween_templates == -1:
            return False
    return True


# === Ajout des templates ===


def verify_template_placement(map, template, x_start, y_start, x=0, y=0) -> bool:
    """Fonction recursive qui verifie que l'emplacement est libre durant la descente
    et qui place les valeurs du template lors de la remontee"""
    # Si il y a autre chose que du vide, on arrete
    if map[y_start + y][x_start + x] != 0:
        return False

    # Si on arrive a la fin : en renvoie True
    if y == len(template) - 1 and x == len(template[0]):
        return True

    # Si on arrive en fin de ligne, on change de ligne en revenant a la colone 0
    if x == len(template[0]):
        x = 0
        y += 1
        booleen = verify_template_placement(map, template, x_start, y_start, x, y)
    # Sinon en verifie que le prochain emplacement de la ligne est libre
    else:
        booleen = verify_template_placement(map, template, x_start, y_start, x + 1, y)
    # Si tout est libre alors on place les elmt du template sur la map
    if booleen:
        map[y_start + y][x_start + x] = template[y][x]
    # Fait remonter le booleen qui indique l'echec ou la reussite du placement
    return booleen


def add_templates_to_map(map: list, templates_list: list):
    """Place les templates sur la map aléatoirement"""
    x, y = 0, 0  # x : colonne, y : ligne
    is_template_placed = False  # Verifie que le template est place
    iteration = 0  # Compte le nombre d'iteration dans la boucle while

    for template in templates_list:  # Place chaque template selon des coordonees random

        while (
            not (is_template_placed) and iteration <= 250
        ):  # 250 est totalement arbitraire
            x = rdm.randint(
                0, len(map[0]) - template.size[0] - 1
            )  # Change les coordonees
            y = rdm.randint(0, len(map) - template.size[1] - 1)
            is_template_placed = verify_template_placement(
                map, template.content, x, y
            )  # Appele la fonction recursive
            iteration += 1
        template.origin = (x, y)  # set l'origine du template

        # supprime le template de la liste de template s'il n'est pas placé
        if not is_template_placed:
            templates_list.remove(template)

        # Reset tout en vue d'un nouveau passage dans la boucle for
        is_template_placed = False
        iteration = 0


# === Génération de la map vide ===


def empty_map_size_finder(template_list) -> tuple:
    """Détermine la taille de la map vide en fonction des templates à placer"""
    height, width = 30, 30  # Un peut de marge ne fait pas de mal ;-)

    for (
        template
    ) in template_list:  # Aggrandit la map en fonction de la taille des templates
        height += (template.size[1] // 5) * 4
        width += (template.size[0] // 5) * 4
    return height, width


def empty_map_generator(template_list: list) -> list:
    # Génère la tilemap de hauteur height et de largeur width
    tuple_w_h = empty_map_size_finder(template_list)
    return [[0 for i in range(tuple_w_h[1])] for j in range(tuple_w_h[0])]


# === Vérifie si la map est possible ===


def verify_is_map_possible(map, template_list):
    """Cherche un chemin entre chaque template (en partant de leur origine)
        Et True si c'est le cas, False sinon

    Args:
        map (list): map avec les templates et les couloirs de placés
        template_list (list): liste des templates placés

    Returns:
        bool: True si tout les templates sont atteignable, False sinon
    """
    for id_first_template in range(len(template_list) - 1):
        for id_second_template in range(id_first_template + 1, len(template_list)):
            if (
                aStar(
                    map,
                    template_list[id_first_template].origin,
                    template_list[id_second_template].origin,
                )
                is None
            ):
                return False
    return True


# === Retirer les Ground de la map ===


def remove_ground_from_map_and_add_to_tilegroup(map: list, tilegroup):
    """Remplace les Ground par des 0 et ajoute les Wall a tilegroup"""
    for y in range(len(map)):
        for x in range(len(map[0])):
            if type(map[y][x]) is Ground:
                map[y][x] = 0
            elif type(map[y][x]) is Wall:
                tilegroup.add(map[y][x])
