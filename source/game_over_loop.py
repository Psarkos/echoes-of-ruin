# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg

from entity import Entity
from button import ClickableObject
from event_listener import generate_player

pg.init()


# Boucle principale du jeu
def game_over_loop(
    screen: pg.Surface, clock, run, mode, button, text, player, inv_viewer, stash
):

    clock.tick(Entity.FPS)

    ClickableObject.is_m1_pressed = False
    ClickableObject.is_m3_pressed = False

    screen_width, screen_height = screen.get_size()

    button.rect.x = screen_width // 2 - button.rect.width // 2
    button.rect.y = screen_height // 2 - button.rect.height // 2
    button.resize((button.rect.width, button.rect.height))

    text.rect.x = screen_width // 2

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

        if button.update():
            mode = "main_menu"
            player = generate_player()
            inv_viewer.create_view(screen.get_size(), player.inventory)
            stash.create_view(screen.get_size(), player.inventory)

    # Actualisation de l'affichage
    screen.fill("black")
    # Récupération des dimensions actuelles de la fenêtre
    text.draw(screen)
    button.draw(screen)

    pg.display.flip()
    return run, mode, player
