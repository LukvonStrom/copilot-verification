class ShoppingCart:

    def __init__(self, max_items: int):
        self.max_items = max_items
        self.items: dict[str, float] = {}

    def add_item(self, item_name: str, quantity: int) -> None:
        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def remove_item(self, item_name: str, quantity: int) -> None:
        self.items[item_name] -= quantity
        if self.items[item_name] == 0:
            del self.items[item_name]

    def get_total_price(self, item_prices: dict[str, float]) -> float:
        total_price:float = 0
        for item_name, quantity in self.items.items():
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
