class Error:
    def __init__(self, line_number):
        self.line_number = line_number
        self.error_message = ""

    # if HAI and KTHXBYE are not where they're supposed to be
    def _program_delimiter_mismatch(self, delimiter):
        if delimiter.value == "HAI":
            self.error_message = "Expecting HAI at the start of the program."
        elif delimiter.value == "KTHXBYE":
            self.error_message = "Expecting KTHXBYE at the end of the program."
        return self

    # if the wrong word got used at a specific index
    def _word_mismatch(self, correct_word, wrong_word):
        if correct_word.value in ("UPPIN", "NERFIN"):
            self.error_message = f"Expecting 'UPPIN' or 'NERFIN, got '{wrong_word.value}'."
        elif correct_word.value in ("TIL", "WILE"):
            self.error_message = f"Expecting 'TIL' or 'WILE, got '{wrong_word.value}'."
        else:
            self.error_message = f"Expecting '{correct_word.value}', got '{wrong_word.value}'."
        return self

    # if there's an unknown variable present in the line
    def _invalid_variable(self, unknown):
        self.error_message = f"Invalid variable '{unknown.value}'."
        return self

    # if the opening and closing tags do not match
    def _tag_mismatch(self, tag):
        if tag.type == "closing statement" or tag.value in ("TLDR", "KTHXBYE"):
            self.error_message = f"{tag.value} expecting an opening statement."
        else:
            self.error_message = f"{tag.value} expecting a closing statement."
        return self

    # if there's too many operands than the expected number
    def _operand_count_mismatch(self, operation):
        self.error_message = f"{operation.value} has invalid number of operands."
        return self

    # if there are declarations made outside of their scope
    def _declared_outside(self, operation):
        self.error_message = f"{operation.value} declared outside of respective block."
        return self
    
    # if there is no existing IT value for comparison
    def _nothing_to_compare(self, operation):
        self.error_message = f"No expression to compare for {operation.value}."
        return self
    
    # if the loop labels don't match
    def _label_mismatch(self, correct_label, wrong_label):
        self.error_message = (f"Expecting label '{correct_label}', got label '{wrong_label}'.")
        return self
    
    # if using an undeclared variable
    def _var_undeclared(self, variable):
        self.error_message = f"'{variable.value}' not declared."


    def __repr__(self):
        return f"Line {self.line_number}: {self.error_message}"