# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from text_handler import Text


class Bar:

    def __init__(
        self, x, y, size, bar_color, bg_color, border_color=(0, 0, 0), border_size=1
    ):
        self.bar_color = bar_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_size = border_size
        self.size = size

        self.is_active = True

        self.x, self.y = x, y
        self.width, self.height = size

        self.ratio = 1

        self.text = None
        self.value = 0
        self.max_value = 0

    def draw(self, screen):
        if self.is_active:
            pg.draw.rect(
                screen, self.bg_color, (self.x, self.y, self.width, self.height)
            )
            pg.draw.rect(
                screen,
                self.bar_color,
                (self.x, self.y, self.width * self.ratio, self.height),
            )
            pg.draw.rect(
                screen, self.border_color, (self.x, self.y, self.width, self.height), 1
            )
            self.text.draw(screen)

    def update(self, value, max_value):

        if self.value != value or self.max_value != max_value:

            self.value = value
            self.max_value = max_value

            if self.value > self.max_value:
                self.value = self.max_value
            if self.value < 0:
                self.value = 0

            self.text = Text(
                "arial",
                str(self.value) + "/" + str(self.max_value),
                (250, 250, 250),
                (self.height - 4, self.height - 4),
                (self.x + 2, self.y + 2),
                is_resizable=False,
                is_text_centered=False,
                is_border=True,
            )

        if 1 >= value / max_value >= 0:
            self.ratio = value / max_value
        elif value / max_value > 1:
            self.ratio = 1
        else:
            self.ratio = 0
