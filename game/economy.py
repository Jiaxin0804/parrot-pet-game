class Economy:

    """
    The economic system of the pet game, which handles coins, inventory and bird feed.
    coins (integer): The number of coins the player currently has.
    feed_stock (integer): The current inventory of bird feed units.
    buy_price (integer): The number of coins required to buy one unit of bird feed.
    """

    def __init__(self):
        self.coins = 20
        self.feed_stock = 5    # Initial bird feed stock
        self.buy_price = 5     # Coins per feed unit purchase

    def earn(self, amount: int):
        """
        Increase the player's coin balance.
        """
        self.coins += amount

    def spend(self, cost: int) -> bool:
        """
        Deduct coins for a given cost.
        """
        if self.coins >= cost:
            self.coins -= cost
            return True
        return False

    def buy_feed(self, amount: int = 1) -> bool:
        """
        Spend coins to buy bird food.
        """
        cost = amount * self.buy_price
        if self.spend(cost):
            self.feed_stock += amount
            return True
        return False
