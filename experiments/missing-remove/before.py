class ShoppingCart:

    def __init__(self, max_items: int):
        assert max_items > 0, "Maximum items must be positive"
        self.max_items = max_items
        self.items: dict[str, float] = {}

    def add_item(self, item_name: str, quantity: int) -> None:
        assert quantity > 0, "Quantity must be positive"
        total_items = sum(self.items.values()) + quantity
        assert total_items <= self.max_items, "Maximum item limit reached"

        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def get_total_price(self, item_prices: dict[str, float]) -> float:
        total_price:float = 0 
        for item_name, quantity in self.items.items():
            assert item_name in item_prices, f"Price for '{item_name}' not defined"
            total_price += item_prices[item_name] * quantity
        return total_price


if __name__ == "__main__":
    # Trigger max_items assertion (negative value)
    try:
        cart = ShoppingCart(max_items=-5)
    except AssertionError as e:
        print(f"Assertion Error (init): {e}")

    # Trigger positive scenario
    cart = ShoppingCart(max_items=10)

    # Trigger quantity assertion (non-positive)
    try:
        cart.add_item("Apple", 0)
    except AssertionError as e:
        print(f"Assertion Error (add_item - quantity): {e}")

    # Trigger max_items assertion (adding too many)
    try:
        cart.add_item("Apple", 11)
    except AssertionError as e:
        print(f"Assertion Error (add_item - max_items): {e}")

    # Valid item addition
    cart.add_item("Apple", 3)
    cart.add_item("Banana", 2)
    cart.add_item("Orange", 4)

    # Trigger get_total_price assertion (missing price)
    item_prices = {"Banana": 0.3, "Orange": 0.4}
    try:
        cart.get_total_price(item_prices)
    except AssertionError as e:
        print(f"Assertion Error (get_total_price - missing price): {e}")

    # Valid scenario with complete item prices
    item_prices = {"Apple": 0.5, "Banana": 0.3, "Orange": 0.4}
    total_price = cart.get_total_price(item_prices)
    print(f"Total price: {total_price:.2f}GBP")
