# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from counter import Counter
from usefull_fonctions import scale_by
from entity import Entity
pg.font.init()


# Code de add_outline_to_image (modifie) venant d'un post sur la page 
# https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame


def add_outline_to_image(image: pg.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pg.Surface:
    mask = pg.mask.from_surface(image)
    if color == (0,0,0):
        color = (1,1,1)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pg.Surface((image.get_width() + 2*thickness, image.get_height() + 2*thickness))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    new_img.blit(mask_surf, (0, thickness))
    new_img.blit(mask_surf, (thickness, 0))
    new_img.blit(mask_surf, (2*thickness, thickness))
    new_img.blit(mask_surf, (thickness, 2*thickness))

    new_img.blit(image, (thickness, thickness))

    return new_img



class Text(Entity, pg.sprite.Sprite):
    """Permet d'afficher du text.
    
    font = Police du text
    
    size ( en px )
    
    movement = tuple qui indique le decalage du text chaque frame
    
    duration = duree de vie du text avant qu'il ne disparaisse

    border = affiche une bordure de la couleur donne dans border_color

    is_text_fadding = Indique si le text disparait au cours du temps
    
    antialias = Permet d'empecher que le text soit pixelise
    
    """

    def __init__(self,
            font:str, 
            text:str, 
            color:tuple, 
            size:tuple[int, int],
            px_pos:tuple[int, int],
            movement:tuple[int, int]=(0, 0),
            duration:int=None,
            is_text_centered:bool=True,
            is_border:bool=False,
            border_color:tuple=(0,0,0),
            is_text_fadding:bool=False,
            antialias:bool=False,
            is_resizable:bool=True
            ):
        
        # --- Init ---
        
        self.text = str(text)
        self.size = size
        self.is_text_fadding = is_text_fadding
        self.is_text_centered = is_text_centered
        self.is_border = is_border
        self.is_resizable = is_resizable

        # --- Font ---
        if self.is_resizable :
            self.font = pg.font.SysFont(font,round(size[1]*Entity.zoom))
        else:
            self.font = pg.font.SysFont(font,round(size[1]))
        if self.is_border :
            self.border_font = pg.font.SysFont(font, round(size[1]), True)

        # --- Rect/Position ---
        
        self.px_pos = px_pos
        self.movement = movement
        self.dx, self.dy = 0, 0

        Entity.__init__(self, self.font.render(text, antialias, color).convert_alpha(), (0,0), px_pos)
        pg.sprite.Sprite.__init__(self)
        
        # --- Image ---
        if self.is_border :
            self.image = add_outline_to_image(self.image, 1, border_color)

        # --- Duration ---
        if duration is not None :
            self.duration = duration
            self.counter = Counter(duration)
            self.counter.start()
    
        
    # ================
    # === METHODES ===
    # ================

    # === ZOOM ===
    def zoom_img(self):
        if self.is_resizable:
            """Permet de changer la taille des images lors d'un zoom"""
            if self.is_text_centered :
                self.image = pg.transform.scale(
                                        self.image, 
                                        (len(self.text)*round(self.size[0]*Entity.zoom), 
                                        round(self.size[1]*Entity.zoom))
                                        )
            else :
                self.image = scale_by(self.image, Entity.zoom)

    def draw(self, screen:pg.Surface):
        if self.is_text_centered :
            screen.blit(self.image, (self.rect.x - self.rect.width //2, self.rect.y))
        else :
            screen.blit(self.image, self.rect)

    # === UPDATE ===
    def update(self, deltatime:float, camera_gap:tuple[int, int]):
        if self.duration is not None :
            if self.counter.update(deltatime) :
                self.kill()
            if self.is_text_fadding :
                self.image.set_alpha(round(255*self.counter.get_time_left()/self.duration))

        self.dx += self.movement[0]
        self.dy += self.movement[1]

        self.rect.topleft = (
            (self.px_pos[0] + self.dx + camera_gap[0])*Entity.zoom,
            (self.px_pos[1] + self.dy + camera_gap[1])*Entity.zoom
        )




class TextHandler():
    """Permet de gerer les text affin d'eviter qu'ils se superpose"""

    def __init__(self):
        self.text_list = []             # Contient tout les text
        self.updatable_text_list = []   # Contient seulement les texts qui peuvent etre update
        self.interval_btw_text = 0.3    # Interval de temps avant qu'un nouveau text puisse etre updatable
        self.counter = Counter(self.interval_btw_text)
        self.counter.start()

    def add_text(self, text:Text):
        self.text_list.append(text)
    
    def clear_updatable_text_list(self):
        self.updatable_text_list.clear()

    def get_updatable_text(self) -> list:
        return self.updatable_text_list

    def update(self, deltatime:float):
        if self.counter.update(deltatime):
            if len(self.text_list) > 0 :
                self.counter.start()
                self.updatable_text_list.append(self.text_list[0])
                self.text_list.remove(self.text_list[0])