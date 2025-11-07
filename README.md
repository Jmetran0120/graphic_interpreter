# Drawing Interpreter

A simple graphics/drawing interpreter system built in Python that accepts user-defined commands, performs lexical analysis, parses commands, and executes them to draw graphics on a canvas.

## Features

- **Lexical Analysis (Tokenization)**: Breaks down input commands into tokens
- **Parsing**: Parses tokens according to defined grammar rules
- **Execution**: Executes commands and draws graphics on a canvas
- **Error Handling**: Gracefully handles invalid inputs with descriptive error messages
- **GUI Interface**: User-friendly graphical interface with input/output areas

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Installation

No additional installation required! Just make sure you have Python 3.6+ installed. The interpreter uses tkinter which comes standard with Python.

## Usage

### Running the Interpreter

```bash
python interpreter.py
```

### Command Syntax

The interpreter supports the following commands:

#### Drawing Commands

1. **Draw Line**
   ```
   draw line x1 y1 x2 y2
   ```
   Draws a line from point (x1, y1) to point (x2, y2)
   
   Example: `draw line 100 100 500 300`

2. **Draw Circle**
   ```
   draw circle x y radius
   ```
   Draws a circle centered at (x, y) with the specified radius
   
   Example: `draw circle 400 300 50`

3. **Draw Rectangle**
   ```
   draw rectangle x y width height
   ```
   Draws a rectangle with top-left corner at (x, y) with specified width and height
   
   Example: `draw rectangle 300 200 100 80`

#### Color Commands

4. **Set Color**
   ```
   set color <color_name>
   ```
   Sets the drawing color. Available colors: red, green, blue, yellow, orange, purple, pink, black, white, gray, brown, cyan, magenta
   
   Example: `set color blue`

#### Canvas Commands

5. **Clear Canvas**
   ```
   clear
   ```
   Clears the entire canvas

6. **Move Pen**
   ```
   move x y
   ```
   Moves the pen to position (x, y). If pen is down, draws a line to the new position.
   
   Example: `move 200 200`

#### Pen Control Commands

7. **Pen Up**
   ```
   pen up
   ```
   Lifts the pen (stops drawing when moving)

8. **Pen Down**
   ```
   pen down
   ```
   Lowers the pen (starts drawing when moving)

### Example Script

```python
# Example Drawing Script
set color blue
draw circle 400 300 50

set color red
draw rectangle 300 200 100 80

set color green
draw line 100 100 700 500

set color purple
draw circle 200 150 30

set color orange
draw rectangle 500 400 150 100
```

### Comments

You can add comments to your commands using `#`:

```
# This is a comment
set color red
draw line 0 0 100 100  # Draw a diagonal line
```

## Project Structure

```
.
├── lexer.py          # Lexical analyzer (tokenizer)
├── parser.py         # Parser for command syntax
├── executor.py       # Command executor for drawing
├── interpreter.py    # Main GUI application
└── README.md         # This file
```

## How It Works

1. **Lexical Analysis (lexer.py)**: 
   - Breaks input text into tokens (keywords, numbers, colors, etc.)
   - Handles whitespace, comments, and special characters
   - Identifies keywords, numbers, colors, and identifiers

2. **Parsing (parser.py)**:
   - Takes tokens and builds command structures
   - Validates command syntax
   - Creates Command objects with parameters

3. **Execution (executor.py)**:
   - Executes parsed commands
   - Draws graphics on the tkinter canvas
   - Manages drawing state (color, pen position, etc.)

4. **GUI (interpreter.py)**:
   - Provides input area for commands
   - Displays output and error messages
   - Shows the drawing canvas with results

## Error Handling

The interpreter provides detailed error messages for:

- **Lexical Errors**: Invalid characters or token structure
- **Parse Errors**: Invalid command syntax or missing parameters
- **Execution Errors**: Invalid parameters or drawing errors

Errors are displayed in the output area and via error dialogs, preventing the interpreter from crashing.

## Limitations

- Canvas size is fixed at 800x600 pixels
- Only supports outlined shapes (no fill mode currently)
- Limited set of predefined colors
- Coordinates must be within canvas bounds for best results

## Future Enhancements

Possible improvements:
- Support for variables and loops
- More drawing primitives (polygons, curves, etc.)
- Save/load drawing scripts
- Undo/redo functionality
- Zoom and pan capabilities

## License

This project is created for educational purposes as part of a Programming Language Principles project.

