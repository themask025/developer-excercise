from item import Item
from discounts import Discount
from basket import Basket


class System:
    def __init__(self, items: list[Item] | None = None,
                 discounts: list[Discount] | None = None,
                 basket: Basket | None = None) -> None:
        self.items = items
        self.discounts = discounts
        self.basket = basket

    def add_item_to_catalog(self) -> None:
        pass

    def edit_catalog_item(self) -> None:
        pass

    def remove_catalog_item(self) -> None:
        pass

    def view_catalog_items(self) -> None:
        pass

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
