class Pet:
    """
    Tracks your pet's hunger, happiness, energy, and health, letting you know how your pet is doing at all times.
    When any of these data reaches dangerous levels, a timer starts,
    giving you a chance to intervene before the situation gets worse.
    If the time limit is exceeded, it records exactly why the game was lost.
    """
    def __init__(self, name: str):
        """
        Initialize a new pet with default attribute levels.
        """
        self.name = name
        self.hunger = 0          # Hunger level (0-100)
        self.happiness = 100     # Happiness level (0-100)
        self.energy = 100        # Energy level (0-100)
        self.health = 100        # Health level (0-100)

        # Timers for critical states (in seconds)
        self.hunger_timer = 0    # Timer for sustained high hunger (>80)
        self.unhappy_timer = 0   # Timer for sustained low happiness (<20)
        self.neglect_timer = 0   # Timer for sustained low health (<30)

        self.failure_reason = None  # Reason for game over ('neglect', 'protection', 'death')

    def update(self, delta: float):
        """
        Update the pet's status over elapsed time.
        """
        # Base attribute decay and growth
        self.hunger = min(100, self.hunger + delta * 1.0)
        self.happiness = max(0, self.happiness - delta * 0.5)
        self.energy = max(0, self.energy - delta * 0.5)

        # Death occurs immediately when starvation or energy deficiency occurs
        if self.hunger >= 100 or self.energy <= 0:
            self.failure_reason = 'neglect'
            self.health = 0
            return

        # If the hunger value is ≥80 for 30 seconds, pet will be taken away by the animal protection organization
        if self.hunger >= 80:
            self.hunger_timer += delta
            if self.hunger_timer >= 30:
                self.failure_reason = 'protection'
                self.health = 0
                return
        else:
            self.hunger_timer = 0

        # If happiness ≤20 sustained for 30s, pet will be taken away by the animal protection organization
        if self.happiness <= 20:
            self.unhappy_timer += delta
            if self.unhappy_timer >= 30:
                self.failure_reason = 'protection'
                self.health = 0
                return
        else:
            self.unhappy_timer = 0

        # If health <30 sustained for 20s, pet dies
        if self.health < 30:
            self.neglect_timer += delta
            if self.neglect_timer >= 20:
                self.failure_reason = 'death'
                self.health = 0
                return
        else:
            self.neglect_timer = 0

    def play(self, duration=1):
        """
        Interact with the pet, Increase pleasure while decreasing energy.
        """
        happiness_gain = 15 * duration
        energy_cost = 10 * duration
        self.happiness = min(100, self.happiness + happiness_gain)
        self.energy = max(0, self.energy - energy_cost)
        return happiness_gain, energy_cost

    def is_alive(self) -> bool:
        """
        Check if the pet is still alive.
        """
        return self.health > 0
