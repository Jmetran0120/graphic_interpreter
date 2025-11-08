"""
Executor for the Drawing Interpreter
Executes parsed commands and draws graphics on a canvas
"""

import tkinter as tk
from typing import Dict, Any, Optional
from parser import Command, CommandType


class DrawingExecutor:
    """Executes drawing commands on a tkinter canvas"""
    
    # Color mapping for tkinter
    COLOR_MAP = {
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        'yellow': '#FFFF00',
        'orange': '#FFA500',
        'purple': '#800080',
        'pink': '#FFC0CB',
        'black': '#000000',
        'white': '#FFFFFF',
        'gray': '#808080',
        'grey': '#808080',
        'brown': '#A52A2A',
        'cyan': '#00FFFF',
        'magenta': '#FF00FF',
    }
    
    def __init__(self, canvas: tk.Canvas, width: int = 800, height: int = 600):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.current_color = '#000000'  # Default: black
        self.pen_x = width // 2  # Start pen position at center of canvas
        self.pen_y = height // 2
        self.pen_down = True  # Pen starts down (drawing mode enabled)
        self.fill_mode = False  # Shapes are drawn as outlines by default
    
    def get_color(self, color_name: str) -> str:
        """Convert color name to hex color code"""
        color_lower = color_name.lower()
        return self.COLOR_MAP.get(color_lower, '#000000')
    
    def execute(self, command: Command) -> str:
        """Execute a single command and return result message"""
        try:
            if command.command_type == CommandType.DRAW_LINE:
                return self.execute_draw_line(command.params)
            elif command.command_type == CommandType.DRAW_CIRCLE:
                return self.execute_draw_circle(command.params)
            elif command.command_type == CommandType.DRAW_RECTANGLE:
                return self.execute_draw_rectangle(command.params)
            elif command.command_type == CommandType.SET_COLOR:
                return self.execute_set_color(command.params)
            elif command.command_type == CommandType.CLEAR:
                return self.execute_clear()
            elif command.command_type == CommandType.MOVE:
                return self.execute_move(command.params)
            elif command.command_type == CommandType.PEN_UP:
                return self.execute_pen_up()
            elif command.command_type == CommandType.PEN_DOWN:
                return self.execute_pen_down()
            else:
                return f"Error: Unknown command type: {command.command_type}"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def execute_draw_line(self, params: Dict[str, Any]) -> str:
        """Draw a line from (x1, y1) to (x2, y2)"""
        x1 = int(params.get('x1', 0))
        y1 = int(params.get('y1', 0))
        x2 = int(params.get('x2', 0))
        y2 = int(params.get('y2', 0))
        
        # Draw the line on canvas with current color
        self.canvas.create_line(x1, y1, x2, y2, fill=self.current_color, width=2)
        
        # Update pen position to end of line if pen is down
        if self.pen_down:
            self.pen_x = x2
            self.pen_y = y2
        
        return f"Drew line from ({x1}, {y1}) to ({x2}, {y2})"
    
    def execute_draw_circle(self, params: Dict[str, Any]) -> str:
        """Draw a circle at (x, y) with given radius"""
        x = int(params.get('x', 0))
        y = int(params.get('y', 0))
        radius = int(params.get('radius', 10))
        
        # Calculate bounding box coordinates for tkinter oval (requires bounding box, not center+radius)
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius
        
        # Draw the circle (filled or outlined based on fill_mode)
        if self.fill_mode:
            self.canvas.create_oval(x1, y1, x2, y2, outline=self.current_color, fill=self.current_color, width=2)
        else:
            self.canvas.create_oval(x1, y1, x2, y2, outline=self.current_color, fill='', width=2)
        
        # Update pen position to circle center
        if self.pen_down:
            self.pen_x = x
            self.pen_y = y
        
        return f"Drew circle at ({x}, {y}) with radius {radius}"
    
    def execute_draw_rectangle(self, params: Dict[str, Any]) -> str:
        """Draw a rectangle at (x, y) with given width and height"""
        x = int(params.get('x', 0))
        y = int(params.get('y', 0))
        width = int(params.get('width', 10))
        height = int(params.get('height', 10))
        
        # Calculate corner coordinates (x, y is top-left corner)
        x1 = x
        y1 = y
        x2 = x + width
        y2 = y + height
        
        # Draw the rectangle (filled or outlined based on fill_mode)
        if self.fill_mode:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.current_color, fill=self.current_color, width=2)
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.current_color, fill='', width=2)
        
        # Update pen position to bottom-right corner
        if self.pen_down:
            self.pen_x = x2
            self.pen_y = y2
        
        return f"Drew rectangle at ({x}, {y}) with size {width}x{height}"
    
    def execute_set_color(self, params: Dict[str, Any]) -> str:
        """Set the current drawing color"""
        color_name = params.get('color', 'black')
        self.current_color = self.get_color(color_name)
        return f"Color set to {color_name}"
    
    def execute_clear(self) -> str:
        """Clear the canvas"""
        self.canvas.delete("all")
        return "Canvas cleared"
    
    def execute_move(self, params: Dict[str, Any]) -> str:
        """Move the pen to a new position"""
        x = int(params.get('x', 0))
        y = int(params.get('y', 0))
        
        # If pen is down, draw a line from current position to new position
        if self.pen_down:
            self.canvas.create_line(self.pen_x, self.pen_y, x, y, fill=self.current_color, width=2)
        
        # Update pen position
        self.pen_x = x
        self.pen_y = y
        
        return f"Pen moved to ({x}, {y})"
    
    def execute_pen_up(self) -> str:
        """Lift the pen (stop drawing when moving)"""
        self.pen_down = False
        return "Pen lifted"
    
    def execute_pen_down(self) -> str:
        """Lower the pen (start drawing when moving)"""
        self.pen_down = True
        return "Pen lowered"

