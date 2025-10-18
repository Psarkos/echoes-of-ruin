# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
from entity import Entity


class CellSelector(Entity):

    def __init__(self, blue_img, red_img, cell_pos: tuple):
        
        super().__init__(blue_img, cell_pos)
        self.cell_pos = cell_pos  # Position absolue

        # Image
        self.base_blue_image = blue_img  # Garde l'image rouge en memoire
        self.base_red_image = red_img  # Garde l'image bleue en memoire

        self.is_img_blue = True  # Indique quelle est l'image actuelle
        self.alpha = 255

    # ================
    # === METHODES ===
    # ================

    # === SETTERS ===

    def set_alpha(self, value):
        """Permet de changer la transparence de l'image."""
        self.alpha = value
        self.image.set_alpha(value)

    # === DRAW ===

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # === UPDATE ===

    def update(self, camera_gap: tuple, mouse_cell: tuple, mob_cell_pos: tuple):

        # Update la position relative (px) du curseur
        self.rect.topleft = (
            (mouse_cell[0] * 32 + camera_gap[0]) * Entity.zoom,
            (mouse_cell[1] * 32 + camera_gap[1]) * Entity.zoom,
        )

        # Update la position absolue du curseur
        self.cell_pos = mouse_cell

        # Permet de changer l'image si un mob est 'hover' ou non
        if self.is_img_blue:
            if self.cell_pos in mob_cell_pos:
                self.base_image = self.base_red_image
                self.zoom_img()
                self.image.set_alpha(self.alpha)
                self.is_img_blue = False
        else:
            if not self.cell_pos in mob_cell_pos:
                self.base_image = self.base_blue_image
                self.zoom_img()
                self.image.set_alpha(self.alpha)
                self.is_img_blue = True
