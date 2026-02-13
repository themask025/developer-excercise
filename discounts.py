from abc import ABC, abstractmethod

from item import Item


class Discount(ABC):
    @abstractmethod
    def apply_to_basket(self) -> None:
        pass

    @abstractmethod
    def get_info_str(self) -> str:
        pass

    @abstractmethod
    def get_info_list(self) -> list[list[list[str]] | str | int]:
        pass
    
    @abstractmethod
    def update_info_from_list(self, item_data: str | list[list[str]] | None, numeric_data: list[int | None]) -> None:
        pass

class BundleDiscount(Discount):
    def __init__(self,
                 bundles: list[list[str]],
                 threshold: int,
                 quantity_to_pay: int) -> None:
        self.bundles = bundles
        self.threshold = threshold
        self.quantity_to_pay = quantity_to_pay

    def apply_to_basket(self) -> None:
        pass

    def get_info_str(self) -> str:
        info = f"Bulk Discount: {self.threshold} for {self.quantity_to_pay} on {self.bundles[0]}"
        
        for bundle in self.bundles[1:]:
            info = info + f", {bundle}"
        return info

    def get_info_list(self) -> list[list[list[str]] | str | int]:
        return ['bundle', self.bundles, self.threshold, self.quantity_to_pay]
    
    def update_info_from_list(self, item_data: str | list[list[str]] | None, numeric_data: list[int | None]) -> None:
        new_bundles = item_data
        new_threshold, new_quantity_to_pay = numeric_data
        if new_bundles is not None:
            self.bundles = new_bundles
        if new_threshold is not None:
            self.threshold = new_threshold
        if new_quantity_to_pay is not None:
            self.quantity_to_pay = new_quantity_to_pay

class ProgressiveDiscount(Discount):
    def __init__(self,
                 item: str,
                 threshold: int,
                 percentage_off_next: int) -> None:
        self.item = item
        self.threshold = threshold
        self.percentage_off_next = percentage_off_next

    def apply_to_basket(self) -> None:
        pass

    def get_info_str(self) -> str:
        return f"Progressive Discount: Buy {self.threshold} Get 1 at {self.percentage_off_next}% off on \"{self.item}\""
            
    def get_info_list(self) -> list[list[list[str]] | str | int]:
        return ['progressive', self.item, self.threshold, self.percentage_off_next]
    
    def update_info_from_list(self, item_data: str | list[list[str]] | None, numeric_data: list[int | None]) -> None:
        if item_data is not None:
            self.item = item_data
            
        new_threshold, new_percentage = numeric_data
        if new_threshold is not None:
            self.threshold = new_threshold
        if new_percentage is not None:
            self.percentage_off_next = new_percentage


class BulkDiscount(Discount):
    def __init__(self,
                 item: str,
                 threshold: int,
                 new_price: int) -> None:
        self.item = item
        self.threshold = threshold
        self.new_price = new_price

    def apply_to_basket(self) -> None:
        pass

    def get_info_str(self) -> str:
        return f"Bulk Purchase: {self.threshold} or more \"{self.item}\" for {self.new_price}c each"

    def get_info_list(self) -> list[list[list[str]] | str | int]:
        return ['bulk', self.item, self.threshold, self.new_price]
    
    def update_info_from_list(self, item_data: str | list[list[str]] | None, numeric_data: list[int | None]) -> None:
        if item_data is not None:
            self.item = item_data
            
        new_threshold, new_discounted_price = numeric_data
        if new_threshold is not None:
            self.threshold = new_threshold
        if new_discounted_price is not None:
            self.new_price = new_discounted_price