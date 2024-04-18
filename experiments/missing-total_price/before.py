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

    def remove_item(self, item_name: str, quantity: int) -> None:
        assert quantity > 0, "Quantity must be positive"
        assert item_name in self.items, f"Item '{item_name}' not in cart"
        assert (
            self.items[item_name] >= quantity
        ), f"Insufficient quantity of '{item_name}'"

        self.items[item_name] -= quantity
        if self.items[item_name] == 0:
            del self.items[item_name]
    def calculate_total_price(self, item_prices: dict[str, float]) -> float:
        assert isinstance(item_prices, dict), "Item prices must be a dictionary"
        assert all(isinstance(price, float) for price in item_prices.values()), "Item prices must be floats"
        assert all(item_name in item_prices for item_name in self.items), "Item prices missing for some items"
        
        total_price = sum(self.items[item_name] * item_prices[item_name] for item_name in self.items)
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

    # Trigger remove_item assertion (non-positive quantity)
    try:
        cart.remove_item("Apple", 0)
    except AssertionError as e:
        print(f"Assertion Error (remove_item - quantity): {e}")

    # Trigger remove_item assertion (missing item)
    try:
        cart.remove_item("Grape", 1)
    except AssertionError as e:
        print(f"Assertion Error (remove_item - missing item): {e}")

    # Trigger remove_item assertion (insufficient quantity)
    try:
        cart.remove_item("Orange", 5)  # Only 4 oranges in cart
    except AssertionError as e:
        print(f"Assertion Error (remove_item - insufficient quantity): {e}")

    # Valid item removal
    cart.remove_item("Apple", 1)

    cart.remove_item("Apple", 1)
    # Calculate and print the total price
    # total_price = cart.calculate_total_price({"Apple": 1.0, "Banana": 1.5, "Orange": 2.0})
    # print(f"Total Price: ${total_price}")
    