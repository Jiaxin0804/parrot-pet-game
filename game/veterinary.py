class Veterinary:
    """
    Veterinary treatment system for pet games.
    Costs 15 coins and fully restores the health and energy of your pet.
    """
    def __init__(self, pet, economy):
        """
        Initialize the Veterinary system.
        """
        self.pet = pet
        self.economy = economy

    def visit(self):
        """
        Costs 15 coins and fully restores health and energy.
        """
        cost = 15
        # Spend coins for treatment
        if self.economy.spend(cost):
            # Fully restore health and energy
            self.pet.health = 100
            self.pet.energy = 100
            print(f"Treatment successful: Health fully restored, Energy fully restored, Coins spent: {cost}.")
        else:
            print("Insufficient coins for treatment.")
