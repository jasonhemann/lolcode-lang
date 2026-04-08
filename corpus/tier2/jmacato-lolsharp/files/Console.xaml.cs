using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace LOLSharp
{
    /// <summary>
    /// Interaction logic for Console.xaml
    /// </summary>
    public partial class Console : Window
    {

        public string inputbuffer = "";
        public int freezePoint = 0;

        public bool awaitinput = false;

        public Console()
        {
            InitializeComponent();
        }

        public void Clear()
        {
            this.Dispatcher.Invoke(() => Out.Clear());
        }

        public void Write(string s)
        {
            this.Dispatcher.Invoke(() => {
                Out.AppendText(s);
                Out.CaretIndex = Out.Text.Length;
            });
        }

        public void WriteLine(string s)
        {
            this.Dispatcher.Invoke(() => {
                Out.AppendText(s + "\n");
                Out.CaretIndex = Out.Text.Length;
            });
        }

        public void StartIn()
        {
            awaitinput = true;
            this.Dispatcher.Invoke(() => {
                Out.CaretBrush = new SolidColorBrush(Colors.White);
                Out.CaretIndex = Out.Text.Length;
                freezePoint = Out.Text.Length;
            });
        }

        /// <summary>
        /// Read and clear the input buffer
        /// </summary>
        /// <returns>User input</returns>
        public string ReadBuffer()
        {
            freezePoint = 0;
            this.Dispatcher.Invoke(() => {
                Out.CaretBrush = new SolidColorBrush(Colors.Transparent);
                Out.CaretIndex = Out.Text.Length;
            });
            var x = inputbuffer;
            inputbuffer = "";
            return x;
        }

        /// <summary>
        /// Emulate a terminal
        /// </summary>
        private void Window_PreviewKeyUp(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (awaitinput)
            {
                if (e.Key == Key.Enter)
                {
                    awaitinput = false;
                    Out.Text += "\r\n";
                    return;
                } else if (e.Key == Key.Back){
                    if(inputbuffer.Length > 0)
                    {
                        inputbuffer= inputbuffer.Substring(0, inputbuffer.Length - 1);
                        Out.Text= Out.Text.Substring(0, Out.Text.Length - 1);
                    }
                    else
                    {
                        Out.CaretIndex = freezePoint;
                    }
                }
                else {
                    inputbuffer += GetCharFromKey(e.Key);
                    Out.Text += GetCharFromKey(e.Key);
                }

            }
            e.Handled = true;

            Out.CaretIndex = Out.Text.Length;
        }

        private void Out_Loaded(object sender, RoutedEventArgs e)
        {
            this.Dispatcher.Invoke(() => Out.CaretBrush = new SolidColorBrush(Colors.Transparent));
        }

        public bool HaltExec = false;


        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (!HaltExec) { HaltExec = true;}

            this.Visibility = Visibility.Collapsed;
            e.Cancel = true;
        }

        #region Key Translation
        public enum MapType : uint
        {
            MAPVK_VK_TO_VSC = 0x0,
            MAPVK_VSC_TO_VK = 0x1,
            MAPVK_VK_TO_CHAR = 0x2,
            MAPVK_VSC_TO_VK_EX = 0x3,
        }

        [DllImport("user32.dll")]
        public static extern int ToUnicode(
            uint wVirtKey,
            uint wScanCode,
            byte[] lpKeyState,
            [Out, MarshalAs(UnmanagedType.LPWStr, SizeParamIndex = 4)]
            StringBuilder pwszBuff,
            int cchBuff,
            uint wFlags);

        [DllImport("user32.dll")]
        public static extern bool GetKeyboardState(byte[] lpKeyState);

        [DllImport("user32.dll")]
        public static extern uint MapVirtualKey(uint uCode, MapType uMapType);

        public static char GetCharFromKey(Key key)
        {
            char ch = ' ';

            int virtualKey = KeyInterop.VirtualKeyFromKey(key);
            byte[] keyboardState = new byte[256];
            GetKeyboardState(keyboardState);

            uint scanCode = MapVirtualKey((uint)virtualKey, MapType.MAPVK_VK_TO_VSC);
            StringBuilder stringBuilder = new StringBuilder(2);

            int result = ToUnicode((uint)virtualKey, scanCode, keyboardState, stringBuilder, stringBuilder.Capacity, 0);
            switch (result)
            {
                case -1:
                    break;
                case 0:
                    break;
                case 1:
                    {
                        ch = stringBuilder[0];
                        break;
                    }
                default:
                    {
                        ch = stringBuilder[0];
                        break;
                    }
            }
            return ch;
        }
        #endregion



    }
}
