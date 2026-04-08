using ICSharpCode.AvalonEdit.Highlighting;
using ICSharpCode.AvalonEdit.Highlighting.Xshd;
using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Xml;
using System.Text.RegularExpressions;
using System.Windows.Input;
namespace LOLSharp
{
    /// <summary>
    /// Interaction logic for MetroWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        /* Declare var, not war */
        DebugWindow DebugWin = new DebugWindow();
        Lexer Lexer = new Lexer();
        Tokenizer Tokenizer = new Tokenizer();
        Console Console = new Console();
        Interpreter Interpreter = new Interpreter();

        /* Property accessors for handling source files */
        public string CurrentDocumentPath { get; set; }
        public bool CurrentDocumentModified = false;
        private string currentDocumentTitle;
        public string CurrentDocumentTitle
        {
            get { return currentDocumentTitle; }
            set
            {
                currentDocumentTitle = value;
                if (CurrentDocumentModified)
                {
                    DocTitle.Text = currentDocumentTitle + " (Modified)";
                    saveFile.IsEnabled = true;
                }
                else { DocTitle.Text = currentDocumentTitle; }
                if (CurrentDocumentPath != "")
                {
                    DocTitle.Text += "- (" + CurrentDocumentPath + ")";
                }
            }
        }

        public MainWindow()
        {
            InitializeComponent();
        }

        #region Event Handlers
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {

            Lexer.DebugWin = DebugWin;
            Tokenizer.DebugWin = DebugWin;
            Tokenizer.ErrorList = Lexer.ErrorList;
            Interpreter.Console = Console;
            Interpreter.Tokenizer = Tokenizer;
            Interpreter.Lexer = Lexer;

            Interpreter.MainWindow = this;

            //Load LOLCODE syntax highlighting file
            using (Stream s = this.GetType().Assembly.GetManifestResourceStream("LOLSharp.LOL.xshd"))
            {
                using (XmlTextReader reader = new XmlTextReader(s))
                {
                    LOLinput.SyntaxHighlighting = HighlightingLoader.Load(reader, HighlightingManager.Instance);
                }
            }
            currentDocumentTitle = "Untitled.lol";
            CurrentDocumentPath = "";
            CurrentDocumentModified = false;
            CurrentDocumentTitle = "Untitled.lol";
            DocTitle.Text = currentDocumentTitle;
            this.Title = "LOLSharp";
            LOLinput.TextArea.Caret.PositionChanged += new EventHandler(updatePosBar);
            LOLinput.Document.TextChanged += new EventHandler(LOLinput_TextChanged);
            LOLinput.TextChanged += new EventHandler(LOLinput_TextChanged);

            DebugWin.ErrorTable.ItemsSource = Lexer.ErrorList;
            DebugWin.SymbolTable.ItemsSource = Lexer.StringConstTable;


        }
        private void newFile_Click(object sender, RoutedEventArgs e)
        {
            SafeSaveHandler();
            LOLinput.Text = "";
            LOLinput.Document.Text = "";
            LOLinput.Document.UndoStack.ClearAll();
            LOLinput.Document.UndoStack.ClearRedoStack();
            CurrentDocumentPath = "";
            CurrentDocumentTitle = "Untitled.lol";
            saveFile.IsEnabled = false;
            CurrentDocumentModified = false;
            DocTitle.Text = currentDocumentTitle;
            this.Title = "LOLSharp - " + DocTitle.Text;
        }
        private void startProg_Click(object sender, RoutedEventArgs e)
        {
            var x = Lexer.PreProccess(LOLinput.Text);
            ClearDebugWin();

            if (x == null && ErrorHelper.CountBreakingErrors(Lexer.ErrorList) > 0)
            {
                DebugWin.Print("Parsing Halted.");
                ShowErrors();
            }
            else
            {
                Tokenizer.Tokenize(x);
                Interpreter.StringTable = Lexer.StringConstTable;
                Interpreter.Run(Tokenizer.prog_asm.ToArray());
            }
            DebugWin.ErrorTable.ItemsSource = Lexer.ErrorList;
            DebugWin.SymbolTable.ItemsSource = Lexer.StringConstTable;
            DebugWin.TokenTable.ItemsSource = Lexer.StringConstTable;

        }
        private void openFile_Click(object sender, RoutedEventArgs e)
        {
            SafeSaveHandler();
            OpenFileDialog dialog = new OpenFileDialog();
            dialog.Filter = "LOLCODE Source files|*.lol|All files (*.*)|*.*";
            dialog.Title = "Select source file";
            if (dialog.ShowDialog() == true)
            {
                System.IO.StreamReader sr = new
                   System.IO.StreamReader(dialog.FileName);
                var lolstream = NormalizeEndings(sr.ReadToEnd());
                LOLinput.Document.UndoStack.ClearAll();
                LOLinput.Document.UndoStack.ClearRedoStack();
                LOLinput.Document.FileName = (dialog.FileName);
                LOLinput.Text = lolstream;
                CurrentDocumentModified = false;
                CurrentDocumentPath = Path.GetDirectoryName(dialog.FileName);
                CurrentDocumentTitle = dialog.SafeFileName;
                sr.Close();
            }
        }
        private void LOLinput_TextChanged(object sender, EventArgs e)
        {
            CurrentDocumentModified = true;
            CurrentDocumentTitle = CurrentDocumentTitle;
            updatePosBar(null, null);
        }
        private void Window_GotKeyboardFocus(object sender, KeyboardFocusChangedEventArgs e)
        {
            updatePosBar(null, null);
        }
        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            updatePosBar(null, null);
        }
        private void saveFile_Click(object sender, RoutedEventArgs e)
        {
            SafeSaveHandler(false);
        }
        private void redoText_Click(object sender, RoutedEventArgs e)
        {
            LOLinput.Redo();
        }
        private void undoText_Click(object sender, RoutedEventArgs e)
        {
            LOLinput.Undo();
        }
        private void debugWin_Click(object sender, RoutedEventArgs e)
        {
            ToggleDebugWin();
        }
        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            Application.Current.Shutdown();
        }
        #endregion
        #region Helper Functions
        /// <summary>
        /// Display the lexemes on the debugging window
        /// </summary>
        public void ShowLexemes()
        {
            DebugWin.Visibility = Visibility.Visible;
            DebugWin.DebugTab.SelectedIndex = 3;
        }
        /// <summary>
        /// Display the debugging window when there is errors
        /// </summary>
        public void ShowErrors()
        {
            DebugWin.Visibility = Visibility.Visible;
            DebugWin.DebugTab.SelectedIndex = 0;
        }
        /// <summary>
        /// Show/Hide the debugging window
        /// </summary>
        public void ToggleDebugWin()
        {
            if (DebugWin.Visibility == Visibility.Visible)
            {
                DebugWin.Visibility = Visibility.Collapsed;
            }
            else
            {
                DebugWin.Visibility = Visibility.Visible;
                DebugWin.Activate();
            }
        }

        /// <summary>
        /// Show/Hide the Console window
        /// </summary>
        public void ToggleConsole()
        {
            if (Console.Visibility == Visibility.Visible)
            {
                Console.Visibility = Visibility.Collapsed;
                
            }
            else
            {
                Console.Visibility = Visibility.Visible;
                debugWin.Visibility = Visibility.Visible;

                Console.Activate();
            }
        }
        /// <summary>
        /// Clear debugging window tables
        /// </summary>
        public void RefreshDebugWin()
        {
            if (DebugWin.IsVisible)
            {
                DebugWin.ErrorTable.ItemsSource = null;
                DebugWin.SymbolTable.ItemsSource = null;
                DebugWin.TokenTable.ItemsSource = null;
                DebugWin.ErrorTable.ItemsSource = Lexer.ErrorList;
                DebugWin.SymbolTable.ItemsSource = Lexer.StringConstTable;
                DebugWin.TokenTable.ItemsSource = Lexer.StringConstTable;
                DebugWin.debugtxt.Text = "";
            }

        }
        /// <summary>
        /// Clear debugging window tables
        /// </summary>
        public void ClearDebugWin()
        {
            DebugWin.ErrorTable.ItemsSource = null;
            DebugWin.SymbolTable.ItemsSource = null;
            DebugWin.TokenTable.ItemsSource = null;
            DebugWin.debugtxt.Text = "";
        }
        /// <summary>
        /// Safely save documents
        /// </summary>
        private void SafeSaveHandler(bool showdialog = true)
        {
            if (CurrentDocumentModified)
            {
                MessageBoxResult result;
                if (showdialog)
                {
                    result = MessageBox.Show("Do you want to save your changes?", CurrentDocumentTitle + " is unsaved.", MessageBoxButton.YesNo, MessageBoxImage.Question);
                }
                else
                {
                    result = MessageBoxResult.Yes;
                }
                if (result == MessageBoxResult.Yes)
                {
                    try
                    {
                        if (CurrentDocumentPath == "")
                        {
                            SaveFileDialog saveFileDialog1 = new SaveFileDialog();
                            saveFileDialog1.Filter = "LOLCODE Source files|*.lol|All files (*.*)|*.*";
                            saveFileDialog1.Title = "Save source file";
                            saveFileDialog1.ShowDialog();
                            if (saveFileDialog1.FileName == "")
                            {
                                return;
                            }
                            saveFile.IsEnabled = false;
                            CurrentDocumentTitle = saveFileDialog1.SafeFileName;
                            CurrentDocumentPath = Path.GetDirectoryName(saveFileDialog1.FileName);
                        }
                        File.WriteAllText(CurrentDocumentPath + "\\" + CurrentDocumentTitle, LOLinput.Text);
                        CurrentDocumentModified = false;
                        CurrentDocumentTitle = CurrentDocumentTitle;
                    }
                    catch
                    {
                        throw;
                    }
                }
            }
        }
        /// <summary>
        /// Standardize line endings to windows (CR LF) instead of linux (LF) only
        /// </summary>
        /// <param name="input">The raw text to process</param>
        /// <returns></returns>
        private string NormalizeEndings(string input)
        {
            if (Regex.IsMatch(input, "\r"))
            {
                return input;
            }
            else
            {
                return Regex.Replace(input, "\n", Environment.NewLine);
            }
        }
        /// <summary>
        /// Update Statusbars
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void updatePosBar(object sender, EventArgs e)
        {
            var x = LOLinput.TextArea.Caret.Position.Location;
            LineCount.Content = "LN " + x.Line.ToString();
            CharCount.Content = "CH " + x.Column.ToString();
            var isNumLockToggled = Keyboard.IsKeyToggled(Key.NumLock);
            var isCapsLockToggled = Keyboard.IsKeyToggled(Key.CapsLock);
            var isInsToggled = Keyboard.IsKeyToggled(Key.Insert);
            if (isNumLockToggled) { NumStat.Opacity = 1; } else { NumStat.Opacity = 0.2; }
            if (isCapsLockToggled) { CapStat.Opacity = 1; } else { CapStat.Opacity = 0.2; }
            if (isInsToggled) { InsStat.Opacity = 1; } else { InsStat.Opacity = 0.2; }
            CurrentDocumentTitle = CurrentDocumentTitle;
            redoText.IsEnabled = LOLinput.Document.UndoStack.CanRedo;
            undoText.IsEnabled = LOLinput.Document.UndoStack.CanUndo;
        }
        #endregion
        private void consoleWin_Click(object sender, RoutedEventArgs e)
        {
        }

        private void consoleWin_Click_1(object sender, RoutedEventArgs e)
        {
            ToggleConsole();
        }
    }
}
