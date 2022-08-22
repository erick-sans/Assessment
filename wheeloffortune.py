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


def read_dictionary_file():
    global dictionary
    
    # fill dictionary list with words from text
    f = open(r'data\dictionary.txt')
    dictionary = f.read().splitlines()
    f.close
    
def wheel_segments():
    global wheel_list
    wheel_list = [100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,"BANKRUPT","Lost a Turn"]

def game_setup():
    global dictionary
    global wheel_list
    
    read_dictionary_file()
    wheel_segments()

def get_word():
    round_word = dictionary[random.randrange(1,len(dictionary) + 1)] 

    blank_word = ['-' for letter in round_word]
    
    return round_word, blank_word

def wof_round_setup():
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

def spin_wheel(player_num):
    global wheel_list
    global players
    global vowels
    
    wheel_selection = wheel_list[random.randrange(0,len(wheel_list))]    # uses randrange to select random element from wheel list

    if wheel_selection == 'BANKRUPT':
        print("The wheel landed on BANKRUPT. Sorry!")
        players[player_num]["roundtotal"] = 0
        still_in_turn = False

    elif wheel_selection == 'Lost a Turn':
        print("The wheel landed on 'Lost a Turn', so you lose a turn!")
        still_in_turn = False

    else: 
        valid_guess = False
        print(f"You landed on ${wheel_selection}. Here's the blank word.")
        print(''.join(blank_word))
        print('===================')
        # print(round_word)                                                     # uncomment to see actual word for testing game
        
        while not valid_guess:
            letter = input("Please guess a letter: ")
            temp_tuple = guess_letter(letter, player_num)
            valid_guess = temp_tuple[2]                                          # guess_letter()[2] returns a False boolean if a vowel is guessed without being purchased
        
        players[player_num]["roundtotal"] += wheel_selection * temp_tuple[1]     # get reward money if correct guess, add 0 if not good guess
        
        still_in_turn = temp_tuple[0]

    return still_in_turn

def guess_letter(letter, player_num, purchased_vowel = False):
    global round_word
    global blank_word
    
    good_guess = None
    count = 0
    valid_guess = False
    
    if not purchased_vowel and letter not in vowels:
        if letter in round_word:
            count = 0
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
                players[player_num]["gametotal"] += players[player_num]["roundtotal"]    # if player guesses last consonant
                print("You got the full word!")
               
                
            good_guess = True
            valid_guess = True
        else:
            print(f"Sorry, '{letter}' isn't in the word.")
            good_guess = False
            valid_guess = True
            count = 0
    elif letter in vowels and not purchased_vowel:
        print('Consonants only please. ')
    
    elif letter not in vowels and purchased_vowel:
        print("Vowels only please.")
            
    elif letter in vowels and purchased_vowel:
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
                players[player_num]["gametotal"] += players[player_num]["roundtotal"]    # if player guesses last buys last vowel
                print("You got the full word!") 
                
            
            good_guess = True
            valid_guess = True
        else:
            print(f"Sorry, '{letter}' isn't in the word!")
            good_guess = False
            valid_guess = True
    return good_guess, count, valid_guess

def guess_letter_final_round(letter, player_num, guessing_vowel = False):
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

def buy_vowel(player_num):
    global players
    global blank_word
    
    if players[player_num]["roundtotal"] >= 250:
        valid_guess = False

        while not valid_guess:
            letter = input("Please choose a vowel: ")
            temp_tuple = guess_letter(letter, player_num, True)
            valid_guess = temp_tuple[2]

        players[player_num]["roundtotal"] -= 250
        good_guess = temp_tuple[0]
    else:
        print('You do not have enough to buy a vowel. Please make another selection.')
        good_guess = True

    return good_guess

def guess_word(player_num):
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
    else:
        print('Wrong guess!')
        
    return False

def final_round_guess_word(final_guess, player_num):
    global players
    global blank_word
    global round_word
    
 

    if final_guess == round_word:
        
        players[player_num]["gametotal"] += 50000000    
        players[player_num]["roundtotal"] = 0                                   
        for i in range(0,len(round_word[0])):
            blank_word[i] = round_word[0][i]
        good_guess = True
    else:
        print(f'Wrong guess!\nThe correct answer was {round_word}')
        good_guess = False
        
    return good_guess

def wof_turn(player_num):
    global round_word
    global blank_word
    global players
    
    still_in_turn = True
    while still_in_turn and '-' in blank_word:
        print('Player {} currently has {} in their bank'.format(player_num, players[player_num]['roundtotal']))
        choice = input("""
                      'S' to spin
                      'B' to buy a vowel
                      'G' to guess the word
                      ______________________
                      Choose a menu option: """)
        if(choice.strip().upper() == "S"):
            still_in_turn = spin_wheel(player_num)
        elif(choice.strip().upper() == "B"):
            still_in_turn = buy_vowel(player_num)
        elif(choice.strip().upper() == "G"):
            still_in_turn = guess_word(player_num)
        else:
            print("Not an option.")
            
def wof_round():
    global players
    global round_word
    global blank_word
    global round_status
    current_player = wof_round_setup()    # wof round setup outputs random player number
    
    print("Let's begin the round")
    
    while '-' in blank_word:    # used to be an if instead of while
        if current_player == 0:
            wof_turn(current_player)    
            current_player += 1
        elif current_player == 1:
            wof_turn(current_player)
            current_player += 1
        else:
            wof_turn(current_player)
            current_player -= 2
    if '-' not in blank_word:
        print(f'''
                  Player 0 has {players[0]["gametotal"]} game total bank
                  Player 1 has {players[1]["gametotal"]} game total bank
                  Player 2 has {players[2]["gametotal"]} game total bank''')
        
# final round

def wof_final_round():
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
    print('Now to reveal the letters {}'.format(', '.join(round_three_letters).upper()))

    for i in range(0,len(blank_word)):
        for j in range(0,len(round_three_letters)):
            if round_word[i] == round_three_letters[j]:
                blank_word[i] = round_three_letters[j]

    print(''.join(blank_word))
    print('--------')
    print(round_word)

    valid_guess = False
    round_three_guesses = []

    while not valid_guess:
        user_input = input('Please choose your first consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:
        user_input = input('Please choose your second consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:
        user_input = input('Please choose your third consonant: ')
        if user_input in vowels:
            print('Consonants only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    valid_guess = False
    while not valid_guess:
        user_input = input('Now choose a vowel: ')
        if user_input not in vowels:
            print('Vowels only')
        else:
            round_three_guesses.append(user_input)
            valid_guess = True

    for i in range(0,3):
        guess_letter_final_round(round_three_guesses[i], win_player)

    guess_letter_final_round(round_three_guesses[3], win_player, True)

    print(''.join(blank_word))

    if '-' in blank_word:
        timeout = 30
        t = Timer(timeout, print, ['Times up!'])
        t.start()
        final_guess = input(f"You have {timeout} seconds to make your word guess.\n")
        t.cancel()

        if final_round_guess_word(final_guess, win_player):
            print(f"Congratulations, you won! You're total prize is ${players[win_player]['gametotal']}")
    else:
        print(f"Congratulations player {win_player}! You won ${players[win_player]['gametotal']}")
    
def main():
    game_setup()
    
    for i in range(0, maxrounds):
        if i in [0,1]:
            wof_round()
        else:
            wof_final_round()

if __name__ == "__main__":
    main()