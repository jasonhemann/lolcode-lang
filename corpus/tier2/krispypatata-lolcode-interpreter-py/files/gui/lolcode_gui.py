import tkinter as tk
from tkinter import ttk # For tables
from tkinter import filedialog # For opening files
import os
import tkinter.font as tkfont
import sys

# Add the project root directory to Python path (to use globals.py when running just this gui)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import globals

# Declare important variables in which most functions will operate
root = None
lexemeTree = None
symbolTree = None
console = None

# GUI Color constants
_BACKGROUND = "#0d1117"
_SECONDARY_BACKGROUND = "#161b22"
_BORDER = "#30363d"
_TEXT = "#c9d1d9"
_TEXT_MUTED = "#8b949e"
_ACCENT = "#58a6ff"
# _DARK_ACCENT = "#112240"
_DARK_ACCENT = "#134C61"
_SELECT_ACCENT = "#134C61"
_GREEN = "#238636"
_RED = "#f85149"
_YELLOW = "#e3b341"
_PURPLE = "#a371f7"

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Class to create a code editor with line numbers, scrollbars, and context menu/right-click options
class CodeEditor(tk.Frame):
    def __init__(self, parent, root, **kwargs):
        super().__init__(parent)

        self.config(bg=_BACKGROUND)
        
        # Create line number text widget
        self.lineNumbers = tk.Text(self, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none', cursor='arrow', borderwidth=0, 
                                   highlightthickness=0, 
                                   background=_BACKGROUND, foreground=_TEXT,
                                   selectbackground=_BACKGROUND, selectforeground=_TEXT, inactiveselectbackground=_BACKGROUND,
                                )

        # Create main text widget
        self.textWidget = tk.Text(self, wrap='none', **kwargs, 
                                  background=_SECONDARY_BACKGROUND, foreground=_TEXT, insertbackground=_TEXT,
                                  selectbackground=_SELECT_ACCENT, selectforeground=_TEXT, inactiveselectbackground=_SELECT_ACCENT,
                                  padx=5, pady=5, borderwidth=0, highlightthickness=0,
                                )
        
        # Disable all interaction with the line numbers section
        # <Button-1> = clicking, <MouseWheel>   = scroll (Windows/macOS), <Button-4/5>   = scroll up/down (Linux)
        for event in ['<Button-1>', '<MouseWheel>', '<Button-4>', '<Button-5>']:
            self.lineNumbers.bind(event, lambda e: 'break')

        # Create divider
        self.divider_frame = tk.Frame(self, width=1, bg=_BORDER)
        self.divider_frame.grid_propagate(False)

        # Grid layout
        self.lineNumbers.grid(row=0, column=0, sticky='ns')
        self.divider_frame.grid(row=0, column=1, sticky='ns')
        self.textWidget.grid(row=0, column=2, sticky='nsew')
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create scrollbars
        self.verticalScrollbar = ttk.Scrollbar(self, orient='vertical')
        self.horizontalScrollbar = ttk.Scrollbar(self, orient='horizontal')

        # Initialize scrollbars
        self.verticalScrollbar.grid(row=0, column=3, sticky='ns')
        self.horizontalScrollbar.grid(row=1, column=2, sticky='ew')
        
        # Track last line count to avoid unnecessary updates when scrolling
        self.last_line_count = 1 

        # Configure scrollbar commands
        self.verticalScrollbar.config(command=self.on_scrollbar)
        self.horizontalScrollbar.config(command=self.textWidget.xview)
        self.textWidget.config(yscrollcommand=self.on_textscroll)
        self.textWidget.config(xscrollcommand=self.horizontalScrollbar.set)
        
        # Configure scrollbar styling using ttk.Style
        scrollbarStyle = ttk.Style()
        for component in ['Vertical.TScrollbar', 'Horizontal.TScrollbar']:
            scrollbarStyle.configure(component,
                background=_BORDER,
                troughcolor=_SECONDARY_BACKGROUND,
                bordercolor=_SECONDARY_BACKGROUND,
                darkcolor=_SECONDARY_BACKGROUND,
                lightcolor=_SECONDARY_BACKGROUND,
                arrowcolor=_TEXT_MUTED,
                gripcount=0,
                border = 0,
                relief='flat',
            )

            scrollbarStyle.map(component,
                background=[('active', _BORDER), ('pressed', _BORDER)],
                arrowcolor=[('active', _DARK_ACCENT), ('pressed', _DARK_ACCENT)],
            )

        # Bind events
        self.textWidget.bind('<Key>', self.on_content_changed)
        self.textWidget.bind('<Button-1>', self.on_left_click)
        self.textWidget.bind('<MouseWheel>', self.on_mousewheel)
        self.textWidget.bind('<Button-3>', self.show_context_menu)  # Right click
        
        # Bind left click to line numbers as well
        self.lineNumbers.bind('<Button-1>', self.on_left_click)
        
        # Keyboard shortcuts
        self.textWidget.bind('<Control-c>', self.copy_text)
        self.textWidget.bind('<Control-x>', self.cut_text)
        self.textWidget.bind('<Control-v>', self.paste_text)
        self.textWidget.bind('<Control-a>', self.select_all)
        
        # Initialize line numbers
        self.update_line_numbers()
        
        # Create context menu
        self.contextMenu = tk.Menu(self, tearoff=0, 
                                   bg=_SECONDARY_BACKGROUND, fg=_TEXT, activebackground=_DARK_ACCENT, activeforeground=_TEXT)
        self.contextMenu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.contextMenu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.contextMenu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Select All", command=self.select_all_menu, accelerator="Ctrl+A")

        # Bind mouse click outside the context menu (right click menu) to hide it (so it doesn't stay open)
        root.bind('<Button-1>', self.hide_context_menu)
    
    # Handle vertical scrollbar movement
    def on_scrollbar(self, *args):
        self.textWidget.yview(*args)
        self.lineNumbers.yview(*args)
    
    # Handle text widget scrolling
    def on_textscroll(self, *args):
        self.verticalScrollbar.set(*args)
        self.lineNumbers.yview_moveto(args[0])
    
    # Handle mouse wheel scrolling
    def on_mousewheel(self, event):
        self.lineNumbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    # Handle left click events
    def on_left_click(self, event=None):
        self.hide_context_menu()
        # self.after_idle(self.update_line_numbers)
    
    # Handle content changes
    def on_content_changed(self, event=None):
        self.after_idle(self.update_line_numbers)
    
    # Update line numbers display
    def update_line_numbers(self):
        # Get current number of lines in text widget
        current_line_count = int(self.textWidget.index(tk.END).split('.')[0])
        
        # Only update if the line count has actually changed
        if current_line_count != self.last_line_count:
            # Store the current scroll position of the main text widget
            current_scroll_position = self.textWidget.yview()
            
            self.lineNumbers.config(state='normal')
            self.lineNumbers.delete('1.0', tk.END)
            
            # Generate line numbers
            lineNumbersText = '\n'.join(str(i) for i in range(1, current_line_count))
            self.lineNumbers.insert('1.0', lineNumbersText)
            
            self.lineNumbers.config(state='disabled')
            
            # Restore the scroll position to match the main text widget
            self.lineNumbers.yview_moveto(current_scroll_position[0])
            
            # Update the tracked line count
            self.last_line_count = current_line_count

    # Show right-click context menu
    def show_context_menu(self, event):
        try:
            self.contextMenu.tk_popup(event.x_root, event.y_root)

        finally:
            self.contextMenu.grab_release()

    # Hide context menu
    def hide_context_menu(self, event=None):
        try:
            self.contextMenu.unpost()
        except:
            pass

        # Prevent context menu from appearing when clicking outside the code editor
        if event and event.widget not in (self.textWidget, self.lineNumbers):
            return
        return "break"
    
    # Copy selected text
    def copy_text(self, event=None):
        try:
            self.textWidget.event_generate("<<Copy>>")
        except tk.TclError:
            pass
        return "break"
    
    # Cut selected text
    def cut_text(self, event=None):
        try:
            self.textWidget.event_generate("<<Cut>>")
            self.update_line_numbers()
        except tk.TclError:
            pass
        return "break"
    
    # Paste text from clipboard
    def paste_text(self, event=None):
        try:
            self.textWidget.event_generate("<<Paste>>")
            self.update_line_numbers()
        except tk.TclError:
            pass
        return "break"
    
    # Select all text (keyboard shortcut)
    def select_all(self, event=None):
        self.textWidget.tag_add(tk.SEL, "1.0", tk.END)
        self.textWidget.mark_set(tk.INSERT, "1.0")
        self.textWidget.see(tk.INSERT)
        return "break"
    
    # Select all text (menu command)
    def select_all_menu(self):
        self.select_all()
    
    # Get text content
    def get(self, start, end=None):
        return self.textWidget.get(start, end)
    
    # Insert text
    def insert(self, index, text):
        self.textWidget.insert(index, text)
        self.update_line_numbers()
    
    # Delete text
    def delete(self, start, end=None):
        self.textWidget.delete(start, end)
        self.update_line_numbers()

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Class for tooltips for tables
# Functionality: If the text in a cell is longer than the column width, a tooltip will appear when hovering over the cell
class TreeviewTooltip:
    def __init__(self, treeview):
        self.treeview = treeview
        self.tooltip = None
        self.current_item = None
        self.current_column = None
        self.treeview.bind('<Motion>', self.on_motion)
        self.treeview.bind('<Leave>', self.hide_tooltip)
        
    def on_motion(self, event):
        # Get the item and column under the cursor
        item = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)
        
        # Check if we've moved to a different cell
        if item != self.current_item or column != self.current_column:
            # Hide current tooltip since we've moved to a different cell
            self.hide_tooltip()
            
            # Update current position
            self.current_item = item
            self.current_column = column
            
            if item and column:
                # Get column index (tkinter uses 1-based indexing for columns)
                columnIndex = int(column.replace('#', '')) - 1
                
                # Get the text in the cell
                values = self.treeview.item(item, 'values')
                if columnIndex < len(values):
                    text = str(values[columnIndex])
                    
                    # Get column width
                    col_name = self.treeview['columns'][columnIndex]
                    col_width = self.treeview.column(col_name, 'width')
                    
                    # Check if text is longer than what can fit in the column
                    # Use default font
                    font = tkfont.nametofont("TkDefaultFont")
                    text_width = font.measure(text)
                    
                    if text_width > col_width - 10:  # (-10) for padding
                        self.show_tooltip(event, text)
        elif self.tooltip:
            # We're in the same cell but cursor moved - update tooltip position
            self.update_tooltip_position(event)
    
    def show_tooltip(self, event, text):
        if self.tooltip:
            self.tooltip.destroy()
            
        # Create a tooltip window
        self.tooltip = tk.Toplevel(self.treeview)
        self.tooltip.wm_overrideredirect(True)
        
        # Initially place the tooltip window outside the screen (not visible to the users) - this is to fix flickering issues
        self.tooltip.wm_geometry(f"+{-1000}+{-1000}")
        
        self.tooltip.configure(bg='lightyellow', relief='solid', borderwidth=1)
        label = tk.Label(self.tooltip, text=text, bg='lightyellow', 
                         wraplength=300, justify='left', font=('TkDefaultFont', 10))
        label.pack(padx=2, pady=1)
        
        # Update the tooltip to get actual dimensions
        self.tooltip.update_idletasks()
        tooltip_height = self.tooltip.winfo_reqheight()
        
        # Calculate final position
        x_pos = event.x_root + 10
        y_pos = event.y_root - tooltip_height - 5  # offset above cursor
        
        # Move tooltip to final position
        self.tooltip.wm_geometry(f"+{x_pos}+{y_pos}")
        
        # Make tooltip visible
        self.tooltip.deiconify()
    
    # Update tooltip position to follow cursor within the same cell
    def update_tooltip_position(self, event):
        if self.tooltip:
            # Get tooltip dimensions
            tooltip_height = self.tooltip.winfo_reqheight()
            
            # Calculate new position
            x_pos = event.x_root + 10
            y_pos = event.y_root - tooltip_height - 5  # offset above cursor
            
            # Move tooltip to new position
            self.tooltip.wm_geometry(f"+{x_pos}+{y_pos}")
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        # Reset current position tracking
        self.current_item = None
        self.current_column = None


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Function to choose a file and load its content into the code editor
# Open a file dialog to choose a LOLCODE file and load its content into the code editor.
def choose_file(fileChooserButton, codeEditor):
    fileTypes = [
        ("LOLCODE files", "*.lol"),
        ("All files", "*.*"),
    ]
    filePath = filedialog.askopenfilename(
        title="Open file",
        filetypes=fileTypes,
        defaultextension=".lol"
    )
    if filePath:
        filename = os.path.basename(filePath)
        fileChooserButton.config(text=filename) 
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                content = f.read()
            codeEditor.textWidget.delete("1.0", tk.END)
            codeEditor.textWidget.insert("1.0", content)
            codeEditor.update_line_numbers()
        except Exception as e:
            print(f"Failed to open file: {e}")

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to update the contents of a table (tree) with new data
# Update the contents of a table (tree) with new data.
# Data are expected to be a list of tuples, where each tuple represents a row.
def update_table_contents(table, data):
    # Clear existing data
    for item in table.get_children():
        table.delete(item)
    
    # Insert new data
    for row in data:
        table.insert("", "end", values=row)

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function for popping up a window to get user input
def get_user_input():
    def clear_input():
        userInput.delete(0, tk.END)

    def submit_input():
        nonlocal result
        result = userInput.get()
        popup.destroy()

    result = None
    popup = tk.Toplevel(root)
    popup.configure(bg=_BACKGROUND)
    popup.title("User Input")
    popup.resizable(False, False)  # Prevent window resizing and maximizing
    popup.grab_set()  # Make popup modal

    tk.Label(popup, text="Enter something:", 
             bg=_BACKGROUND, fg=_TEXT).pack(pady=10)

    userInput = tk.Entry(popup, 
                        #  width=30  # Optional (to widen the entire popup window)'
                        bg=_SECONDARY_BACKGROUND, fg=_TEXT, insertbackground=_TEXT
                         )
    userInput.pack(padx=10, pady=5, fill="x")

    buttonFrame = tk.Frame(popup, bg=_BACKGROUND)
    buttonFrame.pack(pady=10)

    clearBtn = tk.Button(buttonFrame, text="Clear", command=clear_input,
                         bg=_SECONDARY_BACKGROUND, fg=_TEXT, activebackground=_ACCENT, activeforeground=_TEXT)
    clearBtn.pack(side="left", padx=10, ipadx=5, ipady=5)

    submitBtn = tk.Button(buttonFrame, text="Submit", command=submit_input,
                          bg=_SECONDARY_BACKGROUND, fg=_TEXT, activebackground=_ACCENT, activeforeground=_TEXT)
    submitBtn.pack(side="left", padx=10, ipadx=5, ipady=5)

    popup.wait_window()  # Wait until popup closes
    return result

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to run when the execute button is clicked
# Execute the code in the code editor and display the result in the console while also updating 
# the lexeme and symbol tables.
def execute_code(codeEditor, console, lexemeTree, symbolTree):
    # Get the code from the code editor
    code = codeEditor.get("1.0", "end-1c")  # Get all text, excluding the last newline character

    # Clear the console before executing new code
    console.config(state="normal")
    console.delete("1.0", "end")
    console.config(state="disabled")

    # Check if the code is empty
    if not code.strip():
        print("No code to execute.")
        return

    # Run the LOLCODE interpreter
    from lolcode import handle_run_lolcode
    handle_run_lolcode(code)

    update_table_contents(lexemeTree, globals.tokens)  # Update lexeme table with tokens
    update_table_contents(symbolTree, globals.symbol_table.symbols.items())  # Update symbol table with variables and functions

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to redirect everything printed in Python console to a custome console (text widget)
def redirect_python_output_to_custom_console(text_widget):
    class Redirect:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            
        def write(self, string):
            self.text_widget.config(state="normal")
            self.text_widget.insert(tk.END, string)
            self.text_widget.see(tk.END)
            self.text_widget.config(state="disabled")
            
        def flush(self): 
            pass

    sys.stdout = Redirect(text_widget)
    sys.stderr = Redirect(text_widget)

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to allow right-clicking in the console to copy selected text to clipboard
def right_click_to_copy_console_text(event, console):
    try:
        # Check if there's a selection
        if console.tag_ranges(tk.SEL):
            # Get selected text
            selected_text = console.get(tk.SEL_FIRST, tk.SEL_LAST)
            
            # Copy to clipboard (works on cross-platform)
            console.clipboard_clear()
            console.clipboard_append(selected_text)
            
            # Clear selection (works on cross-platform)
            console.tag_remove(tk.SEL, "1.0", tk.END)
            
            # On macOS, we need to update the clipboard immediately
            if sys.platform == 'darwin':
                console.update()
            
        # Prevent default right-click behavior
        return "break"
    except tk.TclError:
        return "break"

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to generate dummy data for gui
def generate_dummy_data(lexemeTree, symbolTree, console):
    sample_data = []
    for i in range(20):
        sample_data.append((f"lexLONGTEXTEXAMPLE{i}", f"Additional Parameter Variable{i%3}", i+1))
    
    update_table_contents(lexemeTree, sample_data)

    sample_data = []
    for i in range(20):
        sample_data.append((f"symbolsymbol{i}", f"value{i}"))

    update_table_contents(symbolTree, sample_data)

    sample_really_long_multi_line_text = (
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."  
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
    )
    print(sample_really_long_multi_line_text)
    
# ═══════════════════════════════════════════════════════════════════════════════════════════════════
# Main function to run the GUI (setups the GUI and starts the application)
def run_gui():
    root = tk.Tk()
    root.title("LOLCODE Interpreter")
    root.configure(bg=_BACKGROUND)

    MIN_WIDTH = 1280 # Preferrably divisible by 5
    MIN_HEIGHT = 720 
    TABLE_VIEWS_FIXED_WIDTH = (MIN_WIDTH * 2) // 4  # Fixed width for table views

    # Set minimum size
    root.minsize(MIN_WIDTH, MIN_HEIGHT)
    root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}") # Window size on launch

    # ───────────────────────────────────────────────────────────────────────────────────────────────
    # Create frames for different areas of the GUI and add them to the root (window)
    # Top and bottom views should equally occupy the available space, whereas the center view should have a fixed height
    topView = tk.Frame(root, 
                       bg=_BACKGROUND)
    centerView = tk.Frame(root, height=50, 
                          bg=_BACKGROUND) 
    bottomView = tk.Frame(root, 
                          bg=_BACKGROUND)

    root.grid_rowconfigure(0, weight=1)  # Top view
    root.grid_rowconfigure(1, weight=0)  # Center view
    root.grid_rowconfigure(2, weight=1)  # Bottom view
    root.grid_columnconfigure(0, weight=1)

    topView.grid(row=0, column=0, sticky="nsew")
    centerView.grid(row=1, column=0, sticky="ew")
    centerView.grid_propagate(False) 
    bottomView.grid(row=2, column=0, sticky="nsew")
    # ═══════════════════════════════════════════════════════════════════════════════════════════════
    # Top view
    topView.columnconfigure(0, weight=1)
    topView.columnconfigure(1, weight=0, minsize=TABLE_VIEWS_FIXED_WIDTH)
    topView.rowconfigure(0, weight=1)
    # ───────────────────────────────────────────────────────────────────────────────────────────────
    # Left side
    codeEditorView = tk.Frame(topView, 
                              bg=_BACKGROUND)
    codeEditorView.grid(row=0, column=0, sticky="nsew")

    # Grid configuration for the code editor view (top = file chooser, bottom = code editor)
    codeEditorView.columnconfigure(0, weight=1)
    codeEditorView.rowconfigure(0, weight=0)
    codeEditorView.rowconfigure(1, weight=1)

    # Bottom (code editor)
    codeEditor = CodeEditor(codeEditorView, root)
    codeEditor.grid(row=1, column=0, sticky="nsew")

    # Top (file chooser)
    # Wrap in a frame to for ce the button to have a fixed height
    fileChooserFrame = tk.Frame(codeEditorView, height=27, 
                                bg=_BACKGROUND)
    fileChooserFrame.grid(row=0, column=0, sticky="ew")
    fileChooserFrame.grid_propagate(False)  # Prevent resizing

    fileChooserButton = tk.Button(fileChooserFrame, text="Open LOLCODE file", 
                                  command=lambda: choose_file(fileChooserButton, codeEditor),
                                # command=get_user_input, # For testing purposes 
                                anchor="w",
                                bg=_BACKGROUND, fg=_TEXT, activebackground=_DARK_ACCENT, 
                                activeforeground=_TEXT, 
                                borderwidth=0, highlightthickness=0
                                )
    fileChooserButton.place(x=0, y=0, relwidth=1, relheight=1)

    # ───────────────────────────────────────────────────────────────────────────────────────────────
    # Right side
    tableViews = tk.Frame(topView, 
                          bg=_BACKGROUND)
    tableViews.grid(row=0, column=1, sticky="ns")

    tableViews.columnconfigure(0, weight=3)
    tableViews.columnconfigure(1, weight=2)
    tableViews.rowconfigure(0, weight=1)

    # -----------------------------------------------------------------------------------------------
    # Left side of the right side
    lexemeTableView = tk.Frame(tableViews, 
                               bg=_BACKGROUND)
    lexemeTableView.grid(row=0, column=0, sticky="nsew")

    lexemeTableLabel = tk.Label(lexemeTableView, text="Lexeme Table", 
                                bg=_BACKGROUND, fg=_TEXT)
    lexemeTableLabel.pack(fill="x")

    lexemeColumns = ("Lexeme", "Classification", "Line #")
    lexemeTree = ttk.Treeview(lexemeTableView, columns=lexemeColumns, show="headings", height=10)

    # Format column widths
    LEXEME_TABLE_WIDTH = (TABLE_VIEWS_FIXED_WIDTH * 3) // 5

    # First column
    lexemeTree.heading(lexemeColumns[0], text=lexemeColumns[0])
    lexemeTree.column(lexemeColumns[0], width=int(LEXEME_TABLE_WIDTH * 2 / 5), anchor="w")

    # Second column
    lexemeTree.heading(lexemeColumns[1], text=lexemeColumns[1])
    lexemeTree.column(lexemeColumns[1], width=int(LEXEME_TABLE_WIDTH * 2 / 5), anchor="w")

    # Third column
    lexemeTree.heading(lexemeColumns[2], text=lexemeColumns[2])
    lexemeTree.column(lexemeColumns[2], width=int(LEXEME_TABLE_WIDTH * 1 / 5), anchor="center")

    lexemeScrollbar = ttk.Scrollbar(lexemeTableView, orient="vertical", command=lexemeTree.yview)
    lexemeTree.configure(yscrollcommand=lexemeScrollbar.set)

    lexemeTree.pack(side="left", fill="both", expand=True)
    lexemeScrollbar.pack(side="right", fill="y")

    # Add tooltip functionality to the lexeme table
    lexemeTooltip = TreeviewTooltip(lexemeTree)

    # -----------------------------------------------------------------------------------------------
    # Right side of the right side
    symbolTableView = tk.Frame(tableViews, 
                               bg=_BACKGROUND)
    symbolTableView.grid(row=0, column=1, sticky="nsew")

    symbolTableLabel = tk.Label(symbolTableView, text="Symbol Table",
                                bg=_BACKGROUND, fg=_TEXT)
    symbolTableLabel.pack(fill="x")

    symbolColumns = ("Symbol", "Value")
    symbolTree = ttk.Treeview(symbolTableView, columns=symbolColumns, show="headings", height=10)

    # Format column widths
    SYMBOL_TABLE_WIDTH = (TABLE_VIEWS_FIXED_WIDTH * 2) // 5

    # First column
    symbolTree.heading(symbolColumns[0], text=symbolColumns[0])
    symbolTree.column(symbolColumns[0], width=int(SYMBOL_TABLE_WIDTH / 2), anchor="w")

    # Second column
    symbolTree.heading(symbolColumns[1], text=symbolColumns[1])
    symbolTree.column(symbolColumns[1], width=int(SYMBOL_TABLE_WIDTH / 2), anchor="w")

    symbolScrollbar = ttk.Scrollbar(symbolTableView, orient="vertical", command=symbolTree.yview)
    symbolTree.configure(yscrollcommand=symbolScrollbar.set)

    symbolTree.pack(side="left", fill="both", expand=True)
    symbolScrollbar.pack(side="right", fill="y")

    # Add tooltip functionality to the symbol table
    symbolTooltip = TreeviewTooltip(symbolTree)

    # -----------------------------------------------------------------------------------------------
    # Configure styling for the tables
    tableStyle = ttk.Style()

    tableStyle.configure('Treeview',
        background=_SECONDARY_BACKGROUND,
        foreground=_TEXT,
        fieldbackground=_SECONDARY_BACKGROUND,
        selectbackground=_SELECT_ACCENT,
        selectforeground=_TEXT,
        borderwidth=0
    )

    tableStyle.configure('Treeview.Heading',
        background=_BACKGROUND,
        foreground=_TEXT,
        relief='flat',
        borderwidth=1,
    )

    tableStyle.map('Treeview',
        background=[('selected', _SELECT_ACCENT)], 
        foreground=[('selected', _TEXT)],
    )

    tableStyle.map('Treeview.Heading',
        background=[('active', _SELECT_ACCENT), ('pressed', _SELECT_ACCENT)],
        foreground=[('active', _TEXT), ('pressed', _TEXT)],
    )

    # ═══════════════════════════════════════════════════════════════════════════════════════════════
    # Center view
    executeButton = tk.Button(centerView, text="EXECUTE LOLCODE", 
                              bg=_BACKGROUND, fg=_TEXT, activebackground=_DARK_ACCENT, activeforeground=_TEXT,
                              border=0, highlightthickness=0,
                              font=("TkDefaultFont", 12),
                              command=lambda: execute_code(codeEditor, console, lexemeTree, symbolTree))
    executeButton.pack(fill = "both", expand=True, 
                       padx=0, pady=0)

    # ═══════════════════════════════════════════════════════════════════════════════════════════════
    # Bottom view
    # This is the console area where output will be displayed
    console = tk.Text(bottomView, state="disabled", wrap="word", 
                    bg=_SECONDARY_BACKGROUND, fg=_TEXT, insertbackground=_TEXT,
                    selectbackground=_SELECT_ACCENT, selectforeground=_TEXT,
                    inactiveselectbackground=_SELECT_ACCENT,
                    font=("Courier New", 15),  
                    padx=10, pady=10, cursor="arrow",
                    borderwidth=0, 
                    highlightthickness=0, 
                    #   spacing1=0,  # Space above each line
                    #   spacing2=0,  # Space between wrapped lines
                    spacing3=0  # Space after last line
        )
    console.pack(fill="both", expand=True)    

    # Allows copying of text from the console by right-clicking selected text
    console.bind("<Button-3>", lambda event: right_click_to_copy_console_text(event, console))

    # ───────────────────────────────────────────────────────────────────────────────────────────────
    # Make sure to redirect Python's standard output to the custom console
    redirect_python_output_to_custom_console(console)

    # Make sure to update the flag for no GUI mode
    globals.no_gui = False
    # ───────────────────────────────────────────────────────────────────────────────────────────────
    # generate_dummy_data(lexemeTree, symbolTree, console) # For testing purposes

    root.mainloop()

# ═══════════════════════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_gui()
