import re

# Ordered by precedence
LOLCODE_TOKENS = [
	# 1. IGNORE TOKENS (Comments and Whitespace)
	('SKIP',         r'[ \t\r]+'),         # Skip spaces, tabs, carriage returns
	('NEWLINE',      r'\n'),               # Newline (important for single-line comments/statement termination)
	('BTW_COMMENT',  r'BTW.*'),            # Single-line comment (BTW followed by anything)
	('OBTW',         r'OBTW'),             # Block comment start
	('TLDR',         r'TLDR'),             # Block comment end

	# 2. KEYWORDS (Exact Matches - Highest Precedence)
	# Match multi-word keywords first
	('I_HAS_A',      r'I\s+HAS\s+A'),
	('SUM_OF',       r'SUM\s+OF'),
	('DIFF_OF',      r'DIFF\s+OF'),
	('PRODUKT_OF',   r'PRODUKT\s+OF'),
	('QUOSHUNT_OF',  r'QUOSHUNT\s+OF'),
	('MOD_OF',       r'MOD\s+OF'),
	('BIGGR_OF',     r'BIGGR\s+OF'),
	('SMALLR_OF',    r'SMALLR\s+OF'),
	('BOTH_OF',      r'BOTH\s+OF'),
	('EITHER_OF',    r'EITHER\s+OF'),
	('WON_OF',       r'WON\s+OF'),
	('ANY_OF',       r'ANY\s+OF'),
	('ALL_OF',       r'ALL\s+OF'),
	('BOTH_SAEM',    r'BOTH\s+SAEM'),
	('IS_NOW_A',     r'IS\s+NOW\s+A'),
	('O_RLY',        r'O\s+RLY\?'),
	('YA_RLY',       r'YA\s+RLY'),
	('NO_WAI',       r'NO\s+WAI'),
	('IM_IN_YR',     r'IM\s+IN\s+YR'),
	('IM_OUTTA_YR',  r'IM\s+OUTTA\s+YR'),
	('HOW_IZ_I',     r'HOW\s+IZ\s+I'),
	('IF_U_SAY_SO',  r'IF\s+U\s+SAY\s+SO'),
	('FOUND_YR',     r'FOUND\s+YR'),
	('I_IZ',         r'I\s+IZ'),

	# Match single-word keywords
	('HAI',          r'HAI'),
	('KTHXBYE',      r'KTHXBYE'),
	('WAZZUP',       r'WAZZUP'),
	('BUHBYE',       r'BUHBYE'),
	('ITZ',          r'ITZ'),
	('R',            r'R'),
	('NOT',          r'NOT'),
	('DIFFRINT',     r'DIFFRINT'),
	('SMOOSH',       r'SMOOSH'),
	('MAEK',         r'MAEK'),
	('AN',           r'AN'),
	('A',            r'A'),
	('PLUS',         r'\+'),
	('VISIBLE',      r'VISIBLE'),
	('GIMMEH',       r'GIMMEH'),
	('OIC',          r'OIC'),
	('WTF',          r'WTF\?'),
	('OMGWTF',       r'OMGWTF'),
	('OMG',          r'OMG'),
	('UPPIN',        r'UPPIN'),
	('NERFIN',       r'NERFIN'),
	('YR',           r'YR'),
	('TIL',          r'TIL'),
	('WILE',         r'WILE'),
	('GTFO',         r'GTFO'),
	('MEBBE',        r'MEBBE'),
	('MKAY',         r'MKAY'),

	# 3. LITERALS (Values)
	# NUMBAR must be before NUMBR to match the decimal point first
	# The '“.*”' regex for YARN is simplified; a full lexer would handle escaped quotes
	('YARN_LITERAL', r'(".*?"|“.*?”)'),
	('NUMBAR_LITERAL', r'-?[0-9]+\.[0-9]+'),
	('NUMBR_LITERAL', r'-?[0-9]+'),
	('TROOF_LITERAL', r'WIN|FAIL'),
	('TYPE_LITERAL', r'NOOB|NUMBR|NUMBAR|YARN|TROOF'),

	# 4. IDENTIFIERS (User-Defined Names - Lowest Precedence)
	# It covers Variable, Function, and Loop identifiers
	('IDENTIFIER',   r'[A-Za-z][A-Za-z0-9_]*'),

	# 5. ERROR (Catch-all for invalid characters)
	('ERROR',        r'.'),
]

def lolcode_lexer(code):
	"""
	Tokenizes the input LOLCODE string based on the defined specifications.

	Args:
		code (str): The raw LOLCODE source code.

	Yields:
		tuple: (token_type, token_value) for each recognized token.
	"""
	position = 0
	code_length = len(code)

	# 1. Pre-compile all regular expressions for efficiency
	token_patterns = [(token_type, re.compile(pattern)) for token_type, pattern in LOLCODE_TOKENS]

	while position < code_length:
		match_found = False

		# 2. Iterate through patterns in ORDER OF PRECEDENCE
		for token_type, pattern in token_patterns:
			# Try to match the pattern starting from the current position
			match = pattern.match(code, position)

			if match:
				value = match.group(0) # Get the matched string

				# 3. Handle 'SKIP' tokens
				if token_type in ('SKIP'):
					# These tokens are consumed but not yielded to the parser
					pass

				# 4. Handle Block Comments
				elif token_type == 'OBTW':
					# Find the corresponding 'TLDR' end marker
					end_match = re.search(r'TLDR', code[position:])
					if end_match:
						# Consume the OBTW, the comment body, and TLDR
						position += end_match.end()
					else:
						# Error: Unclosed block comment
						raise SyntaxError(f"Unclosed OBTW block starting at position {position}")
					# Don't yield comment content

				# 5. Handle Single-Line Comments
				elif token_type == 'BTW_COMMENT':
					# Consume the comment and ignore it
					pass

				# 6. Yield all other meaningful tokens (Keywords, Literals, Identifiers)
				elif token_type != 'ERROR':
					yield (token_type, value)

				# Move the position past the consumed token
				position = match.end()
				match_found = True
				break # IMPORTANT: Exit the inner loop after a match is found

		# 7. Handle Unmatched Input (Error)
		if not match_found:
			# If no pattern matched, it's an unrecognized character/sequence
			char = code[position]
			raise SyntaxError(f"Illegal character '{char}' at position {position}")
			# position += 1 # Or continue/exit based on error strategy

	# Optional: Yield an End-of-File token (EOF)
	yield ('EOF', None)