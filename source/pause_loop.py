# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg

from entity import Entity
from button import ClickableObject
from usefull_fonctions import generate_player


def pause_loop(
    screen: pg.Surface, clock, run, mode, button_list, player, inv_viewer, stash
):

    clock.tick(Entity.FPS)

    screen_width, screen_height = screen.get_size()

    for i, button in enumerate(button_list):
        button.rect.x = screen_width // 2 - button.rect.width // 2
        button.rect.y = screen_height // 2 - button.rect.height // 2 + i * 150
        button.resize((button.rect.width, button.rect.height))

    # Récupération des dimensions actuelles de la fenêtre
    screen_width, screen_height = screen.get_size()

    for button in button_list:
        button.rect.x = screen_width // 2 - button.rect.width // 2
        button.resize((button.rect.width, button.rect.height))

    # Gestion des événements (fermeture, clics, etc.)
    ClickableObject.mouse_px_pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = True
            if event.button == 3:  # Clic Gauche
                ClickableObject.is_m3_pressed = True

        if button_list[0].update():
            mode = "game"
            ClickableObject.is_m1_pressed = False
        if button_list[1].update():
            mode = "main_menu"
            player = generate_player()
            inv_viewer.create_view(screen.get_size(),player.inventory)
            stash.create_view(screen.get_size(),player.inventory)
            ClickableObject.is_m1_pressed = False

    # Actualisation de l'affichage
    screen.fill("black")
    # Récupération des dimensions actuelles de la fenêtre
    screen.fill("black")
    for button in button_list:
        button.draw(screen)

    pg.display.flip()
    return run, mode, player
