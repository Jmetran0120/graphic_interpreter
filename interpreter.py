"""
Main Drawing Interpreter with GUI
Provides a user interface for entering commands and viewing results
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lexer import Lexer, TokenType
from parser import Parser
from executor import DrawingExecutor


class DrawingInterpreter:
    """Main interpreter application with GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Interpreter")
        self.root.geometry("1200x700")
        
        # Canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = None
        self.executor = None
        
        # Setup GUI (canvas and executor will be created in setup_gui)
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Canvas column
        main_frame.columnconfigure(1, weight=1)  # Control panel column
        main_frame.rowconfigure(1, weight=1)     # Main content row
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Drawing Interpreter", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Left panel: Canvas
        canvas_frame = ttk.LabelFrame(main_frame, text="Drawing Canvas", padding="5")
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        
        # Create drawing canvas as child of canvas_frame
        self.canvas = tk.Canvas(
            canvas_frame, 
            width=self.canvas_width, 
            height=self.canvas_height, 
            bg='white',
            borderwidth=2,
            relief='solid',
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Set initial scrollregion to canvas size (allows scrolling if needed)
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        
        # Create executor instance after canvas is set up (executor needs canvas reference)
        self.executor = DrawingExecutor(self.canvas, self.canvas_width, self.canvas_height)
        
        # Right panel: Input and Output controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        control_frame.columnconfigure(0, weight=1)
        control_frame.rowconfigure(0, weight=2)  # Input area takes more space
        control_frame.rowconfigure(1, weight=1)  # Output area
        
        # Input area
        input_frame = ttk.LabelFrame(control_frame, text="Command Input", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=15, 
            width=40,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, pady=(5, 0))
        
        self.execute_button = ttk.Button(
            button_frame, 
            text="Execute", 
            command=self.execute_commands
        )
        self.execute_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(
            button_frame, 
            text="Clear Canvas", 
            command=self.clear_canvas
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_input_button = ttk.Button(
            button_frame, 
            text="Clear Input", 
            command=self.clear_input
        )
        self.clear_input_button.pack(side=tk.LEFT)
        
        # Output area
        output_frame = ttk.LabelFrame(control_frame, text="Output", padding="5")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            height=10, 
            width=40,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Help text at the bottom
        help_text = (
            "Commands: draw line x1 y1 x2 y2 | draw circle x y radius | "
            "draw rectangle x y width height | set color <color> | clear | move x y | pen up/down"
        )
        help_label = ttk.Label(
            main_frame, 
            text=help_text, 
            font=("Arial", 8),
            foreground="gray"
        )
        help_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Bind Ctrl+Enter to execute commands (allows multiline input)
        self.input_text.bind('<Control-Return>', lambda e: self.execute_commands())
        
        # Pre-populate input area with example commands
        self.load_example_commands()
    
    def load_example_commands(self):
        """Load example commands into the input area"""
        examples = """# Example Drawing Commands
# Set colors and draw shapes

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
"""
        self.input_text.insert('1.0', examples)
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas.delete("all")
        # Reset scrollregion after clearing
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        self.canvas.update_idletasks()
        self.append_output("Canvas cleared")
    
    def clear_input(self):
        """Clear the input text area"""
        self.input_text.delete('1.0', tk.END)
    
    def append_output(self, message: str):
        """Append a message to the output area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def execute_commands(self):
        """Execute commands from the input area"""
        # Get input text from text widget
        input_text = self.input_text.get('1.0', tk.END).strip()
        
        if not input_text:
            self.append_output("No commands to execute")
            return
        
        # Clear previous output messages
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        self.append_output("=" * 50)
        self.append_output("Executing commands...")
        self.append_output("=" * 50)
        
        try:
            # Step 1: Tokenize input text into tokens
            lexer = Lexer(input_text)
            tokens = lexer.tokenize()
            
            # Filter out EOF tokens (not needed for parsing)
            tokens = [t for t in tokens if t.type != TokenType.EOF]
            
            if not tokens:
                self.append_output("No valid tokens found")
                return
            
            # Step 2: Parse tokens into command structures
            parser = Parser(tokens)
            commands = parser.parse()
            
            self.append_output(f"Parsed {len(commands)} command(s)")
            self.append_output("-" * 50)
            
            # Step 3: Execute each command sequentially
            for i, command in enumerate(commands, 1):
                try:
                    result = self.executor.execute(command)
                    self.append_output(f"[{i}] {result}")
                except Exception as e:
                    error_msg = f"[{i}] Error: {str(e)}"
                    self.append_output(error_msg)
                    messagebox.showerror("Execution Error", error_msg)
            
            # Update canvas scrollregion to fit all drawn items (with padding)
            try:
                bbox = self.canvas.bbox("all")
                if bbox:
                    # Expand scrollregion to include all items with some padding
                    self.canvas.config(scrollregion=(bbox[0]-10, bbox[1]-10, bbox[2]+10, bbox[3]+10))
            except:
                pass
            # Force GUI update to display changes
            self.canvas.update_idletasks()
            self.root.update()
            
            self.append_output("=" * 50)
            self.append_output("Execution complete!")
            
        except Exception as e:
            # Handle errors during tokenization or parsing
            error_msg = f"Error: {str(e)}"
            self.append_output(error_msg)
            messagebox.showerror("Interpreter Error", error_msg)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DrawingInterpreter(root)
    root.mainloop()


if __name__ == "__main__":
    main()

