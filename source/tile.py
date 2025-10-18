# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg
from entity import Entity

from usefull_fonctions import image_loader

# ========================
#      CLASSE BLOCK
# ========================


#  === Notes ===
# J'ai pris la liberte de rajouter 2 classes en plus des cellules:
#  - La classe Block qui est une cellule pleine
#  - La classe Ground qui est au contraire une cellule vide
# Je les ais ajoutee afin de nous faciliter la tache plus tard
# et pour que chaque classe puissent avoir leur propre contenue

dic_img = {}




class Block(Entity, pg.sprite.Sprite):
    """Reprensente un objet plein qui ne peut etre traverse"""

    def __init__(
        self,
        cell_pos:tuple,
        image = pg.Surface((32, 32))
    ):
        Entity.__init__(self, image, cell_pos)
        pg.sprite.Sprite.__init__(self)

        self.cell_pos = cell_pos

    # --- Getters ---
    def get_wall(self, arg: str):
        """Renvoie "True" lorsque l'on demande le mur, car un block est forcement plein."""
        return True

    # === UPDATE ===
    def update(self, camera_gap: tuple[int, int], *arg):
        self.rect.x = (self.cell_pos[0] * 32 + camera_gap[0]) * Entity.zoom
        self.rect.y = (self.cell_pos[1] * 32 + camera_gap[1]) * Entity.zoom

    # --- Surcharge d'operateur ---
    def __str__(self) -> str:
        return str(self.rect)

    def __repr__(self):
        return "Block"


# ========================
#      CLASSE GROUND
# ========================


class Ground(Entity, pg.sprite.Sprite):
    """Reprensente un sol vide qui peut etre traverse"""

    def __init__(
        self,
        cell_pos:tuple
    ):
        Entity.__init__(self,pg.Surface((32, 32)), cell_pos)
        pg.sprite.Sprite.__init__(self)

        self.cell_pos = cell_pos
        
        self.image.fill((100, 100, 100, 255))

    # --- Getters ---
    def get_wall(self, arg: str):
        """Renvoie "False" lorsque l'on demande le mur, car un sol est forcement vide."""
        return False

    # === UPDATE ===
    def update(self, camera_gap: tuple[int, int], *arg):
        self.rect.x = (self.cell_pos[0] * 32 + camera_gap[0]) * Entity.zoom
        self.rect.y = (self.cell_pos[1] * 32 + camera_gap[1]) * Entity.zoom

    # --- Surcharge d'operateur ---
    def __str__(self):
        return str(self.rect)

    def __repr__(self):
        return "Ground"


# ========================
#      CLASSE WALL
# ========================


class Wall(Entity, pg.sprite.Sprite):
    """Represente une image de 32x32 representant un morceau du labyrinthe.

    Une cellule possede des murs compris entre 1 et 3 inclus"""

    def __init__(
        self,
        cell_pos:tuple,
        img_link: str,
        N: bool = False,
        E: bool = False,
        S: bool = False,
        O: bool = False,
    ):
        Entity.__init__(self,pg.Surface((32, 32)), cell_pos)
        pg.sprite.Sprite.__init__(self)
        self.img_link = img_link

        self.walls = {"N": N, "E": E, "S": S, "O": O}

        self.image_setter(self.img_link)
    # --- Getters ---
    def get_wall(self, string: str):
        """Renvoie la valeur du mur demande"""
        return self.walls[string]

    def get_pos(self):
        return self.rect.x, self.rect.y

    # --- Setters ---
    def image_setter(self, img_link):
        self.img_link = img_link
        if img_link not in  dic_img.keys():
            dic_img[img_link] = image_loader(img_link)
        self.image = dic_img[img_link]
        self.base_image = self.image

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, self.rect)
            if not self.is_seen:
                fog = pg.Surface((self.rect.width, self.rect.height))
                fog.set_alpha(100)
                screen.blit(fog, self.rect)

    # --- Surcharge d'operateur ---
    def __str__(self) -> str:
        return str(self.rect)

    def __repr__(self):
        return "Wall"
