from textwrap import dedent

from system import System
from item import Item
from discounts import BundleDiscount


class CLI:
    def __init__(self, system: System = System()) -> None:
        self.system = system

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
                    self.begin_scanning()
                case '2':
                    self.configure_till()
                case '3':
                    break
                case _:
                    print("Invalid action.\n")

        print("Exiting the system...")

    def begin_scanning(self) -> None:
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
                    self.scan_items()
                case '2':
                    self.finalize()
                    break
                case '3':
                    print("Emptying basket...\n")
                    break
                case _:
                    print("Invalid action.\n")

        print("Returning to main menu...\n")

    def scan_items(self) -> None:
        items_input = input(
            "List names of items to scan (separated with commas):")
        items = self.process_input(items_input)

        print("Scanning items...\n")

    def finalize(self) -> None:
        print("Finalizing...\n")

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
                
                9. Return to main menu\
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

    def view_catalog_items_handler(self) -> None:
        self.system.view_catalog_items()

    def add_catalog_item_handler(self) -> None:
        item_input = input(
            "Please enter item name, price (in clouds) and category, separated with commas:\n")
        item_input = self.process_input(item_input)

        if len(item_input) < 3:
            print("Invalid input: not enough arguments provided")
            return

        name, price, category = item_input
        try:
            self.system.add_catalog_item(name, price, category)
        except ValueError as e:
            print(e)

    def update_catalog_item_handler(self) -> None:
        item_input = input(
            "Please enter information in the format:\n \
            \"<current item name>, <new name>, <new price>, <new category>\"\n \
            (type \"-\" for a field to leave it unchanged):")
        item_input = item_input.split(',')
        item_input = list(
            map(lambda item: item.strip(), item_input))

        if len(item_input) < 4:
            print("Invalid input: not enough arguments provided")
            return

        name, new_name, new_price, new_category = item_input
        try:
            self.system.update_catalog_item(
                name, new_name, new_price, new_category)
        except ValueError as e:
            print(e)

    def remove_catalog_item_handler(self) -> None:
        name = input("Please enter the name of the item to remove:\n")

        try:
            self.system.remove_catalog_item(name)
        except ValueError as e:
            print(e)

    def view_discounts_handler(self) -> None:
        self.system.view_discounts()

    def add_discount_handler(self) -> None:
        type = input("Please enter discount type (bundle, progressive, bulk):")

        match type:
            case "bundle":
                self.add_bundle_discount()
            case "progressive":
                pass
            case "bulk":
                pass
            case _:
                print("Invalid discount type.")
                return

    def add_bundle_discount(self) -> None:
        prompt = """\
            Please enter X(number of items threshold), Y(number of items to pay for)
            and the items in the first bundle, all separated with commas:
        """
        discount_input = input(dedent(prompt))
        discount_input = self.process_input(discount_input)
        threshold, quantity_to_pay, *bundle = discount_input

        if not self.validate_bundle_discount_parameters(threshold, quantity_to_pay, bundle):
            return

        bundles = [bundle]

        choice = input("Do you wish to add more bundles? [y/N]")
        self.add_additional_bundles(choice, current_bundles=bundles)
        
        discount = BundleDiscount(bundles, int(threshold), int(quantity_to_pay))
        self.system.add_discount(discount)

    def validate_bundle_discount_parameters(self, threshold: str, quantity_to_pay: str, bundle: list[str]) -> bool:
        if not threshold.isnumeric():
            print("Invalid threshold value.")
            return False
        if not quantity_to_pay.isnumeric():
            print("Invalid number of items to pay for.")
            return False
        if not self.validate_bundle_items_existence(bundle):
            return False
        return True

    def add_additional_bundles(self, choice: str, current_bundles: list[list[str]]) -> None:
        while choice in ["y", "yes"]:
            bundle_input = input(
                "Please enter bundle items' names, separated with commas:")
            bundle = self.process_input(bundle_input)
            if not self.validate_bundle_items_existence(bundle):
                return
            if self.validate_bundle_items_uniqueness(bundle, current_bundles):
                current_bundles.append(bundle)
            choice = input("Do you wish to add more bundles? [y/N]")

    def validate_bundle_items_existence(self, bundle: list[str]) -> bool:
        items_names = list(map(lambda item: item.name, self.system.items))
        non_existent_items = [
            name for name in bundle if name not in items_names]
        if non_existent_items:
            print(
                f"Cannot add discount: items \"{non_existent_items}\" do not exist.")
            return False
        return True

    def validate_bundle_items_uniqueness(self, bundle, bundles):
        existing_bundles_items = [
            item for bundle in bundles for item in bundle]
        common_items = [
            item for item in bundle if item in existing_bundles_items]
        if common_items:
            print(f"Cannot add bundle: it overlaps with an existing one")
            return False
        return True

    def edit_discount_handler(self):
        pass

    def remove_discount_handler(self):
        pass

    def process_input(self, input: str) -> list[str]:
        return list(map(lambda input_part: input_part.strip(), input.split(',')))
