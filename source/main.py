# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg


# TODO :
# Fix la camera
# Fix les previous pos


# Importation des fichiers secondaires
from text_handler import Text
from usefull_fonctions import (
    generate_player,
    generate_exit,
    generate_hud,
    generate_inv_viewer,
    generate_stash,
    create_button,
)

from inventory_loop import inventory_view_loop
from level_generator import generate_level
from game_loop import game_loop
from menu_loop import menu_loop
from settings_loop import settings_loop
from stash import stash_loop
from game_over_loop import game_over_loop
from pause_loop import pause_loop
from level_editor_tut import level_editor_loop

# === INIT PYGAME ===
pg.init()
pg.mixer.init()

info_object = pg.display.Info()
# Constantes
WIDTH, HEIGHT = info_object.current_w, info_object.current_h  # Taille de la fenetre

# Creation de la fenetre
pg.display.set_caption("Echoes of Ruin")


screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN, vsync=1)
FPS = 60


# =========================
# === BOUCLE PRINCIPALE ===
# =========================
def main():

    # === PRELIMINAIRES ===
    run = True  # Booleen permetant au jeu de tourner
    clock = pg.time.Clock()  # Permet de limiter le framerate

    # === VARIABLES ===
    # Creation des boutons
    button_list_main_menu = create_button(
        (400, 100), (40, 40), "Jouer", "Parametres", "Editeur de niveaux", "Quitter"
    )
    button_list_settings = create_button(
        (400, 100), (40, 40), "Plein Ecran", "Fenetré", "Retour"
    )
    button_pause_list = create_button(
        (400, 100), (40, 40), "Reprendre", "Menu principal"
    )

    button_game_over = create_button((400, 100), (40, 40), "Menu principal")[0]

    # Creation des textes
    text_game_over = Text(
        "arial", "Vous êtes mort.", (180, 20, 20), (50, 50), (0, 50), is_resizable=False
    )
    text_map_generator = Text(
        "arial", "Chargement", (180, 20, 20), (50, 50), (0, 100), is_resizable=False
    )

    # Creation des groupes
    tile_group = pg.sprite.Group()
    enemy_group = pg.sprite.Group()
    dropped_item_group = pg.sprite.Group()
    text_group = pg.sprite.Group()

    # Garder la position des mobs
    mob_cell_pos = []

    camera_gap = None

    # Creation des objets permanents
    player = generate_player()
    exit = generate_exit()
    stash = generate_stash(screen.get_size(), player)
    camera, cursor, hud = generate_hud()
    inv_viewer = generate_inv_viewer(screen.get_size(), player)

    # Mode
    mode = "main_menu"

    # Booleens
    is_map_editor = False
    is_refresh = False
    is_level_created = False

    ambiance_sound = pg.mixer.music.load("assets/sons/ambiances/Catacombs.mp3")

    # =========================
    # === BOUCLE PRINCIPALE ===
    # =========================

    while run:
        match mode:
            case "main_menu":
                run, mode, is_refresh = menu_loop(
                    screen, clock, run, mode, button_list_main_menu, is_refresh
                )
                is_level_created = False

            case "settings":
                run, mode = settings_loop(
                    screen, clock, run, mode, button_list_settings
                )

            case "game":
                run, mode, camera_gap = game_loop(
                    screen,
                    clock,
                    camera,
                    player,
                    cursor,
                    tile_group,
                    text_group,
                    enemy_group,
                    dropped_item_group,
                    mob_cell_pos,
                    camera_gap,
                    hud,
                    exit,
                    stash,
                )

            case "inventory":
                run, mode = inventory_view_loop(screen, clock, inv_viewer, player)

            case "generate_level":
                (
                    mode,
                    is_level_created,
                ) = generate_level(
                    screen,
                    text_map_generator,
                    dropped_item_group,
                    enemy_group,
                    tile_group,
                    text_group,
                    player,
                    exit,
                    mob_cell_pos
                )

                player_px_pos = player.get_px_pos()
                camera_gap = (
                    player_px_pos[0] // 2,
                    player_px_pos[1] // 2,
                )  # Correspond au decalage total cause par la camera (en px)

            case "stash":
                run, mode, is_refresh = stash_loop(
                    screen,
                    clock,
                    stash,
                    player,
                    inv_viewer,
                    is_refresh,
                    is_level_created
                )

            case "game_over":
                run, mode, player = game_over_loop(
                    screen,
                    clock,
                    run,
                    mode,
                    button_game_over,
                    text_game_over,
                    player,
                    inv_viewer,
                    stash,
                )
                is_level_created = False

            case "pause":
                run, mode, player = pause_loop(
                    screen,
                    clock,
                    run,
                    mode,
                    button_pause_list,
                    player,
                    inv_viewer,
                    stash,
                )

            case "level_editor":
                run, mode = level_editor_loop()

            case _:
                run = False

    pg.quit()  # Ferme la fenetre si la boucle while s'arrete
    if is_map_editor:
        level_editor_loop()


if __name__ == "__main__":
    main()
