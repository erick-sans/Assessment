# outside loop

roundNum = 0 # keep track of round 1,2 or 3

dictionary = [] # store words read in from txt file

wheellist = [] # used in readWheelTxtFile() and spinWheel() to display Wheel name

round_word = "" # used in getWord() to store random selected word
               # used in guessWord() to check a guess is in roundWord
              

blank_word = [] # used in getWord() to turn roundWord to list of empty underscores, used in 
               # used in guessWord() to replace blank spaces with correctly guessed letters
               # used in wofRound() to check if filled w/ letters = round over
               # used in wofFinalRound() for same rason
            
vowels = {"a", "e", "i", "o", "u"}      # used in buyVowel --> guessletter 1.check input, 2. check word
                                        # used in spinWheel to check that user guess is not vowel
    

# def read_dictionary_file() to get words from text into dictionary list

# def wheel_sections() to create a list of wheel segments

# def game_setup() to initiate read_dictionary file and wheel sections

# def get_word() to get a random word from dictionary

# def wof_round_setup() to generate word, blank word, clear player round banks for new round

# def spin_wheel(playernum) to get a random wheel section and display to player. 

# def guess_letter(letter, player_num, purchased_vowel) holds logic to validate guess, check guess, return if correct and valid

# def buy_vowel(playernum) to check player has the money, check the vowel bought

# def guess_word(playernum) to check if word guess is correct

# def wof_turn(playernum) to give players actions choices. Include spin, buy, and word guess

# def wof_round() to keep cycling through players while word is not guessed. 

# def wof_final_round() to include special rules for final round. Only one player, populate r,s,t,l,n,e, ask four letters

# def main() to cycle through rounds


# main()
    # Round 1

    # wof_round() 

        # get_word()

        # wof_turn() for players 0 - 2

            # spin_wheel()

            # buy_vowel()

            # guess_word()

        # if '-' not in blank_word, then end wof_round()

    # Round 2

    # wof_round()

        # get_word()

        # wof_turn() for players 0 - 2

            # spin_wheel()

            # buy_vowel()

            # guess_word()

        # if '-' not in blank_word, then end wof_round()

    # Round 3

    # wof_final_round()

        # get_word()

        # fill blank_word with r,s,t,l,n,e

        # get letters from player

        # use timer with guess_word()

        # if '-' not in blank_word, give award money 

        # player lose message if '-' still in blank_word



