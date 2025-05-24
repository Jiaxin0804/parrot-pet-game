import random
from datetime import datetime

class TravelSystem:
    """
    Travel system: provides a variety of location options, scene templates,
    attribute adjustments, and records travel memories.
    """
    def __init__(self, pet):
        """
        Initialize the TravelSystem with a reference to the pet.
        """
        self.pet = pet

        # Define available travel locations and their scenario templates
        self.locations = {
            'beach': {
                'name': 'A golden beach where you can pick up small shells and crabs',
                'scenarios': [
                    {
                        'text': '{name} runs along the shoreline, listening to the waves crash, feeling completely relaxed.',
                        'happiness': +10,
                        'energy': -5
                    },
                    {
                        'text': 'An unexpected storm forces {name} to return to you in a hurry.',
                        'happiness': -5,
                        'energy': -10
                    }
                ]
            },
            'forest': {
                'name': 'A misty forest where wild animals may roam',
                'scenarios': [
                    {
                        'text': 'Birdsong surrounds {name} in the woods, making it feel one with nature.',
                        'happiness': +8,
                        'energy': -8
                    },
                    {
                        'text': 'A confusing path makes {name} anxious, and it rushes back.',
                        'happiness': -7,
                        'energy': -5
                    }
                ]
            },
            'mountain': {
                'name': 'A majestic mountain with a view of the clouds',
                'scenarios': [
                    {
                        'text': '{name} conquers the summit and looks out over the horizon, filled with a sense of accomplishment.',
                        'happiness': +12,
                        'energy': -12
                    },
                    {
                        'text': 'Sudden altitude sickness makes {name} dizzy, forcing a premature descent.',
                        'happiness': -4,
                        'energy': -15
                    }
                ]
            },
            'city': {
                'name': 'A bustling city with tall buildings and shopping malls everywhere',
                'scenarios': [
                    {
                        'text': 'The neon lights of the city dazzle {name}, quickening its heartbeat.',
                        'happiness': +6,
                        'energy': -6
                    },
                    {
                        'text': 'Crowds tire out {name}, who returns with mixed feelings.',
                        'happiness': -6,
                        'energy': -8
                    }
                ]
            }
        }
        # Store memories of each trip
        self.memories = []

    def travel(self, choice_key):
        """
        Perform a trip to the selected location key, apply attribute changes, and log the memory.
        """
        loc = self.locations.get(choice_key)
        if not loc:
            raise ValueError(f"Unknown travel location: {choice_key}")

        scenario = random.choice(loc['scenarios'])

        # Format the scenario text with the pet's name
        text = scenario['text'].format(name=self.pet.name)
        happ = scenario['happiness']
        energy = scenario['energy']

        # Update the pet's attributes, clamping between 0 and 100
        self.pet.happiness = max(0, min(100, self.pet.happiness + happ))
        self.pet.energy    = max(0, min(100, self.pet.energy + energy))

        # Create a memory entry
        record = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'location': loc['name'],
            'text': text,
            'happiness_change': happ,
            'energy_change': energy
        }
        self.memories.append(record)
        return record

    def get_memories(self):
        """
        Return a list of all travel memories for UI display.
        """
        return list(self.memories)
