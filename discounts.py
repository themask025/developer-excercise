from abc import ABC, abstractmethod

from item import Item


class Discount(ABC):
    @abstractmethod
    def apply_to_basket() -> None:
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


class BulkDiscount(Discount):
    def __init__(self,
                 items: list[Item] | None = None,
                 threshold: int | None = None,
                 new_price: int | None = None) -> None:
        self.items = items
        self.threshold = threshold
        self.new_price = new_price
