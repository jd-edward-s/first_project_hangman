import random

incorrect_guesses = 0
game_on = True


def welcome():

    print("""
    Welcome to Hangman! A word will be chosen at random from a text file containing a series of random words. You will
    then be prompted to guess a letter. If the guess is correct you will reveal the position of the correctly guessed 
    letter within the secret word. However, if you guess incorrectly you will lose one of your 8 lives. The race is on
    to guess all the letters within the secret word before losing all your lives. Good Luck!
    """)


def choose_word():
    """
    Opens file 'word_list.txt' and returns a word that is chose at random from within the file.
    This chosen word is the word the player will try and guess during the game.
    """
    with open('word_list.txt') as file:
        word_list = file.readlines()
        return random.choice(word_list)


def display_star_word(word):
    """
    replaces each character in the chosen word with '*'
    :param word: output from choose_word()
    :return: Concealed word containing the same number of '*' as their are characters in the original word.
    """
    return (len(word)-1) * '*'


def player_guess():
    """
    Asks the player to enter their next guess.
    If multiple characters are entered it will accept the first character that was entered.
    """
    guess = str(input("Please enter your next guess: ")).lower()
    return guess[0]


def check_replace_update(word, hidden_word, guess):
    """
    Checks to see if the guessed letter is present in the original word and returns accordingly. The words are initially
    converted to a list for manipulation before being returned in string format.
    :param word: The selected word from choose_word()
    :param hidden_word: the output from display_star_word(word)
    :param guess: output from player_guess()
    :return: If the player_guess is correct it will update the hidden word to reveal the correctly guessed letter(s).
    If the player_guess is incorrect then the hidden_word remains unchanged and the INCORRECT GUESSES variable is
    updated. in addition the correctly guessed letters from the original word will be removed to enable progress
    tracking, this will not be displayed to the player.
    """
    global incorrect_guesses

    if guess in word:
        print("\nGood Guess\n")

        while guess in word:
            index = word.index(guess)
            word = list(word)
            word.remove(guess)
            word.insert(index, '*')
            word = "".join(word)

            hidden_word = list(hidden_word)
            hidden_word.pop(index)
            hidden_word.insert(index, guess)
            hidden_word = "".join(hidden_word)
        return word, hidden_word

    else:
        print(f"\nUnlucky, the letter '{guess}' is not in the secret word!\n")
        incorrect_guesses += 1
        return word, hidden_word


def check_win_or_lose(hidden_word, original_word):
    """
    Takes in the hidden word and assesses it for the number of '*' are present in the string. In theory if all the '*'
    have been replaced by the correct letters then the game has been won. Conversely if the number of incorrect guesses
    is equal to 8 then the game is lost. If neither case has been satisfied the game_on variable remains True and the
    Game control loop remains valid.
    :param hidden_word: This is the concealed representation of the chosen word. It consists of a series of '*' and
    when a letter is correctly guessed it is replaced by that correct letter.
    :return: global variable game_on
    """
    global incorrect_guesses
    global game_on

    check_list = [character for character in hidden_word if character == '*']

    if len(check_list) == 0 and incorrect_guesses < 8:
        print('Congratulations you win')
        game_on = False
        return game_on

    elif incorrect_guesses == 8:
        print(f'Unlucky, you are out of lives. The Secret Word was: {original_word}')
        print('You lose')
        game_on = False
        return game_on

    else:
        return game_on


def print_diagram():
    global incorrect_guesses

    build_blocks = {1: "|______", 2: "|      ", 3: "|/     ", 4: "_______", 5: "|/    |", 6: "|     O", 7: "|     +",
                    8: "|    //", 9: "       "}

    lives = {0: [9, 9, 9, 9, 9, 9, 9], 1: [9, 9, 9, 9, 9, 9, 1], 2: [9, 9, 9, 2, 2, 2, 2, 1], 3: [9, 3, 2, 2, 2, 2, 1],
             4: [9, 4, 3, 2, 2, 2, 2, 1], 5: [9, 4, 5, 2, 2, 2, 2, 1], 6: [9, 4, 5, 6, 2, 2, 2, 1],
             7: [9, 4, 5, 6, 7, 2, 2, 1], 8: [9, 4, 5, 6, 7, 8, 2, 1]}

    for x in lives[incorrect_guesses]:
        print(build_blocks[x])


if __name__ == "__main__":

    welcome()
    word = choose_word()
    original_word = word
    hidden_word = display_star_word(word)
    print(f"Secret Word: {hidden_word}")

    while game_on:
        guess = player_guess()
        word, hidden_word = check_replace_update(word, hidden_word, guess)
        print(f"Lives Remaining: {8 - incorrect_guesses}")
        print_diagram()
        print(f"Secret Word: {hidden_word}")
        check_win_or_lose(hidden_word, original_word)
