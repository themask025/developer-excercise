from textwrap import dedent

from system import System
from item import Item
from discounts import Discount, BundleDiscount, ProgressiveDiscount, BulkDiscount
import discounts


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
        prompt = "Please enter item name, price (in clouds) and category, separated with commas:\n"
        item_input = self.get_processed_input(prompt)

        if len(item_input) < 3:
            print("Invalid input: not enough arguments provided")
            return

        name, price, category = item_input
        try:
            self.system.add_catalog_item(name, price, category)
        except ValueError as e:
            print(e)

    def update_catalog_item_handler(self) -> None:
        prompt = """\
            Please enter information in the format:
            "<current item name>, <new name>, <new price>, <new category>
            (type \"-\" for a field to leave it unchanged):\
            """
        item_input = self.get_processed_input(prompt)

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
        type = type.strip()

        match type:
            case "bundle":
                self.add_bundle_discount()
            case "progressive":
                self.add_progressive_discount()
            case "bulk":
                self.add_bulk_discount()
            case _:
                print("Invalid discount type.")
                return


    def add_bundle_discount(self) -> None:
        prompt = """\
            Please enter X(number of items threshold)
            and Y(number of items to pay for), separated with commas:\n
        """
        discount_input = self.get_processed_input(prompt)
        
        print(discount_input)
        
        if not self.validate_bundle_discount_numeric_input(discount_input):
            return
        threshold, quantity_to_pay = discount_input
        bundles = self.add_bundles()

        discount = BundleDiscount(bundles, int(
            threshold), int(quantity_to_pay))
        self.system.add_discount(discount)

    def validate_bundle_discount_numeric_input(self, discount_input: list[str]) -> bool:
        if not self.validate_number_of_arguments(discount_input, 2):
            return False
        threshold, quantity_to_pay = discount_input
        return self.validate_threshold(threshold) and self.validate_quantity_to_pay(quantity_to_pay)

    def validate_number_of_arguments(self, arguments: list[str], count: int) -> bool:
        if len(arguments) != count:
            print("Invalid input: not enough arguments provided")
            return False
        return True

    def validate_threshold(self, threshold: str) -> bool:
        if not threshold.isnumeric():
            print("Invalid threshold value.")
            return False
        return True

    def validate_quantity_to_pay(self, quantity_to_pay: str) -> bool:
        if not quantity_to_pay.isnumeric():
            print("Invalid number of items to pay for.")
            return False
        return True

    def add_bundles(self) -> list[list[str]]:
        bundles = []
        choice = "y"
        while choice in ["y", "yes"]:
            prompt = "Please enter new bundle items' names, separated with commas:"
            bundle = self.get_processed_input(prompt)
            if self.validate_bundle(bundle, bundles):
                bundles.append(bundle)
                print("Bundle added successfully.")
            else:
                print("Could not add bundle.")
            choice = input("Do you wish to add more bundles? [y/N]")
        return bundles

    def validate_bundle(self, bundle, existing_bundles) -> bool:
        if len(bundle) == 0:
            print("Bundle cannot be empty.")
            return False

        return self.validate_items_existence(bundle) and \
            self.validate_bundle_items_uniqueness(bundle, existing_bundles)

    def validate_items_existence(self, items: list[str]) -> bool:
        existing_names = list(map(lambda item: item.name, self.system.items))
        nonexistent_items = [
            name for name in items if name not in existing_names]
        if nonexistent_items:
            print(
                f"Cannot add discount: items \"{nonexistent_items}\" do not exist.")
            return False
        return True

    def validate_bundle_items_uniqueness(self, current_bundle: list[str], existing_bundles: list[list[str]]) -> bool:
        existing_bundles_items = [
            item for bundle in existing_bundles for item in bundle]
        common_items = [
            item for item in current_bundle if item in existing_bundles_items]
        if common_items:
            print(f"Cannot add bundle: it overlaps with an existing one")
            return False
        return True



    def add_progressive_discount(self) -> None:
        prompt = """\
            Please enter X(number of items threshold), Y(percentage off next item's price)
            and the item for which to apply the discount:
        """
        discount_input = self.get_processed_input(prompt)
        if not self.validate_progressive_discount_input(discount_input):
            return

        threshold, percentage_off_next, item = discount_input
        discount = ProgressiveDiscount(
            item, int(threshold), int(percentage_off_next))
        self.system.add_discount(discount)

    def validate_progressive_discount_input(self, discount_input):
        if not self.validate_number_of_arguments(discount_input, 3):
            return False

        threshold, percentage_off_next, item = discount_input

        return self.validate_threshold(threshold) and \
            self.validate_percentage_input(percentage_off_next) and \
            self.validate_items_existence([item])

    def validate_percentage_input(self, percentage_input: str) -> bool:
        if not percentage_input.isnumeric() or \
                not 0 <= int(percentage_input) <= 100:
            print("Invalid percentage value")
            return False
        return True



    def add_bulk_discount(self) -> None:
        prompt = """\
            Please enter X(minimum number of items to buy), Y(discounted price)
            and item name, separated with commas:
        """
        discount_input = self.get_processed_input(prompt)
        if not self.validate_bulk_discount_input(discount_input):
            return

        threshold, discounted_price, item = discount_input
        discount = BulkDiscount(item=item, threshold=int(
            threshold), new_price=int(discounted_price))
        self.system.add_discount(discount)

    def validate_bulk_discount_input(self, discount_input: list[str]) -> bool:
        if not self.validate_number_of_arguments(discount_input, 3):
            return False
        threshold, discounted_price, item = discount_input
        return self.validate_threshold(threshold) and \
            self.validate_discounted_price_input(discounted_price) and \
            self.validate_items_existence([item])

    def validate_discounted_price_input(self, discounted_price_input: str) -> bool:
        if not discounted_price_input.isnumeric():
            print("Invalid discounted price value")
            return False
        return True



    def edit_discount_handler(self):
        selection = self.select_discount_by_index()
        if selection is None:
            return
        discount, index = selection
        type = discount.get_info_list()[0]
        match type:
            case "bundle":
                self.edit_bundle_discount(index)
            case "progressive":
                self.edit_progressive_discount(index)
            case "bulk":
                self.edit_bulk_discount(index)
            case _:
                print("Unknown discount type.")
                
        

    def select_discount_by_index(self) -> tuple[Discount, int] | None:
        discount_number = input("Please enter active discount number:")
        discount_number = discount_number.strip()

        try:
            discount_number = int(discount_number)
        except ValueError:
            print("Invalid discount number")
            return

        index = discount_number - 1
        if not 0 <= index < len(self.system.discounts):
            print("Invalid discount number")
            return

        discount = self.system.discounts[index]
        print("Selected discount:")
        print(discount.get_info_str())
        return discount, index


    def edit_bundle_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>
            (type \"-\" for a field to leave it unchanged):
            """
        numeric_data = self.get_processed_input(prompt)

        if not self.validate_number_of_arguments(numeric_data, 2):
            return

        threshold, quantity_to_pay = numeric_data
        new_threshold = new_quantity_to_pay = new_bundles = None

        if threshold != '-':
            if not self.validate_threshold(threshold):
                return
            new_threshold = int(threshold)

        if quantity_to_pay != '-':
            if not self.validate_quantity_to_pay(quantity_to_pay):
                return
            new_quantity_to_pay = int(quantity_to_pay)

        choice = input("Do you wish to replace the bundles? [y/N]")
        if choice in ["y", "yes"]:
            new_bundles = self.add_bundles()

        self.system.edit_discount(discount_index, new_bundles, [
                                  new_threshold, new_quantity_to_pay])

    def edit_progressive_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>, <new discounted item name>
            (type \"-\" for a field to leave it unchanged):\
            """
        new_data = self.get_processed_input(prompt)
        if not self.validate_number_of_arguments(new_data, 3):
            return
        threshold, percentage_off_next, item_name = new_data
        new_threshold = new_percentage = new_item_name = None

        if threshold != '-':
            if not self.validate_threshold(threshold):
                return
            new_threshold = int(threshold)
        if percentage_off_next != '-':
            if not self.validate_percentage_input(percentage_off_next):
                return
            new_percentage = int(percentage_off_next)
        if item_name != '-':
            if not self.validate_items_existence([item_name]):
                return
            new_item_name = item_name

        self.system.edit_discount(discount_index, new_item_name, [
                                  new_threshold, new_percentage])

    def edit_bulk_discount(self, discount_index: int) -> None:
        prompt = """\
            Please enter information in the format:
            "<new X value>, <new Y value>, <new discounted item name>
            (type \"-\" for a field to leave it unchanged):\
            """
        new_data = self.get_processed_input(prompt)
        if not self.validate_number_of_arguments(new_data, 3):
            return
        threshold, discounted_price, item_name = new_data
        new_threshold = new_discounted_price = new_item_name = None

        if threshold != '-':
            if not self.validate_threshold(threshold):
                return
            new_threshold = int(threshold)
        if discounted_price != '-':
            if not self.validate_discounted_price_input(discounted_price):
                return
            new_discounted_price = int(discounted_price)
        if item_name != '-':
            if not self.validate_items_existence([item_name]):
                return
            new_item_name = item_name

        self.system.edit_discount(discount_index, new_item_name, [
                                  new_threshold, new_discounted_price])




    def remove_discount_handler(self):
        selection = self.select_discount_by_index()
        if selection is None:
            return
        discount, index = selection
        
        choice = input("Are you sure you want to delete the discount? [y/N]")
        if choice in ["y", "yes"]:
            self.system.remove_discount(index)

    def get_processed_input(self, prompt: str = "") -> list[str]:
        return self.process_input(input(dedent(prompt)))

    def process_input(self, input: str) -> list[str]:
        return list(map(lambda input_part: input_part.strip(), input.split(',')))
