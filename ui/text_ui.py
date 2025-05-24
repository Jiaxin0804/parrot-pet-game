from game.pet import Pet
from game.economy import Economy
from game.events import RandomEventSystem
from game.travel import TravelSystem
from game.interaction import InteractionSystem
from game.veterinary import Veterinary
from game.timer import GameTimer
from game.minigames import ReactionGame, MemoryGame, MathQuizGame, WordScrambleGame
from utils.helpers import print_banner

class TextUI:
    """
    Pet Game User Interface:
    Provides functions such as food inventory, feeding, interaction, travel and memory albums,
    event logs, minigames, status viewing and veterinary visits.
    """
    PROMPT = "[Command (type help to view commands)]> "

    def __init__(self):
        print_banner()
        # Enter the pet name and game difficulty, the default difficulty is normal
        name = input("Pet name (default Polly): ").strip() or "Polly"
        diff_input = input("Difficulty (easy/normal/hard) [normal]: ").strip().lower()
        if diff_input not in ('easy', 'normal', 'hard'):
            print(f"Unknown difficulty '{diff_input}', defaulting to 'normal'.")
            diff = 'normal'
        else:
            diff = diff_input
        # Mapping difficulty to update interval
        interval_map = {'easy': 12.0, 'normal': 8.0, 'hard': 6.0}
        interval = interval_map.get(diff, 8.0)
        print(f"Difficulty set to {diff}, update interval {interval}s.")

        self.pet = Pet(name)
        self.economy = Economy()
        self.events = RandomEventSystem(self.pet, self.economy)
        self.travel = TravelSystem(self.pet)
        self.interact = InteractionSystem(self.pet, self.economy)
        self.vet = Veterinary(self.pet, self.economy)
        self.minigames = {
            '1': ('Reaction Speed', ReactionGame(self.economy)),
            '2': ('Sequence Memory', MemoryGame(self.economy)),
            '3': ('Math Quiz', MathQuizGame(self.economy)),
            '4': ('Word Scramble', WordScrambleGame(self.economy)),
        }
        self.timer = GameTimer(interval, self._tick)
        self.running = False
        self.commands = {
            'feed':     self._cmd_feed,
            'buyfeed':  self._cmd_buyfeed,
            'play':     self._cmd_play,
            'interact': self._cmd_interact,
            'travel':   self._cmd_travel,
            'memories': self._cmd_memories,
            'events':   self._cmd_events,
            'vet':      self._cmd_vet,
            'money':    self._cmd_earn,
            'minigames': self._cmd_earn,
            'status':   self._cmd_status,
            'help':     self._cmd_help,
            'exit':     self._cmd_exit,
        }

    def _tick(self, delta):
        """
        Regular update callbacks: update pet status, trigger events, warnings, and handle game over.
        """
        self.pet.update(delta)
        self.events.trigger()
        if self.pet.hunger >= 80:
            print("[Warning] Hunger is too high! Remember to feed your pet.")
        if self.pet.happiness <= 20:
            print("[Warning] Happiness is too low! Consider interacting with your pet.")
        if not self.pet.is_alive():
            self.timer.stop()
            self.running = False
            reason = getattr(self.pet, 'failure_reason', None)
            if reason == 'protection':
                print("We're sorry: Your pet has been taken by animal protection due to prolonged neglect.")
            elif reason == 'death':
                print("Regrettably: Your pet has passed away due to long-term health neglect.")
            elif reason == 'neglect':
                print("Sadly: Your pet has died due to extreme hunger or energy depletion.")
            print("=== Final Pet Status ===")
            self._display_status()

    def _display_status(self):
        """
        Display the current status of the pet and economy.
        """
        print(f"{self.pet.name} | Hunger={self.pet.hunger:.1f} | Happiness={self.pet.happiness:.1f} | "
              f"Energy={self.pet.energy:.1f} | Health={self.pet.health:.1f} | "
              f"Coins={self.economy.coins} | Feed={self.economy.feed_stock}")

    def _cmd_feed(self, *args):
        """
        Feed the pet: consume one feed unit and reduce hunger.
        """
        if self.economy.feed_stock <= 0:
            print("No feed left! Use buyfeed to purchase feed.")
            return
        self.economy.feed_stock -= 1
        self.pet.happiness = min(100, self.pet.happiness + 10)
        self.pet.hunger = max(0, self.pet.hunger - 10)
        print(f"Feeding successful: Hunger -10, Happiness +10, Remaining feed {self.economy.feed_stock}")

    def _cmd_buyfeed(self, *args):
        """
        Buy Feed: Spend coins to increase your feed inventory.
        """
        amount = 1
        if args and args[0].isdigit():
            amount = int(args[0])
        cost = amount * self.economy.buy_price
        if self.economy.buy_feed(amount):
            print(f"Purchase successful: Bought {amount} feed unit(s), -{cost} coins, Current feed {self.economy.feed_stock}")
        else:
            print(f"Not enough coins to purchase {amount} feed unit(s) (requires {cost} coins)." )

    def _cmd_play(self, *args):
        """
        Play with the pet: increases happiness at the cost of energy.
        """
        dur = 1
        if args and args[0].isdigit():
            dur = int(args[0])
        gain, cost = self.pet.play(dur)
        print(f"Played for {dur} hour(s): Happiness +{gain}, Energy -{cost}")

    def _cmd_interact(self, *args):
        """
        Interact with the pet: head / wing / belly / paw.
        """
        if not args:
            print("Usage: interact <head|wing|belly|paw>")
            return
        part = args[0]
        try:
            self.interact.action(part)
        except ValueError as e:
            print(str(e))

    def _cmd_travel(self, *args):
        """
        Travel with the pet to a chosen location.
        """
        if not args:
            print("Available travel locations:")
            for key, loc in self.travel.locations.items():
                print(f"  {key}: {loc['name']}")
            print("Example: travel beach")
            return
        choice = args[0]
        try:
            record = self.travel.travel(choice)
            print(f"[Travel] {record['time']} - {record['location']}: {record['text']}")
            print(f"Happiness change: {record['happiness_change']}, Energy change: {record['energy_change']}")
        except ValueError as e:
            print(str(e))

    def _cmd_memories(self, *args):
        """
        View the travel memories album.
        """
        mems = self.travel.get_memories()
        if not mems:
            print("No travel memories available.")
            return
        print("=== Travel Memories ===")
        for m in mems:
            print(f"{m['time']} | {m['location']} | {m['text']} | "
                  f"Happiness {m['happiness_change']} | Energy {m['energy_change']} | "
                  f"Health {m.get('health_change', 0)}")

    def _cmd_events(self, *args):
        """
        View the log of triggered random events.
        """
        logs = self.events.get_log()
        if not logs:
            print("No event records.")
            return
        print("=== Event Log ===")
        for e in logs:
            print(f"{e['time']} | {e['key']} | {e['text']} | "
                  f"Happiness {e.get('happiness_change', 0)} | "
                  f"Energy {e.get('energy_change', 0)} | "
                  f"Health {e.get('health_change', 0)}")

    def _cmd_vet(self, *args):
        """
        Take the pet to the veterinarian (restores health and energy to 100 at cost of coins).
        """
        self.vet.visit()

    def _cmd_earn(self, *args):
        """
        Choose a mini-game to earn coins.
        """
        print("Please select a mini-game to earn coins:")
        for key, (name, _) in self.minigames.items():
            print(f"  {key}. {name}")
        choice = input("Enter number to choose: ").strip()
        if choice in self.minigames:
            _, game = self.minigames[choice]
            game.play()
        else:
            print("Invalid choice. Type help to view commands.")

    def _cmd_status(self, *args):
        """
        View current status of pet and economy.
        """
        self._display_status()

    def _cmd_help(self, *args):
        """
        View available commands and their descriptions.
        """
        print("Available commands:")
        for cmd, fn in self.commands.items():
            print(f"  {cmd}\t{fn.__doc__}")

    def _cmd_exit(self, *args):
        """
        Exit the game.
        """
        print("Thank you for playing!")
        self.running = False

    def run(self):
        """
        Start the game UI.
        """
        print(f"Welcome, pet owner of {self.pet.name}! Let's start the game ~")
        self._cmd_help()
        self.timer.start()
        self.running = True
        while self.running and self.pet.is_alive():
            try:
                raw = input(self.PROMPT).strip().split()
            except (KeyboardInterrupt, EOFError):
                print("Exiting game.")
                break
            if not raw:
                continue
            cmd, *args = raw
            fn = self.commands.get(cmd)
            if fn:
                fn(*args)
            else:
                print(f"Unknown command: {cmd}")
        print("Game over. Goodbye!")
