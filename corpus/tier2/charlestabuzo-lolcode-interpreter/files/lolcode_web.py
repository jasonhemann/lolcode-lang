import streamlit as st
import sys
from lolcode_interpreter import Lexer, Parser, evaluate
import tempfile
import os

st.set_page_config(
    page_title="LOLCODE Interpreter",
    page_icon="🐱",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .output-area {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .step-header {
        color: #0066cc;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🐱 LOLCODE Interpreter")
st.markdown("""
Welcome to the LOLCODE Interpreter! You can either:
* Upload a .lol file
* Write LOLCODE directly in the text editor
""")

# Initialize session state for storing outputs and input values
if 'lexer_output' not in st.session_state:
    st.session_state.lexer_output = None
if 'parser_output' not in st.session_state:
    st.session_state.parser_output = None
if 'execution_output' not in st.session_state:
    st.session_state.execution_output = []
if 'input_values' not in st.session_state:
    st.session_state.input_values = []
if 'needs_input' not in st.session_state:
    st.session_state.needs_input = False
if 'current_code' not in st.session_state:
    st.session_state.current_code = None

# Create two columns for input methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload LOLCODE File")
    uploaded_file = st.file_uploader("Choose a .lol file", type=['lol'])

with col2:
    st.subheader("✏️ Write LOLCODE")
    default_code = """HAI
VISIBLE "HELLO WORLD!"
KTHXBYE"""
    manual_code = st.text_area(
        "Enter your LOLCODE here:", value=default_code, height=200)

# Get the code from either source
code = None
if uploaded_file is not None:
    code = uploaded_file.getvalue().decode()
elif manual_code:
    code = manual_code

# Store the current code in session state
if code:
    st.session_state.current_code = code

# Check if code contains GIMMEH and show input field if needed
if code and "GIMMEH" in code:
    st.subheader("📝 Program Input")
    user_input = st.text_input("Enter input value:", key="user_input")
    if user_input:
        st.session_state.input_values.append(user_input)

if code and st.button("▶️ Run Code"):
    try:
        # Clear previous outputs
        st.session_state.lexer_output = None
        st.session_state.parser_output = None
        st.session_state.execution_output = []

        # Step 1: Lexical Analysis
        st.markdown("### 🔍 Step 1: Lexical Analysis")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        st.session_state.lexer_output = tokens

        if tokens:
            st.success("Lexical analysis completed successfully!")
            with st.expander("View Tokens"):
                for token in tokens:
                    st.code(f"{token}")

        # Step 2: Parsing
        st.markdown("### 🔧 Step 2: Parsing")
        parser = Parser(tokens)
        ast = parser.parse()
        st.session_state.parser_output = ast
        st.success("Parsing completed successfully!")

        # Step 3: Execution
        st.markdown("### ⚡ Step 3: Execution")

        # Create a custom output capture class
        class OutputCapture:
            def __init__(self):
                self.outputs = []

            def write(self, text):
                self.outputs.append(text)

            def flush(self):
                pass        # Create a custom input provider class to handle input index

        class CustomInputProvider:
            def __init__(self, input_values):
                self.input_values = input_values
                self.input_idx = 0

            def get_input(self, prompt=""):
                if self.input_idx < len(self.input_values):
                    value = self.input_values[self.input_idx]
                    self.input_idx += 1
                    return value
                st.session_state.needs_input = True
                return ""

        input_provider = CustomInputProvider(st.session_state.input_values)

        def custom_input(prompt=""):
            return input_provider.get_input(prompt)        # Capture stdout and provide custom input
        output_capture = OutputCapture()
        old_stdout = sys.stdout
        old_input = input
        sys.stdout = output_capture
        
        # Replace built-in input function
        builtins = sys.modules['builtins']
        setattr(builtins, 'input', custom_input)

        # Execute the code
        env = {}
        evaluate(ast, env)

        # Restore stdout and input
        sys.stdout = old_stdout
        setattr(builtins, 'input', old_input)

        # Display the output
        st.markdown("#### Output:")
        with st.container():
            st.markdown('<div class="output-area">', unsafe_allow_html=True)
            for output in output_capture.outputs:
                st.write(output.strip())
            if st.session_state.input_values:
                st.write("YOU TYPED:", st.session_state.input_values[-1])
            st.markdown('</div>', unsafe_allow_html=True)

        # Display final environment
        with st.expander("View Variable Environment"):
            st.json(env)

        # Clear input values after successful execution
        st.session_state.input_values = []
        st.session_state.needs_input = False

    except Exception as err:
        st.error(f"Error: {str(err)}")

# Add helpful information
with st.expander("ℹ️ About LOLCODE"):
    st.markdown("""
    LOLCODE is an esoteric programming language inspired by lolspeak/kitty speak. Here are some basic examples:

    ```lolcode
    HAI                     BTW This is a comment
    I HAS A var ITZ 42      BTW Variable declaration
    VISIBLE var             BTW Print the variable
    GIMMEH var             BTW Get user input
    KTHXBYE                BTW End program
    ```

    For more information, check out the [LOLCODE specification](http://www.lolcode.org/).
    """)
