# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg

from entity import Entity
from button import Button, ClickableObject
from usefull_fonctions import image_loader, scaled_background

pg.init()

bg_img = image_loader("assets/images/background/castle.png")

# Boucle principale du jeu
def menu_loop(screen:pg.Surface, clock, run, mode, button_list, is_refresh):
    
    clock.tick(Entity.FPS)
    # Récupération des dimensions actuelles de la fenêtre
    screen_width, screen_height = screen.get_size()
    
    for i, button in enumerate(button_list):
        button.rect.x = screen_width // 2 - button.rect.width //2
        button.rect.y = screen_height // 3 - button.rect.height //2 + i * 150
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

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = False
            if event.button == 3:  # Clic Gauche
                ClickableObject.is_m3_pressed = False
    
        if button_list[0].update():
            mode = "stash"
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(1)
            ClickableObject.is_m1_pressed = False
            is_refresh = True
        if button_list[1].update():
            mode = "settings"
            ClickableObject.is_m1_pressed = False
        if button_list[2].update():
            mode = "level_editor"
            ClickableObject.is_m1_pressed = False
        if button_list[3].update():
            run = False
    
    # Affichage du fond d'écran
    screen.blit(scaled_background(bg_img, screen_width, screen_height), (0,0))
    
    # Actualisation de l'affichage
    for button in button_list:
        button.draw(screen)
    
    pg.display.flip()
    return run, mode, is_refresh
