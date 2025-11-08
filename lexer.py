"""
Lexical Analyzer (Tokenizer) for the Drawing Interpreter
Breaks input text into tokens for parsing
"""

import re
from enum import Enum
from typing import List, Tuple, Optional


class TokenType(Enum):
    """Types of tokens that can be recognized"""
    KEYWORD = "KEYWORD"
    NUMBER = "NUMBER"
    STRING = "STRING"
    COLOR = "COLOR"
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    COMMA = "COMMA"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


class Token:
    """Represents a single token with type and value"""
    
    def __init__(self, token_type: TokenType, value: str, line: int = 1, col: int = 0):
        self.type = token_type
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.col})"
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


class Lexer:
    """Lexical analyzer that tokenizes input text"""
    
    # Keywords supported by the interpreter
    KEYWORDS = {
        'draw', 'line', 'circle', 'rectangle', 'set', 'color', 'clear', 
        'move', 'to', 'from', 'pen', 'up', 'down', 'fill'
    }
    
    # Valid color names
    COLORS = {
        'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink',
        'black', 'white', 'gray', 'grey', 'brown', 'cyan', 'magenta'
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def error(self, message: str) -> Exception:
        """Create a lexer error with position information"""
        return Exception(f"Lexical error at line {self.line}, column {self.col}: {message}")
    
    def advance(self):
        """Move to the next character"""
        if self.current_char == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip comment lines (lines starting with #)"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()
    
    def read_number(self) -> str:
        """Read a number (integer or float)"""
        result = ''
        dot_count = 0  # Track decimal points to prevent multiple dots
        
        # Read digits and at most one decimal point
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:  # Stop if we encounter a second dot
                    break
            result += self.current_char
            self.advance()
        
        return result
    
    def read_string(self) -> str:
        """Read a string literal (enclosed in quotes)"""
        result = ''
        self.advance()  # Skip opening quote
        
        # Read characters until closing quote, handling escape sequences
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                # Handle escape sequences (\n, \t, etc.)
                self.advance()
                if self.current_char is None:
                    raise self.error("Unterminated string")
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                else:
                    result += self.current_char  # Include escaped character as-is
            else:
                result += self.current_char
            self.advance()
        
        if self.current_char is None:
            raise self.error("Unterminated string")
        
        self.advance()  # Skip closing quote
        return result
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self) -> Token:
        """Get the next token from the input"""
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Numbers (check for digit or decimal point followed by digit)
            if self.current_char.isdigit() or (self.current_char == '.' and self.pos + 1 < len(self.text) and self.text[self.pos + 1].isdigit()):
                col = self.col
                num_str = self.read_number()
                return Token(TokenType.NUMBER, num_str, self.line, col)
            
            # Strings
            if self.current_char == '"':
                col = self.col
                str_val = self.read_string()
                return Token(TokenType.STRING, str_val, self.line, col)
            
            # Identifiers and keywords (start with letter or underscore)
            if self.current_char.isalpha() or self.current_char == '_':
                col = self.col
                identifier = self.read_identifier()
                
                # Check if it's a reserved keyword first
                if identifier.lower() in self.KEYWORDS:
                    return Token(TokenType.KEYWORD, identifier.lower(), self.line, col)
                
                # Check if it's a recognized color name
                if identifier.lower() in self.COLORS:
                    return Token(TokenType.COLOR, identifier.lower(), self.line, col)
                
                # Fallback: treat as keyword (for unknown identifiers)
                return Token(TokenType.KEYWORD, identifier.lower(), self.line, col)
            
            # Special characters
            if self.current_char == '(':
                col = self.col
                char = self.current_char
                self.advance()
                return Token(TokenType.LPAREN, char, self.line, col)
            
            if self.current_char == ')':
                col = self.col
                char = self.current_char
                self.advance()
                return Token(TokenType.RPAREN, char, self.line, col)
            
            if self.current_char == ',':
                col = self.col
                char = self.current_char
                self.advance()
                return Token(TokenType.COMMA, char, self.line, col)
            
            # Unknown character
            col = self.col
            char = self.current_char
            self.advance()
            return Token(TokenType.UNKNOWN, char, self.line, col)
        
        # End of input
        return Token(TokenType.EOF, '', self.line, self.col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire input and return a list of tokens"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

