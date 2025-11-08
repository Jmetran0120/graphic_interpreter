"""
Parser for the Drawing Interpreter
Parses tokens into command structures that can be executed
"""

from typing import List, Optional, Dict, Any
from lexer import Token, TokenType
from enum import Enum


class CommandType(Enum):
    """Types of commands that can be executed"""
    DRAW_LINE = "DRAW_LINE"
    DRAW_CIRCLE = "DRAW_CIRCLE"
    DRAW_RECTANGLE = "DRAW_RECTANGLE"
    SET_COLOR = "SET_COLOR"
    CLEAR = "CLEAR"
    MOVE = "MOVE"
    PEN_UP = "PEN_UP"
    PEN_DOWN = "PEN_DOWN"
    FILL = "FILL"


class Command:
    """Represents a parsed command ready for execution"""
    
    def __init__(self, command_type: CommandType, params: Dict[str, Any] = None):
        self.command_type = command_type
        self.params = params or {}
        self.line = 0
        self.col = 0
    
    def __repr__(self):
        return f"Command({self.command_type.name}, {self.params})"


class Parser:
    """Parser that converts tokens into command structures"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def error(self, message: str) -> Exception:
        """Create a parser error with position information"""
        if self.current_token:
            return Exception(f"Parse error at line {self.current_token.line}, column {self.current_token.col}: {message}")
        return Exception(f"Parse error: {message}")
    
    def advance(self):
        """Move to the next token"""
        self.pos += 1
        if self.pos >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.pos]
    
    def expect(self, token_type: TokenType, value: Optional[str] = None):
        """Expect a specific token type (and optionally value)"""
        if self.current_token is None:
            raise self.error(f"Unexpected end of input, expected {token_type.name}")
        if self.current_token.type != token_type:
            raise self.error(f"Expected {token_type.name}, got {self.current_token.type.name}")
        if value is not None and self.current_token.value.lower() != value.lower():
            raise self.error(f"Expected '{value}', got '{self.current_token.value}'")
        token = self.current_token
        self.advance()
        return token
    
    def parse_number(self) -> float:
        """Parse a number token"""
        token = self.expect(TokenType.NUMBER)
        try:
            return float(token.value)
        except ValueError:
            raise self.error(f"Invalid number: {token.value}")
    
    def parse_command(self) -> Command:
        """Parse a single command"""
        if self.current_token is None or self.current_token.type == TokenType.EOF:
            raise self.error("Unexpected end of input")
        
        # Store line/col for error reporting
        line = self.current_token.line
        col = self.current_token.col
        
        # Commands must start with a keyword
        if self.current_token.type != TokenType.KEYWORD:
            raise self.error(f"Expected command keyword, got {self.current_token.type.name}")
        
        keyword = self.current_token.value
        self.advance()
        
        # Route to appropriate parser based on command keyword
        if keyword == 'draw':
            return self.parse_draw_command(line, col)
        elif keyword == 'set':
            return self.parse_set_command(line, col)
        elif keyword == 'clear':
            return self.parse_clear_command(line, col)
        elif keyword == 'move':
            return self.parse_move_command(line, col)
        elif keyword == 'pen':
            return self.parse_pen_command(line, col)
        else:
            raise self.error(f"Unknown command: {keyword}")
    
    def parse_draw_command(self, line: int, col: int) -> Command:
        """Parse a draw command (draw line/circle/rectangle)"""
        if self.current_token is None or self.current_token.type != TokenType.KEYWORD:
            raise self.error("Expected shape type after 'draw'")
        
        shape_type = self.current_token.value
        self.advance()
        
        if shape_type == 'line':
            return self.parse_draw_line(line, col)
        elif shape_type == 'circle':
            return self.parse_draw_circle(line, col)
        elif shape_type == 'rectangle':
            return self.parse_draw_rectangle(line, col)
        else:
            raise self.error(f"Unknown shape type: {shape_type}")
    
    def parse_draw_line(self, line: int, col: int) -> Command:
        """Parse: draw line x1 y1 x2 y2"""
        params = {}
        
        # Parse four coordinate values (start point and end point)
        try:
            params['x1'] = self.parse_number()
            params['y1'] = self.parse_number()
            params['x2'] = self.parse_number()
            params['y2'] = self.parse_number()
        except Exception:
            raise self.error("draw line requires 4 numbers: x1 y1 x2 y2")
        
        cmd = Command(CommandType.DRAW_LINE, params)
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_draw_circle(self, line: int, col: int) -> Command:
        """Parse: draw circle x y radius"""
        params = {}
        
        # Parse center coordinates and radius
        try:
            params['x'] = self.parse_number()
            params['y'] = self.parse_number()
            params['radius'] = self.parse_number()
        except Exception:
            raise self.error("draw circle requires 3 numbers: x y radius")
        
        cmd = Command(CommandType.DRAW_CIRCLE, params)
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_draw_rectangle(self, line: int, col: int) -> Command:
        """Parse: draw rectangle x y width height"""
        params = {}
        
        # Parse top-left corner coordinates and dimensions
        try:
            params['x'] = self.parse_number()
            params['y'] = self.parse_number()
            params['width'] = self.parse_number()
            params['height'] = self.parse_number()
        except Exception:
            raise self.error("draw rectangle requires 4 numbers: x y width height")
        
        cmd = Command(CommandType.DRAW_RECTANGLE, params)
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_set_command(self, line: int, col: int) -> Command:
        """Parse: set color <color_name>"""
        # Verify 'color' keyword follows 'set'
        if self.current_token is None or self.current_token.value != 'color':
            raise self.error("Expected 'color' after 'set'")
        
        self.advance()
        
        # Accept either COLOR token or STRING token for color name
        if self.current_token is None or self.current_token.type not in (TokenType.COLOR, TokenType.STRING):
            raise self.error("Expected color name after 'set color'")
        
        color = self.current_token.value
        self.advance()
        
        cmd = Command(CommandType.SET_COLOR, {'color': color})
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_clear_command(self, line: int, col: int) -> Command:
        """Parse: clear"""
        cmd = Command(CommandType.CLEAR)
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_move_command(self, line: int, col: int) -> Command:
        """Parse: move x y"""
        params = {}
        
        # Parse destination coordinates
        try:
            params['x'] = self.parse_number()
            params['y'] = self.parse_number()
        except Exception:
            raise self.error("move requires 2 numbers: x y")
        
        cmd = Command(CommandType.MOVE, params)
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse_pen_command(self, line: int, col: int) -> Command:
        """Parse: pen up / pen down"""
        if self.current_token is None:
            raise self.error("Expected 'up' or 'down' after 'pen'")
        
        action = self.current_token.value
        self.advance()
        
        if action == 'up':
            cmd = Command(CommandType.PEN_UP)
        elif action == 'down':
            cmd = Command(CommandType.PEN_DOWN)
        else:
            raise self.error(f"Expected 'up' or 'down', got '{action}'")
        
        cmd.line = line
        cmd.col = col
        return cmd
    
    def parse(self) -> List[Command]:
        """Parse all tokens into a list of commands"""
        commands = []
        
        # Parse commands until end of input
        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            try:
                command = self.parse_command()
                commands.append(command)
            except Exception as e:
                # On error, stop parsing and propagate the error
                # (Could be extended with error recovery in the future)
                raise e
        
        return commands

