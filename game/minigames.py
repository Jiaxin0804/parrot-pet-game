import random
import time

class ReactionGame:
    """
    Reaction Speed Minigame: The system generates a random delay and then
    measures the reaction time of the player to press Enter.
    """
    def __init__(self, economy):
        """
        Initialize the reaction game with the economy system.
        """
        self.economy = economy

    def play(self):
        """
        How to play the reaction game:
            1, wait for a random delay of 1 to 3 seconds.
            2, The system will prompt the player to press Enter.
            3, The system calculates the player's reaction time and awards coins according to the speed.
        """
        delay = random.uniform(1, 3)
        print("Get ready...")
        time.sleep(delay)
        start = time.time()
        input("Press Enter to start!")
        rt = time.time() - start
        reward = max(1, int((1.5 - rt) * 10))
        self.economy.earn(reward)
        print(f"Reaction time: {rt:.3f}s. Coins earned: {reward}")

class MemoryGame:
    """
    Sequence Memory Minigame:
    The system displays a random 5-digit sequence, which is hidden after a few seconds,
    and the player needs to enter the correct sequence to get the coins.
    """
    def __init__(self, economy):
        """
        Initialize the memory game with the economy system.
        """
        self.economy = economy

    def play(self):
        """
        How to play the memory game:
            1, The system displays a sequence of 5 random numbers and waits 2 seconds before clearing the screen.
            2, The player needs to enter a space-separated sequence, and if it is correct, 20 coins will be awarded.
        """
        seq = [random.randint(0, 9) for _ in range(5)]
        print("Memorize the sequence:", seq)
        time.sleep(2)
        print("\n" * 50)
        guess = input("Enter the sequence, separated by spaces: ").split()
        success = guess == list(map(str, seq))
        reward = 20 if success else 0
        if success:
            self.economy.earn(reward)
        print(f"Memory {'successful' if success else 'failed'}. Coins earned: {reward}")

class MathQuizGame:
    """
    Arithmetic Challenge Minigame:
    The system asks a series of arithmetic questions, and correct answers are rewarded with coins.
    """
    def __init__(self, economy, questions=5):
        """
        Initialize the math quiz game.
        """
        self.economy = economy
        self.questions = questions
        self.ops = ['+', '-', '*']

    def play(self):
        """
        How to play the math quiz game:
            1, the system asks for a series of arithmetic expressions and the screen clears after 2 seconds.
            2, Players give their answers. Each correct answer awards 5 coins.
        """
        correct = 0
        for i in range(1, self.questions + 1):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(self.ops)
            expr = f"{a} {op} {b}"
            ans = eval(expr)
            try:
                user = int(input(f"Question {i}: {expr} = "))
            except ValueError:
                print("Invalid input, counted as incorrect.")
                continue
            if user == ans:
                print("√ Correct! +5 coins")
                self.economy.earn(5)
                correct += 1
            else:
                print(f"× Incorrect, the correct answer is {ans}")
        print(f"You answered {correct}/{self.questions} correctly, and earned {correct * 5} coins.")

class WordScrambleGame:
    """
    Word Scramble Minigame:
    The system gives a garbled word and the player finds the correct order of the letters.
    """
    def __init__(self, economy, words=None):
        """
        Initialize the word scramble game.
        """
        self.economy = economy
        self.words = words or ["parrot", "python", "gaming", "memory", "challenge"]

    def play(self):
        """
        How to play the word scramble game:
            1, The system randomly selects a word and spells its letters.
            2, The player enters the word in the correct order and receives 10 coins for correctly guessing the word.
        """
        word = random.choice(self.words)
        scrambled = ''.join(random.sample(word, len(word)))
        print(f"Unscramble the word: {scrambled}")
        guess = input("Your guess: ").strip().lower()
        if guess == word:
            print("√ Success! +10 coins")
            self.economy.earn(10)
        else:
            print(f"× Incorrect, the correct word was {word}")
