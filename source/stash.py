# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques
import pygame as pg

from player import Player
from entity import Entity
from text_handler import Text
from button import ClickableObject
from event_listener import create_button
from item import ConsumableItem, EquipableItem
from inventory_loop import ItemSlotHolder, ItemStatViewer, EquipementSlotHolder


class Stash:
    """Planque du joueur permettant de stocker des items"""

    def __init__(self, stash_inv, player_inv, screen_size, zoom: int = 2):

        self.WIDTH, self.HEIGHT = screen_size

        self.zoom = zoom

        self.stash_inv = stash_inv

        self.player_inv = player_inv

        self.padding = 20 * zoom

        self.button_list = []
        self.active_button_list = []
        self.text_list = []

        self.selected_item_slot = None

        self.item_in_stash = False

        self.create_view(screen_size, self.player_inv)

    def create_view(self, screen_size, player_inv):
        """Creation des elements du stash (inventaire, equipement, boutons)"""

        self.active_button_list.clear()
        self.text_list.clear()

        self.WIDTH, self.HEIGHT = screen_size

        self.player_inv = player_inv

        self.padding = 20 * self.zoom

        self.text_list.append(
            Text(
                "arial",
                "Planque",
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

        self.stash_item_slot_holder = ItemSlotHolder(
            self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT - self.padding * 2,
            self.stash_inv,
            screen_size,
            self.zoom,
        )

        self.text_list.append(
            Text(
                "arial",
                "Inventaire",
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

        self.player_item_slot_holder = ItemSlotHolder(
            self.WIDTH // 3 * 2 + self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT - self.padding * 2,
            self.player_inv,
            screen_size,
            self.zoom,
        )

        self.text_list.append(
            Text(
                "arial",
                "Equipement",
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

        self.stat_viewer = ItemStatViewer(
            self.WIDTH // 3 + self.padding,
            self.HEIGHT // 2 - self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT // 2,
            zoom=self.zoom,
        )

        self.equipement_holder = EquipementSlotHolder(
            self.WIDTH // 3 + self.padding,
            self.padding,
            self.WIDTH // 3 - self.padding * 2,
            self.HEIGHT // 2 - self.padding * 2,
            self.player_inv,
            screen_size,
            self.zoom,
        )

        (
            self.equip_button,
            self.unequip_button,
            self.deposit_button,
            self.destroy_button,
        ) = create_button(
            (self.WIDTH // 3 - self.padding * 3, 30 * self.zoom),
            (12 * self.zoom, 12 * self.zoom),
            "Equiper",
            "Désequiper",
            "Déposer",
            "Détruire",
        )
        self.refresh()

    def activate_buttons(self, item):
        """Active les boutons correspondant a l'item selectionne"""
        self.active_button_list.clear()

        self.deposit_button.is_active = False
        self.equip_button.is_active = False
        self.unequip_button.is_active = False
        self.destroy_button.is_active = False

        if type(item) is ConsumableItem:
            self.deposit_button.is_active = True
            self.active_button_list.append(self.deposit_button)

            self.destroy_button.is_active = True
            self.active_button_list.append(self.destroy_button)

        elif type(item) is EquipableItem:
            if not item.is_equiped:
                self.deposit_button.is_active = True
                self.active_button_list.append(self.deposit_button)
                if not self.item_in_stash:
                    self.equip_button.is_active = True
                    self.active_button_list.append(self.equip_button)

                self.destroy_button.is_active = True
                self.active_button_list.append(self.destroy_button)

            else:
                self.unequip_button.is_active = True
                self.active_button_list.append(self.unequip_button)

        for i, active_button in enumerate(self.active_button_list):
            active_button.rect.x = self.WIDTH // 3 * 2 + self.padding * 1.5
            active_button.rect.y = (
                self.HEIGHT // 2 + self.padding * 2 + i * 35 * self.zoom
            )

    def refresh(self):
        """Actualise les elements du stash"""
        self.equipement_holder.create_item_slots()
        self.player_item_slot_holder.create_item_slots()
        self.stat_viewer.create_text_list()
        self.stash_item_slot_holder.create_item_slots()

        self.player_item_slot_holder.listener()
        self.stash_item_slot_holder.listener()
        self.equipement_holder.listener()

        for active_button in self.active_button_list:
            active_button.is_active = False

    def draw(self, screen):
        """Affiche les elements du stash"""
        self.stash_item_slot_holder.draw(screen)
        self.stat_viewer.draw(screen)
        self.equipement_holder.draw(screen)
        self.player_item_slot_holder.draw(screen)

        for active_button in self.active_button_list:
            active_button.draw(screen)

        for text in self.text_list:
            text.draw(screen)

    def update(self, player: Player):

        # tuple( item_slot, m1, m3 )
        result = self.stash_item_slot_holder.update()
        if result is not None:
            item_slot, m1, m3 = result
            if m1:
                self.selected_item_slot = item_slot
                self.item_in_stash = True
                self.stat_viewer.change_item(item_slot.item)
                self.activate_buttons(item_slot.item)
        else:
            result = self.player_item_slot_holder.update()
            if result is not None:
                item_slot, m1, m3 = result
                if m1:
                    self.selected_item_slot = item_slot
                    self.item_in_stash = False
                    self.stat_viewer.change_item(item_slot.item)
                    self.activate_buttons(item_slot.item)
            else:
                result = self.equipement_holder.update()
                if result is not None:
                    item_slot, m1, m3 = result
                    if m1:
                        self.selected_item_slot = item_slot
                        self.stat_viewer.change_item(item_slot.item)
                        self.activate_buttons(item_slot.item)

        self.player_item_slot_holder.update()
        self.equipement_holder.update()
        self.stat_viewer.update()

        # S'il y a du changement, on refresh
        if (
            self.player_item_slot_holder.listener()
            or self.stash_item_slot_holder.listener()
            or self.equipement_holder.listener()
        ):
            self.refresh()

        if self.deposit_button.update():
            for item in self.player_inv.item_list:
                if item is self.selected_item_slot.item:
                    self.player_inv.transfer_item(
                        self.stash_inv, self.selected_item_slot.item
                    )
                    self.selected_item_slot = None
                    ClickableObject.is_m1_pressed = False
                    return

            for item in self.stash_inv.item_list:
                if item is self.selected_item_slot.item:
                    self.stash_inv.transfer_item(
                        self.player_inv, self.selected_item_slot.item
                    )
                    self.selected_item_slot = None
                    ClickableObject.is_m1_pressed = False
                    break

        if self.equip_button.update():
            player.equip_item(self.selected_item_slot.item_index)

        if self.unequip_button.update():
            player.unequip_item(self.selected_item_slot.item.equipement_type)

        if self.destroy_button.update():
            player.remove_item(
                self.selected_item_slot.item.name, self.selected_item_slot.item.quantity
            )


def stash_loop(
    screen, clock, stash, player, inv_viewer, is_refresh=False, is_level_created=False
):
    run = True
    mode = "stash"

    ClickableObject.is_m1_pressed = False
    ClickableObject.is_m3_pressed = False

    # --- CLOCK ET DELTATIME ---
    clock.tick(Entity.FPS)

    abs_mouse_px_pos = pg.mouse.get_pos()

    for event in pg.event.get():  # Recupere tous les event chaque frame
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = True
            if event.button == 3:  # Clic Droit
                ClickableObject.is_m3_pressed = True

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Clic Gauche
                ClickableObject.is_m1_pressed = False
            if event.button == 3:  # Clic Droit
                ClickableObject.is_m3_pressed = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                mode = "generate_level"
                inv_viewer.refresh()
            if is_level_created and event.key == pg.K_ESCAPE:
                mode = "game"
                inv_viewer.refresh()

    ClickableObject.mouse_px_pos = abs_mouse_px_pos

    screen.fill("darkgrey")

    if is_refresh:
        stash.refresh()
        is_refresh = False
    stash.update(player)
    stash.draw(screen)

    pg.display.update()
    return run, mode, is_refresh
