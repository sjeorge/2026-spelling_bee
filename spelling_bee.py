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

    the center letter at least once. Extra points are awarded for 'pangrams',
    words that contain all 7 letters at least once.

    This script reads in the letters from a user input, and scans the Collins
    Scrabble Dictionary (attached as 'US_Scrabble_words.txt') for all words 
    fulfilling these requirements. These are then printed to the terminal.

    NOTE: there is no complete overlap between the Collins Scrabble Dictionary
    and the word list used by the New York Times. Thus, the list found by this
    script may be incomplete, or contain words (in particular, curse words) not 
    accepted by the NYT.

'''

# ==============================================================================
# ==============================================================================

import datetime
from termcolor import colored as clr 

# ==============================================================================

def print_header(fill):
    '''
        Print output header with title and today's date
        Input: 
            fill    int     width of horizontal bars
        Output: 
            None
    '''

    date = datetime.datetime.today()

    print( "\n" + fill*'=' )

    print(
        clr("\nSPELLING BEE\n", 'yellow')
        + date.strftime("%A, %B ")
        + ordinal(date.strftime("%d"))
        + date.strftime(" %Y")
    )    

    print( "\n" + fill*'=' )

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
            center_letter   str 
            other_letter    str     
    '''

    center_letter = ''.join(
        letter.upper()
        for letter in input("\nToday\'s center letter: ")
        if letter.isalpha()
    )

    other_letters = ''.join(
        letter.upper()
        for letter in input("\nToday\'s other letters: ")
        if letter.isalpha() and letter not in center_letter
    )

    return center_letter, other_letters

# ==============================================================================

def display_hexagon(center_letter, other_letters, fill):
    '''
        Display a hexagon containing the letters in the style of the NYT
        Input:
            center_letter   str 
            other_letters   str
            fill            int     width of horizontal bars
        Output:
            None
    '''

    print( "\n" + fill*'-' )

    if len(center_letter) == 1 and len(other_letters) == 6:

        o = center_letter
        a,b,c,d,e,f = tuple(other_letters)

        n = 4   # inset from left edge of terminal

        print(
            f"\n\n{(n+2)*' '}{a}{3*' '}{b}\n\n"
            + f"{n*' '}{c}{3*' '}{clr(o,'yellow')}{3*' '}{d}\n\n"
            + f"{(n+2)*' '}{e}{3*' '}{f}\n"
        )

# ==============================================================================

def find_words(center_letter, letters):
    '''
        Find all words that are allowed by the given letters.
        Input:
            center_letter   str     center letter that allowed words must 
                                    contain
            other_letters   str     other letters that words must be written 
                                    with
        Output:
            words           list    list of all allowed words in the Collins
                                    Scrabble Dictionary
    '''   

    words = []

    with open("US_Scrabble_words.txt", "r") as word_list:

        for line in word_list:

            word = line.rstrip()

            if word_allowed(word, center_letter, letters):

                words.append(word)

    return words

# ==============================================================================

def word_allowed(word, center_letter, other_letters):
    '''
        Check wether a given word 
         - is at least 4 letters long;
         - can be written using the given letters;
         - contains the center letter at least once.
        Input:
            word            str     word to check
            center_letter   str     center letter that word must contain
            other_letters   str     other letters that word must be written with
        Output:
            word_allowed    bool    wether the word is allowed
    '''

    if len(word) < 4: return False 

    contains_center_letter = False

    for letter in word: 

        if letter in center_letter: 
            
            contains_center_letter = True
            continue

        if not letter in other_letters: return False
        
    return contains_center_letter

# ==============================================================================

def print_words(words, center_letter, other_letters, fill):
    '''
        Display all found words, with the center letter and pangrams highlighted 
        in yellow.
        Input:
            words           list    list of found words
            center_letter   str     
            other_letters   str  
            fill            int     width of horizontal bars   
        Output:
            None
    '''

    print( "\n" + fill*'-' + '\n' )

    for word in words: 

        pangram = True

        for letter in other_letters:

            if (
                letter not in center_letter
                or letter not in other_letters
            ): 
                pangram = False
                break

        if pangram: 
            
            print(clr(word, 'yellow'))
            continue
        
        for letter in word:

            if letter in center_letter: print(clr(letter, 'yellow'), end='')
            else:                       print(letter, end='')

        print('')

    print( "\n" + fill*'=' + '\n' )

# ==============================================================================
# ==============================================================================

def main():

    fill = 50

    print_header(fill)

    center_letter, other_letters = user_input()

    display_hexagon(center_letter, other_letters, fill)

    words = find_words(center_letter, other_letters)

    print_words(words, center_letter, other_letters, fill)

# ==============================================================================    

main()

# ==============================================================================
# ==============================================================================
# ==============================================================================