# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from text_handler import Text
from bar import Bar


class HUD:

    zoom = 1.5

    def __init__(self, x, y, size_bar):

        self.x, self.y = x, y
        self.width, self.height = size_bar[0] * HUD.zoom, size_bar[1] * HUD.zoom

        self.health_text = Text(
            "arial",
            "Vie : ",
            (255, 255, 255),
            (self.height, self.height),
            (self.x + 10, self.y + 10),
            is_border=True,
            is_resizable=False,
            is_text_centered=False,
        )
        self.health_bar = Bar(
            self.x + 10 + self.health_text.image.get_width(),
            self.y + 10,
            (self.width, self.height),
            "green",
            "red",
        )

    def draw(self, screen):
        self.health_bar.draw(screen)
        self.health_text.draw(screen)

    def update(self, health, max_health):
        self.health_bar.update(health, max_health)
