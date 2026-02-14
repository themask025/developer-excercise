from textwrap import dedent


class Basket:
    def __init__(self) -> None:
        self.items = []

    def get_discounted_price(self) -> int:
        item_prices = list(map(
            lambda item: item.discounted_price if item.discounted_price is not None else item.normal_price, self.items))
        return sum(item_prices)

    def get_total_price(self) -> int:
        item_prices = list(map(
            lambda item: item.normal_price, self.items))
        return sum(item_prices)
    
    def get_receipt_str(self) -> str:
        info = "Item, Category, Normal Price, Discounted Price, Applied Discount No.\n"
        for item in self.items:
            if item.discounted_price is not None:
                discounted_price = item.discounted_price
            else:
                discounted_price = '-'
            if item.applied_discount_id is not None:
                discount_id = item.applied_discount_id + 1
            else:
                discount_id = 'no discount'
            info = info + f"{item.name}, {item.category}, {item.normal_price}c, {discounted_price}, {discount_id}\n"
        info = info + "----------------------------------\n"
        total = self.get_total_price()
        discounted_total = self.get_discounted_price()
        aws_normal, clouds_normal = self.calculate_aws(total)
        aws_discounted, clouds_discounted = self.calculate_aws(discounted_total)
        prices = f"""\
        Total price:          {total}c = {aws_normal} aws {clouds_normal} clouds
        Price with discounts: {discounted_total}c = {aws_discounted} aws {clouds_discounted} clouds
        Saved:                {total - discounted_total}c\
        """
        return info + dedent(prices)
    
    def calculate_aws(self, clouds:int) -> tuple[int, int]:
        return clouds//100, clouds%100
