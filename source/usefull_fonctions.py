# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg
import pandas as pd
import os as os

# === FONCTIONS ===
def image_loader(path: str) -> pg.Surface:
    """Permet d'importer des images"""
    return pg.image.load(path)


def scale_by(image: pg.Surface, scale_rate):
    if type(scale_rate) is tuple or type(scale_rate) is list:
        return pg.transform.scale(
            image,
            (image.get_width() * scale_rate[0], image.get_height() * scale_rate[1]),
        )
    else:
        return pg.transform.scale(
            image, (image.get_width() * scale_rate, image.get_height() * scale_rate)
        )


def change_display(WIDTH, HEIGHT, is_window_fullscreen: bool):
    global screen
    if is_window_fullscreen:
        screen = pg.display.set_mode((WIDTH, HEIGHT - 60), flags=pg.RESIZABLE, vsync=1)
    else:
        screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN, vsync=1)


def get_sign_of_number(value):
    if value > 0:
        return "+" + str(value)
    elif value < 0:
        return str(value)
    else:
        return "0"


def get_stat_display_name(key):
    stats_name = {
    "health": " - Santé : ",
    "max_health": " - Santé max : ",
    "defense": " - Defense : ",
    "penetration": " - Penetration : ",
    "movement_time": " - Temps de deplacement : ",
    "attack": " - Attaque : ",
    "attack_range": " - Portée d'attaque : ",
    "attack_speed": " - Interval d'attaque : ",
    "dodge_chance": " - Esquive :",
    "precision": " - Precision : ",
    "block_chance": " - Chance de bloquer :",
    "vision": " - Vision : ",
    }
    return stats_name[key]


def get_equipment_display_name(key):
    equipement_name = {
    "helmet": "Casque",
    "chestplate": "Plastron",
    "pants": "Pentalons",
    "boots": "Bottes",
    "necklace": "Collier",
    "ring": "Anneau",
    "main_weapon": "Arme principale",
    "secondary_weapon": "Arme secondaire",
    "accessory": "Accessoires"
    }
    
    return equipement_name[key]
    
    
def csv_to_list(file_path: str) -> list:
    """Convertit un fichier csv en liste"""
    return (pd.read_csv(file_path).values).tolist()


def get_files_in_directory(directory:str) -> list:
    """
    Trouve le nom des fichiers des un folder
    Il le faut pas un folder dans un folder
    """
    if not os.path.exists(directory):
        raise ValueError(f"Le dossier {directory} n'existe pas.")
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def is_tile_neighbor(co_tile1, co_tile2):
    """ Vérifie si deux cases sont voisine, c'est-à-dire qu'elles se trouvent
        dans les huits cases autour de l'une et de l'autre """
    return (
        abs(co_tile1[0] - co_tile2[0]) <= 1 and 
        abs(co_tile1[0] - co_tile2[0]) <= 1
    )


def create_button(size:tuple, text_size:tuple, *text):
    from button import Button
    from text_handler import Text
    list_button = []
    for txt in text:
        list_button.append(
            Button(
                0,
                0,
                size,
                Text("arial", txt, (0, 0, 0), text_size, (100, 50), is_resizable=False),
                (100, 100, 100),
            )
        )
    return list_button


def scaled_background(background, width, height):
    """Renvoie l'image de fond du menu mise à l'échelle de la fenêtre

    Args:
        width (int): largeur de l'écran
        height (int): heuteur de l'écran

    Returns:
        pygame_surface_Surface: image de fond redimmensionnée
    """
    
    return pg.transform.scale(background, (width, height))


def generate_player():
    """Genere le joueur"""
    from player import Player
    return Player(image_loader("assets/images/entity/player.png"), (0, 0))

def generate_exit():
    from exit import Exit
    return Exit(image_loader("assets/images/entity/Exit.png"), (0,0))

def generate_stash(screen_size, player):
    from stash import Stash
    from inventory import Inventory
    return Stash(Inventory(20), player.inventory, screen_size)


def generate_hud():
    from hud import HUD
    from cursor import CellSelector
    from camera import Camera
    # Images
    BLUE_CELL_SELECTOR = image_loader(
        "assets/images/usefull/select_cell_blue.png"
    )
    RED_CELL_SELECTOR = image_loader(
        "assets/images/usefull/select_cell_red.png"
    )

    # === GENERE LE CURSEUR ===
    cursor = CellSelector(BLUE_CELL_SELECTOR, RED_CELL_SELECTOR, (0, 0))
    cursor.set_alpha(100)

    return (Camera(), cursor, HUD(5, 5, (150, 18)))


def generate_inv_viewer(screen_size, player):
    from inventory_loop import InventoryViewer
    return InventoryViewer(player.inventory, screen_size)


def generate(screen_size):
    player = generate_player()
    stash = generate_stash(screen_size, player)
    inv_viewer = generate_inv_viewer(screen_size, player)
    camera, cursor, hud = generate_hud()
    return player, stash, inv_viewer, camera, cursor, hud
