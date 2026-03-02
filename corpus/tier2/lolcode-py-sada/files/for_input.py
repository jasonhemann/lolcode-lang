import tkinter.simpledialog as sd

def get_user_input():
    input = sd.askstring("Input", "Enter variable value: ")
    if input is not None:
        return input
    return None