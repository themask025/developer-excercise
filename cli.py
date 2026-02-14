from textwrap import dedent
from typing import Any

from system import System
from discounts import Discount
import validation


class CLI:
    def __init__(self) -> None:
        self.system = System()

    def main_menu(self) -> None:
        print("Grocery Store Till System")

        user_action = None

        while user_action != '3':

            actions_info = """\
                Available actions:
                1. Begin scanning
                2. Configure till
                3. Exit
            """
            print(dedent(actions_info))

            user_action = input("Please choose an action (using numbers):")
            print()

            match user_action:
                case '1':
                    self.scanning_menu()
                case '2':
                    self.configure_till()
                case '3':
                    break
                case _:
                    print("Invalid action.\n")

        print("Exiting the system...")

    def scanning_menu(self) -> None:
        running_total = 0
        user_action = 0

        while user_action != '3':
            print(f"Running total = {running_total}c")
            actions_info = """\
                Available actions:
                1. Scan items
                2. Finalize
                3. Discard and exit
            """
            print(dedent(actions_info))

            user_action = input("Please choose an action (using numbers):")
            print()

            match user_action:
                case '1':
                    running_total = self.scan_items()
                case '2':
                    self.finalize()
                    break
                case '3':
                    print("Emptying basket...\n")
                    break
                case _:
                    print("Invalid action.\n")

        print("Returning to main menu...\n")

    def scan_items(self) -> int:
        prompt = "List names of items to scan (separated with commas):"
        items = self.get_processed_input(prompt)
        if validation.validate_items_existence(items, self.system.items):
            self.system.add_items_to_basket(items)
        return self.system.basket.get_total_price()

    def finalize(self) -> None:
        self.system.apply_best_discount_combination()
        self.system.view_discounts()
        print(self.system.basket.get_receipt_str())
        self.system.empty_basket()
        input("Proceed...")

    def configure_till(self) -> None:
        print("Configuring till...\n")
        
        user_action = None
        while user_action != '9':
            actions_info = """\
                Available actions:
                
                Product catalog:
                1. View product catalog
                2. Add a product to the catalog
                3. Update a product in the catalog
                4. Remove a product from the catalog
                
                Discounts:
                5. View active discounts
                6. Add a new discount
                7. Modify an existing discount
                8. Remove a discount
                
                9. Return to main menu
                """
            print(dedent(actions_info))
            user_action = input("Please choose an action (using numbers):")
            print()
            match user_action:
                case '1':
                    self.view_catalog_items_handler()
                case '2':
                    self.add_catalog_item_handler()
                case '3':
                    self.update_catalog_item_handler()
                case '4':
                    self.remove_catalog_item_handler()
                case '5':
                    self.view_discounts_handler()
                case '6':
                    self.add_discount_handler()
                case '7':
                    self.edit_discount_handler()
                case '8':
                    self.remove_discount_handler()
                case '9':
                    print("Returning to main menu...")
                    break
                case _:
                    print("Invalid action.\n")
            input("Proceed...")

    def view_catalog_items_handler(self) -> None:
        self.system.view_catalog_items()

    def add_catalog_item_handler(self) -> None:
        prompt = "Please enter item name, price (in clouds) and category, separated with commas:\n"
        item_input = self.get_processed_input(prompt)
        if not validation.validate_minimum_number_of_arguments(item_input, 3):
            return
        name, price, category = item_input
        if self.system.add_catalog_item(name, price, category):
            print("Item added successfuly.\n")
        else:
            print("Could not add item.\n")

    def update_catalog_item_handler(self) -> None:
        prompt = """\
            Please enter information in the format:
            "<current item name>, <new name>, <new price>, <new category>
            (type \"-\" for a field to leave it unchanged):
            """
        item_input = self.get_processed_input(prompt)
        if not validation.validate_minimum_number_of_arguments(item_input, 4):
            return
        name, new_name, new_price, new_category = item_input
        if self.system.update_catalog_item(
            name, new_name, new_price, new_category):
            print("Item updated successfully.\n")
        else:
            print("Could not update item.\n")

    def remove_catalog_item_handler(self) -> None:
        name = input("Please enter the name of the item to remove:\n")
        if self.system.remove_catalog_item(name):
            print("Item removed successfully.\n")
        else:
            print("Could not remove item.\n")

    def view_discounts_handler(self) -> None:
        self.system.view_discounts()

    def add_discount_handler(self) -> None:
        prompt = """\
            Discount types:
            1. Bundle discount
            2. Progressive discount
            3. Bulk purchase discount
            
            Please enter discount type number:
            """
        type = input(dedent(prompt))
        type = type.strip()
        match type:
            case '1':
                self.add_bundle_discount()
            case '2':
                self.add_progressive_discount()
            case '3':
                self.add_bulk_discount()
            case _:
                print("Invalid discount type.\n")

    def add_bundle_discount(self) -> None:
        prompt = """\
            Please enter X(number of items threshold), Y(number of items to pay for)
            and item names for the first bundle, separated with commas:
        """
        discount_input = self.get_processed_input(prompt)
        if not validation.validate_minimum_number_of_arguments(discount_input, 3):
            return
        threshold, quantity_to_pay, *first_bundle = discount_input
        if not first_bundle:
            print("Could not add discount: First bundle is empty")
            return
        bundles = [first_bundle]
        choice = input("Do you wish to add more bundles? [y/N]")
        if choice in ["y", "yes"]:
            bundles.extend(self.add_bundles(existing_bundles=bundles))
        result = self.system.add_bundle_discount(threshold, quantity_to_pay, bundles)
        self.print_discount_adding_result(result)

    def add_bundles(self, existing_bundles) -> list[list[str]]:
        new_bundles = []
        choice = "y"
        while choice in ["y", "yes"]:
            prompt = "Please enter item names for the new bundle, separated with commas:"
            bundle = self.get_processed_input(prompt)
            if not bundle:
                print("Cannot add bundle: The bundle is empty")
                continue
            if not self.validate_bundle_uniqueness(bundle, existing_bundles):
                continue
            new_bundles.append(bundle)
            choice = input("Do you wish to add more bundles? [y/N]")
        return new_bundles

    def validate_bundle_uniqueness(self, current_bundle: list[str], existing_bundles: list[list[str]]) -> bool:
        existing_bundles_items = [
            item for bundle in existing_bundles for item in bundle]
        common_items = [
            item for item in current_bundle if item in existing_bundles_items]
        if common_items:
            print(f"Cannot add bundle: It overlaps with an existing one")
            return False
        return True

    def add_progressive_discount(self) -> None:
        prompt = """\
            Please enter X(number of items threshold), Y(percentage off next item's price)
            and the item for which to apply the discount:
        """
        discount_input = self.get_processed_input(prompt)
        if not validation.validate_exact_number_of_arguments(discount_input, 3):
            return
        threshold, percentage_off_next, item = discount_input
        result = self.system.add_progressive_discount(
            threshold, percentage_off_next, item)
        self.print_discount_adding_result(result)

    def add_bulk_discount(self) -> None:
        prompt = """\
            Please enter X(minimum number of items to buy), Y(discounted price)
            and item name, separated with commas:
        """
        discount_input = self.get_processed_input(prompt)
        if not validation.validate_exact_number_of_arguments(discount_input, 3):
            return
        threshold, discounted_price, item = discount_input

        result = self.system.add_bulk_discount(threshold, discounted_price, item)
        self.print_discount_adding_result(result)
        
    def edit_discount_handler(self) -> None:
        selection = self.select_discount_by_index()
        if selection is None:
            return
        discount, index = selection
        type = discount.get_type()
        match type:
            case "bundle":
                self.edit_bundle_discount(index)
            case "progressive":
                self.edit_progressive_discount(index)
            case "bulk":
                self.edit_bulk_discount(index)
            case _:
                print("Unknown discount type.")

    def edit_bundle_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>
            (type \"-\" for a field to leave it unchanged):
            """
        numeric_data = self.get_processed_input(prompt)
        if not validation.validate_exact_number_of_arguments(numeric_data, 2):
            return
        threshold, quantity_to_pay = numeric_data

        choice = input("Do you want to replace the bundles? [y/N]")
        if choice in ["y", "yes"]:
            bundles = self.add_bundles(existing_bundles=[])
        else:
            bundles = None

        result = self.system.update_bundle_discount(discount_index, bundles,
                                           threshold, quantity_to_pay)
        self.print_discount_updating_result(result)

    def edit_progressive_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>, <new discounted item name>
            (type \"-\" for a field to leave it unchanged):
            """
        new_data = self.get_processed_input(prompt)
        if not validation.validate_exact_number_of_arguments(new_data, 3):
            return
        threshold, percentage_off_next, item_name = new_data
        result = self.system.update_progressive_discount(discount_index, item_name,
                                                threshold, percentage_off_next)
        self.print_discount_updating_result(result)

    def edit_bulk_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>, <new discounted item name>
            (type \"-\" for a field to leave it unchanged):
            """
        new_data = self.get_processed_input(prompt)
        if not validation.validate_exact_number_of_arguments(new_data, 3):
            return
        threshold, discounted_price, item_name = new_data
        result = self.system.update_bulk_discount(discount_index, item_name,
                                         threshold, discounted_price)
        self.print_discount_updating_result(result)

    def remove_discount_handler(self):
        selection = self.select_discount_by_index()
        if selection is None:
            print("Could not remove discount.")
            return
        _, index = selection

        choice = input("Are you sure you want to delete the discount? [y/N]")
        if choice in ["y", "yes"]:
            self.system.remove_discount(index)
        print("Discount removed successfully.")

    def select_discount_by_index(self) -> tuple[Discount, int] | None:
        discount_number = input("Please enter active discount number:")
        discount_number = discount_number.strip()

        if not discount_number.isnumeric():
            print("Invalid discount number")
            return
        discount_number = int(discount_number)

        index = discount_number - 1
        if not 0 <= index < len(self.system.discounts):
            print("Invalid discount number")
            return

        discount = self.system.discounts[index]
        print("Selected discount:")
        print(discount.get_info_str())
        return discount, index

    def get_processed_input(self, prompt: str = "") -> list[str]:
        input_data = input(dedent(prompt))
        print()
        return self.process_input(input_data)

    def process_input(self, input: str) -> list[str]:
        return list(map(lambda input_part: input_part.strip(), input.split(',')))

    def print_discount_adding_result(self, result: bool) -> None:
        if result:
            print("Discount added successfully.")
        else:
            print("Could not add discount.")
            
    def print_discount_updating_result(self, result: bool) -> None:
        if result:
            print("Discount updated successfully.")
        else:
            print("Could not update discount.")