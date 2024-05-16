import time

class CipherEngine:
    ZERO_BIT = '0'
    ONE_BIT = '1'
    BITS = [ZERO_BIT, ONE_BIT]

    def __init__(self, bit_length: int):
        self.bit_length = bit_length
        self.secret_key = self._generate_random_key()

    def _generate_random_key(self) -> str:
        return ''.join(self._get_pseudo_random_bit() for _ in range(self.bit_length))

    def _get_pseudo_random_bit(self) -> str:
        return str(int(time.time() * 1000000) % 2)

    def evaluate_attempt(self, attempt: str) -> int:
        return sum(attempt[i] == self.secret_key[i] for i in range(self.bit_length))


class CipherGame:
    def __init__(self, bit_length=4, max_attempts=10, auto_play=False, show_key=False):
        self.engine = CipherEngine(bit_length)
        self.max_attempts = max_attempts
        self.auto_play = auto_play
        self.show_key = show_key
        self.attempts = []

    def play(self):
        print("Welcome to Cipher Game")
        print(f"Guess the secret key in {self.max_attempts} tries or fewer")

        if self.show_key:
            print(f"Secret key: {self.engine.secret_key}")

        for attempt in range(self.max_attempts):
            guess = self._get_auto_guess() if self.auto_play else self._get_user_guess()
            feedback = self.engine.evaluate_attempt(guess)
            self.attempts.append((guess, feedback))

            print("////////////////////////////////////////////////////////////////")
            print("Your Past Attempts and Feedbacks", self.attempts)
            print("////////////////////////////////////////////////////////////////")

            if feedback == len(self.engine.secret_key):
                print("Congratulations, you've cracked the code!")
                return

        print("Sorry, you have lost.")

    def _get_user_guess(self):
        guess = input(f"Enter your guess ({len(self.engine.secret_key)} digits): ")
        while len(guess) != len(self.engine.secret_key) or any(c not in CipherEngine.BITS for c in guess):
            guess = input(f"Invalid input! Please enter your guess ({len(self.engine.secret_key)} digits): ")
        return guess

    def _get_auto_guess(self) -> str:
        return ''.join(self.engine._get_pseudo_random_bit() for _ in range(len(self.engine.secret_key)))


if __name__ == "__main__":
    game = CipherGame(auto_play=True, show_key=True)
    game.play()
