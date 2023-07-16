import tkinter as tk
from morse import morse_code_dot_dash

MORSE_OUTPUT_FONT = ("Arial", 13, 'normal')
FOOTNOTE_FONT = ("Arial", 8, 'normal')
ROOT_W = 710
ROOT_H = 475

# Defining a new dictionary reversing each key:value pair, to be used when converting Morse code to text.
morse_to_text_dict = {value: key for key, value in morse_code_dot_dash.items()}
del morse_to_text_dict["    "]
# Adding a key which will act as an indicator if spaces will be represented with a forward slash or not.
morse_to_text_dict["fwslash_space"] = False


def on_key_release(event):
    """This function converts the user input to either Morse code or text, depending on what is chosen by the user,
    and updating the text displayed. It is to be triggered whenever the user releases a key. The 'mode' variable
    contains the function responsible for conversion, chosen by the user in one of the checkboxes.
    """
    output_translated_text.config(state='normal')
    output_translated_text.delete("1.0", tk.END)
    output_translated_text.insert("1.0", mode(text_entry_input.get().upper()))
    output_translated_text.config(state='disabled')


# Here the function triggered by the checkbox for the space type (' / ' or seven spaces) is defined.
# This function will update the dictionary entries related to spacing
def space_mode():
    selected = spacing_mode_checkbox_var.get()
    if selected:
        morse_code_dot_dash[" "] = " / "
        morse_to_text_dict["fwslash_space"] = True
    else:
        morse_code_dot_dash[" "] = 4*" "
        morse_to_text_dict["fwslash_space"] = False

    # The code below triggers on_key_release in order to update the output.
    event = tk.Event()
    event.keysym = "Return"
    on_key_release(event)


# Here the function triggered by the checkbox for the converting mode (text to Morse or Morse to text) is defined.
# This function will assign the global variable mode to one of the converting functions, depending on what was chosen by
# the user. These converting functions are defined below.
def converter_mode():
    global mode
    selected = converting_mode_checkbox_var.get()
    if selected:
        mode = morse_to_text
    else:
        mode = to_morse_converter

    # The code below triggers on_key_release in order to update the output.
    event = tk.Event()
    event.keysym = "Return"
    on_key_release(event)


def to_morse_converter(text: str) -> str:
    """
    A function that converts a string into its Morse code equivalent, ignoring any character not included in the
    International Morse code.
    :param text: A string to be converted into Morse code.
    :return: A string containing the Morse code translation of the input.
    """
    morse_translation = ""
    for char in text:
        # Any character not included in the morse_code_dot_dash dictionary is ignored.
        if char not in morse_code_dot_dash:
            pass
        else:
            if morse_code_dot_dash[char] == " / ":
                # If the current character is a space, ' / ' is appended to the converted string if this was the spacing
                # mode chosen by the user. Note that the last 3 characters of the converted string are ignored because
                # they are either three spaces (space between each Morse code letter/number) or ' / ' (in case the user
                # types more than one space in succession).
                morse_translation = morse_translation[:-3] + morse_code_dot_dash[char]
            elif morse_code_dot_dash[char] == 4*" ":
                if morse_translation[-7:] == 7*" ":
                    # In case the user types more than one space in succession, the Morse conversion ignores it.
                    pass
                else:
                    # If the current character is a space, four spaces are appended to the converted string if this was
                    # the spacing mode chosen by the user. Note that four spaces are appended instead of seven because
                    # after every letter/number three spaces are inserted.
                    morse_translation += morse_code_dot_dash[char]
            else:
                # If the current character is not a space, its corresponding Morse code translation is appended to the
                # converted string, plus three more spaces.
                morse_translation += f"{morse_code_dot_dash[char]}   "
    # Once the text is converted, it is returned removing the extra spaces.
    return morse_translation[:-7] if morse_translation[-7:] == 7*" " else morse_translation[:-3]


def morse_to_text(code: str) -> str:
    """
    A function that converts a Morse code string into its text equivalent, ignoring any character (or combination of
    characters) that doesn't represent a letter or number.
    :param code: A string containing Morse code to be converted into text.
    :return: A string containing the text translation of the input.
    """
    if morse_to_text_dict["fwslash_space"]:
        # If the spacing type chosen is ' / ', the input string is split using this separator, yielding a list of
        # Morse code encoded words which are in turn split into a list of Morse code encoded symbols, representing
        # the letter/numbers.
        wordlist = [word.split(" ") for word in code.split(" / ")]
    else:
        # If the spacing type chosen is seven spaces, the input string is split using this separator.
        wordlist = [word.split(" ") for word in code.split(7*" ")]

    # After splitting the input into a nested list of Morse code encoded symbols, the translated text is returned by
    # first converting each symbol into its text equivalent, using the dictionary morse_to_text_dict, then joining
    # this list of letters representing the word, finally joining every word together with a single space.
    return " ".join(["".join([morse_to_text_dict[letter] for letter in word if letter in morse_to_text_dict]) for word
                     in wordlist]).lower()


# Defining the root window and its properties and widgets
root = tk.Tk()
root.title("Morse Code Converter")
root.geometry(f"{ROOT_W}x{ROOT_H}")
root.config(pady=10, padx=10)
root.resizable(False, False)
root.grid_propagate(False)

text_entry_input_label = tk.Label(text="Type here:")
text_entry_input_label.grid(row=0, column=0, sticky="NSEW")
text_entry_input = tk.Entry(width=60)
text_entry_input.grid(row=0, column=1, columnspan=2, sticky="NSEW")

output_translated_text = tk.Text(state="disabled", width=75, height=17, font=MORSE_OUTPUT_FONT, wrap="word")
output_translated_text.grid(row=1, column=0, columnspan=3, sticky="NSEW", pady=5)

ys = tk.Scrollbar(orient='vertical', command=output_translated_text.yview)
output_translated_text.config(yscrollcommand=ys.set)
ys.grid(row=1, column=3, sticky='NS', pady=5)

spacing_mode_checkbox_var = tk.BooleanVar()
spacing_mode_checkbox = tk.Checkbutton(text='Use " / " to separate words',
                                       variable=spacing_mode_checkbox_var,
                                       command=space_mode)
spacing_mode_checkbox.grid(row=2, column=1)

converting_mode_checkbox_var = tk.BooleanVar()
converting_mode_checkbox = tk.Checkbutton(text='Morse code to text',
                                          variable=converting_mode_checkbox_var,
                                          command=converter_mode)
converting_mode_checkbox.grid(row=3, column=1)

footnote1 = tk.Label(text="Characters not included in the International Morse code are ignored.", font=FOOTNOTE_FONT)
footnote1.grid(row=4, column=1)

footnote2 = tk.Label(text="When converting Morse code to text, separate letters with a single space and words\n"
                          "with either ' / ' or seven spaces, depending on what you chose on the first checkbox.",
                     font=FOOTNOTE_FONT)
footnote2.grid(row=5, column=1)

text_entry_input.bind("<KeyRelease>", on_key_release)

# The initial converting mode is defined to be from text to Morse code.
mode = to_morse_converter

root.mainloop()
