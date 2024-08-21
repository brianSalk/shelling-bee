import shutil
import subprocess
import platform
import random
import time

def clear_term():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)





def print_colored(text, bg_col='black', txt_col='white', centered=False, loffset = 0 ,end='\n'):
    def get_spaces(text):
        term_width = shutil.get_terminal_size().columns
        return (' ' * (term_width//2 - (len(text)//2) - loffset))
    spaces = ''
    if centered:
        spaces = get_spaces(text)
    
    bg_ansi = '40'
    if bg_col == 'black':
        bg_ansi = '40'
    elif bg_col == 'red':
        bg_ansi = '41'
    elif bg_col == 'green':
        bg_ansi = '42'
    elif bg_col == 'yellow':
        bg_ansi = '43'
    elif bg_col == 'white':
        bg_ansi = '47'
    txt_ansi = '37'
    if txt_col == 'white':
        txt_ansi = '37'
    elif txt_col == 'red':
        txt_ansi = '31'
    elif txt_col == 'green':
        txt_ansi = '32'
    elif txt_col == 'yellow':
        txt_ansi = '33'
    elif txt_col == 'blue':
        txt_ansi = '34'
    elif txt_col == 'black':
        txt_ansi = '30'
    ansi = f'\033[{txt_ansi};{bg_ansi}m'
    print(spaces + ansi + text + '\033[0m',end=end)
def erase_prompt():
    # scroll prompt out of view
    for _ in range(100):
        print()
    # place cursor at top left of current window
    print("\033[H", end="")


def display_intro():
    erase_prompt()
    print_colored('welcome to', bg_col='yellow', centered=True)
    print_colored('SHELLING BEE', bg_col='yellow',txt_col='black', centered=True)
    print_colored('... Spelling Bee on your Shell!', bg_col='yellow', centered=True)
    print()
    print_colored('press any key to begin...', txt_col='green',centered=True)


def create_hive():
    def __create_hive():
        hive_letters = set()
        all_letters = 'ABCDEFGHIJKLMNOPQRTUVWXYZ' # exclude S
        vowels = 'AEIOU'
        hive_letters.add(random.choice(vowels))
        while len(hive_letters) < 7:
            hive_letters.add(random.choice(all_letters))
        hive_letters = list(hive_letters)
        middle_letter = random.choice(hive_letters)
        return hive_letters, middle_letter
    words = []
    vocab_words = []
    with open('word_list.txt') as file:
        for word in file.readlines():
            vocab_words.append(word[:-1])
    is_valid = False
    while not is_valid:
        hive_letters, middle_letter = __create_hive()
        # make sure at least 1 panagram exists 
        words = []
        has_letter = {letter:False for letter in hive_letters}
        has_pangram = False
        pangrams = []
        for word in vocab_words:
            if all(letter.lower() in word for letter in hive_letters):
                pangrams.append(word)
            for letter in has_letter.keys():
                if letter.lower() in word:
                    has_letter[letter] = True
            if middle_letter.lower() in word and all(letter.upper() in hive_letters for letter in word):
                words.append(word)

        # at least 20 words total, one pangram and all letters used
        if len(set(has_letter.values())) == 1 and len(words) > 20 and len(pangrams) > 0:
            is_valid = True
    return hive_letters, middle_letter, pangrams, words  


def print_hive(hive_letters, middle_letter):
    print_colored('   ' + hive_letters[0] + '   ', bg_col='white', txt_col='black',centered=True)
    print_colored(' ' + hive_letters[1] + '   ' + hive_letters[2] + ' ', bg_col='white', txt_col='black',centered=True, loffset=0)
    print_colored('   ', bg_col='white', txt_col='black',centered=True, loffset=2, end='')
    print_colored(middle_letter, bg_col='yellow', txt_col='black', loffset=1, end='')
    print_colored('   ', bg_col='white', txt_col='black')
    print_colored(' ' + hive_letters[3] + '   ' + hive_letters[4] + ' ', bg_col='white', txt_col='black',centered=True, loffset=0)
    print_colored('   ' + hive_letters[5] + '   ', bg_col='white', txt_col='black',centered=True)

if __name__ == '__main__':
    display_intro()
    input()
    clear_term()
    hive_letters, middle_letter, pangrams, answer_words = create_hive()
    guessed_words = []
    hive_letters.remove(middle_letter)
    game_over = False
    while not game_over:
        print_hive(hive_letters, middle_letter)
        for guessed_word in guessed_words:
            if guessed_word in pangrams:
                print(f'\033[1m{guessed_word}\033[0m')
            else:
                print(guessed_word)
        next_guess = input('next guess: ').lower()
        if next_guess in answer_words:
            print('good job!')
            guessed_words.append(next_guess)
            time.sleep(1)
        else:
            print('try again')
            time.sleep(1)
        clear_term()


