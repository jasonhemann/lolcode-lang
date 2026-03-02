import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog
import subprocess
import sys
import os
import threading
import re

class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")

        self.open_button = tk.Button(root, text="Open .lol File", command=self.open_file)
        self.open_button.pack(pady=10)

        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.output_area.pack(padx=10, pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("LOLCODE files", "*.lol")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("File Error", str(e))
            return

        # Extract GIMMEH vars
        gimmeh_vars = re.findall(r"\bGIMMEH\s+(\w+)", content)

        inputs = ""
        if gimmeh_vars:
            for var in gimmeh_vars:
                user_input = simpledialog.askstring("User Input", f"Enter value for `{var}`:")
                if user_input is None:
                    return  # User cancelled
                inputs += user_input + "\n"

        def run_code():
            if not os.path.exists("main.py"):
                messagebox.showerror("Error", "main.py not found in current folder.")
                return

            result = subprocess.run(
                [sys.executable, "main.py", file_path],
                input=inputs,
                capture_output=True,
                text=True
            )

            self.output_area.delete(1.0, tk.END)
            if result.stdout:
                self.output_area.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_area.insert(tk.END, "\n[stderr]\n" + result.stderr)

        threading.Thread(target=run_code).start()

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeGUI(root)
    root.mainloop()
