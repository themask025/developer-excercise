from abc import ABC, abstractmethod

from basket import Basket


class Discount(ABC):
    @abstractmethod
    def apply_to_basket(self, basket: Basket, discount_id: int) -> None:
        pass

    @abstractmethod
    def get_info_str(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
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

    def apply_to_basket(self, basket: Basket, discount_id: int) -> None:
        for bundle in self.bundles:
            eligible_items_indices = self.get_eligible_items_indices(
                basket, bundle)
            if not eligible_items_indices:
                continue
            self.discount_items(
                basket, eligible_items_indices, bundle, discount_id)

    def get_eligible_items_indices(self, basket: Basket, bundle: list[str] | str) -> list[int]:
        return [index for (index, item) in enumerate(basket.items) if item.name in bundle and item.applied_discount_id is None]

    def discount_items(self, basket: Basket, eligible_indices: list[int], bundle: list[str] | str, discount_id: int) -> None:
        if len(eligible_indices) < self.threshold:
            return
        candidates = eligible_indices[:self.threshold]
        candidates.sort(key=lambda index: basket.items[index].normal_price)
        quantity_to_discount = self.threshold - self.quantity_to_pay
        cheapest = candidates[:quantity_to_discount]
        basket_size = len(basket.items)
        for index in range(basket_size):
            if index in candidates:
                basket.items[index].applied_discount_id = discount_id
            if index in cheapest:
                basket.items[index].discounted_price = 0

    def get_info_str(self) -> str:
        info = f"Bundle Discount: {self.threshold} for {self.quantity_to_pay} on {self.bundles[0]}"

        for bundle in self.bundles[1:]:
            info = info + f", {bundle}"
        return info
    
    def get_type(self) -> str:
        return "bundle"

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

    def apply_to_basket(self, basket: Basket, discount_id: int) -> None:
        eligible_items_indices = self.get_eligible_items_indices(basket)
        if not eligible_items_indices:
            return
        self.discount_items(basket, eligible_items_indices, discount_id)

    def get_eligible_items_indices(self, basket: Basket) -> list[int]:
        return [index for (index, item) in enumerate(basket.items) if item.name == self.item and item.applied_discount_id is None]

    def discount_items(self, basket: Basket, eligible_indices: list[int], discount_id: int) -> None:
        candidate_group_size = self.threshold + 1
        if len(eligible_indices) < candidate_group_size:
            return
        candidate_groups_count = len(eligible_indices) // candidate_group_size
        candidates_count = candidate_groups_count * candidate_group_size
        candidates = eligible_indices[:candidates_count]
        items_to_discount = candidates[:candidate_groups_count]
        basket_size = len(basket.items)
        for index in range(basket_size):
            if index in candidates:
                basket.items[index].applied_discount_id = discount_id
            if index in items_to_discount:
                price = basket.items[index].normal_price
                basket.items[index].discounted_price = price - \
                    round((self.percentage_off_next/100)*price)

    def get_info_str(self) -> str:
        return f"Progressive Discount: Buy {self.threshold} Get 1 at {self.percentage_off_next}% off on \"{self.item}\""

    def get_type(self) -> str:
        return "progressive"

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

    def apply_to_basket(self, basket: Basket, discount_id: int) -> None:
        eligible_items_indices = self.get_eligible_items_indices(basket)
        if not eligible_items_indices:
            return
        self.discount_items(basket, eligible_items_indices, discount_id)

    def get_eligible_items_indices(self, basket: Basket) -> list[int]:
        return [index for (index, item) in enumerate(basket.items) if item.name == self.item and item.applied_discount_id is None]

    def discount_items(self, basket: Basket, eligible_indices: list[int], discount_id: int) -> None:
        if len(eligible_indices) < self.threshold:
            return
        basket_size = len(basket.items)
        for index in range(basket_size):
            if index in eligible_indices:
                basket.items[index].applied_discount_id = discount_id
                basket.items[index].discounted_price = self.new_price

    def get_info_str(self) -> str:
        return f"Bulk Purchase: {self.threshold} or more \"{self.item}\" for {self.new_price}c each"
    
    def get_type(self) -> str:
        return "bulk"

    def update_info_from_list(self, item_data: str | list[list[str]] | None, numeric_data: list[int | None]) -> None:
        if item_data is not None:
            self.item = item_data

        new_threshold, new_discounted_price = numeric_data
        if new_threshold is not None:
            self.threshold = new_threshold
        if new_discounted_price is not None:
            self.new_price = new_discounted_price
