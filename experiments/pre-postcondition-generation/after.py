class ShoppingCart:

    def __init__(self, max_items: int):
        self.max_items = max_items
        self.items: dict[str, float] = {}

    def add_item(self, item_name: str, quantity: int) -> None:
        assert quantity >= 0, "Quantity must be non-negative."
        assert isinstance(quantity, int), "Quantity must be an integer."
        assert item_name != "", "Item name must not be empty."
        
        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def remove_item(self, item_name: str, quantity: int) -> None:
        assert item_name in self.items, f"Item '{item_name}' not found in shopping cart."
        assert quantity >= 0, f"Quantity of item '{item_name}' must be non-negative."
        assert isinstance(quantity, int), f"Quantity of item '{item_name}' must be an integer."
        
        self.items[item_name] -= quantity
        if self.items[item_name] == 0:
            del self.items[item_name]

    def get_total_price(self, item_prices: dict[str, float]) -> float:
        assert isinstance(item_prices, dict), "Item prices must be a dictionary."
        assert all(isinstance(price, float) for price in item_prices.values()), "Item prices must be floats."
        
        total_price: float = 0
        for item_name, quantity in self.items.items():
            assert item_name in item_prices, f"Item '{item_name}' not found in item prices."
            assert quantity >= 0, f"Quantity of item '{item_name}' must be non-negative."
            assert isinstance(quantity, int), f"Quantity of item '{item_name}' must be an integer."
            
            total_price += item_prices[item_name] * quantity
        return total_price


if __name__ == "__main__":

    cart = ShoppingCart(max_items=-5)
    cart = ShoppingCart(max_items=10)

    cart.add_item("Apple", 0)
    cart.add_item("Apple", 11)

    cart.add_item("Apple", 3)
    cart.add_item("Banana", 2)
    cart.add_item("Orange", 4)

    cart.remove_item("Apple", 0)

    cart.remove_item("Grape", 1)

    cart.remove_item("Orange", 5)

    cart.remove_item("Apple", 1)

    item_prices = {"Banana": 0.3, "Orange": 0.4}
    cart.get_total_price(item_prices)

    # Valid scenario with complete item prices
    item_prices = {"Apple": 0.5, "Banana": 0.3, "Orange": 0.4}
    total_price = cart.get_total_price(item_prices)
    print(f"Total price: {total_price:.2f}GBP")
