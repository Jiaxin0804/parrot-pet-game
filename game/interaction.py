class InteractionSystem:
    """
    Interaction System: determines responses based on pet status and interaction part, and updates happiness and energy.
    Acceptance priority: head > wing > belly > paw.
    """
    def __init__(self, pet, economy=None):
        self.pet = pet
        self.economy = economy
        # Set happiness thresholds for each part, Higher threshold means more likely to be rejected by parrots
        self.thresholds = {
            'head': 0,
            'wing': 25,
            'belly': 50,
            'paw': 75
        }
        # Define the effects and responses of different parts of the interaction on attribute values
        self.actions = {
            'head': {
                'label': 'touch head',
                'happiness': 5,
                'energy': -2,
                'text': 'It closes its eyes, enjoying being petted on the head. Happiness +5, Energy -2.'
            },
            'wing': {
                'label': 'touch wing',
                'happiness': 4,
                'energy': -3,
                'text': 'It flutters its wings gratefully. Happiness +4, Energy -3.'
            },
            'belly': {
                'label': 'touch belly',
                'happiness': 3,
                'energy': -4,
                'text': 'It emits a contented purr. Happiness +3, Energy -4.'
            },
            'paw': {
                'label': 'touch paw',
                'happiness': 2,
                'energy': -5,
                'text': 'It lifts its little paw and rubs your hand. Happiness +2, Energy -5.'
            }
        }

    def action(self, part):
        """
        Perform an interaction. part must be one of 'head', 'wing', 'belly', 'paw'.
        """
        info = self.actions.get(part)
        if not info:
            print(f"Unknown interaction part: {part}. Options: head, wing, belly, paw.")
            return

        # Parrot refuses to interact due to hunger
        if self.pet.hunger >= 80:
            print(f"You try to {info['label']}, but it is too hungry and angrily bites your hand!")
            print(f"Current Hunger: {self.pet.hunger:.1f}, Energy: {self.pet.energy:.1f}")
            return

        # Parrot refuses to interact due to low energy
        if self.pet.energy <= 20:
            print(f"You want to {info['label']}, but it is too tired and just wants to rest quietly.")
            print(f"Current Hunger: {self.pet.hunger:.1f}, Energy: {self.pet.energy:.1f}")
            return

        # Parrot accept or reject based on happiness threshold
        current_hap = self.pet.happiness
        threshold = self.thresholds[part]
        if current_hap >= threshold:
            # Accept interaction and update attributes
            self.pet.happiness = min(100, current_hap + info['happiness'])
            self.pet.energy = max(0, self.pet.energy + info['energy'])
            print(info['text'])
        else:
            # Reject interaction
            print(f"You attempt to {info['label']}, but it shakes its head, not wanting to be touched.")
