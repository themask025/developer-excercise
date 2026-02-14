from itertools import permutations
from copy import deepcopy

from item import Item
from discounts import Discount
from basket import Basket


class System:
    def __init__(self) -> None:
        self.items = []
        self.discounts = []
        self.basket = Basket()

    def add_catalog_item(self, name: str, price: str, category: str) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name in items_names:
            raise ValueError(
                "Cannot add the item: an item with the same name already exists.")
        if not price.isnumeric():
            raise ValueError(
                "Cannot add the item: invalid item price."
            )

        new_item = Item(name=name, category=category, normal_price=int(price))
        self.items.append(new_item)

    def update_catalog_item(self, name: str, new_name: str, new_price: str, new_category) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name not in items_names:
            raise ValueError(
                "Cannot update item info: Item with the given name does not exist.")
        if new_name != name and new_name != '-' and new_name in items_names:
            raise ValueError(
                "Cannot update item info: Another item with the given new name already exists")

        item_idx = items_names.index(name)
        item = self.items[item_idx]

        if new_name != name and new_name != '-':
            item.name = new_name
        if new_category != '-':
            item.category = new_category
        if new_price != '-':
            if not new_price.isnumeric():
                raise ValueError("Cannot update item info: invalid new price.")
            item.normal_price = int(new_price)

    def remove_catalog_item(self, name: str) -> None:
        items_names = list(map(lambda item: item.name, self.items))
        if name not in items_names:
            raise ValueError("Cannot remove item: Item not found.")
        item_idx = items_names.index(name)
        self.items.pop(item_idx)

    def view_catalog_items(self) -> None:
        if len(self.items) == 0:
            print("The catalog is empty.")
            return

        print("Catalog items: (name, price, category)")
        for item in self.items:
            print(f"{item.name}, {item.normal_price}, {item.category}")
        print()

    def view_discounts(self) -> None:
        if len(self.discounts) == 0:
            print("No active discounts.")
            return

        print("Active discounts:")
        for indexed_discount in enumerate(self.discounts):
            discount_index = indexed_discount[0] + 1
            discount_info = indexed_discount[1].get_info_str()
            print(str(discount_index) + ". " + discount_info)
        print()

    def add_discount(self, discount) -> None:
        self.discounts.append(discount)

    def edit_discount(self, discount_index, item_data, numeric_data) -> None:
        self.discounts[discount_index].update_info_from_list(
            item_data, numeric_data)

    def remove_discount(self, index) -> None:
        self.discounts.pop(index)

    def add_items_to_basket(self, items: list[str]) -> None:
        for item_name in items:
            item_idx = self.find_item_index_by_name(item_name)
            self.basket.items.append(deepcopy(self.items[item_idx]))

    def apply_best_discount_combination(self) -> None:
        basket = self.basket
        discounts = tuple(enumerate(self.discounts))
        self.basket = self.find_best_discounted_basket(
            deepcopy(basket), discounts)

    def find_best_discounted_basket(self, basket: Basket, discounts: tuple[tuple[int, Discount], ...]) -> Basket:
        if not discounts:
            return basket
        baskets = []
        for p in permutations(discounts):
            discount_id, current_discount = p[0]
            discounted_basket = current_discount.apply_to_basket(
                deepcopy(basket), discount_id)
            best_derived_basket = self.find_best_discounted_basket(
                deepcopy(discounted_basket), p[1:])
            baskets.append(best_derived_basket)
        baskets_totals = list(
            map(lambda basket: basket.get_discounted_price(), baskets))
        min_total = min(baskets_totals)
        min_total_index = baskets_totals.index(min_total)
        return baskets[min_total_index]

    def empty_basket(self) -> None:
        self.basket = Basket()

    def find_item_index_by_name(self, item_name: str) -> int:
        items_names = list(map(lambda item: item.name, self.items))
        return items_names.index(item_name)
