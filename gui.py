import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
import threading

from scanner import Scanner
from parser import Parser
from visualizer import SyntaxTreeVisualizer

class TinyCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TINY Compiler")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        self.scanner = Scanner()
        self.parser = Parser()
        self.visualizer = SyntaxTreeVisualizer()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create a main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a frame for the top part (code input and buttons)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create a label for the code input
        code_label = ttk.Label(top_frame, text="TINY Code:")
        code_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Create buttons
        button_frame = ttk.Frame(top_frame)
        button_frame.grid(row=0, column=1, sticky=tk.E)
        
        load_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        load_button.pack(side=tk.LEFT, padx=5)
        
        compile_button = ttk.Button(button_frame, text="Compile", command=self.compile_code)
        compile_button.pack(side=tk.LEFT, padx=5)
        
        # Create a text area for code input
        self.code_text = scrolledtext.ScrolledText(main_frame, height=10)
        self.code_text.pack(fill=tk.X, pady=(0, 10))
        
        # Create a notebook for the output
        self.output_notebook = ttk.Notebook(main_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create a tab for tokens
        self.tokens_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.tokens_frame, text="Tokens")
        
        # Create a text area for tokens output
        self.tokens_text = scrolledtext.ScrolledText(self.tokens_frame)
        self.tokens_text.pack(fill=tk.BOTH, expand=True)
        
        # Create a tab for syntax tree
        self.tree_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.tree_frame, text="Syntax Tree")
        
        # Create a label for syntax tree status
        self.tree_status_var = tk.StringVar(value="No syntax tree generated yet.")
        self.tree_status = ttk.Label(self.tree_frame, textvariable=self.tree_status_var)
        self.tree_status.pack(pady=5)
        
        # Create a canvas for the syntax tree
        self.tree_canvas = tk.Canvas(self.tree_frame, bg="white")
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create a statusbar
        self.status_var = tk.StringVar(value="Ready")
        self.statusbar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_file(self):
        """
        Load a file containing TINY code.
        """
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            title="Open TINY Code File",
            filetypes=filetypes
        )
        
        if filename:
            try:
                with open(filename, "r") as file:
                    code = file.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, code)
                self.status_var.set(f"Loaded file: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                
    def compile_code(self):
        """
        Compile the TINY code: scan, parse, and visualize.
        """
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            messagebox.showwarning("Warning", "No code to compile.")
            return
        
        try:
            # Update status
            self.status_var.set("Scanning...")
            self.root.update_idletasks()
            
            # Scan the code
            tokens = self.scanner.scan(code)
            
            # Display tokens
            self.tokens_text.delete(1.0, tk.END)
            for i, (token_value, token_type) in enumerate(tokens):
                self.tokens_text.insert(tk.END, f"{i+1}. {token_value},{token_type}\n")
            
            # Update status
            self.status_var.set("Parsing...")
            self.root.update_idletasks()
            
            # Parse the code
            success, result = self.parser.parse(tokens)
            
            if success:
                # Update tree status
                self.tree_status_var.set("✅ Syntax is correct.")
                
                # Update status
                self.status_var.set("Generating syntax tree...")
                self.root.update_idletasks()
                
                # Visualize the syntax tree in a separate thread
                threading.Thread(target=self.visualize_tree, args=(result,)).start()
                
                # Switch to the syntax tree tab
                self.output_notebook.select(1)  # Index 1 is the syntax tree tab
                
                # Update status
                self.status_var.set("Compilation completed successfully.")
            else:
                # Update tree status
                self.tree_status_var.set(f"❌ Syntax error: {result}")
                
                # Update status
                self.status_var.set("Compilation failed: syntax error.")
                
                # Switch to the tokens tab
                self.output_notebook.select(0)  # Index 0 is the tokens tab
                
        except Exception as e:
            messagebox.showerror("Error", f"Compilation error: {e}")
            self.status_var.set(f"Compilation failed: {e}")
    
    def visualize_tree(self, tree):
        """
        Visualize the syntax tree and display it in the GUI.
        """
        try:
            # Generate a unique filename for the syntax tree image
            import time
            timestamp = int(time.time())
            output_file = f"syntax_tree_{timestamp}"
            
            # Visualize the tree
            output_path = self.visualizer.visualize(tree, output_file)
            
            # Load the image
            image = Image.open(output_path)
            
            # Resize image to fit the canvas if needed
            canvas_width = self.tree_canvas.winfo_width()
            canvas_height = self.tree_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Calculate the scaling factor to fit the image in the canvas
                img_width, img_height = image.size
                scale_width = canvas_width / img_width
                scale_height = canvas_height / img_height
                scale = min(scale_width, scale_height)
                
                if scale < 1:
                    new_width = int(img_width * scale)
                    new_height = int(img_height * scale)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.photo_image = ImageTk.PhotoImage(image)
            
            # Display the image
            self.tree_canvas.delete("all")
            self.tree_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            
            # Configure canvas scrolling if the image is larger than the canvas
            self.tree_canvas.config(scrollregion=self.tree_canvas.bbox(tk.ALL))
            
            # Update status
            self.status_var.set("Syntax tree visualization completed.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize syntax tree: {e}")
            self.status_var.set(f"Visualization failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TinyCompilerGUI(root)
    root.mainloop() 