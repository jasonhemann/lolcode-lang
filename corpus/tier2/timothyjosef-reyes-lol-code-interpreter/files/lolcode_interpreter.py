
import tkinter as tk
import lexical_analyzer as Lexer
# import semantic_analyzer as sematic
# import syntactic_analyzer as syntax
from syntactic_analyzer import Parser
from tkinter import messagebox
from tkinter import filedialog



#https://www.youtube.com/watch?v=ibf5cx221hk
class GUI:
    def __init__(self):
        self.root = tk.Tk()

        
        #menubar
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.filemenu, label="File")
        
        
        #menubar options        
        self.filemenu.add_command(label="Open File", command = self.load_file)
        self.filemenu.add_command(label="Close with Prompt", command = self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quick Close", command = exit)

       

        # add menubar to config??
        self.root.config(menu=self.menubar)


        self.label = tk.Label(self.root, text="LOLCode Interpreter", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        # file display/editor
        self.editor = tk.Text(self.root, height=5, font=('Arial', 16))
        self.editor.pack(padx=10, pady=10)

        self.root.geometry("500x500")
        self.root.title("Lolcode Interpreter")

    
        #events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # run gui
        self.root.mainloop()

    # get file
    def load_file(self):
        self.filepath = filedialog.askopenfilename(
            title="Select a LOLCode file",
            filetypes=[("LOLCODE files", "*.lol"),
                       ("All files", "*.*")]
        )

        if self.filepath:

            with open(self.filepath, "r") as file:
                content = file.read()
                # display conent to window
                self.editor.insert(1.0, content)
                

        pass


        
    # terminal display
    def execute_file(self):
        pass
        
        # tokens display

    def on_closing(self):
        if messagebox.askyesno(title="Close Program?", message="Do you really want to close the interpreter?"):
            self.root.destroy()
   
# runn
GUI()

        

        


