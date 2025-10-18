# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg
import random as rd

from pathfinder import aStar
from status_effect import StatusEffectsHandler, StatusEffect
from entity import Entity
from inventory import Inventory
from counter import Counter
from text_handler import Text, TextHandler
from usefull_fonctions import get_signed_number, get_stat_display_name
from ray_caster import is_case_lookable


class Player(Entity):

    def __init__(self, image, cell_pos: tuple):

        super().__init__(image, cell_pos)
        # === Init ===

        self.current_cell_pos = cell_pos
        self.previous_cell_pos = self.current_cell_pos

        # === Pathfinder ===

        self.path = []  # Chemin vers cible
        self.temp_path = (
            []
        )  # Nouveau chemin stocké temporairement. Rend l'animation fluide
        self.is_moving = False  # Indique si le joueur bouge
        self.is_on_cell = True  # Verifie si le joueur est sur une celule ou entre 2
        self.end_pos = self.current_cell_pos  # Garde en memoire la position a atteindre

        # === Moving animation ===

        self.base_moving_time = 0.16  # En seconde
        self.counter = Counter(self.base_moving_time)
        self.dx, self.dy = (
            0,
            0,
        )  # Correspond au decalage par frame pour l'animation de deplacements

        # === BASE STATS ===

        # Correspond aux stats avant que les items les changent
        self.dic_base_stats = {
            # --- Health ---
            "health": 100,  # La vie du joueur
            "max_health": 100,
            # --- Defense ---
            "defense": 0,
            # --- Movement speed ---
            "movement_time": 100,  # Le nombre de point d'action utilises pour faire un deplacement
            # --- Attack ---
            "attack": 30,  # L'ataque brut du mob
            "attack_range": 2,
            "attack_speed": 50,  # Le nombre de point d'action utilises pour faire une ataque
            "penetration": 0,
            # --- Dodge/Block ---
            "dodge_chance": 0,
            "block_chance": 0,
            # --- Precision ---
            "precision": 0,
            # --- Vision ---
            "vision": 6,
        }

        # === STATS ===

        # Correspond aux stats apres que les items les changent
        self.dic_stats = {
            "health": self.dic_base_stats["health"],
            "max_health": self.dic_base_stats["max_health"],
            "defense": self.dic_base_stats["defense"],
            "movement_time": self.dic_base_stats["movement_time"],
            "attack": self.dic_base_stats["attack"],
            "attack_range": self.dic_base_stats["attack_range"],
            "attack_speed": self.dic_base_stats["attack_speed"],
            "penetration": self.dic_base_stats["penetration"],
            "dodge_chance": self.dic_base_stats["dodge_chance"],
            "block_chance": self.dic_base_stats["block_chance"],
            "precision": self.dic_base_stats["precision"],
            "vision": self.dic_base_stats["vision"],
        }

        # Correspond aux stats apres que les effets les changent

        self.is_attacking = False

        # === INVENTAIRE ET EFFETS===
        self.inventory = Inventory(10)
        self.effects_handler = StatusEffectsHandler()

        # === TEXT ===
        self.text_list = TextHandler()
        
        
        # === SOUND ===
        self.is_walk_sound_active = False
        self.walk_sound = pg.mixer.Sound("assets/sons/sfx/Walk.mp3")

    # |||================|||
    # |||=== METHODES ===|||
    # |||================|||

    # =================================
    # === PATHFINDER ET DEPLACEMENT ===
    # =================================

    def find_path(self, mob_coordinates=[]):
        """Trouve le chemin le plus court entre la position du joueur et la cible"""
        var = aStar(Entity.MAP, self.current_cell_pos, self.end_pos, mob_coordinates)
        if var is not None:  # Si le chemin existe
            self.path = var[1:]
            return len(self.path) > 0
        else:
            return False

    # --- Getters ---

    def get_px_pos(self):
        """Retourne la position du joueur (en px)"""
        return self.rect.topleft

    # =================================
    # === INTERACTION ENTRE ENTITES ===
    # =================================

    def get_raw_attack(self):
        return self.dic_stats["attack"]

    def get_range(self):
        return self.dic_stats["attack_range"]

    def get_is_alive(self):
        return self.dic_stats["health"] > 0

    def attack_a_mob(self, mob_pos: tuple):
        """Fait l'action d'ataquer.

        Retourne None si n'est pas a portee
        """
        if (
            self.dic_stats["attack_range"] > 1
            and abs(self.current_cell_pos[0] - mob_pos[0])
            + abs(self.current_cell_pos[1] - mob_pos[1])
            <= self.dic_stats["attack_range"]
            or abs(self.current_cell_pos[0] - mob_pos[0])
            <= self.dic_stats["attack_range"]
            <= 1
            and abs(self.current_cell_pos[1] - mob_pos[1])
            <= self.dic_stats["attack_range"]
            <= 1
        ):
            if is_case_lookable(
                Entity.MAP, 
                self.current_cell_pos, 
                mob_pos
            ):
                self.is_attacking = True
                self.is_moving = False
                return (
                    self.dic_stats["attack"],
                    self.dic_stats["penetration"],
                    self.dic_stats["precision"],
                )
        return None

    def take_damage(self, attack_data):
        """Aplique les degats brute.

        Retourne les degats reelement infliges"""
        raw_damage = attack_data[0]
        penetration = attack_data[1]
        precision = attack_data[2]
        # Arrete le joueur
        self.is_moving = False
        # Dodge
        rd_int = rd.randint(0, 99)
        if not rd_int < self.dic_stats["dodge_chance"] - precision:
            # Block
            rd_int = rd.randint(0, 99)
            if not rd_int < self.dic_stats["block_chance"]:
                # Applique les degats
                damage = -round(
                    raw_damage
                    - raw_damage
                    * max((self.dic_stats["defense"] - penetration), 0)
                    * 0.01
                )
                self.dic_stats["health"] += damage
                text = damage
            else:
                text = "Blocked"
        else:
            text = "Dodged"
        self.text_list.add_text(
            Text(
                "arial",
                str(text),
                (255, 0, 0),
                (10, 10),
                (self.previous_cell_pos[0] * 32 + 16, self.previous_cell_pos[1] * 32),
                movement=(0, -1.5),
                duration=1,
                is_border=True,
                is_text_fadding=True,
            )
        )

    # ============================
    # === INVENTORY ET EFFECTS ===
    # ============================

    # === INVENTORY ===

    def add_item(self, item):
        """Ajoute l'item a l'inventaire s'il y a de la place.

        La fonction priorise le stackage et ajoute le reste dans une nouvelle case."""
        return self.inventory.add_item(item)

    def remove_item(self, item_name: str, quantity: int = 1):

        return self.inventory.remove_item(item_name, quantity)

    def equip_item(self, item_index):
        """Change les stats du joueur en fonction de l'item equipee"""
        # Recupere les infos de l'item dans l'inventaire
        item = self.inventory.equip_item(item_index)
        if item is not None:
            self.add_stat(item.stats)

    def unequip_item(self, item_type):
        """Change les stats du joueur en fonction de l'item equipee"""
        item = self.inventory.unequip_item(item_type)
        if item is not None:
            self.remove_stat(item.stats)

    def use_item(self, item_index):
        effects_list = self.inventory.use_item(item_index)
        for effect in effects_list:
            if type(effect) is StatusEffect:
                self.effects_handler.add_status_effect(effect)

    def add_stat(self, dictionary: dict, is_stat_shown=False):
        for key, value in dictionary.items():
            self.dic_stats[key] = value + self.dic_stats[key]
            if self.dic_stats["health"] > self.dic_stats["max_health"]:
                self.dic_stats["health"] = self.dic_stats["max_health"]
            if is_stat_shown:
                if value < 0:
                    self.text_list.add_text(
                        Text(
                            "arial",
                            get_stat_display_name(key) + get_signed_number(value),
                            (255, 0, 0),
                            (10, 10),
                            (
                                self.previous_cell_pos[0] * 32 + 16,
                                self.previous_cell_pos[1] * 32,
                            ),
                            movement=(0, -1.5),
                            duration=2,
                            is_border=True,
                            is_text_fadding=True,
                            is_text_centered=True
                        )
                    )
                else:
                    self.text_list.add_text(
                        Text(
                            "arial",
                            get_stat_display_name(key) + get_signed_number(value),
                            (0, 255, 0),
                            (10, 10),
                            (
                                self.previous_cell_pos[0] * 32 + 16,
                                self.previous_cell_pos[1] * 32,
                            ),
                            movement=(0, -1.5),
                            duration=2,
                            is_border=True,
                            is_text_fadding=True,
                            is_text_centered=True
                        )
                    )

    def remove_stat(self, dictionary: dict):
        for key, value in dictionary.items():
            self.dic_stats[key] = self.dic_stats[key] - value

    # ============
    # === DRAW ===
    # ============

    def draw(self, screen: pg.Surface):

        screen.blit(self.image, self.rect)

    # ==============
    # === UPDATE ===
    # ==============

    def update(
        self,
        deltatime: float,
        camera_gap: tuple,
        mob_coordinates: tuple,
        textgroup: pg.sprite.Group,
    ):
        """Update la position du joueur"""

        # ======================
        # === A CHAQUE FRAME ===
        # ======================
        self.text_list.update(deltatime)
        for text in self.text_list.get_updatable_text() :
            textgroup.add(text)
        self.text_list.clear_updatable_text_list()

        action_points = 0  # Indique le nombre de tours qu'auront les mobs

        # SI LE JOUEUR EST SUR UNE CELULE
        if self.is_on_cell:

            #  SI LE JOUEUR SE DEPLACE
            if self.is_moving:  # Si le joueur se deplace
                
                

                if self.find_path(mob_coordinates):  # S'il existe un chemin
                    self.current_cell_pos = self.path.pop(0)
                    self.is_on_cell = False
                    self.counter.start()
                    action_points += self.dic_stats["movement_time"]

                else:  # S'il n'y a pas de chemin
                    self.is_moving = False
                    self.walk_sound.stop()
                    self.is_walk_sound_active = False

                # SI LE JOUEUR ATAQUE
            if self.is_attacking:
                self.is_attacking = False
                action_points += self.dic_stats["attack_speed"]
            
            # Son de marche
            if not self.is_moving and self.is_walk_sound_active :
                self.walk_sound.stop()
                self.is_walk_sound_active = False
                
            elif self.is_moving and not self.is_walk_sound_active :
                self.is_walk_sound_active = True
                self.walk_sound.play(loops=1)


        # SI LE JOUEUR EST ENTRE 2 CELULES
        else:
            if not self.counter.update(
                deltatime
            ):  # S'il est en train de bouger entre 2 celules

                if self.current_cell_pos[0] - self.previous_cell_pos[0] != 0:
                    self.dx += 32 / (
                        (self.current_cell_pos[0] - self.previous_cell_pos[0])
                        * self.base_moving_time
                        * Entity.FPS
                    )
                if self.current_cell_pos[1] - self.previous_cell_pos[1] != 0:
                    self.dy += 32 / (
                        (self.current_cell_pos[1] - self.previous_cell_pos[1])
                        * self.base_moving_time
                        * Entity.FPS
                    )

            else:  # Lorsqu'il arrive sur une cellule
                self.is_on_cell = True
                self.dx, self.dy = 0, 0
                self.previous_cell_pos = self.current_cell_pos

        # Update la position (px) du joueur
        self.rect.topleft = (
            (self.previous_cell_pos[0] * 32 + self.dx + camera_gap[0]) * Entity.zoom,
            (self.previous_cell_pos[1] * 32 + self.dy + camera_gap[1]) * Entity.zoom,
        )

        # =============================================================
        # === SI LE JOUEUR A FAIT UNE ACTION / SI UN TOUR EST PASSE ===
        # =============================================================
        cell_pos_seen = None
        if action_points > 0:
            # Gere les effets de status
            self.add_stat(self.effects_handler.update(), True)

        if self.is_on_cell or action_points > 0:
            cell_pos_seen = [self.current_cell_pos]
            for x in range(self.dic_stats["vision"] + 1):
                for y in range(self.dic_stats["vision"] + 1 - x):
                    if is_case_lookable(Entity.MAP, self.current_cell_pos, (self.current_cell_pos[0] + x, self.current_cell_pos[1] + y)):
                        cell_pos_seen.append(
                            (self.current_cell_pos[0] + x, self.current_cell_pos[1] + y)
                        )
                        
                    if is_case_lookable(Entity.MAP, self.current_cell_pos, (self.current_cell_pos[0] - x, self.current_cell_pos[1] - y)):
                        cell_pos_seen.append(
                            (self.current_cell_pos[0] - x, self.current_cell_pos[1] - y)
                        )
                        
                    if is_case_lookable(Entity.MAP, self.current_cell_pos, (self.current_cell_pos[0] + x, self.current_cell_pos[1] - y)):
                        cell_pos_seen.append(
                            (self.current_cell_pos[0] + x, self.current_cell_pos[1] - y)
                        )
                    
                    if is_case_lookable(Entity.MAP, self.current_cell_pos, (self.current_cell_pos[0] - x, self.current_cell_pos[1] + y)):
                        cell_pos_seen.append(
                            (self.current_cell_pos[0] - x, self.current_cell_pos[1] + y)
                        )
                    

        # =========================================================
        # Retourne le nombre de tours que doivent executer les mobs

        return action_points, cell_pos_seen
