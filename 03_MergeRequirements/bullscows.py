import random
import sys
from urllib import request
import cowsay


COW_FILE = "cow.txt"
UTF8 = "utf8"


def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for g, s in zip(guess, secret):
        if g == s:
            bulls += 1
        elif g in secret:
            cows += 1
    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    k = 0
    while True:
        guess = ask("Введите слово: ", words)
        k += 1
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))
        if guess == secret:
            return k


if __name__ == "__main__":
    def ask(prompt: str, valid: list[str] = None) -> str:
        cow = random.choice(cowsay.list_cows())
        if valid is None:
            print(cowsay.cowsay(prompt, cow=cow))
            return input()
        else:
            while True:
                print(cowsay.cowsay(prompt, cow=cow))
                guess = input()
                if guess in valid:
                    return guess

    def inform(format_string: str, bulls: int, cows: int) -> None:
        cow = random.choice(cowsay.list_cows())
        print(cowsay.cowsay(format_string.format(bulls, cows), cow=cow))

    secret_len = int(sys.argv[2]) if len(sys.argv) == 3 else 5
    dict_path = sys.argv[1]

    try:
        words = open(dict_path).readlines()
        words = [word.strip() for word in words if word.strip()]
    except Exception as e:
        words = request.urlopen(dict_path).readlines()
        words = [word.decode(UTF8).strip() for word in words if word.decode(UTF8).strip()]

    words = [word for word in words if len(word) == secret_len]

    print(gameplay(ask, inform, words))
