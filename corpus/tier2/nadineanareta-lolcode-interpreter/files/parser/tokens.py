# get current token by indexing/position
def current_token(self):
    if self.position < len(self.tokens):
        return self.tokens[self.position]
    return None

# count newlines and moves to next token
def count_newline(self):
    while self.current_token() and self.current_token().type == 'NEWLINE':
        self.numline+=1
        self.position+=1

# increments index
def next_pos(self):
    if self.current_token():
        print(f"Current line {self.numline}: Parsing {self.current_token().type} - {self.current_token().value}")
    self.position+=1
    self.count_newline()

# gets next token by moving to new position and returns token
def get_next_token(self):
    self.next_pos()
    return self.current_token()

def prev_pos(self):
    # print("jump back")
    self.position-=1
    self.sub_newline()

def sub_newline(self):
    while self.current_token() and self.current_token().type == 'NEWLINE':
        self.numline-=1
        self.position-=1