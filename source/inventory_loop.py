# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from item import Item, ConsumableItem, EquipableItem
from button import ClickableObject
from usefull_fonctions import (
    scale_by,
    get_signed_number,
    get_stat_display_name,
    get_equipment_display_name
)
from event_listener import create_button
from inventory import Inventory
from text_handler import Text
from entity import Entity
from player import Player


class PlayerStatViewer(Entity):
    """Permet de voir les stats du joueur"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        player_dic_stats: Player = None,
        zoom: int = 2,
    ):
        super().__init__(pg.Surface((width, height)), (0, 0), (x, y))
        self.text_list = []

        self.zoom = zoom

        self.width, self.height = width, height
        self.image.fill((100, 100, 100))

        self.player_stats = player_dic_stats

    def create_text_list(self):

        self.text_list.clear()

        if self.player_stats is not None:
            self.player_stats: dict

            self.text_list.append(
                Text(
                    "arial",
                    "Statistiques du Joueur",
                    (0, 0, 0),
                    (14 * self.zoom, 14 * self.zoom),
                    (20, 20),
                    is_text_centered=False,
                    is_resizable=False,
                )
            )

            for key, value in self.player_stats.items():
                self.text_list.append(
                    Text(
                        "arial",
                        get_stat_display_name(key) + str(value),
                        (0, 0, 0),
                        (12 * self.zoom, 12 * self.zoom),
                        (30, 15 * len(self.text_list) * self.zoom + 40),
                        is_text_centered=False,
                        is_resizable=False,
                    )
                )

    def draw(self, screen: pg.Surface):
        self.image.fill((100, 100, 100))

        self.create_text_list()

        for text in self.text_list:
            text: Text
            text.draw(self.image)
        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def update(self, player_dic_stats):
        if ItemStatViewer.is_resize:
            self.resize()
        if player_dic_stats != self.player_stats:
            self.player_stats = player_dic_stats
            self.create_text_list()


class ItemStatViewer(Entity):

    def __init__(self, x, y, width, height, item: Item = None, zoom: int = 2):
        super().__init__(pg.Surface((width, height)), (0, 0), (x, y))

        self.text_list = []

        self.image.fill((100, 100, 100))

        self.item = item

        self.zoom = zoom

    def change_item(self, item):
        self.item = item
        self.create_text_list()

    def create_text_list(self):

        self.text_list.clear()

        if self.item is not None:
            self.item: Item
            self.text_list.append(
                Text(
                    "arial",
                    "Nom : " + self.item.name,
                    (0, 0, 0),
                    (12 * self.zoom, 12 * self.zoom),
                    (20, 40),
                    is_text_centered=False,
                    is_resizable=False,
                )
            )

            if self.item.is_stackable:
                self.text_list.append(
                    Text(
                        "arial",
                        "Quantité : " + str(self.item.quantity),
                        (0, 0, 0),
                        (12 * self.zoom, 12 * self.zoom),
                        (20, 40 * len(self.text_list) + 40),
                        is_text_centered=False,
                        is_resizable=False,
                    )
                )
            elif type(self.item) is EquipableItem:
                self.text_list.append(
                    Text(
                        "arial",
                        "Type : " + get_equipment_display_name(self.item.equipement_type),
                        (0, 0, 0),
                        (12 * self.zoom, 12 * self.zoom),
                        (20, 40 * len(self.text_list) + 40),
                        is_text_centered=False,
                        is_resizable=False,
                    )
                )

                if (
                    (self.item.equipement_type == "main_weapon"
                    or self.item.equipement_type == "secondary_weapon")
                    and self.item.is_weapon_two_handed
                ):
                    self.text_list.append(
                        Text(
                            "arial",
                            "Arme à deux mains",
                            (0, 0, 0),
                            (12 * self.zoom, 12 * self.zoom),
                            (20, 40 * len(self.text_list) + 40),
                            is_text_centered=False,
                            is_resizable=False,
                        )
                    )

            if type(self.item) is EquipableItem:
                self.text_list.append(
                    Text(
                        "arial",
                        "Statistiques : ",
                        (0, 0, 0),
                        (12 * self.zoom, 12 * self.zoom),
                        (20, 40 * len(self.text_list) + 40),
                        is_text_centered=False,
                        is_resizable=False,
                    )
                )

                for key, value in self.item.stats.items():
                    self.text_list.append(
                        Text(
                            "arial",
                            get_stat_display_name(key) + get_signed_number(value),
                            (0, 0, 0),
                            (12 * self.zoom, 12 * self.zoom),
                            (30, 40 * len(self.text_list) + 40),
                            is_text_centered=False,
                            is_resizable=False,
                        )
                    )

            elif type(self.item) is ConsumableItem:
                self.text_list.append(
                    Text(
                        "arial",
                        "Effets : ",
                        (0, 0, 0),
                        (12 * self.zoom, 12 * self.zoom),
                        (20, 40 * len(self.text_list) + 40),
                        is_text_centered=False,
                        is_resizable=False,
                    )
                )

                for effect in self.item.effects_list:
                    self.text_list.append(
                        Text(
                            "arial",
                            str(effect.name),
                            (0, 0, 0),
                            (12 * self.zoom, 12 * self.zoom),
                            (30, 40 * len(self.text_list) + 40),
                            is_text_centered=False,
                            is_resizable=False,
                        )
                    )
                    for key, value in effect.stats.items():
                        self.text_list.append(
                            Text(
                                "arial",
                                get_stat_display_name(key) + get_signed_number(value),
                                (0, 0, 0),
                                (12 * self.zoom, 12 * self.zoom),
                                (40, 40 * len(self.text_list) + 40),
                                is_text_centered=False,
                                is_resizable=False,
                            )
                        )

    def draw(self, screen: pg.Surface):
        self.image.fill((100, 100, 100))

        self.create_text_list()

        for text in self.text_list:
            text: Text
            text.draw(self.image)
        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def update(self):
        """Renvoi l'item dans self.item"""
        if ItemStatViewer.is_resize:
            self.resize()
        return self.item


class ItemSlot(Entity, ClickableObject):

    def __init__(
        self, image, x, y, item_index: int = None, item: Item = None, zoom: int = 2
    ):

        Entity.__init__(self, scale_by(image, zoom), (0, 0), (x, y))
        ClickableObject.__init__(self, self.rect)

        self.zoom = zoom

        self.item = item
        self.item_index = item_index
        if self.item is not None:
            self.image.blit(
                scale_by(self.item.image, self.zoom),
                (2 * self.zoom, 2 * self.zoom),
            )

        self.is_hover = False
        self.is_pressed_with_m1 = False
        self.is_pressed_with_m3 = False

    def draw(self, screen: pg.Surface):

        screen.blit(self.image, self.rect)
        if self.is_pressed_with_m1:
            pg.draw.rect(screen, (180, 180, 0), self.rect, 1)
        elif self.is_hover:
            pg.draw.rect(screen, (200, 200, 200), self.rect, 1)
        else:
            pg.draw.rect(screen, (20, 20, 20), self.rect, 1)

    def update(self) -> tuple[bool, bool, bool]:
        """Renvoie si la sourie interragie avec le slot"""
        if ItemSlot.is_resize:
            self.resize()

        self.is_hover, self.is_pressed_with_m1, self.is_pressed_with_m3 = (
            self.check_if_clicked()
        )
        return self.is_hover, self.is_pressed_with_m1, self.is_pressed_with_m3


class ItemSlotHolder(Entity):

    def __init__(
        self,
        x,
        y,
        width,
        height,
        inventory: Inventory,
        screen_size: tuple,
        zoom: int = 2,
    ):
        super().__init__(pg.Surface((width, height)), (0, 0), (x, y))

        self.image.fill((100, 100, 100))

        self.is_changed = False
        self.margin = 40  # Margin du Viewer

        self.zoom = zoom

        self.inventory = inventory
        self.WIDTH, self.HEIGHT = screen_size
        self.nb_col = (width - self.margin * 2) // (32 * self.zoom)

        # Item Slot
        self.item_slot_img = pg.image.load(
            "assets/images/items/item_slots/item_slot.png"
        )
        self.item_slot_list = []

    def create_item_slots(self):
        self.is_changed = True
        self.item_slot_list.clear()

        for i in range(self.inventory.item_list_size):
            item = None
            if i < len(self.inventory.item_list):
                item = self.inventory.item_list[i]
            # Creation du slot
            self.item_slot_list.append(
                ItemSlot(
                    self.item_slot_img,
                    i % self.nb_col * (32 * self.zoom) + self.margin + self.rect.x,
                    i // self.nb_col * (32 * self.zoom) + self.margin + self.rect.y,
                    i,
                    item,
                    self.zoom,
                )
            )

    def listener(self):
        """Permet d'indiquer s'il y a du changement au coeur de l'objet"""
        if self.is_changed:
            self.is_changed = False
            return True
        return False

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)
        for item_slot in self.item_slot_list:
            item_slot: ItemSlot
            item_slot.draw(screen)
            pg.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def update(self):
        """Renvoie un tuple si un des slots est presse.
        (item_slot, m1, m3)"""

        if ItemSlotHolder.is_resize:
            self.resize()

        if self.inventory.listener():
            self.create_item_slots()

        tuple_to_return = None
        for item_slot in self.item_slot_list:
            item_slot: ItemSlot

            click = item_slot.update()

            if click[1] or click[2]:
                tuple_to_return = (item_slot, click[1], click[2])
        return tuple_to_return


class EquipementSlotHolder(Entity):

    def __init__(
        self,
        x,
        y,
        width,
        height,
        inventory: Inventory,
        screen_size: tuple,
        zoom: int = 2,
    ):
        super().__init__(pg.Surface((width, height)), (0, 0), (x, y))

        self.image.fill((100, 100, 100))

        self.inventory = inventory
        self.equiped_items_dic = inventory.dic_equiped_item
        self.WIDTH, self.HEIGHT = screen_size

        self.zoom = zoom

        self.is_changed = False
        self.margin_width = max((width - 3 * 32 * self.zoom) // 2, 0)
        self.margin_height = max((height // 2 - 4 * 32 * self.zoom) // 2, 0)

        # Item Slot
        path = "assets/images/items/item_slots/"
        self.empty_slot_img = pg.image.load(path + "item_slot.png")
        self.locked_slot_img = pg.image.load(path + "locked_item_slot.png")

        self.item_slot_img = {
            key: pg.image.load(path + key + "_slot.png")
            for key in self.equiped_items_dic.keys()
        }
        self.item_slot_coord = {
            "helmet": (0, 1),
            "chestplate": (1, 1),
            "pants": (2, 1),
            "boots": (3, 1),
            "necklace": (0, 2),
            "ring": (2, 2),
            "main_weapon": (1, 0),
            "secondary_weapon": (1, 2),
            "accessory": (2, 0),
        }
        self.item_slot_list = []

    def create_item_slots(self):
        self.is_changed = True
        self.item_slot_list.clear()
        for key, item in self.equiped_items_dic.items():
            img = self.item_slot_img[key]

            # Img
            if item is not None:
                if item == "locked":
                    img = self.locked_slot_img
                    item = None
                else:
                    img = self.empty_slot_img

            self.item_slot_list.append(
                ItemSlot(
                    img,
                    self.rect.x
                    + self.margin_width
                    + (32 * self.zoom) * self.item_slot_coord[key][1],
                    self.rect.y
                    + self.margin_height
                    + (32 * self.zoom) * self.item_slot_coord[key][0],
                    item=item,
                    zoom=self.zoom,
                )
            )

    def listener(self):
        if self.is_changed:
            self.is_changed = False
            return True
        return False

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)
        for item_slot in self.item_slot_list:
            item_slot: ItemSlot
            item_slot.draw(screen)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def update(self):
        """Renvoie un tuple si un des slots est presse"""
        if EquipementSlotHolder.is_resize:
            self.resize()

        if self.inventory.listener():
            self.create_item_slots()

        tuple_to_return = None
        for item_slot in self.item_slot_list:
            item_slot: ItemSlot

            var = item_slot.update()
            if var[1] or var[2]:
                tuple_to_return = (item_slot, var[1], var[2])
        return tuple_to_return


# Contient le ItemSlotHolder, le ItemStatViewer et le Equipement
class InventoryViewer:

    def __init__(self, inventory: Inventory, screen_size: tuple, zoom: int = 2.5):

        self.inventory = inventory
        self.selected_item_slot = None
        self.WIDTH, self.HEIGHT = screen_size

        self.padding = 20 * zoom

        self.zoom = zoom

        self.text_list = []

        self.create_view(screen_size, self.inventory)

    def refresh(self):

        self.use_button.is_active = False
        self.equip_button.is_active = False
        self.unequip_button.is_active = False
        self.destroy_button.is_active = False

        self.item_slot_holder.create_item_slots()
        self.equipement_slot_holder.create_item_slots()

        self.item_stat_viewer.change_item(None)

        self.item_slot_holder.listener()
        self.equipement_slot_holder.listener()

    def create_view(self, screen_size, player_inv):

        self.padding = 20 * self.zoom

        self.text_list.clear()

        self.inventory = player_inv

        self.WIDTH, self.HEIGHT = screen_size

        # Inventaire
        self.text_list.append(
            Text(
                "arial",
                "Inventaire",
                (0, 0, 0),
                (14 * self.zoom, 14 * self.zoom),
                (
                    self.WIDTH // 6 * 3,
                    max(self.padding - 15 * self.zoom, 0) // 2,
                ),
                is_text_centered=True,
                is_resizable=False,
            )
        )

        self.item_slot_holder = ItemSlotHolder(
            self.WIDTH // 3 + self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT - self.padding * 2,
            self.inventory,
            screen_size,
            self.zoom,
        )

        # Equipement
        self.text_list.append(
            Text(
                "arial",
                "Equipement",
                (0, 0, 0),
                (14 * self.zoom, 14 * self.zoom),
                (
                    self.WIDTH // 6,
                    max(self.padding - 15 * self.zoom, 0) // 2,
                ),
                is_text_centered=True,
                is_resizable=False,
            )
        )

        self.equipement_slot_holder = EquipementSlotHolder(
            self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT - self.padding * 3,
            self.inventory,
            screen_size,
            self.zoom,
        )

        # Description
        self.text_list.append(
            Text(
                "arial",
                "Description",
                (0, 0, 0),
                (14 * self.zoom, 14 * self.zoom),
                (
                    self.WIDTH // 6 * 5,
                    max(self.padding - 15 * self.zoom, 0) // 2,
                ),
                is_text_centered=True,
                is_resizable=False,
            )
        )

        self.item_stat_viewer = ItemStatViewer(
            (self.WIDTH // 3) * 2 + self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT - self.padding * 2,
            zoom=self.zoom,
        )

        self.player_stat_viewer = PlayerStatViewer(
            self.padding,
            self.HEIGHT // 2 - self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT // 2,
            zoom=self.zoom,
        )
        # === Buttons ===
        self.active_button_list = []

        (
            self.use_button,
            self.equip_button,
            self.unequip_button,
            self.destroy_button,
        ) = create_button(
            (self.WIDTH // 3 - self.padding * 3, 30 * self.zoom),
            (12 * self.zoom, 12 * self.zoom),
            "Utiliser",
            "Equiper",
            "Désequiper",
            "Détruire",
        )
        self.refresh()

        self.use_button.is_active = False
        self.equip_button.is_active = False
        self.unequip_button.is_active = False
        self.destroy_button.is_active = False

        self.refresh()

    def activate_buttons(self, item):

        self.active_button_list.clear()

        self.use_button.is_active = False
        self.equip_button.is_active = False
        self.unequip_button.is_active = False
        self.destroy_button.is_active = False

        if type(item) is ConsumableItem:
            self.use_button.is_active = True
            self.destroy_button.is_active = True

            self.active_button_list.append(self.use_button)
            self.active_button_list.append(self.destroy_button)

        elif type(item) is EquipableItem:
            if not item.is_equiped:
                self.equip_button.is_active = True
                self.destroy_button.is_active = True

                self.active_button_list.append(self.equip_button)
                self.active_button_list.append(self.destroy_button)

            else:
                self.unequip_button.is_active = True
                self.active_button_list.append(self.unequip_button)

        for i, active_button in enumerate(self.active_button_list):
            active_button.rect.x = self.WIDTH // 3 * 2 + self.padding * 1.5
            active_button.rect.y = (
                self.HEIGHT // 2 + self.padding * 2 + i * 35 * self.zoom
            )

    def draw(self, screen):

        self.item_slot_holder.draw(screen)
        self.item_stat_viewer.draw(screen)
        self.equipement_slot_holder.draw(screen)
        self.player_stat_viewer.draw(screen)

        for active_button in self.active_button_list:
            active_button.draw(screen)

        for text in self.text_list:
            text.draw(screen)

    def update(self, player: Player):

        self.player_stat_viewer.update(player.dic_stats)

        # tuple( item, item_slot, is_hover, m1, m3 )
        result = self.equipement_slot_holder.update()
        # Changement de l'affichage des stats si clic gauche
        if result is not None:
            item_slot, is_m1, is_m3 = result
            if is_m1:
                self.selected_item_slot = item_slot
                self.item_stat_viewer.change_item(item_slot.item)
                self.activate_buttons(item_slot.item)
        else:
            result = self.item_slot_holder.update()
            # Changement de l'affichage des stats si clic gauche
            if result is not None:
                item_slot, is_m1, is_m3 = result
                if is_m1:
                    self.selected_item_slot = item_slot
                    self.item_stat_viewer.change_item(item_slot.item)
                    self.activate_buttons(item_slot.item)

        # S'il y a du changement, on refresh
        if self.item_slot_holder.listener() or self.equipement_slot_holder.listener():
            self.refresh()

        if self.use_button.update():
            player.use_item(self.selected_item_slot.item_index)
            ClickableObject.is_m1_pressed = False

        if self.equip_button.update():
            player.equip_item(self.selected_item_slot.item_index)

        if self.unequip_button.update():
            player.unequip_item(self.selected_item_slot.item.equipement_type)

        if self.destroy_button.update():
            player.remove_item(
                self.selected_item_slot.item.name, self.selected_item_slot.item.quantity
            )


def inventory_view_loop(screen, clock, inv_viewer, player):
    run = True
    mode = "inventory"

    ClickableObject.is_m1_pressed = False
    ClickableObject.is_m3_pressed = False

    # --- CLOCK ET DELTATIME ---
    clock.tick(Entity.FPS)

    abs_mouse_px_pos = pg.mouse.get_pos()

    for event in pg.event.get():  # Recupere tous les event chaque frame
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_a
        ):  # Permet de fermet la fenetre
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = True
            if event.button == 3:  # Clic Gauche
                ClickableObject.is_m3_pressed = True

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = False
            if event.button == 3:  # Clic Gauche
                ClickableObject.is_m3_pressed = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                mode = "game"

    ClickableObject.mouse_px_pos = abs_mouse_px_pos

    screen.fill("darkgrey")

    inv_viewer.update(player)
    inv_viewer.draw(screen)

    pg.display.update()
    return run, mode
