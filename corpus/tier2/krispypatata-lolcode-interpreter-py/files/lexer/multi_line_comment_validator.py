import sys
import re

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# MULT-LINE VALIDATOR
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function to check if a certain word in a line is inside a string or not
def is_word_in_quotes(line, word):
    return bool(re.search(rf'"[^"]*\b{re.escape(word)}\b[^"]*"', line))

# Function to validate multiline comments in the input text.
# Ensures that:
# - 'OBTW' starts a block and is properly closed by 'TLDR' on a separate line.
# - 'TLDR' does not appear without a preceding 'OBTW'.
# - 'OBTW' and 'TLDR' do not coexist on the same line unless both are inside a string.
# - 'OBTW' is only preceded by whitespace/s, and 'TLDR' is only followed by whitespace/s.
def validate_multiline_comments(characters) :
    # print(characters) # For debugging

    inside_obtw = False                 # Flag to track if we're inside an OBTW block
    found_tldr_without_obtw = False     # Flag to track standalone TLDR

    # Traverse through the contents of the input
    for line_number, line in  enumerate(characters.splitlines(), 1):
        # Check if both OBTW and TLDR are on the same line
        # Raise an error if they are
        if re.search(r'\bOBTW\b', line) and re.search(r'\bTLDR\b', line):
            if not (is_word_in_quotes(line, 'OBTW') and is_word_in_quotes(line, 'TLDR')):
                sys.stderr.write(f"Error: 'OBTW' and 'TLDR' cannot coexist on the same line (line {line_number}).\n")
                sys.exit(1)

        # Validate the existence of the 'OBTW' keyword
        if re.search(r'\bOBTW\b', line):
            # Skip if 'OBTW' is inside a string
            if is_word_in_quotes(line, 'OBTW'):
                continue            

            # Skip if inside an OBTW block
            if inside_obtw:         
                continue

            # Skip if 'OBTW' is preceded by whitespace/s only
            if line.lstrip().startswith("OBTW"):
                inside_obtw = True  # Set flag to indicate we're inside an OBTW block
                continue            

            # Raise an error if 'OBTW' is preceded by anything other than whitespace/s
            sys.stderr.write(f"Error: 'OBTW' multiline comment keyword at line {line_number} can only be preceded by whitespace/s.\n")
            sys.exit(1)

        # Validate the existence of the 'TLDR' keyword
        if re.search(r'\bTLDR\b', line):
            # Skip if 'TLDR' is inside a string
            if is_word_in_quotes(line, 'TLDR') and not inside_obtw:
                continue
            
            # Skip if 'TLDR' is followed by whitespace/s only
            # But first check if it has a valid 'OBTW' pair
            if line.rstrip().endswith("TLDR"):
                if not inside_obtw:  # TLDR found without a preceding OBTW
                    found_tldr_without_obtw = True

                inside_obtw = False  # Reset the flag when exiting the block
                continue

            # Raise an error if 'OBTW' is followed by anything other than whitespace/s
            sys.stderr.write(f"Error: 'TLDR' multiline comment keyword at line {line_number} can only be followed by whitespace/s.\n")
            sys.exit(1)
    
    # Ensure that there's a closing TLDR if we left the block open
    if inside_obtw:
        sys.stderr.write(f"Error: Missing 'TLDR' to close the 'OBTW' block.\n")
        sys.exit(1)

    # Ensure that TLDR does not appear without a preceding OBTW
    if found_tldr_without_obtw:
        sys.stderr.write("Error: Found 'TLDR' without a preceding 'OBTW'.\n")
        sys.exit(1)
        