# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from entity import Entity

class Exit(Entity, pg.sprite.Sprite):
    
    def __init__(self, image, cell_pos):
        Entity.__init__(self, image, cell_pos)
        pg.sprite.Sprite.__init__(self)
        self.cell_pos = cell_pos

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, self.rect)
            if not self.is_seen : 
                fog = pg.Surface((self.rect.width, self.rect.height))
                fog.set_alpha(100)
                screen.blit(fog, self.rect)
    
    def update(self, camera_gap, player, mode, cell_pos_seen):
        
        Entity.update(self, camera_gap,cell_pos_seen)

        if self.cell_pos == player.current_cell_pos:
            
            player.current_cell_pos = player.previous_cell_pos
            player.is_moving = False
            player.walk_sound.stop()
            return "stash"
        return mode
