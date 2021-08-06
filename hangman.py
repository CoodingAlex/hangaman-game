import os
import random
from termcolor import colored

HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

score = 0
fails = 0
MAX_FAILS = 6


def get_random_word_from_file():
    words = []
    with open("./archivos/words.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            # len(line) - 1 for delete the last char (a \n)
            if line[len(line) - 1] == '\n':
                words.append(line[:len(line) - 1])
    return words[random.randrange(0, len(words))]


def check_if_user_won(word_dict, word):
    hasWon = False
    for key, value in word_dict.items():
        if value == False:
            hasWon = False
            return hasWon
        hasWon = True
    if hasWon:
        render("Congrats, you won the game with the word " +
               colored(word, "yellow"))
        modify_score(100)
    return hasWon


def game():
    word = get_random_word_from_file()
    word_dict = create_word(word)
    err = ""
    while True:
        render(parse_word_dict_for_render(word_dict, word), err=err)
        err = ""
        user_letter = input("Ingrese un caracter: ")
        if len(user_letter) != 1:
            err = "Solo puedes ingresar un caracter"
            continue
        userLose = attemp(word_dict, word, user_letter)
        hasWon = check_if_user_won(word_dict, word)
        if userLose:
            render(colored("You Lose :(", "red"))
            input("Press Enter for play Again")
            return
        if hasWon:
            return


def modify_score(newScore):
    global score
    score += newScore


def get_score():
    return score


def create_word(word):
    word_dict = {}
    for letter in word:
        word_dict[letter] = False
    return word_dict


def parse_word_dict_for_render(word_dict, word):
    render_word = ""
    for l in word:
        if word_dict.get(l, "_") == l:
            render_word += l
        else:
            render_word += "_"
    return render_word


def attemp(word_dict, word, letter):
    exist = word_dict.get(letter, "_")
    if exist != "_":
        # Just execute modify_score once per letter
        if word_dict[letter] != letter:
            modify_score(10)
        word_dict[letter] = letter
        return False
    else:
        global fails
        if fails == 6:
            return True
        fails += 1
        return False


def render(string, err="", printBanner=True):
    os.system("clear")
    if err:
        print(colored(err, "red"))
    if printBanner:
        print(f"""=============================
The hangman Game!
Score {colored(score, "blue")}
Left Tries: {colored(MAX_FAILS - fails, "red")}
=============================
    """)
        print(HANGMANPICS[fails])
    print(string)


def load_score_from_file():
    with open("./archivos/score.txt", "r") as f:
        global score
        score = f.readline()
        score = int(score)
        f.close()


def exit_program():
    with open("./archivos/score.txt", "w") as f:
        f.write(str(score))
        f.close()
    exit(1)


def main():
    load_score_from_file()
    while True:
        render("Welcome to the hangman game!!", printBanner=False)
        option = input("""
[1]Press 1 for play
[2]Press 2 for exit
[3]Press 3 for watch your score
""")
        if option == "1":
            global fails
            fails = 0
            game()
        elif option == "2":
            render(f"Your Final Score is " +
                   colored(score, "red"), printBanner=False)
            exit_program()
        elif option == "3":
            render("Score: " + colored(score, "red"), printBanner=False)
            input("Press enter to continue")


if __name__ == "__main__":
    main()
