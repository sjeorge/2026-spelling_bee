# ==============================================================================
# spelling_bee.py
# ==============================================================================

'''

    Author: Sjors Verduin
    Date:   November 20th, 2026

    
    This script plays the New York Times game Spelling Bee.

    Given 1 center letter and 6 other letters, the player has to find all 
    American English words that:

     - are at least 4 letters long;
     - can be written using the 7 given letters;
     - contain the center letter at least once.

    Extra points are awarded for 'pangrams', words that contain all 7 letters at 
    least once.

    This script reads in the letters from a user input, and scans a list of 
    279,496 words taken from the Collins Scrabble Dictionary (attached as 
    'US_Scrabble_words.txt') for all words fulfilling these requirements. These 
    are then printed to the terminal and saved in a .txt file.

    NOTE: As a rule, the Collins Scrabble Dictionary is a lot more comprehensive
    than the word list used by the New York Times. Thus, the list found by this
    script likely contains words (in particular, curse words) not accepted by 
    the NYT.

'''

# ==============================================================================
# ==============================================================================

import datetime
from termcolor import cprint, colored as clr

# ==============================================================================
# ==============================================================================

def print_header(width):
    '''
        Print output header with title and today's date
        Input: 
            width   int     width of horizontal bars
        Output: 
            None
    '''

    date = datetime.datetime.today()

    cprint( '\n' + width*'=', "yellow")

    print(
        clr("\nSPELLING BEE \n", "yellow")
        + date.strftime("%A, %B ")
        + ordinal(date.strftime("%d"))
        + date.strftime(" %Y")
    )    

    cprint( '\n' + width*'=', "yellow" )

# ==============================================================================

def ordinal(n):
    '''
        Return the ordinal of the given number n, 
        e.g. '1st' for n=1 and '2nd' for n=2.
        Input:
            n           int
        Output:
            ordinal     str 
    '''

    n = int(n)

    tens = (n % 100) // 10
    ones = (n % 10)

    if ones == 1 and tens != 1: return str(n)+'st'
    if ones == 2 and tens != 1: return str(n)+'nd'
    if ones == 3 and tens != 1: return str(n)+'rd'
    else:                       return str(n)+'th'

# ==============================================================================

def user_input():
    '''
        Read in the center letter and other letters from user input.
        Input: 
            None
        Output:
            center_letter       str     
            other_letters       str  
            is_center_letter    dict    dict that has value True for the key 
                                        corresponding to the center letter, and
                                        False otherwise
            is_other_letter     dict    dict that has value True for the keys 
                                        corresponding to the other letters, and
                                        False otherwise
    '''

    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    center_letter = ''
    is_center_letter = dict(zip(alphabet, [False]*26))

    for letter in input("\nToday\'s center letter: "):

        if letter.isalpha(): 

            center_letter += letter.upper()
            is_center_letter[letter.upper()] = True

    other_letters = ''
    is_other_letter = dict(zip(alphabet, [False]*26))

    for letter in input("\nToday\'s other letters: "):

        if(
            letter.isalpha() 
            and not is_center_letter[letter.upper()]
        ):

            other_letters += letter.upper()
            is_other_letter[letter.upper()] = True

    return center_letter, is_center_letter, other_letters, is_other_letter

# ==============================================================================

def display_hexagon(center_letter, other_letters, width):
    '''
        Display a hexagon containing the letters in the style of the NYT
        Input:
            center_letter   str 
            other_letters   str
            width           int     width of horizontal bars
        Output:
            None
    '''

    cprint( '\n' + width*'-' + '\n', "yellow" )

    if len(center_letter) == 1 and len(other_letters) == 6:

        o = center_letter
        a,b,c,d,e,f = tuple(other_letters)

        inset = 4   # inset from left edge of terminal

        print(
            f"\n{(inset+2)*' '}{a}{3*' '}{b}\n\n"
            + f"{inset*' '}{c}{3*' '}{clr(o,"yellow")}{3*' '}{d}\n\n"
            + f"{(inset+2)*' '}{e}{3*' '}{f}\n"
        )

        cprint( '\n' + width*'-' + '\n', "yellow" )

# ==============================================================================

def find_words(is_center_letter, is_other_letter):
    '''
        Find all words that are allowed by the given letters.
        Input:
            is_center_letter    dict
            is_other_letter     dict
        Output:
            words               list    list of all allowed words in the Collins
                                        Scrabble Dictionary
    '''   

    words = []

    with open("US_Scrabble_words.txt", "r") as word_list:

        for line in word_list:

            word = line.rstrip()

            if is_word_allowed(word, is_center_letter, is_other_letter):

                words.append(word)

    return words

# ==============================================================================

def is_word_allowed(word, is_center_letter, is_other_letter):
    '''
        Check wether a given word 
         - is at least 4 letters long;
         - can be written using the given letters;
         - contains the center letter at least once.
        Input:
            word                str     word to check
            is_center_letter    dict   
            other_letters       dict
        Output:
            word_allowed        bool  
    '''

    if len(word) < 4: return False 

    contains_center_letter = False

    for letter in word: 

        if is_center_letter[letter]: 
            
            contains_center_letter = True
            continue

        if not is_other_letter[letter]: return False
        
    return contains_center_letter

# ==============================================================================

def print_words(words, is_center_letter, other_letters, width):
    '''
        Display all found words, with the center letter and pangrams highlighted 
        in yellow.
        Input:
            words               list    list of found words
            is_center_letter    dict    
            other_letters       str  
            width               int     width of horizontal bars   
        Output:
            None
    '''

    if len(words) == 0: print("No words found.")

    for word in words: 

        pangram = True

        for letter in other_letters:

            if letter not in word: 
                pangram = False
                break

        if pangram: 
            
            cprint(word, "yellow", attrs=["blink"])
            continue
        
        for letter in word:

            if is_center_letter[letter]: print(clr(letter, "yellow"), end='')
            else:                        print(letter, end='')

        print('')

    cprint( '\n' + width*'-' + '\n', "yellow" )

# ==============================================================================

def write_words(words, center_letter, other_letters, width):
    '''
        At the user's request, the found words are saved to a .txt file.
        Input:
            words           list
            center_letter   str
            other_letters   str
        Output:
            None
    '''

    write = ( input("Save solution? (y/n) ").lower() == 'y' )

    if write: 

        date = datetime.datetime.today().strftime("%Y-%m-%d")

        with open(f"spelling_bee_{date}.txt", "w") as file:
                    
            file.write(f"center letter: {center_letter}")
        
            file.write(f"\nother letters: {other_letters}")

            if len(words) > 0: 

                file.write(f"\n{len(words)} words found")
                
                for word in words: file.write(f"\n{word}")

            else: file.write(f"\nNo words found")

    cprint( '\n' + width*'=' + '\n', "yellow" )

# ==============================================================================
# ==============================================================================

def main():

    width= 50

    print_header(width)

    center_letter, is_center_letter, other_letters, is_other_letter = (
        user_input() )

    display_hexagon(center_letter, other_letters, width)

    words = find_words(is_center_letter, is_other_letter)

    print_words(words, is_center_letter, other_letters, width)

    write_words(words, center_letter, other_letters, width)

# ==============================================================================    

main()

# ==============================================================================
# ==============================================================================
# ==============================================================================