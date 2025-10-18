# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from text_handler import Text
from status_effect import StatusEffect
from entity import Entity
from usefull_fonctions import scale_by


# === DISCLAIMER ===
# Voici les nom des stats du joueur et des mobs :

# "health"           # La vie du joueur

# "defense"          # A quel point les degats sont diminue
# "penetration"      # Diminue la defense lors d'une attaque

# "movement_time"   # Le nombre de point d'action utilises pour faire un deplacement

# "attack"           # L'ataque brut du mob
# "attack_range"     # La portee de l'attaque
# "attack_speed"     # Le nombre de point d'action utilises pour faire une ataque

# "dodge_chance"     # La chance d'esquiver
# "precision"        # Diminue la chance d'esquiver

# "block_chance"     # La chance de bloquer une attaque, plus fort que l'esquive car ne peut pas etre diminuee

# Et voici les emplacements ou peuvent etre equipee les EquipableItem
# "helmet"              # Casque
# "chestplate"          # Corps
# "pants"               # Pentalons
# "boots"               # Bottes
# "necklace"            # Collier
# "ring"                # Anneau
# "main_weapon"         # Arme principale
# "secondary_weapon"    # Arme secondaire
# "accessory"           # Accessoires (ce qui rentre pas dans les autres categories)


class Item:

    def __init__(
        self,
        name: str,
        image: pg.Surface,
        quantity: int,
        max_quantity: int,
        is_stackable: bool,
        dic_stats={},
    ):
        self.name = name
        self.image = image
        self.quantity = quantity
        self.max_quantity = max_quantity
        self.is_stackable = is_stackable
        self.stats = dic_stats

    def add_quantity(self, value: int) -> int:
        """Ajoute la quantite indiquee a la quantite de l'item.

        Retourne le reste si la quantite est trop grande"""
        if self.is_stackable:
            if self.max_quantity >= self.quantity + value:
                self.quantity += value
                return 0
            else:
                value = value - (self.max_quantity - self.quantity)
                self.quantity = self.max_quantity
        return value

    def remove_quantity(self, value: int) -> tuple:
        """Enleve la quantite indiquee a la quantite de l'item.

        Retourne le reste si la quantite est trop grande"""
        if self.quantity - value >= 0:
            self.quantity -= value
            result = (
                Item(
                    self.name,
                    self.image,
                    value,
                    self.max_quantity,
                    self.is_stackable,
                    self.stats,
                ),
                0,
            )
        else:
            value = abs(self.quantity - value)
            result = (
                Item(
                    self.name,
                    self.image,
                    self.quantity,
                    self.max_quantity,
                    self.is_stackable,
                    self.stats,
                ),
                value,
            )
            self.quantity = 0
        return result

    def update(self, *args, **kwargs):
        pass

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name and self.stats == other.stats
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(
            (self.name, self.quantity, self.max_quantity, self.is_stackable, self.stats)
        )


class ConsumableItem(Item):

    def __init__(
        self,
        name: str,
        image: pg.Surface,
        quantity: int,
        max_quantity: int,
        is_stackable: bool,
        effects,
        dic_stats={}
    ):
        super().__init__(name, image, quantity, max_quantity, is_stackable, dic_stats)
        self.effects_list = effects

    def remove_quantity(self, value: int) -> tuple:
        """Enleve la quantite indiquee a la quantite de l'item.

        Retourne le reste si la quantite est trop grande"""
        if self.quantity - value >= 0:
            self.quantity -= value
            result = (
                ConsumableItem(
                    self.name,
                    self.image,
                    value,
                    self.max_quantity,
                    self.is_stackable,
                    [effect.copy() for effect in self.effects_list],
                    self.stats
                ),
                0,
            )
        else:
            value = abs(self.quantity - value)
            result = (
                ConsumableItem(
                    self.name,
                    self.image,
                    self.quantity,
                    self.max_quantity,
                    self.is_stackable,
                    [effect.copy() for effect in self.effects_list],
                    self.stats
                ),
                value,
            )
            self.quantity = 0
        return result

    def use(self):
        """Utilise l'item et retourne les effets qu'il produit"""
        self.quantity -= 1
        return [effect.copy() for effect in self.effects_list]


class EquipableItem(Item):

    def __init__(
        self,
        name: str,
        image: pg.Surface,
        equipement_type: str,
        is_weapon_two_handed: bool = False,
        stats={},
    ):
        # equipement_type est le type de l'item ( chestplate, helmet, main_weapon...)
        # Utile pour savoir ou l'equiper
        super().__init__(name, image, 1, 1, False, stats)

        self.equipement_type = equipement_type
        self.is_weapon_two_handed = is_weapon_two_handed
        self.is_equiped = False

    def get_is_weapon_two_handed(self):  # Work In Progress (WIP)
        return self.is_weapon_two_handed

    def get_equipement_type(self):
        """Retourne le type (helmet, chestplate, main_weapon...)
        de l'equipement"""
        return self.equipement_type
    
    def remove_quantity(self, value: int) -> tuple:
        """Enleve la quantite indiquee a la quantite de l'item.

        Retourne le reste si la quantite est trop grande"""
        value = abs(self.quantity - value)
        result = (
            EquipableItem(
                self.name,
                self.image,
                self.equipement_type,
                self.is_weapon_two_handed,
                self.stats,
            ),
            value,
        )
        self.quantity = 0
        return result


class DropedItem(Entity, pg.sprite.Sprite):

    def __init__(self, item: Item, cell_pos: tuple):

        Entity.__init__(self, item.image, cell_pos)
        pg.sprite.Sprite.__init__(self)

        self.item = item

        self.is_seen = False

        self.zoom_img()
        self.cell_pos = cell_pos

        self.is_hidden = True  # Indique si l'item est caché (ex : par un mob)

    def draw(self, screen: pg.Surface):
        if self.is_seen and not (self.is_hidden):
            screen.blit(
                self.image,
                (self.rect.x + 2 * Entity.zoom, self.rect.y + 2 * Entity.zoom),
            )
            pg.draw.rect(
                screen,
                (180, 180, 60),
                (
                    self.rect.x + 2 * Entity.zoom,
                    self.rect.y + 2 * Entity.zoom,
                    self.rect.width,
                    self.rect.height,
                ),
                1,
            )

    def update(self, player, camera_gap, mob_cell_pos, cell_pos_seen):
        if player.previous_cell_pos == self.cell_pos:
            self.item = player.add_item(self.item)
            if self.item is None:
                self.kill()

        if cell_pos_seen is not None:
            self.is_seen = False
            if self.cell_pos in cell_pos_seen:
                self.is_seen = True

        self.is_hidden = False
        if self.cell_pos in mob_cell_pos:
            self.is_hidden = True
        if self.cell_pos == player.previous_cell_pos:
            self.is_hidden = True

        # Update la position (px) du joueur
        self.rect.topleft = (
            (self.cell_pos[0] * 32 + camera_gap[0]) * Entity.zoom,
            (self.cell_pos[1] * 32 + camera_gap[1]) * Entity.zoom,
        )
