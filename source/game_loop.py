# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from button import ClickableObject
from entity import Entity
from player import Player
from tile import Wall
from hud import HUD


def game_loop(
    screen,
    clock,
    camera,
    player: Player,
    cursor,
    tile_group,
    text_group,
    enemy_group,
    droped_item_group,
    mob_cell_pos,
    camera_gap,
    hud,
    exit,
    stash
):
    # =====================
    # === PRELIMINAIRES ===
    # =====================

    ClickableObject.is_m1_pressed = False
    ClickableObject.is_m3_pressed = False

    run = True
    mode = "game"
    is_changing_camera_mode = False

    # --- CLOCK ET DELTATIME ---
    deltatime = (
        clock.tick(Entity.FPS) * 0.001
    )  # Garantit un deplacement en pixel/sec constant

    # --- Interaction entre entites ---
    player_attack_data = None

    # ==============
    # === INPUTS ===
    # ==============
    key_pressed = pg.key.get_pressed()  # Recupere les touches pressees
    # Recupere la position de la sourie
    # Recupere la position absolue de la souris (sera utile quand on aura des boutons a clic)
    abs_mouse_pos = pg.mouse.get_pos()
    # Recupere la position relative a camera_gap (utile pour le pathfinder)
    relative_mouse_pos = (
        abs_mouse_pos[0] - (camera_gap[0]) * Entity.zoom,
        abs_mouse_pos[1] - (camera_gap[1]) * Entity.zoom,
    )
    mouse_cell = player.current_cell_pos
    if relative_mouse_pos[0] >= 0 and relative_mouse_pos[1] >= 0:
        mouse_cell = relative_mouse_pos[0] // (32 * Entity.zoom), relative_mouse_pos[
            1
        ] // (32 * Entity.zoom)

    # ==============
    # === EVENTS ===
    # ==============

    # === MAIN EVENT ===
    # Event qui doivent etre constement actifs
    for event in pg.event.get():  # Recupere tous les event chaque frame
        if event.type == pg.QUIT:  # Permet de fermet la fenetre
            run = False

        # === CLAVIER ===
        if event.type == pg.KEYDOWN:

            # --- PAUSE ---
            # Change le mode en pause
            if event.key == pg.K_ESCAPE:
                mode = "pause"

            # --- CAMERA ---
            # Change entre la camera libre et la camera centre sur le joueur
            if event.key == pg.K_SPACE:
                if camera.get_is_camera_free():
                    camera.toggle_camera_on_player(screen, player.rect.topleft)
                else:
                    camera.toggle_free_camera()
                is_changing_camera_mode = True

            if event.key == pg.K_e:
                mode = "inventory"

            # --- ZOOM ---
            # Zoom in
            if event.key == pg.K_UP:
                if Entity.zoom <= 4:
                    Entity.zoom += 1
                    Entity.is_changing_zoom = True

            # Zoom out
            if event.key == pg.K_DOWN:
                if Entity.zoom > 1:
                    Entity.zoom -= 1
                    Entity.is_changing_zoom = True

        # === SOURIE ===
        # Set le nouveau point de depart du pathfinder lors d'un clic sourie
        if event.type == pg.MOUSEBUTTONDOWN:
            if 0 <= mouse_cell[0] < len(Entity.MAP[0]) and 0 <= mouse_cell[1] < len(
                Entity.MAP
            ):

                if event.button == 3:  # Clic droit
                    if type(Entity.MAP[mouse_cell[1]][mouse_cell[0]]) is Wall:
                        if Entity.MAP[mouse_cell[1]][mouse_cell[0]].is_active:
                            player.end_pos = mouse_cell
                            player.is_moving = True

                if event.button == 1:  # Clic Gauche
                    if mouse_cell in mob_cell_pos:
                        player_attack_data = player.attack_a_mob(mouse_cell)

    # ==========================
    # === UPDATE LES SPRITES ===
    # ==========================

    # === CAMERA ===
    if camera.get_is_camera_free():
        camera_gap = camera.update(screen, key_pressed, deltatime)
    else:
        camera_gap = camera.update(screen, key_pressed, deltatime, player.rect.topleft)

    # === PLAYER ===
    # S'il y a un zoom
    if Entity.is_changing_zoom:
        player.zoom_img()
    action_points, cell_pos_seen = player.update(
        deltatime, camera_gap, mob_cell_pos, text_group
    )

    # === TILE ===
    for tile in tile_group:
        # S'il y a un zoom
        if Entity.is_changing_zoom:
            tile.zoom_img()
            
        tile.update(camera_gap, cell_pos_seen)
    
    # === EXIT ===
    if Entity.is_changing_zoom:
        exit.zoom_img()
    mode = exit.update(camera_gap, player, mode, cell_pos_seen)

    # === DROPED ITEMS ===
    for droped_item in droped_item_group:
        # S'il y a un zoom
        if Entity.is_changing_zoom:
            droped_item.zoom_img()
        droped_item.update(player, camera_gap, mob_cell_pos, cell_pos_seen)

    # === ENEMY ===
    # Update chaque enemy du group
    for enemy in enemy_group:
        # Si le enemy a pris des degats
        if player_attack_data is not None and enemy.get_current_cell() == mouse_cell:
            enemy.take_damage(player_attack_data)

        # S'il y a un zoom
        if Entity.is_changing_zoom:
            enemy.zoom_img()

        # --- Update le enemy ---
        previous_pos, mob_attack_data = enemy.update(
            deltatime,
            camera_gap,
            player.current_cell_pos,
            action_points,
            mob_cell_pos,
            text_group,
            droped_item_group,
            cell_pos_seen,
        )

        # Change les positions des enemys dans mob_coordinates
        if previous_pos is not None and previous_pos in mob_cell_pos:
            mob_cell_pos.remove(previous_pos)
            if enemy.get_is_alive():
                mob_cell_pos.append(enemy.get_current_cell())
        # Gere les attaque vers le joueur
        if mob_attack_data[0] is not None:
            # Applique les degats au joueur
            player.take_damage(mob_attack_data)

    # === TEXTGROUP ===
    # S'il y a un zoom
    if Entity.is_changing_zoom:
        for text in text_group:
            text.zoom_img()
    text_group.update(deltatime, camera_gap)

    # === CURSOR ===
    # S'il y a un zoom
    if Entity.is_changing_zoom:
        cursor.zoom_img()
    cursor.update(camera_gap, mouse_cell, mob_cell_pos)

    # === HUD ===
    hud.update(player.dic_stats["health"], player.dic_stats["max_health"])

    # ========================
    # === DRAW LES SPRITES ===
    # ========================

    # Permet de skip la frame que la camera a besoins pour se màj
    # J'ai rien trouve d'autre pour l'instant, dsl
    if not Entity.is_changing_zoom and not is_changing_camera_mode:
        screen.fill("black")

        for tile in tile_group:
            tile.draw(screen)

        player.draw(screen)

        for droped_item in droped_item_group:
            droped_item.draw(screen)

        for enemy in enemy_group:
            enemy.draw(screen)

        for text in text_group:
            text.draw(screen)
        cursor.draw(screen)
        hud.draw(screen)
        exit.draw(screen)
    else:
        Entity.is_changing_zoom = False

    if player.dic_stats["health"] <= 0:
        player.walk_sound.stop()
        mode = "game_over"
        
    if mode =="stash":
        stash.create_view(screen.get_size(), player.inventory)

    if mode != "game":
        player.walk_sound.stop()
        
    pg.display.update()  # Permet d'afficher les changements faits dans la boucle
    return run, mode, camera_gap
