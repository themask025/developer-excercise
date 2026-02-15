from itertools import permutations
from copy import deepcopy

from item import Item
from discounts import Discount, BundleDiscount, ProgressiveDiscount, BulkDiscount
from basket import Basket
import validation


class System:
    def __init__(self) -> None:
        self.items = []
        self.discounts = []
        self.basket = Basket()

    def add_catalog_item(self, name: str, price: str, category: str) -> bool:
        items_names = self.get_items_names()
        if not validation.validate_catalog_item(name, price, items_names):
            return False
        new_item = Item(name=name, category=category, normal_price=int(price))
        self.items.append(new_item)
        return True

    def update_catalog_item(self, name: str, new_name: str, new_price: str, new_category) -> bool:
        items_names = self.get_items_names()
        if not validation.validate_items_exist([name], items_names):
            return False
        if new_name != name and new_name != '-':
            if not validation.validate_item_does_not_exist(new_name, items_names):
                return False

        item_idx = items_names.index(name)
        item = self.items[item_idx]

        if new_name != name and new_name != '-':
            item.name = new_name
        if new_category != '-':
            item.category = new_category
        if new_price != '-':
            if not validation.validate_item_price(new_price):
                return False
            item.normal_price = int(new_price)
        return True

    def remove_catalog_item(self, name: str) -> bool:
        items_names = self.get_items_names()
        if not validation.validate_items_exist([name], items_names):
            return False
        item_idx = items_names.index(name)
        self.items.pop(item_idx)
        return True

    def view_catalog_items(self) -> None:
        if not self.items:
            print("The catalog is empty.\n")
            return

        print("Catalog items: (name, price, category)")
        for item in self.items:
            print(f"{item.name}, {item.normal_price}, {item.category}")
        print()

    def view_discounts(self) -> None:
        if not self.discounts:
            print("No active discounts.\n")
            return

        print("Active discounts:")
        for indexed_discount in enumerate(self.discounts):
            discount_index = indexed_discount[0] + 1
            discount_info = indexed_discount[1].get_info_str()
            print(str(discount_index) + ". " + discount_info)
        print()

    def add_bundle_discount(self, threshold, quantity_to_pay, bundles) -> bool:
        if not validation.validate_bundle_discount_input(threshold, quantity_to_pay, bundles, self.items):
            return False
        discount = BundleDiscount(bundles, int(
            threshold), int(quantity_to_pay))
        self.discounts.append(discount)
        return True

    def add_progressive_discount(self, threshold: str, percentage_off_next: str, item: str) -> bool:
        if not validation.validate_progressive_discount_input(threshold, percentage_off_next, item, self.items):
            return False
        discount = ProgressiveDiscount(
            item, int(threshold), int(percentage_off_next))
        self.discounts.append(discount)
        return True

    def add_bulk_discount(self, threshold: str, discounted_price: str, item: str) -> bool:
        if not validation.validate_bulk_discount_input(threshold, discounted_price, item, self.items):
            return False
        discount = BulkDiscount(item=item, threshold=int(
            threshold), new_price=int(discounted_price))
        self.discounts.append(discount)
        return True

    def update_bundle_discount(self, discount_index: int, bundles: list[list[str]] | None,
                               threshold: str, quantity_to_pay: str) -> bool:
        new_bundles = new_threshold = new_quantity_to_pay = None

        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return False
            new_threshold = int(threshold)

        if quantity_to_pay != '-':
            if not validation.validate_quantity_to_pay(quantity_to_pay):
                return False
            new_quantity_to_pay = int(quantity_to_pay)

        if bundles is not None:
            bundles_items = [
                item_name for bundle in bundles for item_name in bundle]
            if not validation.validate_items_exist(bundles_items, self.items):
                return False
            new_bundles = bundles

        self.discounts[discount_index].update_info_from_list(
            new_bundles, [new_threshold, new_quantity_to_pay])
        return True

    def update_progressive_discount(self, discount_index: int, item_name: str, threshold: str, percentage: str) -> bool:
        new_threshold = new_percentage = new_item_name = None

        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return False
            new_threshold = int(threshold)
        if percentage != '-':
            if not validation.validate_percentage_input(percentage):
                return False
            new_percentage = int(percentage)
        if item_name != '-':
            if not validation.validate_items_exist([item_name], self.items):
                return False
            new_item_name = item_name

        self.discounts[discount_index].update_info_from_list(
            new_item_name, [new_threshold, new_percentage])
        return True

    def update_bulk_discount(self, discount_index: int, item_name: str, threshold: str, discounted_price: str) -> bool:
        new_threshold = new_discounted_price = new_item_name = None

        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return False
            new_threshold = int(threshold)
        if discounted_price != '-':
            if not validation.validate_discounted_price_input(discounted_price):
                return False
            new_discounted_price = int(discounted_price)
        if item_name != '-':
            if not validation.validate_items_exist([item_name], self.items):
                return False
            new_item_name = item_name

        self.discounts[discount_index].update_info_from_list(
            new_item_name, [new_threshold, new_discounted_price])
        return True

    def remove_discount(self, index) -> None:
        self.discounts.pop(index)

    def add_items_to_basket(self, items: list[str]) -> None:
        for item_name in items:
            item_idx = self.find_item_index_by_name(item_name)
            self.basket.items.append(deepcopy(self.items[item_idx]))

    def apply_best_discount_combination(self) -> None:
        discounts = enumerate(self.discounts)
        baskets = [self.apply_discount_sequence(
            deepcopy(self.basket), p) for p in permutations(discounts)]
        self.basket = min(
            baskets, key=lambda basket: basket.get_discounted_price())

    def apply_discount_sequence(self, basket: Basket, discounts: tuple[tuple[int, Discount], ...]) -> Basket:
        for discount_id, current_discount in discounts:
            current_discount.apply_to_basket(basket, discount_id)
        return basket

    def empty_basket(self) -> None:
        self.basket = Basket()

    def find_item_index_by_name(self, item_name: str) -> int:
        items_names = self.get_items_names()
        return items_names.index(item_name)

    def get_items_names(self):
        return list(map(lambda item: item.name, self.items))
