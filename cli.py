from textwrap import dedent

from system import System
from item import Item


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
        items = items_input.split(',')
        items = list(map(lambda item: item.strip(), items))


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
                    self.system.view_catalog_items()
                case '2':
                    self.add_catalog_item_handler()
                case '3':
                    self.update_catalog_item_handler()
                case '4':
                    self.remove_catalog_item_handler()
                case '5':
                    self.system.view_discounts()
                case '6':
                    self.system.add_discount()
                case '7':
                    self.system.edit_discount()
                case '8':
                    self.system.remove_discount()
                case '9':
                    print("Returning to main menu...")
                    break
                case _:
                    print("Invalid action.\n")

    def add_catalog_item_handler(self) -> None:
        item_input = input(
            "Please enter item name, price (in clouds) and category, separated with commas:\n")
        item_input = item_input.split(',')
        item_input = list(
            map(lambda item: item.strip(), item_input))
        
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
            
    
