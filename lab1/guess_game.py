from rand_int import randint_safe


def start():
    difficulty = int(input("Pick a difficulty (1 Easy, 2 Medium, or 3 Hard): "))
    
    ans = randint_safe(1, 5 if difficulty == 1 else 10 if difficulty == 2 else 100)

    first_msg = "I’m thinking of a number, can you guess what it is? "
    low_msg = "Too Low! Guess again. "
    high_msg = "Too High! Guess again. "
    correct_msg = "Well done. The number is"
    
    msg = first_msg
    
    while (n := int(input(msg))) != ans:
        if n > ans:
            msg = high_msg
        else:
            msg = low_msg
    else:
        msg = correct_msg
        print(msg, ans)


if __name__ == "__main__":
    start()
