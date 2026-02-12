from item import Item


class Basket:
    def __init__(self,
                 items: list[Item] = []) -> None:
        self.items = items
