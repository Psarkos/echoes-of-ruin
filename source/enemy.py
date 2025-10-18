# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

import pygame as pg
import random as rd

from pathfinder import aStar
from text_handler import TextHandler, Text
from status_effect import StatusEffectsHandler, StatusEffect
from inventory import Inventory
from item import DropedItem
from counter import Counter
from entity import Entity
from ray_caster import is_case_lookable


class Enemy(Entity, pg.sprite.Sprite):

    def __init__(
        self,
        image,
        cell_pos,
        size,
        health,
        defense,
        movement_time,
        attack,
        attack_range,
        attack_speed,
        penetration,
        dodge,
        block,
        precision,
        vision,
    ):
        Entity.__init__(self, image, cell_pos)
        pg.sprite.Sprite.__init__(self)

        # === Init ===

        self.is_seen = False

        self.current_cell_pos = cell_pos
        self.previous_cell_pos = self.current_cell_pos

        # === Pathfinder ===
        self.path = []  # Chemin vers cible
        self.is_on_cell = True  # Verifie si le mob est sur une celule ou entre 2
        self.last_seen_player_pos = ()

        # === Moving animation ===
        self.base_moving_time = 0.16
        self.counter = Counter(self.base_moving_time)
        self.dx, self.dy = (
            0,
            0,
        )  # Correspond au decalage par frame pour l'animation de deplacements
        self.animation_speed_multiplier = (
            1  # Accelere l'animation quand le mob est plus rapide
        )
        self.image_left = pg.transform.flip(self.image, True, False)
        self.image_right = self.image
        self.is_facing_left = False

        # === Point d'action du mob ===
        self.action_points = 0  # Indique le nbr de point d'action du mob
        self.is_alive = True  # S'il est en vie

        # === BASE STATS ===

        # Correspond aux stats avant que les items les changent
        self.dic_base_stats = {
            # --- Health ---
            "health": health,  # La vie du joueur
            "max_health": health,
            # --- Defense ---
            "defense": defense,
            # --- Movement speed ---
            "movement_time": movement_time,  # Le nombre de point d'action utilises pour faire un deplacement
            # --- Attack ---
            "attack": attack,  # L'ataque brut du mob
            "attack_range": attack_range,
            "attack_speed": attack_speed,  # Le nombre de point d'action utilises pour faire une ataque
            "penetration": penetration,
            # --- Dodge/Block ---
            "dodge_chance": dodge,
            "block_chance": block,
            # --- Precision ---
            "precision": precision,
            # --- Vision ---
            "vision": vision,
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
        self.is_attacking = False

        # === INVENTAIRE ET EFFETS===
        self.inventory = Inventory(10)
        self.effects_handler = StatusEffectsHandler()

        # === TEXT ===
        self.text_list = TextHandler()

    # ================
    # === METHODES ===
    # ================

    # === INVENTORY ===

    def add_item(self, item):
        """Ajoute l'item a l'inventaire s'il y a de la place.

        La fonction priorise le stackage et ajoute le reste dans une nouvelle case."""
        return self.inventory.add_item(item)

    def remove_item(self, item_name: str, quantity: int = 1):

        return self.inventory.remove_item(item_name, quantity)

    def equipe_item(self, item_index):
        """Change les stats du joueur en fonction de l'item equipee"""
        # Recupere les infos de l'item dans l'inventaire
        item = self.inventory.equip_item(item_index)
        if item is not None:
            self.add_stat(item.stats)

    def unequipe_item(self, item_type):
        """Change les stats du joueur en fonction de l'item equipee"""
        item = self.inventory.unequip_item(item_type)
        if item is not None:
            self.remove_stat(item.stats)

    def use_item(self, item_index):
        effects_list = self.inventory.use_item(item_index)
        for effect in effects_list:
            if type(effect) is StatusEffect:
                self.effects_handler.add_status_effect(effect)

    def add_stat(self, dictionary: dict):
        for key, value in dictionary.items():
            self.dic_stats[key] = value + self.dic_stats[key]

    def remove_stat(self, dictionary: dict):
        for key, value in dictionary.items():
            self.dic_stats[key] = self.dic_stats[key] - value

    # --- Path ---
    def get_current_path(self):
        """Retourne le chemin actuel du mob.
        Retourne la position du mob si le chemin est vide"""
        if self.path != []:
            return self.path
        return [self.current_cell_pos]

    def find_path(self, end_pos, mob_cell_pos=[], ignore_last_pos=True) -> bool:
        """Trouve le chemin le plus court entre la position de l'enemis et la cible"""
        path = aStar(Entity.MAP, self.current_cell_pos, end_pos, mob_cell_pos)
        if path is not None:  # Si le chemin existe
            if ignore_last_pos :
                self.path = path[1:-1]
            else :
                self.path = path[1:]
            return len(self.path) > 2
        else:
            return False

    def move_to(self, cell, mob_cell_pos, ignore_last_pos=True):
        """Fait bouger le mob vers la cellule"""
        if self.action_points >= self.dic_stats["movement_time"] :
            # S'il existe un chemin
            if (
                self.find_path(cell, mob_cell_pos, ignore_last_pos)
                and self.action_points >= self.dic_stats["movement_time"]
            ):  
                #self.previous_cell_pos = self.current_cell_pos
                self.current_cell_pos = self.path.pop(1) 
                # Change les positions des enemis dans mob_cell_pos
                """
                if self.previous_cell_pos in mob_cell_pos :
                    mob_cell_pos.remove(self.previous_cell_pos)
                    mob_cell_pos.append(self.current_cell_pos)
                """
                self.is_on_cell = False
                self.animation_speed_multiplier = (
                    self.action_points // self.dic_stats["movement_time"]
                )
                self.action_points -= self.dic_stats["movement_time"]
                self.counter.start()

    # --- Position/Deplacement ---
    def get_pos(self):
        """Retourne la position du mob (en px)"""
        return self.rect.topleft

    def get_current_cell(self):
        """Retourne la position du mob (en celules)"""
        return self.current_cell_pos

    def get_previous_cell(self):
        """Retourne la position precedente du mob (en celules)"""
        return self.previous_cell_pos

    def get_is_on_cell(self):
        """Indique si le mob bouge vers une autre celule"""
        return self.is_on_cell

    def stop_moving(self):
        """Arrete le deplacement du mob"""
        self.is_moving = False

    # --- Combat ---
    def get_health(self):
        return self.health

    def get_is_alive(self):
        return self.is_alive

    def take_damage(self, raw_damage, penetration, precision):
        """Aplique les degats en fonction des stats de l'attaquant et du defenseur"""
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

    # Image

    def zoom_img(self):
        super().zoom_img()
        self.image_left = pg.transform.flip(self.image, True, False)
        self.image_right = self.image
        if self.is_facing_left:
            self.image = self.image_left

    # ============
    # === DRAW ===
    # ============

    def draw(self, screen):
        if self.is_seen:
            screen.blit(self.image, self.rect)

    # ==============
    # === UPDATE ===
    # ==============

    def update(
        self,
        deltatime,
        camera_gap,
        player,
        action_points: int,
        mob_cell_pos:list[tuple],
        textgroup: pg.sprite.Group,
        dropped_item_group,
        cell_pos_seen,
    ):
        """Update le mob"""

        # ======================
        # === A CHAQUE FRAME ===
        # ======================

        self.text_list.update(deltatime)
        for text in self.text_list.get_updatable_text():
            textgroup.add(text)
        self.text_list.clear_updatable_text_list()

        previous_cell_to_return = None
        
        if cell_pos_seen is not None:
            self.is_seen = False
            if self.current_cell_pos in cell_pos_seen:
                self.is_seen = True

        # SI LE MOB MEURT
        if self.dic_stats["health"] <= 0:
            self.is_alive = False
            for item in self.inventory.dic_equiped_item.values():
                if item is not None:
                    item.is_equiped = False
                    dropped_item_group.add(DropedItem(item, self.current_cell_pos))
            return self.previous_cell_pos, (
                self.kill(),
                self.dic_stats["penetration"],
                self.dic_stats["precision"],
            )

        # S'IL EST SUR UNE CELLULE
        if self.is_on_cell:
            
            player_cell_pos = player.current_cell_pos
            
            # Si le mob voit le joueur
            if abs(player_cell_pos[0] - self.current_cell_pos[0]) + abs(
                player_cell_pos[1] - self.current_cell_pos[1]
            ) <= self.dic_stats["vision"] and is_case_lookable(
                Entity.MAP, self.current_cell_pos, player_cell_pos
            ):
                self.action_points += action_points
                self.last_seen_player_pos = player_cell_pos

                # Verifie que le mob fait face au joueur et le pivote si besoins
                if (
                    player_cell_pos[0] - self.current_cell_pos[0] > 0
                    and self.is_facing_left
                ):
                    self.image = self.image_right
                    self.is_facing_left = False
                elif (
                    player_cell_pos[0] - self.current_cell_pos[0] < 0
                    and not self.is_facing_left
                ):
                    self.image = self.image_left
                    self.is_facing_left = True

                # Si le mob peut ataquer
                if (
                    self.dic_stats["attack_range"] > 1
                    and abs(self.current_cell_pos[0] - player_cell_pos[0])
                    + abs(self.current_cell_pos[1] - player_cell_pos[1])
                    <= self.dic_stats["attack_range"]
                    or abs(self.current_cell_pos[0] - player_cell_pos[0])
                    <= self.dic_stats["attack_range"]
                    <= 1
                    and abs(self.current_cell_pos[1] - player_cell_pos[1])
                    <= self.dic_stats["attack_range"]
                    <= 1
                ):
                    # Si le mob a assez de point d'action
                    if self.action_points >= self.dic_stats["attack_speed"]:
                        if is_case_lookable(
                            Entity.MAP, self.current_cell_pos, player_cell_pos
                        ):
                            player.take_damage(self.dic_stats["attack"], self.dic_stats["penetration"], self.dic_stats["precision"])
                            self.action_points -= self.dic_stats["attack_speed"]

                # Si le mob n'est pas a portee d'attaque
                # S'il peut bouger
                else :
                    self.move_to(player_cell_pos, mob_cell_pos)

            # Si le mob n'a pas de vision directe sur le joueur
            elif self.last_seen_player_pos != ():
                
                if self.previous_cell_pos == self.last_seen_player_pos:
                    self.last_seen_player_pos = ()
                else:
                    
                    self.action_points += action_points
                    self.move_to(self.last_seen_player_pos, mob_cell_pos, False)

        # S'IL N'EST PAS SUR UNE CELLULE
        else:
            if not self.counter.update(
                deltatime * self.animation_speed_multiplier
            ):  # S'il est en train de bouger entre 2 celules

                if self.current_cell_pos[0] - self.previous_cell_pos[0] != 0:
                    self.dx += (32 * self.animation_speed_multiplier) / (
                        (self.current_cell_pos[0] - self.previous_cell_pos[0])
                        * self.base_moving_time
                        * Entity.FPS
                    )
                if self.current_cell_pos[1] - self.previous_cell_pos[1] != 0:
                    self.dy += (32 * self.animation_speed_multiplier) / (
                        (self.current_cell_pos[1] - self.previous_cell_pos[1])
                        * self.base_moving_time
                        * Entity.FPS
                    )
            else:  # Lorsqu'il arrive sur une cellule
                self.is_on_cell = True
                self.dx, self.dy = 0, 0
                # Change les positions des enemis dans mob_cell_pos
                if self.previous_cell_pos in mob_cell_pos :
                    mob_cell_pos.remove(self.previous_cell_pos)
                    mob_cell_pos.append(self.current_cell_pos)
                else :
                    print(False, self.previous_cell_pos, self.current_cell_pos)
                self.previous_cell_pos = self.current_cell_pos
                    
        # Update la position (px) du mob
        self.rect.topleft = (
            (self.previous_cell_pos[0] * 32 + self.dx + camera_gap[0]) * Entity.zoom,
            (self.previous_cell_pos[1] * 32 + self.dy + camera_gap[1]) * Entity.zoom,
        )
        # =============================================================
        # === SI LE MOB A FAIT UNE ACTION / SI UN TOUR EST PASSE ===
        # =============================================================

        if action_points > 0:
            # Gere les effets de status
            self.add_stat(self.effects_handler.update())
