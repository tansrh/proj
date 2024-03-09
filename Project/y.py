import tkinter as tk
from tkinter import filedialog
import os

class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        #self.geometry("500x500")
        
        self.initialize_components()
        self.bind("<Configure>", self.resize_window)
        
        # Set minimum size
        self.minsize(500, 500)
        self.last_wid=500
        self.last_hgt=500
        
    def initialize_components(self):
        # Menu Bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        self.geometry("500x500")
        
        # Home Menu Button
        home_menu = tk.Menu(menu_bar, tearoff=0)
        home_menu.add_command(label="Home", command=self.show_home)
        menu_bar.add_cascade(label="Home", menu=home_menu)
        
        # History Menu Button
        history_menu = tk.Menu(menu_bar, tearoff=0)
        history_menu.add_command(label="History", command=self.show_history)
        menu_bar.add_cascade(label="History", menu=history_menu)
        
        # Recommendations Menu Button
        recommendations_menu = tk.Menu(menu_bar, tearoff=0)
        recommendations_menu.add_command(label="Recommendations", command=self.show_recommendations)
        menu_bar.add_cascade(label="Recommendations", menu=recommendations_menu)
        
        # Chat Frame
        self.chat_frame = tk.Frame(self)
        self.chat_frame.pack(pady=10)
        
        # Chat Display
        self.chat_display = tk.Text(self.chat_frame, height=20, width=60)
        self.chat_display.pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(self.chat_frame)
        input_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Input Label
        self.input_label = tk.Label(input_frame, text="Enter message:", font=("Helvetica", 12))
        self.input_label.pack(side=tk.LEFT)
        
        # Message Entry
        self.message_entry = tk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, ipadx=100, expand=True, fill=tk.BOTH)  # Adjusted width and height
        
        # Send Button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 0))
        
        self.show_home()
        
    def show_home(self):
        self.clear_chat_display()
        self.chat_display.insert(tk.END, "Welcome to the Home Page!\n")
    
    def show_history(self):
        file_path = "history.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            with open(file_path, 'w') as file:
                content = ""
        
        self.display_history(content)
    
    def show_recommendations(self):
        file_path = "recommendations.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            with open(file_path, 'w') as file:
                content = ""
        
        self.display_recommendations(content)
    
    def display_history(self, content):
        top = tk.Toplevel(self)
        top.title("History")
        text_widget = tk.Text(top)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def display_recommendations(self, content):
        top = tk.Toplevel(self)
        top.title("Recommendations")
        text_widget = tk.Text(top)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def clear_chat_display(self):
        self.chat_display.delete('1.0', tk.END)
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_display.insert(tk.END, f"User: {message}\n")
            self.message_entry.delete(0, tk.END)
    def resize_window(self, event):
        if(self.last_hgt!=event.height and self.last_wid!=event.width):
            self.geometry(f"{event.width}x{event.height}")
            self.last_hgt=event.height
            self.last_wid=event.width
            self.chat_frame.pack(pady=10)



        


if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
