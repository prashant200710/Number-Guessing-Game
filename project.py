import random
import time
 
# name: (min, max, max attempts)
LEVELS = {
    "1": ("Easy", 1, 50, 15),
    "2": ("Medium", 1, 100, 10),
    "3": ("Hard", 1, 500, 8),
    "4": ("Extreme", 1, 1000, 7),
}
 
# keeps track of everything across games
stats = {"played": 0, "won": 0, "lost": 0, "best": 0, "guesses": 0}
 
 
def line(char="-"):
    print(char * 50)
 
 
def show_menu():
    print()
    line()
    print("  NUMBER GUESSING GAME")
    line()
    print("  1. Start game")
    print("  2. How to play")
    print("  3. Stats")
    print("  4. Quit")
    line()
 
 
def how_to_play():
    print("""
The computer picks a secret number and you try to find it.
After each guess you'll be told to go higher or lower.
Fewer guesses = higher score. Pick a harder level for a bigger challenge.
Every 3rd attempt you can ask for a hint.
""")
    input("Press Enter to go back...")
 
 
def pick_level():
    print("\nChoose a difficulty:")
    for key, (name, low, high, tries) in LEVELS.items():
        print(f"  {key}. {name} ({low}-{high}, {tries} tries)")
 
    while True:
        choice = input("> ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Just type 1, 2, 3 or 4.")
 
 
def ask_number(prompt):
    # keep asking until we get an actual number
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("That's not a number, try again.")
 
 
def get_score(high, attempts):
    # bigger range = more points, every extra guess costs 50
    return max(high * 10 - (attempts - 1) * 50, 0)
 
 
def give_hint(secret, guess, attempts):
    gap = abs(secret - guess)
 
    if gap <= 5:
        print("Hint: you're VERY close!")
    elif gap <= 15:
        print("Hint: you're close.")
    elif gap <= 30:
        print("Hint: kind of far.")
    else:
        print("Hint: way off.")
 
    print("Hint: it's", "even." if secret % 2 == 0 else "odd.")
 
    if attempts % 3 == 0:
        if secret % 5 == 0:
            print("Bonus hint: it's divisible by 5.")
        else:
            print("Bonus hint: it's NOT divisible by 5.")
 
 
def play_round():
    name, low, high, max_tries = pick_level()
    secret = random.randint(low, high)
    attempts = 0
    won = False
 
    print(f"\n{name} mode: guess a number from {low} to {high}.")
    print(f"You get {max_tries} tries. Good luck!\n")
 
    while attempts < max_tries:
        guess = ask_number(f"Guess #{attempts + 1}/{max_tries}: ")
 
        # out-of-range guesses don't cost an attempt
        if guess < low or guess > high:
            print(f"Stay between {low} and {high} please.")
            continue
 
        attempts += 1
 
        if guess == secret:
            won = True
            break
 
        print("Too high, go lower!" if guess > secret else "Too low, go higher!")
        print(f"({max_tries - attempts} tries left)\n")
 
        if attempts % 3 == 0 and attempts < max_tries:
            if input("Want a hint? (y/n): ").strip().lower() == "y":
                give_hint(secret, guess, attempts)
                print()
 
    stats["played"] += 1
    stats["guesses"] += attempts
 
    if won:
        score = get_score(high, attempts)
        stats["won"] += 1
        print(f"\nYou got it in {attempts} tries! Score: {score}")
        if score > stats["best"]:
            stats["best"] = score
            print("That's a new best score!")
    else:
        stats["lost"] += 1
        print(f"\nOut of tries. The number was {secret}.")
 
 
def show_stats():
    print()
    line()
    print("  YOUR STATS")
    line()
    print("Played :", stats["played"])
    print("Won    :", stats["won"])
    print("Lost   :", stats["lost"])
    print("Best   :", stats["best"])
 
    if stats["played"]:
        win_rate = stats["won"] / stats["played"] * 100
        avg = stats["guesses"] / stats["played"]
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Avg guesses: {avg:.1f}")
    else:
        print("Play a game first to see more!")
 
    print()
    input("Press Enter to go back...")
 
 
def play_again():
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("y or n, please.")
 
 
def countdown():
    print("\nStarting in...")
    for i in (3, 2, 1):
        print(i)
        time.sleep(0.5)
    print("Go!\n")
 
 
def main():
    while True:
        show_menu()
        choice = input("> ").strip()
 
        if choice == "1":
            countdown()
            play_round()
            while play_again():
                play_round()
        elif choice == "2":
            how_to_play()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            print("\nThanks for playing, see you!")
            break
        else:
            print("Pick a number from 1 to 4.")
 
 
if __name__ == "__main__":
    main()
