from config import dictionaryloc
from config import maxrounds
from threading import Timer

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

round_num = 0
dictionary = []
wheel_list = []
round_word = ""
blank_word = []
vowels = {"a", "e", "i", "o", "u"}


def read_dictionary_file():                                                                                             # takes dictionary file and imports words into dictionary list variable
    global dictionary
    
    # fill dictionary list with words from text
    f = open(r'data\dictionary.txt')
    dictionary = f.read().splitlines()
    f.close
    
def wheel_segments():                                                                                                   # creates the wheel sections
    global wheel_list
    wheel_list = [100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,"BANKRUPT","Lost a Turn"]

def game_setup():
    global dictionary
    global wheel_list
    
    read_dictionary_file()
    wheel_segments()

def get_word():                                                                                                         # generate random word from dictionary, create list of '-'s 
    round_word = dictionary[random.randrange(1,len(dictionary) + 1)] 

    blank_word = ['-' for letter in round_word]
    
    return round_word, blank_word

def wof_round_setup():                                                                                                  # at the start of each round, clears round totals, generates random starting player number
    global players
    global round_word
    global blank_word
    
    for i in players:                        # resets roundtotal value to zero
        players[i]["roundtotal"] = 0
    
    init_player = random.randrange(0,3)       # selects player randomly to start
    
    temp_tuple = get_word()                   # get random word, blank list of dashes
    round_word = temp_tuple[0]
    blank_word = temp_tuple[1]
    
    return init_player

def spin_wheel(player_num):                                                                                            # take player number, randomly selects wheel segment and dives into appropriate function
    global wheel_list
    global players
    global vowels
    
    wheel_selection = wheel_list[random.randrange(0,len(wheel_list))]    # uses randrange to select random element from wheel list

    if wheel_selection == 'BANKRUPT':                                               # if bankrupt, clear player's round total and end turn
        print("The wheel landed on BANKRUPT. Sorry!")
        players[player_num]["roundtotal"] = 0
        still_in_turn = False

    elif wheel_selection == 'Lost a Turn':                                          # if lost turn, end turn
        print("The wheel landed on 'Lost a Turn', so you lose a turn!")
        still_in_turn = False

    else:                                                                       
        valid_guess = False
        print(f"You landed on ${wheel_selection}. Here's the blank word.")
        print(''.join(blank_word))
        print('===================')
        # print(round_word)                                                     # uncomment to see actual word for testing game
        
        while not valid_guess:                                                   # as long as user inputs invalid guess, keep asking for letter
            letter = input("Please guess a letter: ")
            temp_tuple = guess_letter(letter, player_num)                        # function returns a tuple of (was the guess good bool, how many guessed letters in word, was the guess valid bool), stored in temp_tuple
            valid_guess = temp_tuple[2]                                          # guess_letter()[2] returns a False boolean if a vowel is guessed without being purchased
        
        players[player_num]["roundtotal"] += wheel_selection * temp_tuple[1]     # get reward money if correct guess, temp_tuple[1] returns 0 if not good guess so nothing is added
        
        still_in_turn = temp_tuple[0]

    return still_in_turn                                                         # function returns True if player has made a good guess

def guess_letter(letter, player_num, purchased_vowel = False):                   # takes player guess, player number, and boolean to identify if this is called from buy_vowel or spin_wheel function
    global round_word
    global blank_word
    
    good_guess = None
    count = 0
    valid_guess = False
    
    if not purchased_vowel and letter not in vowels:                                    # consonant guesses made from spin wheel function are passed through
        if letter in round_word:
            count = 0
            for i in range(0,len(blank_word)):                                          # if guess is correct, replace the blank word dashes that represent the letter
                if round_word[i] == letter:
                    blank_word[i] = letter
                    count += 1
            if '-' in blank_word:
                if count == 1:
                    print(f"Good guess! '{letter}' shows up {count} time")
                else:
                    print(f"Good guess! '{letter}' shows up {count} times")
            else:
                players[player_num]["gametotal"] += players[player_num]["roundtotal"]    # if player guesses last consonant, print a message congratulating the player and move round total to game total
                print("You got the full word!")
               
                
            good_guess = True
            valid_guess = True
        else:                                                                           # if guess is wrong, print message and function will return False good guess, true valid guess, zero count
            print(f"Sorry, '{letter}' isn't in the word.")
            good_guess = False
            valid_guess = True
            count = 0
    elif letter in vowels and not purchased_vowel:                                      # if a vowel is guessed when consonant is expected, print message and valid_guess stays False, so input is looped until valid guess
        print('Consonants only please. ')
    
    elif letter not in vowels and purchased_vowel:                                      # if this function called from buy vowel option but a consonant is guessed, print message and loop until valid guess
        print("Vowels only please.")
            
    elif letter in vowels and purchased_vowel:                                          # if vowel bought and vowel guessed, if its in the word replace dashes in blank_word and 
        if letter in round_word:
            for i in range(0,len(blank_word)):
                if round_word[i] == letter:
                    blank_word[i] = letter
                    count += 1
            if '-' in blank_word:
                if count == 1:
                    print(f"Good guess! '{letter}' shows up {count} time")
                else:
                    print(f"Good guess! '{letter}' shows up {count} times")
            else:
                players[player_num]["gametotal"] += players[player_num]["roundtotal"]    # if player buys last vowel, move round total to game total and print message
                print("You got the full word!") 
                
            
            good_guess = True
            valid_guess = True
        else:                                                                            # if vowel that is bought isn't in word, print message and return good guess as False, valid guess as True
            print(f"Sorry, '{letter}' isn't in the word!")
            good_guess = False
            valid_guess = True
    return good_guess, count, valid_guess

def guess_letter_final_round(letter, player_num, guessing_vowel = False):                # guess_letter version for the final round. No messages, and added values are the final prize money
    global round_word
    global blank_word
    
    good_guess = None
    valid_guess = False
    
    if not guessing_vowel and letter not in vowels:
        if letter in round_word:
           
            for i in range(0,len(blank_word)):          
                if round_word[i] == letter:
                    blank_word[i] = letter
                    
            if '-' not in blank_word:
                players[player_num]["gametotal"] += 5000000    # if player guesses last consonant
            good_guess = True
            valid_guess = True
       
    elif not guessing_vowel and letter in vowels:
        print('Consonants only please')
            
    elif guessing_vowel and letter in vowels:
        if letter in round_word:
            for i in range(0,len(blank_word)):
                if round_word[i] == letter:
                    blank_word[i] = letter
                    
            if '-' not in blank_word:
                players[player_num]["gametotal"] += 5000000    # if player guesses last vowel
                
                
            good_guess = True
            valid_guess = True
            
    elif guessing_vowel and letter not in vowels:
        print('Vowels only please')
       
    return blank_word

def buy_vowel(player_num):                                                                      # function to buy a vowel, needs player number parameter
    global players
    global blank_word
    
    if players[player_num]["roundtotal"] >= 250:                                                # check if player has the money to buy vowel
        valid_guess = False

        while not valid_guess:                                                                  # loops input until a vowel is entered
            letter = input("Please choose a vowel: ")
            temp_tuple = guess_letter(letter, player_num, True)                                 # the boolean in guess_letter tells function that a vowel is expected, function returns a tuple
            valid_guess = temp_tuple[2]                                                         # if a vowel is not entered, temp_tuple[2] returns false, so player must input a vowel to break loop

        players[player_num]["roundtotal"] -= 250                                                # deduct cost of vowel
        good_guess = temp_tuple[0]                                                              # set good_guess to true if vowel in word, false if not
    else:                                                                                       # if player doesn't have money for vowel, print message and return good guess to give player chance to choose other options
        print('You do not have enough to buy a vowel. Please make another selection.')
        good_guess = True

    return good_guess

def guess_word(player_num):                                                         # function takes a player input and checks if it is the round word
    global players
    global blank_word
    global round_word
    
    print(f"The board: {''.join(blank_word)}")
    player_guess = input("Make your guess: ")

    if player_guess == round_word:
        print("Correct guess!!")
        players[player_num]["gametotal"] += players[player_num]["roundtotal"]    # moves round $ to total $ if correct guess
        players[player_num]["roundtotal"] = 0                                    # removes roundtotal for player winner here, so it isn't added again at the end of the wof_turn() fx
        for i in range(0,len(round_word)):
            blank_word[i] = round_word[i]
    else:                                                                       # if wrong guess
        print('Wrong guess!')
        
    return False                                                                # regardless of guess's correctness, returns a false to end player's turn

def final_round_guess_word(final_guess, player_num):                            # the final round version of guess_word
    global players
    global blank_word
    global round_word
    
 

    if final_guess == round_word:                                               # if the final round guess is correct, add prize money to player's game total, replace blank word dashes with letters
        
        players[player_num]["gametotal"] += 50000000    
        players[player_num]["roundtotal"] = 0                                   
        for i in range(0,len(round_word[0])):
            blank_word[i] = round_word[0][i]
        good_guess = True
    else:                                                                       # if guess is wrong, show correct answer
        print(f'Wrong guess!\nThe correct answer was {round_word}')
        good_guess = False
        
    return good_guess

def wof_turn(player_num):                                                       # function to keep a player in play while still in turn is true
    global round_word
    global blank_word
    global players
    
    still_in_turn = True
    while still_in_turn and '-' in blank_word:                                                                          # if '-' no longer in blank word, end turn because word has been guessed
        print('Player {} currently has {} in their bank'.format(player_num, players[player_num]['roundtotal']))         # give player options for actions
        choice = input("""
                      'S' to spin
                      'B' to buy a vowel
                      'G' to guess the word
                      ______________________
                      Choose a menu option: """)
        if(choice.strip().upper() == "S"):
            still_in_turn = spin_wheel(player_num)                              # if player makes good guess, spin_wheel returns True. Returns false if lands on skip turn and bankrupt
        elif(choice.strip().upper() == "B"):
            still_in_turn = buy_vowel(player_num)                               # if player buys vowel in word, returns True. Returns False if vowel is not in word
        elif(choice.strip().upper() == "G"):
            still_in_turn = guess_word(player_num)                              # guess word always returns false
        else:                                                                   # if player types a letter not on options menu, prints message and loops input until valid
            print("Not an option.")
            
def wof_round():                             # function for round 1 and 2                                                   
    global players
    global round_word
    global blank_word
    
    current_player = wof_round_setup()       # wof round setup outputs random player number
    
    print("Let's begin the round")
    
    while '-' in blank_word:                 # while the word has not been guessed, cycle through players
        if current_player == 0:
            wof_turn(current_player)    
            current_player += 1
        elif current_player == 1:
            wof_turn(current_player)
            current_player += 1
        else:
            wof_turn(current_player)
            current_player -= 2
    if '-' not in blank_word:                                                       # once the word is guessed, print a round summary of prize money
        print(f'''
                  Player 0 has {players[0]["gametotal"]} game total bank
                  Player 1 has {players[1]["gametotal"]} game total bank
                  Player 2 has {players[2]["gametotal"]} game total bank''')
        

def wof_final_round():                                                              # the third round
    global round_word
    global blank_word
    
    win_player = 0
    amount = 0
    players_totals = [players[key]['gametotal'] for key in players]                # create a list of game totals
    players_identity = list(players.keys())                                        # create list of players
    win_player = players_identity[players_totals.index(max(players_totals))]        # select player that has max game total
    amount = max(players_totals)                                                   # select player's game total
    temp_tuple = get_word()                                                        # get random word, blank list of dashes
    round_word = temp_tuple[0]
    blank_word = temp_tuple[1]
    round_three_letters = ['r','s','t','l','n','e']
    
    print(f"Player {win_player}, you've made it to Round 3.\nA new word has been chosen.")
    print('Now to reveal the letters {}'.format(', '.join(round_three_letters).upper()))                    # print message that states the letters being revealed first

    for i in range(0,len(blank_word)):                                                              #  replace all dashes in the blank_word with r,s,t,l,n,e if present
        for j in range(0,len(round_three_letters)):
            if round_word[i] == round_three_letters[j]:
                blank_word[i] = round_three_letters[j]

    print(''.join(blank_word))
    print('--------')
    # print(round_word)                                                                         # uncomment for testing final round, reveal word to player

    valid_guess = False
    round_three_guesses = []                                                                   # list will hold the player's guesses

    while not valid_guess:                                                                     # only accepts consonant, loops if vowel is entered
        user_input = input('Please choose your first consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:                                                                      # only accepts consonant, loops if vowel is entered
        user_input = input('Please choose your second consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:                                                                      # only accepts consonant, loops if vowel is entered
        user_input = input('Please choose your third consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:                                                                      # only accepts vowel, loops if consonant is entered
        user_input = input('Now choose a vowel: ')
        if user_input not in vowels:
            print('Vowels only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    for i in range(0,3):                                                                        # checks all three consonant guesses with special final round guess letter function, replace in blank word
        guess_letter_final_round(round_three_guesses[i], win_player)

    guess_letter_final_round(round_three_guesses[3], win_player, True)                          # checks vowel, replaces in blank word

    print(''.join(blank_word))                                                                  # print the new blank word

    if '-' in blank_word:                                                                       # if the previous guesses have not filled all empty spaces, give player 30 secs to input a word guess
        timeout = 30
        t = Timer(timeout, print, ['Times up!'])
        t.start()
        final_guess = input(f"You have {timeout} seconds to make your word guess.\n")
        t.cancel()

        if final_round_guess_word(final_guess, win_player):
            print(f"Congratulations, you won! You're total prize is ${players[win_player]['gametotal']}")
    else:                                                                                                           # if the 3 consonants and vowel filled the word before word guess, player wins
        print(f"Congratulations player {win_player}! You won ${players[win_player]['gametotal']}")
    
def main():                                                                 # main game function
    game_setup()                                                            # game setup function fills dictionary list and wheel segment list
    
    for i in range(0, maxrounds):                                           # for values 0,1 use wof_round() function
        if i in [0,1]:
            wof_round()
        else:                                                               # for value 2 use wof_final_round() function
            wof_final_round()

if __name__ == "__main__":
    main()