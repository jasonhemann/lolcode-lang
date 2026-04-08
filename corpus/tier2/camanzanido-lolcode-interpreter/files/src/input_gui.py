import tkinter as tk 
from tkinter import simpledialog


def ask_input(variable):
    value = simpledialog.askstring("Input", f"Enter value for {variable}:")
    return value  # Return the input value

