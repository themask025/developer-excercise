from abc import ABC, abstractmethod


class Item:
    def __init__(self, name: str | None = None, 
                 price: int | None = None, 
                 category: str | None = None) -> None:
        self.name = name
        self.price = price
        self.category = category


class Discount(ABC):
    @abstractmethod
    def apply_discount() -> None:
        pass


class BundleDiscount(Discount):
    def __init__(self, 
                 bundles: list[list[Item]] | None = None, 
                 threshold: int | None = None, 
                 quantity_to_pay: int | None = None) -> None:
        self.bundles = bundles
        self.threshold = threshold
        self.quantity_to_pay = quantity_to_pay


class ProgressiveDiscount(Discount):
    def __init__(self, 
                 items: list[Item] | None = None, 
                 threshold: int | None = None, 
                 percentage_off_next: int | None = None) -> None:
        self.items = items
        self.threshold = threshold
        self.percentage_off_next = percentage_off_next
        pass


class BulkDiscount(Discount):
    def __init__(self, 
                 items: list[Item] | None = None, 
                 threshold: int | None = None, 
                 new_price: int | None = None) -> None:
        self.items = items
        self.threshold = threshold
        self.new_price = new_price


class System:
    def __init__(self, items: list[Item] | None = None, 
                 discounts: list[Discount] | None = None, 
                 basket=None) -> None:
        self.items = items
        self.discounts = discounts
        self.basket = basket

    def start_scanning(self) -> None:
        pass

    def add_item(self) -> None:
        pass

    def edit_item(self) -> None:
        pass

    def remove_item(self) -> None:
        pass

    def view_items(self) -> None:
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


def begin_scanning() -> None:
    running_total = 0
    user_action = 0

    while user_action != '3':
        print(f"Running total = {running_total}c")

        print("Available actions:")
        print("1. Scan items")
        print("2. Finalize")
        print("3. Discard and exit")

        user_action = input("Please choose an action (using numbers):")
        print("\n")

        match user_action:
            case '1':
                scan_items()
            case '2':
                finalize()
                break
            case '3':
                print("Emptying basket...\n")
                break

    print("Returning to main menu...\n")


def scan_items() -> None:
    print("Scanning items...\n")


def finalize() -> None:
    print("Finalizing...\n")


def configure_till() -> None:
    print("Configuring till...\n")


def cli() -> None:
    print("Grocery Store Till System")

    user_action = None

    while user_action != '3':
        print("Available actions:")
        print("1. Begin scanning")
        print("2. Configure till")
        print("3. Exit")

        user_action = input("Please choose an action (using numbers):")
        print("\n")

        match user_action:
            case '1':
                begin_scanning()
            case '2':
                configure_till()
            case '3':
                break

    print("Exiting the system...")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
