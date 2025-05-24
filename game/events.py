import random
import json
import os
from datetime import datetime

class RandomEventSystem:
    """
    Random event system: load event configurations from data/events.json,
    randomly trigger events based on game state and defined weights, and record event logs.
    """
    def __init__(self, pet, economy, config_path='data/events.json'):
        self.pet = pet
        self.economy = economy
        # Load event configurations from JSON file
        path = os.path.join(os.getcwd(), config_path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.events = json.load(f)
        except Exception as e:
            print(f"Failed to load event configurations: {e}")
            self.events = []
        # Initialize event trigger log
        self.event_log = []

    def trigger(self):

        # Chance filter: only continue with a 40% probability.
        # The 40% probability here is to balance the pace of the game.
        if random.random() > 0.4:
            return

        # Filter events by condition and build weighted candidate list
        candidates = []
        for ev in self.events:
            cond = ev.get('condition', {})
            min_h = cond.get('min_hunger', 0)
            max_h = cond.get('max_hunger', 100)
            if min_h <= self.pet.hunger <= max_h:
                weight = ev.get('weight', 1)
                candidates.extend([ev] * weight)
        if not candidates:
            return
        ev = random.choice(candidates)

        # Extract attribute deltas
        delta_h = ev.get('happiness', 0)
        delta_e = ev.get('energy', 0)
        delta_g = ev.get('hunger', 0)
        delta_c = ev.get('coins', 0)
        delta_health = ev.get('health', 0)

        # Adjust coins
        if delta_c:
            if delta_c > 0:
                self.economy.earn(delta_c)
            else:
                self.economy.spend(-delta_c)

        # Adjust other attributes with clamping to [0,100]
        self.pet.happiness = min(100, max(0, self.pet.happiness + delta_h))
        self.pet.energy    = min(100, max(0, self.pet.energy + delta_e))
        self.pet.hunger    = min(100, max(0, self.pet.hunger + delta_g))
        self.pet.health    = min(100, max(0, self.pet.health + delta_health))

        # Format and print event text
        text = ev.get('text', '').format(pet_name=self.pet.name)
        print(f"[Event] {text}")

        # Record the event in the log
        self.event_log.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key': ev.get('key'),
            'text': text,
            'happiness_change': delta_h,
            'energy_change': delta_e,
            'hunger_change': delta_g,
            'health_change': delta_health
        })

    def get_log(self):
        """
        Return a list of logged events that have been triggered.
        """
        return list(self.event_log)
