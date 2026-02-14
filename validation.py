from item import Item

def validate_bundle_discount_input(threshold: str, quantity_to_pay: str, bundles: list[list[str]], existing_items: list[Item]) -> bool:
    bundles_items = [item_name for bundle in bundles for item_name in bundle]
    return validate_threshold(threshold) and\
        validate_quantity_to_pay(quantity_to_pay) and \
        validate_items_existence(bundles_items, existing_items)


def validate_bulk_discount_input(threshold: str, discounted_price: str, item: str, existing_items: list[Item]) -> bool:
    return validate_threshold(threshold) and \
        validate_discounted_price_input(discounted_price) and \
        validate_items_existence([item], existing_items)


def validate_progressive_discount_input(threshold: str, percentage_off_next: str, item: str, existing_items: list[Item]) -> bool:
    return validate_threshold(threshold) and \
        validate_percentage_input(percentage_off_next) and \
        validate_items_existence([item], existing_items)


def validate_items_existence(items: list[str], existing_items: list[Item]) -> bool:
    existing_names = list(map(lambda item: item.name, existing_items))
    nonexistent_items = [name for name in items if name not in existing_names]
    if nonexistent_items:
        print(
            f"Invalid input: items \"{nonexistent_items}\" do not exist.")
        return False
    return True


def validate_threshold(threshold: str) -> bool:
    if not threshold.isnumeric():
        print("Invalid threshold value.")
        return False
    return True


def validate_quantity_to_pay(quantity_to_pay: str) -> bool:
    if not quantity_to_pay.isnumeric():
        print("Invalid number of items to pay for.")
        return False
    return True


def validate_percentage_input(percentage_input: str) -> bool:
    if not percentage_input.isnumeric() or \
            not 0 <= int(percentage_input) <= 100:
        print("Invalid percentage value")
        return False
    return True


def validate_discounted_price_input(discounted_price_input: str) -> bool:
    if not discounted_price_input.isnumeric():
        print("Invalid discounted price value")
        return False
    return True