# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
from item import Item, ConsumableItem, EquipableItem

class Inventory:
    """Inventaire fait d'une liste contenant des Items."""

    def __init__(self, item_list_size):

        self.item_list_size = item_list_size
        self.item_list = []

        self.effect_list = []

        self.dic_equiped_item = {
            "helmet": None,
            "chestplate": None,
            "pants": None,
            "boots": None,
            "necklace": None,
            "ring": None,
            "main_weapon": None,
            "secondary_weapon": None,
            "accessory": None,
        }

        self.is_changed = False

    # === INVENTORY ===
    def add_item(self, item: Item) -> Item | None:
        """Ajoute l'item a l'inventaire s'il y a de la place.

        La fonction priorise le stackage et ajoute le reste dans une nouvelle case."""
        if item.is_stackable:
            if self.stack_items(item).quantity > 0:
                if len(self.item_list) < self.item_list_size:
                    self.item_list.append(item)
                else:
                    self.update()
                    return item
        elif len(self.item_list) < self.item_list_size:
            self.item_list.append(item)
        else:
            return item
        self.update()

    def stack_items(self, item_to_stack: Item) -> Item:
        """Ajoute l'item au stock deja present"""

        for item in self.item_list:
            item: Item
            if item == item_to_stack:
                item_to_stack.quantity = item.add_quantity(item_to_stack.quantity)
            if item_to_stack.quantity <= 0:
                return item_to_stack
        return item_to_stack

    def remove_item(self, item_name, quantity=1) -> None | Item:
        """Enleve"""

        new_item = None
        for item in self.item_list[::-1]:
            item: Item
            if item.name == item_name:
                if new_item is None :
                    new_item, quantity = item.remove_quantity(quantity)
                else:
                    quantity = item.remove_quantity(quantity)[1]
                    new_item.add_quantity(quantity)
            if quantity <= 0:
                break
        self.update()
        return new_item
    
    def transfer_item(self, other, item):
        item = self.remove_item(item.name, item.quantity)
        other.add_item(item)
        self.update()

    def search(self, item: Item) -> bool:
        """Recherche si un item avec ce nom est dans l'inventaire."""
        for i in range(len(self.item_list)):
            if self.item_list[i] == item:
                return True
        return False

    def get_item_with_name(self, item_name: int) -> any:
        """Retourn le premier item avec le nom passe en argument"""
        for i in range(len(self.item_list)):
            if self.item_list[i].name == item_name:
                return self.item_list[i]

    def change_index(self, previous_index: int, new_index: int):
        """Change la position d'un item dans l'inventaire."""
        self.item_list.insert(new_index, self.item_list[previous_index])
        self.item_list.pop(previous_index + 1)
        self.update()

    # === EQUIPEMENT ===

    def equip_item(self, item_index):
        """Change les stats du joueur en fonction de l'item equipee"""
        # Recupere les infos de l'item dans l'inventaire
        item: EquipableItem = self.item_list[item_index]
        # test si l'item est equipable
        if type(item) is EquipableItem:
            item_equpmt_type = item.get_equipement_type()
            # test si l'emplacement est vide
            if self.dic_equiped_item[item_equpmt_type] is None:

                if item.is_weapon_two_handed:
                    if self.dic_equiped_item["secondary_weapon"] is None:
                        # Ajoute l'item au dico dic_equiped_item
                        self.dic_equiped_item["secondary_weapon"] = "locked"
                    else:
                        return None

                self.item_list.pop(item_index)
                self.dic_equiped_item[item_equpmt_type] = item
                item.is_equiped = True
                self.update()
                return item

        else:
            print("error: pas equipable")

    def unequip_item(self, item_type):
        """Change les stats du joueur en fonction de l'item equipee"""
        if self.dic_equiped_item[item_type] is not None:
            item = self.dic_equiped_item[item_type]
            if item.is_weapon_two_handed:
                self.dic_equiped_item["secondary_weapon"] = None
            self.dic_equiped_item[item_type] = None
            item.is_equiped = False
            self.add_item(item)
            self.update()
            return item

    # === CONSUMABLES ===

    def use_item(self, item_index):
        item = self.item_list[item_index]
        if type(item) is ConsumableItem:
            effects_list = item.use()
            if item.quantity <= 0:
                self.update()
            return effects_list

    # === OTHER ===
    def listener(self):
        if self.is_changed:
            self.is_changed = False
            return True
        return False

    def update(self):
        self.is_changed = True
        for i, item in enumerate(self.item_list):
            item: Item
            if item.quantity <= 0:
                self.item_list.pop(i)

    def __repr__(self):
        return "Inventory Object"

    def __str__(self):
        str_to_return = "[ "
        for item in self.item_list:
            str_to_return += str(item) + ", "
        return str_to_return + " ]"
