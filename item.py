class Item:
    def __init__(self, name: str,
                 category: str,
                 normal_price: int) -> None:
        self.name = name
        self.category = category
        self.normal_price = normal_price
        self.discounted_price = None
        self.applied_discount_id = None
