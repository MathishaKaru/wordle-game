"""
File: wordle.py
Authors: Brianna Floyd and Mathisha Karunaratne
Date: 16 May 2022
Description: Fully working version of popular word guessing game Wordle.
"""

# Imports
import random
import tkinter as tk
import tkinter.font as font
from enum import Enum
import time
from turtle import up

from numpy import full

class Wordle:
    def __init__(self):
        """ Initialize the game """
        # Constants
        self.WORD_SIZE = 5  # number of letters in the hidden word
        self.NUM_GUESSES = 6 # number of guesses that the user gets 
        self.LONG_WORDLIST_FILENAME = "long_wordlist.txt"
        self.SHORT_WORDLIST_FILENAME = "short_wordlist.txt"

        # Size of the frame that holds all guesses.  This is the upper left
        # frame in the window.
        self.PARENT_GUESS_FRAME_WIDTH = 750
        self.PARENT_GUESS_FRAME_HEIGHT = 500

        # Parameter instance variables
        self.guesses_words = True
        self.show_word = False
        self.specify_word = False
        self.repeated_letters = False
        self.game_started = False
        self.game_finished = False
        self.game_won = False
        self.incorrect_guess = False
        
        self.word = ""
        self.full_guess = ""

        self.window = tk.Tk()
        self.window.title("Wordle")

        self.previous_indexes = []
        self.colors_list = []

        self.buttons = {}
        self.guess_boxes = {}
        self.guess_frames = {}
        self.letters = {}
        self.letter_instances_word = {}
        self.letter_instances_guess = {}
        self.repeats = {}
        self.buttons_color_changed = {}

        self.guess_row = 1
        self.guess_column = 1

        # Parameters for an individual letter in the guess frame
        # A guess frame is an individual box that contains a guessed letter.
        self.GUESS_FRAME_SIZE = 50  # the width and height of the guess box.
        self.GUESS_FRAME_PADDING = 3 
        self.GUESS_FRAME_BG_BEGIN = 'white' # background color of a guess box 
                                            # after the user enters the letter,
                                            # but before the guess is entered.
        self.GUESS_FRAME_TEXT_BEGIN = 'black' # color of text in guess box after the
                                            # user enters the letter, but before
                                            # the guess is entered.
        self.GUESS_FRAME_BG_WRONG = 'grey'  # background color of guess box
                                            # after the guess is entered, and the
                                            # letter is not in the hidden word.
        self.GUESS_FRAME_BG_CORRECT_WRONG_LOC = 'orange' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # but in the wrong location.
        self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC = 'green' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # and in the correct location.
        self.GUESS_FRAME_TEXT_AFTER = 'white' # color of text in guess box after
                                            # the guess is entered.
        self.FONT_FAMILY = 'ariel'          # Font to use for letters in the guess boxes.
        self.FONT_SIZE_GUESS = 34           # Font size for letters in the guess boxes.

        # Parameters for the keyboard frame
        self.KEYBOARD_FRAME_HEIGHT = 200
        self.KEYBOARD_BUTTON_HEIGHT = 1
        self.KEYBOARD_BUTTON_WIDTH = 6  # width of the letter buttons.  Remember,
                                        # width of buttons is measured in characters.
        self.KEYBOARD_BUTTON_WIDTH_LONG = 8 # width of the enter and back buttons.
        self.KEYBOARD_KEYS_PADDING = 3
        self.KEYBOARD_ROW_HEIGHT = 31

        # The following colors for the keyboard buttons
        # follow the same specifications as the colors defined above for the guess
        # boxes.  The problem is that if one or both of you have a mac, you will
        # not be able to change the background color of a button.  In this case,
        # just change the color of the text in the button, instead of the background color.
        # So the text color starts as the default (black), and then changes to grey, orange, 
        # green depending on the result of the guess for that letter.
        self.KEYBOARD_BUTTON_BG_BEGIN = 'white' 
        self.KEYBOARD_BUTTON_TEXT_BEGIN = 'black' 
        self.KEYBOARD_BUTTON_BG_WRONG = 'grey'  
        self.KEYBOARD_BUTTON_BG_CORRECT_WRONG_LOC = 'orange' 
        self.KEYBOARD_BUTTON_BG_CORRECT_RIGHT_LOC = 'green' 
        self.KEYBOARD_BUTTON_TEXT_AFTER = 'white' 

        self.KEYBOARD_BUTTON_NAMES = [   
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]]
        
        # Parameters for the control frame
        self.CONTROL_FRAME_HEIGHT = self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT
        self.CONTROL_FRAME_WIDTH = 300

        self.USER_SELECTION_PADDING = 10  # Horizontal padding on either side of the widgets in
                                            # the parameter frame.

        self.MESSAGE_DISPLAY_TIME_SECS = 5 # Length of time the message should be
                                            # displayed.
        self.PROCESS_GUESS_WAITTIME = 1  # When processing a guess (changing color
                                        # of the guess frames), time to wait between
                                        # updating successive frames.        
        
        # Run initial methods
        self.read_files()
        self.guess_frame_method()
        self.keyboard_frame_method()
        self.all_control_frames()
        self.control_frame_message()
        self.control_frame_widgets()
        self.control_frame_buttons()
        self.colors_list_creation()

        self.window.mainloop()

    def guess_frame_method(self):
        """
        Create guess frame
        """
        self.guess_frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.PARENT_GUESS_FRAME_HEIGHT, width = self.PARENT_GUESS_FRAME_WIDTH)
        self.guess_frame.grid(row = 1, column = 1)
        self.guess_frame.grid_propagate(False)

        # Create and position letter frames
        for r in range(self.NUM_GUESSES):
            for c in range(self.WORD_SIZE):
                square = tk.Frame(self.guess_frame, height = self.GUESS_FRAME_SIZE, 
                    borderwidth = 1, relief = 'solid', width = self.GUESS_FRAME_SIZE)
                self.letter_variable = tk.StringVar()
                letter = tk.Label(square, textvariable = self.letter_variable, font = (self.FONT_FAMILY, self.FONT_SIZE_GUESS))
                
                # Create dictionary with letter locations
                self.guess_boxes[(r + 1, c + 1)] = self.letter_variable
                self.guess_frames[(r + 1, c + 1)] = square
                self.letters[(r + 1, c + 1)] = letter

                square.grid(row = r + 1, column = c + 1, padx = self.GUESS_FRAME_PADDING, pady = self.GUESS_FRAME_PADDING)
                square.grid_propagate(False)

                letter.grid(row = 1, column = 1)

                # Center text within guess boxes
                square.rowconfigure(0, weight = 1)
                square.rowconfigure(2, weight = 1)
                square.columnconfigure(0, weight = 1)
                square.columnconfigure(2, weight = 1)
        
        # Center guess frame boxes
        self.guess_frame.rowconfigure(0, weight = 1)
        self.guess_frame.rowconfigure(7, weight = 1)
        self.guess_frame.columnconfigure(0, weight = 1)
        self.guess_frame.columnconfigure(6, weight = 1)

    def button_handler(self, text):
        """
        Prints the text of the button that was pressed
        """
        if self.game_started == True and self.game_finished == False:
            # Checks to do if 'enter' button is clicked
            if text == 'ENTER':
                if self.guess_column == 6:
                    self.word_valid_check()
                    
                    # Display if game is lost
                    if self.guess_row == 7 and self.game_won == False:
                        wrong_error = "Guesses used up. \n" + "Word was " + self.word + ". Game over."
                        self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, wrong_error)
                        self.game_finished = True
                        self.process_guesses()
                        self.full_guess = ""
                
                # Message if word is less than 5 letters
                else:
                    self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, "Word not finished")

            elif text == 'BACK':
                # Delete letter if back button is clicked and there are letters to delete
                if self.guess_column != 1:
                    self.guess_column -= 1
                    box = self.guess_boxes[(self.guess_row, self.guess_column)]
                    box.set('     ')
            elif self.guess_column == 6:
                pass
            else:
                # Display types letter
                box = self.guess_boxes[(self.guess_row, self.guess_column)]
                self.guess_column += 1
                box.set(text)

    def word_valid_check(self):
        """
        Checking if word is valid (if necessary), and then move on to next row if so
        """
        for i in range(self.WORD_SIZE):
            box = self.guess_boxes[(self.guess_row, i + 1)]
            letter = box.get()
            self.full_guess += letter
        
        self.count_letters()
        self.full_guess = self.full_guess.lower()

        # Check if the guess is a valid word if the checkbox is clixked
        if self.checkbox_wordguesses_var.get() == True:
            if self.full_guess in self.long_list:
                self.guess_row += 1
                self.guess_column = 1
                self.process_guesses()
                self.full_guess = ""
                self.letter_instances_guess = {}
                self.letter_instances_word = {}
                self.repeats = {}
            
            # If the guess is not a valid word display an error message
            else:
                not_word_error = self.full_guess + " is not in the word list"
                self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, not_word_error)
                self.full_guess = ""
                self.letter_instances_guess = {}
                self.letter_instances_word = {}
                self.repeats = {}
        
        # Move onto next row
        else:
            self.guess_row += 1
            self.guess_column = 1
            self.process_guesses()
            self.full_guess = ""
            self.letter_instances_guess = {}
            self.letter_instances_word = {}
            self.repeats = {}
    
    def process_guesses(self):
        """
        Takes guesses and compares with hidden word to color guess boxes with hints
        """
        for i in range(len(self.full_guess)):
            upper_guess = self.full_guess[i].upper()
            upper_letter = self.word[i].upper()          
            self.repeats[i] = False      

            # Change all correct letters to green, 
            # and remember that they have been changed to green
            if upper_letter == upper_guess:
                self.color_changes('green', i)  
                self.buttons[upper_guess]['fg'] = 'green'
                self.letter_instances_guess[upper_guess] -= 1
                self.letter_instances_word[upper_guess] -= 1
                self.repeats[i] = True
                self.buttons_color_changed[upper_guess] = True
        
        self.process_guesses_second_run()

        self.check_winning()

    def process_guesses_second_run(self):
        """
        Processes the guesses a second time for incorrect letters and letters in the wrong location
        """
        for i in range(len(self.full_guess)):
            upper_guess = self.full_guess[i].upper()
            upper_letter = self.word[i].upper()      

            # Check if the letter is in the word
            if upper_guess in self.word.upper():
                # Check if letter in the word repeats and if it needs to to 
                # be made orange (repeated) or gray (does not appear again)
                # Also change keyboard text colors to match guesses
                if self.repeats[i] == False:
                    if self.letter_instances_word[upper_guess] == 0:
                        self.color_changes('gray', i)

                        if self.buttons_color_changed[upper_guess] == False:
                            self.buttons[upper_guess]['fg'] = 'gray'
                            self.buttons_color_changed[upper_guess]
                    else:
                        self.color_changes('orange', i)
                        self.letter_instances_word[upper_guess] -= 1
                        if self.buttons_color_changed[upper_guess] == False:
                            self.buttons[upper_guess]['fg'] = 'orange'
                            #if self.hard_mode == True:
                                #self.colors_list[i] = 'orange'
                               
            else:
                self.color_changes('gray', i)
                self.buttons[upper_guess]['fg'] = 'gray'

                if self.buttons_color_changed[upper_guess] == False:
                    self.buttons[upper_guess]['fg'] = 'gray'
                    self.buttons_color_changed[upper_guess] = True

    def colors_list_creation(self):
        """
        Creates a list of necessary length to remember colors of guesses
        """
        for i in range(self.WORD_SIZE):
            self.colors_list.append("")

    def check_winning(self):
        """
        Check if the player has won the game on that round
        """    
        count = 0

        # Count how many letters are correct
        for i in self.repeats:
            if self.repeats[i] == True:
                count += 1

        if count == 5:
            self.game_won = True

        # If all letters are correct the game has been won
        if self.game_won == True:
            self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, "Correct. Nice job. Game over")
            self.game_finished = True
            
    def color_changes(self, color, i):
        """
        Modifies colors of guess boxes
        """
        letter_label = self.letters[(self.guess_row - 1, i + 1)]
        box = self.guess_frames[(self.guess_row - 1, i + 1)]
        box.configure(bg = color)
        letter_label.configure(bg = color)
        letter_label.configure(fg = 'white')
        
    def count_letters(self):
        """
        Counts instances of every letter in the hidden word
        """
        # Count instances of letters in the hidden word
        for i in self.word.upper():
            if i in self.letter_instances_word:
                self.letter_instances_word[i] += 1
            else:
                self.letter_instances_word[i] = 1
        
         # Count instances of letters in the guess
        for i in self.full_guess:
            if i in self.letter_instances_guess:
                self.letter_instances_guess[i] += 1
                self.repeated_letters = True
            else:
                self.letter_instances_guess[i] = 1
    
    def keyboard_frame_row(self):
        """
        Create seperate frames for each keyboard row to allow for correct key positioning and centering.
        """
        self.keyboard_row_frame_1 = tk.Frame(self.keyboard_frame, height = self.KEYBOARD_ROW_HEIGHT, 
                width = self.PARENT_GUESS_FRAME_WIDTH)
        self.keyboard_row_frame_1.grid(row = 1, column = 1)
        self.keyboard_row_frame_1.grid_propagate(False)

        self.keyboard_row_frame_2 = tk.Frame(self.keyboard_frame, height = self.KEYBOARD_ROW_HEIGHT, 
                width = self.PARENT_GUESS_FRAME_WIDTH)
        self.keyboard_row_frame_2.grid(row = 2, column = 1)
        self.keyboard_row_frame_2.grid_propagate(False)

        self.keyboard_row_frame_3 = tk.Frame(self.keyboard_frame, height = self.KEYBOARD_ROW_HEIGHT, 
                width = self.PARENT_GUESS_FRAME_WIDTH)
        self.keyboard_row_frame_3.grid(row = 3, column = 1)
        self.keyboard_row_frame_3.grid_propagate(False)

    def keyboard_buttons_placement(self):
        """
        Loop at create all keyboard buttons and their respective handlers.
        """
        for r in range(len(self.KEYBOARD_BUTTON_NAMES)):
            for c in range(len(self.KEYBOARD_BUTTON_NAMES[r])):
                def handler(key = self.KEYBOARD_BUTTON_NAMES[r][c]):
                    """
                    Create handler for each keyboard button
                    """
                    self.button_handler(key)

                # Place keyboard buttons in respective frames depending on row.
                if r == 0:
                    button = tk.Button(self.keyboard_row_frame_1, height = self.KEYBOARD_BUTTON_HEIGHT,
                        width = self.KEYBOARD_BUTTON_WIDTH, text = self.KEYBOARD_BUTTON_NAMES[r][c],
                        fg = self.KEYBOARD_BUTTON_TEXT_BEGIN, bg = self.KEYBOARD_BUTTON_BG_BEGIN,
                        font = self.FONT_FAMILY, command = handler)

                elif r == 1:
                    button = tk.Button(self.keyboard_row_frame_2, height = self.KEYBOARD_BUTTON_HEIGHT, 
                        width = self.KEYBOARD_BUTTON_WIDTH, text = self.KEYBOARD_BUTTON_NAMES[r][c], 
                        fg = self.KEYBOARD_BUTTON_TEXT_BEGIN, bg = self.KEYBOARD_BUTTON_BG_BEGIN, 
                        font = self.FONT_FAMILY, command = handler)

                else:
                    # Check if keyboard button requires longer length
                    if (r == 2 and c == 0) or (r == 2 and c == len(self.KEYBOARD_BUTTON_NAMES[r]) - 1):
                        button = tk.Button(self.keyboard_row_frame_3, height = self.KEYBOARD_BUTTON_HEIGHT,
                            width = self.KEYBOARD_BUTTON_WIDTH_LONG, text = self.KEYBOARD_BUTTON_NAMES[r][c],
                            fg = self.KEYBOARD_BUTTON_TEXT_BEGIN, bg = self.KEYBOARD_BUTTON_BG_BEGIN,
                            font = self.FONT_FAMILY, command = handler)

                    else:
                        button = tk.Button(self.keyboard_row_frame_3, height = self.KEYBOARD_BUTTON_HEIGHT,
                            width = self.KEYBOARD_BUTTON_WIDTH, text = self.KEYBOARD_BUTTON_NAMES[r][c],
                            fg = self.KEYBOARD_BUTTON_TEXT_BEGIN, bg = self.KEYBOARD_BUTTON_BG_BEGIN,
                            font = self.FONT_FAMILY, command = handler)

                button.grid(row = 0, column = c + 1, padx = self.KEYBOARD_KEYS_PADDING)

                # Create dictionary containing keyboard buttons and remembering if color of button has been changed
                self.buttons[self.KEYBOARD_BUTTON_NAMES[r][c]] = button
                self.buttons_color_changed[self.KEYBOARD_BUTTON_NAMES[r][c]] = False

        
        # Center keyboard rows in the keyboard frame
        self.keyboard_row_frame_1.columnconfigure(0, weight = 1)
        self.keyboard_row_frame_1.columnconfigure(len(self.KEYBOARD_BUTTON_NAMES[0]) + 1, weight = 1)
        self.keyboard_row_frame_2.columnconfigure(0, weight = 1)
        self.keyboard_row_frame_2.columnconfigure(len(self.KEYBOARD_BUTTON_NAMES[0]) + 1, weight = 1)
        self.keyboard_row_frame_3.columnconfigure(0, weight = 1)
        self.keyboard_row_frame_3.columnconfigure(len(self.KEYBOARD_BUTTON_NAMES[0]) + 1, weight = 1)

    def keyboard_frame_method(self):
        """
        Create keyboard frame
        """
        self.keyboard_frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.KEYBOARD_FRAME_HEIGHT, width = self.PARENT_GUESS_FRAME_WIDTH)
        self.keyboard_frame.grid(row = 2, column = 1)
        self.keyboard_frame.grid_propagate(False)
        
        self.keyboard_frame_row()
        
        self.keyboard_buttons_placement()
                
        # Center the grid of buttons in the button frame
        self.keyboard_frame.rowconfigure(0, weight = 1)
        self.keyboard_frame.rowconfigure(4, weight = 1)
        self.keyboard_frame.columnconfigure(0, weight = 1)
        self.keyboard_frame.columnconfigure(2, weight = 1)

    def all_control_frames(self):
        """
        Create control frame
        """
        self.control_frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT, width = self.CONTROL_FRAME_WIDTH)
        self.control_frame.grid(row = 1, column = 3)
        self.control_frame.grid(rowspan = 2)
        self.control_frame.grid_propagate(False)
    
    def control_frame_message(self):
        """
        Create message frame and invisible message label
        """
        # Creates the frame
        self.control_frame_1 = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = (self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT) / 3, width = self.CONTROL_FRAME_WIDTH)
        self.control_frame_1.grid(row = 1, column = 1)
        self.control_frame_1.grid_propagate(False)

        # Creates invisible label
        self.message_var = tk.StringVar()
        self.message = tk.Label(self.control_frame_1, textvariable = self.message_var)
        self.message.grid(row = 1, column = 1, padx = self.USER_SELECTION_PADDING)

        self.control_frame_1.grid_rowconfigure(1, weight = 1)
        self.control_frame_1.grid_columnconfigure(1, weight = 1)

    def control_frame_widgets(self):
        """
        Create widgets control frame and create all checkboxes, the entry field and display word label
        """
        # Creates the frame
        self.control_frame_2 = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = (self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT) / 3, width = self.CONTROL_FRAME_WIDTH)
        self.control_frame_2.grid(row = 2, column = 1)
        self.control_frame_2.grid_propagate(False)

        # Creates guesses must be words checkbox
        self.checkbox_wordguesses_var = tk.BooleanVar()
        self.checkbox_wordguesses_var.set(True)
        self.checkbox_wordguesses = tk.Checkbutton(self.control_frame_2, text="Guesses must be words", 
                            var = self.checkbox_wordguesses_var)
        self.checkbox_wordguesses.grid(row = 2, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        # Creates show word checkbox
        self.checkbox_show_word_var = tk.BooleanVar()
        self.checkbox_show_word_var.set(False)
        self.checkbox_show_word = tk.Checkbutton(self.control_frame_2, text="Show word", 
                            var = self.checkbox_show_word_var, command = self.show_word_command)
        self.checkbox_show_word.grid(row = 3, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)
        
        # Creates display word label
        self.display_word_var = tk.StringVar()
        self.display_word = tk.Label(self.control_frame_2, textvariable = self.display_word_var)
        self.display_word.grid(row = 3, column = 2, padx = self.USER_SELECTION_PADDING)

        # Creates specify word checkbox
        self.checkbox_specify_var = tk.BooleanVar()
        self.checkbox_specify_var.set(False)
        self.checkbox_specify = tk.Checkbutton(self.control_frame_2, text="Specify word", 
                            var = self.checkbox_specify_var)
        self.checkbox_specify.grid(row = 4, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)

        # Creates specify word entry
        self.hidden_word_var = tk.StringVar()
        self.hidden_word_entry = tk.Entry(self.control_frame_2, textvariable=self.hidden_word_var, width = self.WORD_SIZE)
        self.hidden_word_entry.grid(row = 4, column = 2, padx = self.USER_SELECTION_PADDING)

        self.control_frame_2.grid_rowconfigure(0, weight = 1)
        self.control_frame_2.grid_rowconfigure(5, weight = 1)

    def control_frame_buttons(self):
        """
        Create button frame and add start game and quit buttons
        """
        # Creates the frame
        self.control_frame_3 = tk.Frame(self.control_frame, 
            borderwidth = 1, relief = 'solid',
            height = (self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT) / 3, width = self.CONTROL_FRAME_WIDTH)
        self.control_frame_3.grid(row = 3, column = 1)
        self.control_frame_3.grid_propagate(False)

        # Creates start button
        start_button = tk.Button(self.control_frame_3, text = "Start Game", command = self.start_game)
        start_button.grid(row = 1, column=1)

        # Creates quit button
        quit_button = tk.Button(self.control_frame_3, text = "Quit", command = self.window.destroy)
        quit_button.grid(row = 1, column=2)

        self.control_frame_3.grid_rowconfigure(1, weight = 1)
        self.control_frame_3.grid_columnconfigure(0, weight = 1)
        self.control_frame_3.grid_columnconfigure(3, weight = 1)

    def read_files(self):
        """
        Read word files and add words to two lists
        """
        self.short_list = []
        self.long_list = []
        short_file = open(self.SHORT_WORDLIST_FILENAME)
        long_file = open(self.LONG_WORDLIST_FILENAME)

        # Read short file and append words to short list
        for line in short_file:
            line = line.split()
            line[0].strip()
            if len(line[0]) == self.WORD_SIZE:
                self.short_list.append(line[0])

        # Read long file and append words to long list
        for line in long_file:
            line = line.split()
            line[0].strip()
            if len(line[0]) == self.WORD_SIZE:
                self.long_list.append(line[0])

    def start_game(self):
        """
        Start the game and disable necessary widgets
        """
        if self.game_started == False:
            found = False
            
            # Check if word is going to be specified, if not choose a random word
            if self.checkbox_specify_var.get() != True:
                self.word = random.choice(self.short_list)
            else:
                self.word = self.hidden_word_entry.get()
                
                # Check if word is correct length and show error message if not
                if len(self.word) != self.WORD_SIZE:
                    self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, "Incorrect specified word length")
                    return
                
                # Check if word is a valid word (if necessary) and show error message if not
                elif self.checkbox_wordguesses_var.get() == True:
                    for i in self.short_list:
                        if i == self.word:
                            found = True
                    if found == False:
                        self.message_display(self.MESSAGE_DISPLAY_TIME_SECS, "Specified word not a valid word")
                        return
            
            self.show_word_command()
            
            self.hidden_word_var.set("")

            # Get status of all checkboxes
            self.guesses_words = self.checkbox_wordguesses_var.get()
            self.show_word = self.checkbox_show_word_var.get()
            self.specify_word = self.checkbox_specify_var.get()

            # Print parameter settings
            print("Guesses must be words = " + str(self.guesses_words))
            print("Show word = " + str(self.show_word))
            print("Specify word = " + str(self.specify_word))
            print("Hidden word = " + self.word)

            # Disable necessary checkboxes
            self.checkbox_specify['state'] = 'disabled'
            self.checkbox_wordguesses['state'] = 'disabled'
            self.hidden_word_entry['state'] = 'disabled'

            self.game_started = True

    def show_word_command(self):
        """
        Displays selected word, if selected
        """
        if self.checkbox_show_word_var.get() == True:
            self.display_word_var.set(self.word)
        else:
            self.display_word_var.set("")

    def message_display(self, time, message):
        """
        Displays message in message frame for specific time
        """
        self.message_var.set(message)
        self.message.after(time * 1000, self.message_blank)

    def message_blank(self):
        """
        Resets message frame
        """
        self.message_var.set("")

if __name__ == "__main__":
   Wordle()
