# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
from usefull_fonctions import scale_by


class Entity:

    # Variable de class
    # Permet de partager des variables entre TOUTES les instances de la class
    # Pour cela il faut faire <NomClass>.<variable> et non self.<variable>

    FPS = 60
    MAP = [[]]

    zoom = 1
    screen_ratio = (1, 1)
    is_resize = False
    is_changing_zoom = False

    def __init__(self, image, cell_pos, px_pos:tuple=None):

        self.base_image = image
        self.image = self.base_image
        if px_pos is None :
            self.rect = self.image.get_rect(topleft=(cell_pos[0]*32, cell_pos[1]*32))
            self.cell_pos = cell_pos
        else:
            self.rect = self.image.get_rect()
            self.rect.topleft = px_pos
            self.cell_pos = (px_pos[0]//32, px_pos[1]//32)
            
        self.is_seen = False
        self.is_active = False

    def zoom_img(self):
        """Permet de changer la taille des images lors d'un zoom"""
        self.image = scale_by(self.base_image, Entity.zoom)
        self.rect = self.image.get_rect()

    def resize(self):
        """Permet de changer la taille des images lors d'un zoom"""
        self.image = scale_by(
            scale_by(self.base_image, Entity.screen_ratio), Entity.zoom
        )
        self.rect = self.image.get_rect(
            topleft=(
                self.rect.x * Entity.screen_ratio[0],
                self.rect.y * Entity.screen_ratio[1],
            )
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, camera_gap, cell_pos_seen):
        
        if cell_pos_seen is not None:
            self.is_seen = False
            if self.cell_pos in cell_pos_seen:
                self.is_seen = True
                self.is_active = True
                
        self.rect.topleft = (
            (self.cell_pos[0]*32 + camera_gap[0]) * Entity.zoom,
            (self.cell_pos[1]*32 + camera_gap[1]) * Entity.zoom,
        )
