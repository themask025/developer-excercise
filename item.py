class Item:
    def __init__(self, name: str,
                 category: str,
                 normal_price: int,
                 discounted_price: int | None = None,
                 applied_discount_id: int | None = None) -> None:
        self.name = name
        self.category = category
        self.normal_price = normal_price
        self.discounted_price = discounted_price
        self.applied_discount_id = applied_discount_id
