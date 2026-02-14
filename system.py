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

    def add_catalog_item(self, name: str, price: str, category: str) -> None:
        items_names = self.get_items_names()
        if name in items_names:
            print("Cannot add item: Item with the same name already exists.")
            return
        if not price.isnumeric():
            print("Cannot add item: Invalid item price.")
            return

        new_item = Item(name=name, category=category, normal_price=int(price))
        self.items.append(new_item)

    def update_catalog_item(self, name: str, new_name: str, new_price: str, new_category) -> None:
        items_names = self.get_items_names()
        if name not in items_names:
            print("Cannot update item info: Item with the given name does not exist.")
            return
        if new_name != name and new_name != '-' and new_name in items_names:
            print("Cannot update item info: Item with the same new name already exists")
            return

        item_idx = items_names.index(name)
        item = self.items[item_idx]

        if new_name != name and new_name != '-':
            item.name = new_name
        if new_category != '-':
            item.category = new_category
        if new_price != '-':
            if not new_price.isnumeric():
                print("Cannot update item info: Invalid new price.")
                return
            item.normal_price = int(new_price)

    def remove_catalog_item(self, name: str) -> None:
        items_names = self.get_items_names()
        if name not in items_names:
            print("Cannot remove item: Item not found.")
            return
        item_idx = items_names.index(name)
        self.items.pop(item_idx)

    def get_items_names(self):
        return list(map(lambda item: item.name, self.items))

    def view_catalog_items(self) -> None:
        if not self.items:
            print("The catalog is empty.")
            return

        print("Catalog items: (name, price, category)")
        for item in self.items:
            print(f"{item.name}, {item.normal_price}, {item.category}")
        print()

    def view_discounts(self) -> None:
        if not self.discounts:
            print("No active discounts.")
            return

        print("Active discounts:")
        for indexed_discount in enumerate(self.discounts):
            discount_index = indexed_discount[0] + 1
            discount_info = indexed_discount[1].get_info_str()
            print(str(discount_index) + ". " + discount_info)
        print()

    def add_bundle_discount(self, threshold, quantity_to_pay, bundles) -> None:
        if not validation.validate_bundle_discount_input(threshold, quantity_to_pay, bundles, self.items):
            return
        discount = BundleDiscount(bundles, int(threshold), int(quantity_to_pay))
        self.discounts.append(discount)

    # def validate_new_bundle(self, bundle, discount_id) -> bool:
    #     if not bundle:
    #         print("Bundle cannot be empty.")
    #         return False
    #     return self.validate_items_existence(bundle) and \
    #         self.validate_bundle_uniqueness(bundle, discount_id)



    # def validate_non_overlapping(self, bundles: list[list[str]]) -> bool:
    #     for bundle in bundles:
    #         other_bundles_items = [
    #         item for other_bundle in bundles.remove(bundle) for item in bundle]
    #     common_items = [
    #         item for item in current_bundle if item in existing_bundles_items]
    #     if common_items:
    #         print(f"Cannot add bundle: it overlaps with an existing one")
    #         return False
    #     return True

    # def validate_bundle_uniqueness(self, current_bundle: list[str], discount_id: int) -> bool:
    #     existing_bundles_items = [
    #         item for bundle in self.discounts[discount_id].bundles for item in bundle]
    #     common_items = [
    #         item for item in current_bundle if item in existing_bundles_items]
    #     if common_items:
    #         print(f"Cannot add bundle: it overlaps with an existing one")
    #         return False
    #     return True

    def add_progressive_discount(self, threshold: str, percentage_off_next: str, item: str) -> None:
        if not validation.validate_progressive_discount_input(threshold, percentage_off_next, item, self.items):
            return
        discount = ProgressiveDiscount(
            item, int(threshold), int(percentage_off_next))        
        self.discounts.append(discount)

    def add_bulk_discount(self, threshold: str, discounted_price: str, item: str) -> None:
        if not validation.validate_bulk_discount_input(threshold, discounted_price, item, self.items):
            return
        discount = BulkDiscount(item=item, threshold=int(
            threshold), new_price=int(discounted_price))        
        self.discounts.append(discount)

    def update_bundle_discount(self, discount_index: int, bundles: list[list[str]] | None,
                                  threshold: str, quantity_to_pay: str) -> None:
        new_bundles = new_threshold = new_quantity_to_pay = None
        
        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return
            new_threshold = int(threshold)

        if quantity_to_pay != '-':
            if not validation.validate_quantity_to_pay(quantity_to_pay):
                return
            new_quantity_to_pay = int(quantity_to_pay)
            
        if bundles is not None:
            bundles_items = [item_name for bundle in bundles for item_name in bundle]
            if not validation.validate_items_existence(bundles_items, self.items):
                return
            new_bundles = bundles
            
        self.discounts[discount_index].update_info_from_list(new_bundles, [new_threshold, new_quantity_to_pay])
            
    def update_progressive_discount(self, discount_index: int, item_name: str, threshold: str, percentage: str) -> None:
        new_threshold = new_percentage = new_item_name = None

        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return
            new_threshold = int(threshold)
        if percentage != '-':
            if not validation.validate_percentage_input(percentage):
                return
            new_percentage = int(percentage)
        if item_name != '-':
            if not validation.validate_items_existence([item_name], self.items):
                return
            new_item_name = item_name
        
        self.discounts[discount_index].update_info_from_list(new_item_name, [new_threshold, new_percentage])

    def update_bulk_discount(self, discount_index: int, item_name: str, threshold: str, discounted_price: str) -> None:
        new_threshold = new_discounted_price = new_item_name = None

        if threshold != '-':
            if not validation.validate_threshold(threshold):
                return
            new_threshold = int(threshold)
        if discounted_price != '-':
            if not validation.validate_discounted_price_input(discounted_price):
                return
            new_discounted_price = int(discounted_price)
        if item_name != '-':
            if not validation.validate_items_existence([item_name], self.items):
                return
            new_item_name = item_name
            
        self.discounts[discount_index].update_info_from_list(new_item_name, [new_threshold, new_discounted_price])

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
        discounts = enumerate(self.discounts)
        baskets = [self.apply_discount_sequence(
            deepcopy(self.basket), p) for p in permutations(discounts)]
        self.basket = min(
            baskets, key=lambda basket: basket.get_discounted_price())

    def apply_discount_sequence(self, basket: Basket, discounts: tuple[tuple[int, Discount], ...]) -> Basket:
        if not discounts:
            return basket
        discount_id, current_discount = discounts[0]
        current_discount.apply_to_basket(basket, discount_id)
        return self.apply_discount_sequence(basket, discounts[1:])

    def empty_basket(self) -> None:
        self.basket = Basket()

    def find_item_index_by_name(self, item_name: str) -> int:
        items_names = list(map(lambda item: item.name, self.items))
        return items_names.index(item_name)
