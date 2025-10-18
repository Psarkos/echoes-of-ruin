# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg

from entity import Entity
from button import ClickableObject
from usefull_fonctions import change_display, image_loader, scaled_background

pg.init()

bg_img = image_loader("assets/images/background/castle.png")

# Boucle principale du jeu
def settings_loop(screen:pg.Surface, clock, run, mode, button_list):
    
    clock.tick(Entity.FPS)
    
    ClickableObject.is_m1_pressed = False
    ClickableObject.is_m3_pressed = False
    
    
    # Récupération des dimensions actuelles de la fenêtre
    screen_width, screen_height = screen.get_size()
    
    for i, button in enumerate(button_list):
        button.rect.x = screen_width // 2 - button.rect.width //2
        button.rect.y = screen_height // 2 - button.rect.height //2 + i * 150
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
            change_display(screen_width, screen_height, False)
        if button_list[1].update():
            change_display(screen_width, screen_height, True)
        if button_list[2].update():
            mode = "main_menu"
            ClickableObject.is_m1_pressed = False
            
    # Actualisation de l'affichage
    screen.fill("black")
    # Récupération des dimensions actuelles de la fenêtre
    screen.blit(scaled_background(screen,screen_width, screen_height), (0, 0))
    for button in button_list:
        button.draw(screen)
    
    pg.display.flip()
    return run, mode
