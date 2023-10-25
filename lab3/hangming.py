import os
import random
import sys


def find_word() -> str:
    words = []
    with open("./words", "r") as f:
        for word in f:
            words.append(word.strip())
    return random.choice(words)


def draw_hangman(lives: int):
    os.system("clear")
    if lives == 6:
        print("=========\n ||     |\n ||\n ||\n ||\n ||\n/  \\")
    elif lives == 5:
        print("=========\n ||     |\n ||     O\n ||\n ||\n ||\n/  \\")
    elif lives == 4:
        print("=========\n ||     |\n ||     O\n ||     |\n ||\n ||\n/  \\")
    elif lives == 3:
        print("=========\n ||     |\n ||    \O\n ||     |\n ||\n ||\n/  \\")
    elif lives == 2:
        print("=========\n ||     |\n ||    \O/\n ||     |\n ||\n ||\n/  \\")
    elif lives == 1:
        print("=========\n ||     |\n ||    \O/\n ||     |\n ||    /\n ||\n/  \\")
    elif lives == 0:
        print(
            "=========\n ||     |\n ||     O \n ||    /|\\\n ||    / \\\n ||\n/  \\"
        )


def win_game():
    print("you win!")


class Hangman:
    ans_dict = {}

    def __init__(self):
        self.hidden_word = find_word()
        self.__make_hidden_word_struct()
        self.blank_string = "-" * len(self.hidden_word)
        self.lives = 6
        print(self.hidden_word)

    def process_guess(self, guess: str):
        if guess not in self.ans_dict:
            if guess not in self.hidden_word:
                self.lives -= 1
                draw_hangman(self.lives)
                if self.lives == 0:
                    print("You Die!")
                    print(f"Ans is: {self.hidden_word}")
                    sys.exit(0)
                return
            print("You have guessed this word !")
            return

        del self.ans_dict[guess]

    def __make_hidden_word_struct(self):
        for i, c in enumerate(self.hidden_word):
            stored = self.ans_dict.get(c, None)
            self.ans_dict[c] = [i, *stored] if stored is not None else [i]

    def __draw_guess_status(self):
        status = list(self.hidden_word)
        for v in self.ans_dict.values():
            for i in v:
                status[i] = "-"
        print("".join(status))

    def play(self):
        while True:
            try:
                guess = input("Guess a char: ")
                self.process_guess(guess)
                self.__draw_guess_status()
                if len(self.ans_dict) == 0:
                    win_game()
                    break
            except KeyboardInterrupt:
                print("\nGame interrupted")
                sys.exit(0)


if __name__ == "__main__":
    game = Hangman()
    game.play()
