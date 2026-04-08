using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace safeprojectname
{
    public partial class Form2 : Form
    {
        private int row1;
        public Form2(int row)
        {
            InitializeComponent();
            row1 = row;
        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Return)
            {
                if (System.Windows.Forms.Application.OpenForms["Form1"] != null)
                {

                    (System.Windows.Forms.Application.OpenForms["Form1"] as Form1).table2.Rows[row1].Cells[2].Value = textBox1.Text;
                    (System.Windows.Forms.Application.OpenForms["Form1"] as Form1).table2.Rows[row1].Cells[1].Value = (System.Windows.Forms.Application.OpenForms["Form1"] as Form1).checkInput(textBox1.Text);
                   // (System.Windows.Forms.Application.OpenForms["Form1"] as Form1).output.AppendText(textBox1.Text);
                    (System.Windows.Forms.Application.OpenForms["Form1"] as Form1).symbolTable[(System.Windows.Forms.Application.OpenForms["Form1"] as Form1).table2.Rows[row1].Cells[0].Value.ToString()] = textBox1.Text;
                }
                this.Close();
            }
        }
    }
}
