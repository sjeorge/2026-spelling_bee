# ==============================================================================
# letter_boxed.py
# ==============================================================================

'''

    Author: Sjors Verduin
    Date:   November 22nd, 2026

    
    This script plays the New York Times game Letter Boxed.

    Given 12 letters divided over 4 sides of a square, as well as a target 
    number of words, the goal is to find a sequence of words such that:

     - the sequence contains at most the target number of words;
     - each word contains only the given letters;
     - within each word, no two adjacent letters are on the same side of the
       square;
     - each but the first word starts with the last letter of the previous word;
     - together, the words contain all the given letters.

    This script reads in the grouped letters and the target number from a user 
    input, and from a list of 279,496 words taken from the Collins Scrabble 
    Dictionary (attached as 'US_Scrabble_words.txt') constructs all sequences of
    words fulfilling these requirements. The sequences with the minimum possible
    number of words are then printed to the terminal and saved in a .txt file.

    NOTE: As a rule, the Collins Scrabble Dictionary is a lot more comprehensive
    than the word list used by the New York Times. Thus, the solutions found by 
    this script likely contain words (in particular, curse words) not accepted 
    by the NYT.

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

    cprint( '\n' + width*'=' + '\n', "red", attrs=["bold"])

    print(
        clr("LETTER BOXED\n", "red", attrs=["bold"])
        + date.strftime("%A, %B ")
        + ordinal(date.strftime("%d"))
        + date.strftime(" %Y")
    )    

    cprint( '\n' + width*'=' + '\n', "red", attrs=["bold"] )

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

def user_input(width):
    '''
        Read in the letter groups and the target number of words from user input.
        Input: 
            width               int     width of horizontal
        Output:
            letters             str     full set of letters 
            groups              list    grouped letters
            group_of_letter     dict    group_of_letter[letter] = i if letter is
                                        in group i, -1 if letter is not in group 
            solve_in            int     maximum number of words in solution        
    '''

    groups = input("Today\'s letters: ").split()

    groups = [
        ''.join(
            letter.upper()
            for letter in group
            if letter.isalpha()
        ) 
        for group in groups
    ]

    letters = list(''.join(groups))

    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    group_of_letter = dict(zip(alphabet,[-1]*len(alphabet)))

    for i in range(len(groups)):

        for letter in groups[i]:

            group_of_letter[letter] = i

    solve_in = input("\nSolve in _ words: ")

    solve_in = int(''.join(
        number 
        for number in solve_in
        if number.isdigit()
    ))

    cprint( '\n' + width*'-' + '\n', "red", attrs=["bold"] )

    return letters, groups, group_of_letter, solve_in

# ==============================================================================

def display_square(groups, width):
    '''
        Display a square containing the letters in the style of the NYT
        Input:
            groups          list    
            width           int     width of horizontal bars
        Output:
            None
    '''

    if (
        len(groups) != 4
        or len(groups[0]) != 3
        or len(groups[1]) != 3
        or len(groups[2]) != 3
        or len(groups[3]) != 3
    ): 

        return

    A,B,C = tuple(groups[0])
    D,E,F = tuple(groups[1])
    G,H,I = tuple(groups[2])
    J,K,L = tuple(groups[3])

    inset = 4

    print(
        clr(f"\n{inset*' '}  {A}  {B}  {C}", "red", attrs=["bold"]),
        clr(f"\n{inset*' '}{D}{9*' '}{G}", "red", attrs=["bold"]),
        clr(f"\n{inset*' '}{E}{9*' '}{H}", "red", attrs=["bold"]),
        clr(f"\n{inset*' '}{F}{9*' '}{I}", "red", attrs=["bold"]),
        clr(f"\n{inset*' '}  {J}  {K}  {L}", "red", attrs=["bold"])
    )

    cprint( 2*'\n' + width*'-' + '\n', "red", attrs=["bold"] )

# ==============================================================================

def find_words(letters, group_of_letter):
    '''
        Scan the Collins Scrabble Dictionary for all words that can be made
        using the grouped letters
        input:
            letters                 str
            group_of_letter         dict    
        output:
            words                   list    the list of valid words
            words_by_first_letter   dict    valid words listed by first letter
    '''

    words = []
    words_by_first_letter = dict(zip(
        letters, 
        [ [] for i in range(len(letters)) ]
    ))
    
    with open("US_Scrabble_words.txt", "r") as word_list:

        for line in word_list:

            word = line.rstrip()

            if is_word_allowed(word, group_of_letter):

                words.append(word)
                words_by_first_letter[word[0]].append(word)

    return words, words_by_first_letter

# ==============================================================================

def is_word_allowed(word, group_of_letter):
    '''
        Checks if word is a valid sequence of the letters
        input:
            word                str
            group_of_letter     dict
        output:
            is_word_allowed     bool    
    '''

    n = len(word)

    if n < 3: return False

    for i in range(n-1):

        if(
            group_of_letter[word[i]] == -1
            or group_of_letter[word[i]] == group_of_letter[word[i+1]]
        ):
            return False

    if group_of_letter[word[-1]] == -1: return False

    return True

# ==============================================================================

def find_sequences(letters, words, words_by_first_letter, solve_in):
    '''
        Find all valid sequences of words by calling 
        find_sequences_starting_with for each valid starting word
        input:
            letters                 str     all letters in the game
            words                   list    all valid words
            words_by_first_letter   dict    valid words indexed by first letter
            solve_in                int     maximum number of words in a valid 
                                            sequence
        output:
            None
    '''
    
    sequences = []
    
    for i in range(1, solve_in+1):

        for word in words:
    
            current_sequence = [word]
    
            find_sequences_starting_with(
                sequences,
                current_sequence,
                letters,
                words_by_first_letter,
                i
            )

        if len(sequences) > 0: 

            break

    return sequences


# ==============================================================================

def find_sequences_starting_with(
    sequences, 
    current_sequence, 
    letters, 
    words_by_first_letter,
    solve_in
): 
    '''
        Recursively find all valid sequences of words that:
         - start with current_sequence;
         - contain all letters;
         - contain at most solve_in words;
         - contains no redundant words,
        and add them to sequences
        input:
            sequences               list    list of all valid sequences
            current_sequence        list    starting sequence
            letters                 str     all letters in the game
            words_by_first_letter   dict    valid words indexed by first letter
            solve_in                int     maximum number of words in a valid 
                                            sequence
        output:
            None
    '''

    if contains_redundant_word(current_sequence): return

    if contains_all_letters(letters, current_sequence):

        sequences.append(current_sequence.copy())
        print_sequence(current_sequence)
        return 

    if len(current_sequence) >= solve_in: return

    last_letter = (current_sequence[-1])[-1]

    for word in words_by_first_letter[last_letter]:
    
        current_sequence.append(word)

        find_sequences_starting_with(
            sequences,
            current_sequence,
            letters,
            words_by_first_letter,
            solve_in
        )

        del current_sequence[-1]

# ==============================================================================

def contains_redundant_word(sequence):
    '''
        Check if a sequence contains a word all of whose letters are
        also contained in other words in the sequence
        input:
            sequence                    list    list of words in sequence
        output:
            contains_redundant_word     bool
    '''

    for i in range(len(sequence)):
    
        word = sequence[i]
        sequence_without_word = sequence[:i] + sequence[i+1:]
    
        if contains_all_letters(word, sequence_without_word): 
                
            return True

    return False

# ==============================================================================

def contains_all_letters(letters, sequence):
    '''
        Check if a sequence contains all letters
        input:
            letters                 str     letters to check
            sequence                list    list of words in sequence
        output:
            contains_all_letters    bool
    '''

    letters_sequence = ''.join(sequence)

    for letter in letters:

        if not letter in letters_sequence: return False

    return True

# ==============================================================================

def print_sequence(sequence):
    '''
        Print the words in sequence
        input:
            sequence    list    list of words in the sequence
        output:
            None
    '''

    for word in sequence[:-1]:
    
        print(
            word, 
            clr(" - ", "red", attrs = ["bold"]),
            sep = '',
            end = ''
        )

    print(sequence[-1])

# ==============================================================================
    
def write_sequences(groups, sequences, width):
    '''
        At the user's request, the found sequences are saved to a .txt file.
        Input:
            groups      list
            sequences   list
            width       int
        Output:
            None
    '''

    write = ( input("Save solution? (y/n) ").lower() == 'y' )

    if write: 

        date = datetime.datetime.today().strftime("%Y-%m-%d")
        solved = ( len(sequences) > 0 )
        if solved: solved_in = len(sequences[0])

        with open(f"letter_boxed_{date}.txt", "w") as file:

            file.write("letters:")

            for group in groups: 

                file.write(f" {group}")

            if solved: 
                
                file.write(f"\nsolved in {solved_in}")

                for sequence in sequences: 

                    file.write('\n')

                    for word in sequence:
                
                        file.write(f"{word} ")

            else: file.write(f"\nnot solved")

    cprint( "\n" + width*'=' + '\n', 'red' )

# ==============================================================================
# ==============================================================================

def main():

    width= 50

    print_header(50)

    letters, groups, group_of_letter, solve_in = user_input(width)

    display_square(groups, width)

    words, words_by_first_letter = find_words(letters, group_of_letter)
    
    sequences = find_sequences(
        letters,
        words,
        words_by_first_letter,
        solve_in
    )

    if len(sequences) == 0: print("No solutions found.")

    cprint( '\n' + width*'-' + '\n', "red", attrs=["bold"] )

    write_sequences(groups, sequences, width)

# ==============================================================================

main()

# ==============================================================================
# ==============================================================================
# ==============================================================================