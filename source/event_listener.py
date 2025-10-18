# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from usefull_fonctions import image_loader


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
