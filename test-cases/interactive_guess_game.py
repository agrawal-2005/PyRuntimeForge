import random


def guess_the_number():
    secret_number = random.randint(1, 20)
    attempts = 0
    max_attempts = 6

    print("I am thinking of a number between 1 and 20.")
    print(f"You have {max_attempts} attempts to guess it!")

    while attempts < max_attempts:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1

            if guess < secret_number:
                print("Too low!")
            elif guess > secret_number:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                return
        except ValueError:
            print("Please enter a valid whole number.")

    print(f"Game Over! The number was {secret_number}.")


if __name__ == "__main__":
    guess_the_number()
