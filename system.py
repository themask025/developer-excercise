from item import Item
from discounts import Discount
from basket import Basket


class System:
    def __init__(self, items: list[Item] = [],
                 discounts: list[Discount] = [],
                 basket: Basket | None = None) -> None:
        self.items = items
        self.discounts = discounts
        self.basket = basket

    def add_catalog_item(self, name: str, price: str, category: str) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name in items_names:
            raise ValueError(
                "Cannot add the item: an item with the same name already exists.")
        if price.isnumeric() == False:
            raise ValueError(
                "Cannot add the item: invalid item price."
            )
        
        new_item = Item(name=name, category=category, normal_price=int(price))
        self.items.append(new_item)

    def update_catalog_item(self, name: str, new_name: str, new_price: str, new_category) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name not in items_names:
            raise ValueError("Cannot update item info: Item with the given name does not exist.")
        if new_name != name and new_name != '-' and new_name in items_names:
            raise ValueError("Cannot update item info: Another item with the given new name already exists")
        
        item_idx = items_names.index(name)
        item = self.items[item_idx]
        
        if new_name != name and new_name != '-':
            item.name = new_name
        if new_category != '-':
            item.category = new_category
        if new_price != '-':
            if new_price.isnumeric() == False:
                raise ValueError("Cannot update item info: invalid new price.")
            item.normal_price = int(new_price)
            
    def remove_catalog_item(self, name: str) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name not in items_names:
            raise ValueError("Cannot remove item: Item not found.")
        item_idx = items_names.index(name)
        self.items.remove(self.items[item_idx])

    def view_catalog_items(self) -> None:
        if len(self.items) == 0:
            print("The catalog is empty.")
            return
        
        print("Catalog items: (name, price, category)")
        for item in self.items:
            print(f"{item.name}, {item.normal_price}, {item.category}")
        print()

    def view_discounts(self) -> None:
        pass

    def add_discount(self) -> None:
        pass

    def edit_discount(self) -> None:
        pass

    def remove_discount(self) -> None:
        pass

    def add_items_to_basket(self) -> None:
        pass

    def empty_basket(self) -> None:
        pass
