from abc import ABC, abstractmethod

from item import Item


class Discount(ABC):
    @abstractmethod
    def apply_to_basket(self) -> None:
        pass

    @abstractmethod
    def print_info(self) -> None:
        pass


class BundleDiscount(Discount):
    def __init__(self,
                 bundles: list[list[str]],
                 threshold: int | None = None,
                 quantity_to_pay: int | None = None) -> None:
        self.bundles = bundles
        self.threshold = threshold
        self.quantity_to_pay = quantity_to_pay

    def print_info(self) -> None:
        info = f"Bulk Discount: {self.threshold} for {self.quantity_to_pay} on {self.bundles[0]}"
        for bundle in self.bundles[1:]:
            info = info + f", {bundle}"
        print(info)
        
    def apply_to_basket(self) -> None:
        pass


class ProgressiveDiscount(Discount):
    def __init__(self,
                 items: list[str],
                 threshold: int | None = None,
                 percentage_off_next: int | None = None) -> None:
        self.items = items
        self.threshold = threshold
        self.percentage_off_next = percentage_off_next

    def print_info(self) -> None:
        info = f"Progressive Discount: Buy {self.threshold} Get 1 at {self.percentage_off_next}% off on {self.items[0]}"
        for item in self.items:
            info = info + f", {item}"
        print(info)


class BulkDiscount(Discount):
    def __init__(self,
                 item: str,
                 threshold: int | None = None,
                 new_price: int | None = None) -> None:
        self.item = item
        self.threshold = threshold
        self.new_price = new_price

    def print_info(self) -> None:
        print(f"Bulk Purchase: {self.threshold} or more \"{self.item}\" for {self.new_price}c each")
