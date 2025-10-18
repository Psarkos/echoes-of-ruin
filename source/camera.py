# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from entity import Entity


class Camera(Entity):

    def __init__(self):
        self.is_camera_free = True
        self.camera_gap = (0, 0)
        self.screen_width = None
        self.screen_height = None
        self.previous_zoom = Entity.zoom

    def toggle_free_camera(self):
        """Permet de se balader en camera libre"""
        self.is_camera_free = True

    def toggle_camera_on_player(self, screen: pg.Surface, player_pos: tuple[int, int]):
        """Centre la camera sur le joueur"""
        self.camera_gap = (
            player_pos[0] // self.previous_zoom,
            player_pos[1] // self.previous_zoom,
        )
        self.is_camera_free = False
        self.previous_zoom = Entity.zoom

    def get_is_camera_free(self):
        """Indique si la camera est libre"""
        return self.is_camera_free

    def update(
        self,
        screen: pg.Surface,
        key_pressed,
        deltatime: float,
        player_pos: tuple[int, int] = (0, 0),
    ) -> tuple[int, int]:
        """Retourne le tuple camera_gap utilisé dans le positionement des elmts"""

        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

        if self.is_camera_free:
            # Permet de se deplacer en camera libre sur la map
            # Ce n est qu une illusion car on decale en realite tous les elmt vers la direction inverse
            camera_movement = [0.0, 0.0]
            camera_speed = (
                300 * deltatime
            )  # Vitesse de la camera en pixel/sec (300px/sec)
            camera_speed_boost = 1  # Permet de boost la vitesse de la camera
            if key_pressed[pg.K_LSHIFT]:
                camera_speed_boost = 2
            if key_pressed[
                pg.K_z
            ]:  # Ce qui entre crochet est la touche demandee, le tout est un booleen
                camera_movement[1] += camera_speed * camera_speed_boost
            if key_pressed[pg.K_s]:
                camera_movement[1] -= camera_speed * camera_speed_boost
            if key_pressed[pg.K_q]:
                camera_movement[0] += camera_speed * camera_speed_boost
            if key_pressed[pg.K_d]:
                camera_movement[0] -= camera_speed * camera_speed_boost
            self.camera_gap = (
                round(self.camera_gap[0] + camera_movement[0]),
                round(self.camera_gap[1] + camera_movement[1]),
            )
            return (self.camera_gap[0], self.camera_gap[1])

        else:
            # Camera centree sur le joueur
            self.camera_gap = (
                self.camera_gap[0]
                - player_pos[0] // Entity.zoom
                + (self.screen_width // 2) // Entity.zoom,
                self.camera_gap[1]
                - player_pos[1] // Entity.zoom
                + (self.screen_height // 2) // Entity.zoom,
            )

            return self.camera_gap
