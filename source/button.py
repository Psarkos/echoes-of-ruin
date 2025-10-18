# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from text_handler import Text

class ClickableObject:

    is_m1_pressed = False
    is_m3_pressed = False
    mouse_px_pos = (0, 0)

    def __init__(self, rect):

        self.rect: pg.Rect = rect

        # Booleens
        self.__is_hover = False
        self.__is_pressed_with_m1 = False  # Clic Gauche
        self.__is_pressed_with_m3 = False  # Clic Droit

    def check_if_clicked(self) -> tuple[bool, bool, bool]:

        self.__is_hover = False
        self.__is_pressed_with_m1 = False  # Clic Gauche
        self.__is_pressed_with_m3 = False  # Clic Droit

        if self.rect.collidepoint(
            ClickableObject.mouse_px_pos[0], ClickableObject.mouse_px_pos[1]
        ):
            self.__is_hover = True
            if ClickableObject.is_m1_pressed:
                self.__is_pressed_with_m1 = True
            if ClickableObject.is_m3_pressed:
                self.__is_pressed_with_m3 = True

        return (self.__is_hover, self.__is_pressed_with_m1, self.__is_pressed_with_m3)


class Button(ClickableObject):

    def __init__(self, x, y, size:tuple, text:Text="", bg_color:tuple=None):

        self.text = text
        self.image = pg.Surface(size)
        self.bg_color = bg_color

        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_hover = False
        self.is_pressed_with_m1 = False
        self.is_pressed_with_m3 = False

        self.is_active = True
        
        self.resize(size)

        super().__init__(self.rect)
        
    def resize(self, size:tuple):
        self.image = pg.Surface(size)
        self.image.fill(self.bg_color)
        self.image.blit(self.text.image, (self.rect.width // 2- self.text.rect.width//2 , self.rect.height // 2- self.text.rect.height//2))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, screen: pg.Surface):
        if self.is_active:
            screen.blit(self.image, self.rect)

            if self.is_pressed_with_m1:
                pg.draw.rect(screen, (180, 180, 0), self.rect, 4)
            elif self.is_hover:
                pg.draw.rect(screen, (20, 20, 20), self.rect, 4)
            else:
                pg.draw.rect(screen, (20, 20, 20), self.rect, 2)

    def update(self) -> bool:
        if self.is_active:
            self.is_hover, self.is_pressed_with_m1, self.is_pressed_with_m3 = (
                self.check_if_clicked()
            )
            return self.is_pressed_with_m1
