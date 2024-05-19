import tkinter as tk
import os
from tkinter import filedialog
from chat import get_response, bot_name
import pyttsx3

import tempfile

class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.initialize_components()
        
    def initialize_components(self):
        self.geometry("500x500")
        
        # Menu Bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # Home Menu Button
        home_menu = tk.Menu(self.menu_bar, tearoff=0)
        home_menu.add_command(label="Home", command=self.show_home)
        self.menu_bar.add_cascade(label="Home", menu=home_menu)
        
        # History Menu Button
        history_menu = tk.Menu(self.menu_bar, tearoff=0)
        history_menu.add_command(label="Show History", command=self.show_history)
        self.menu_bar.add_cascade(label="History", menu=history_menu)
        
        # Recommendations Menu Button
        recommendations_menu = tk.Menu(self.menu_bar, tearoff=0)
        recommendations_menu.add_command(label="Show Recommendations", command=self.show_recommendations)
        self.menu_bar.add_cascade(label="Recommendations", menu=recommendations_menu)
        
        
        # Voice Menu Button
        voice_menu = tk.Menu(self.menu_bar, tearoff=0)
        voice_menu.add_command(label="Read Content", command=self.read_content)
        self.menu_bar.add_cascade(label="Voice", menu=voice_menu)
        
        # Chat Frame
        self.chat_frame = tk.Frame(self)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)
        
        # Chat Display
        self.chat_display = tk.Text(self.chat_frame, width=60, wrap=tk.WORD)
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        
        scrollbar_y = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = tk.Scrollbar(self.chat_frame, orient=tk.HORIZONTAL, command=self.chat_display.xview)
        
        
        # Input Frame
        input_frame = tk.Frame(self.chat_frame)
        input_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Input Label
        self.input_label = tk.Label(input_frame, text="Input:", font=("Helvetica", 12))
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
        
        history_window = tk.Toplevel(self)
        history_window.title("History")
        
        text_widget = tk.Text(history_window, wrap=tk.WORD)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar_x = tk.Scrollbar(history_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y = tk.Scrollbar(history_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        
        # Add voice menu to the history window
        voice_menu = tk.Menu(history_window, tearoff=0)
        voice_menu.add_command(label="Read Content", command=lambda: self.read_content_window(content))
        history_window.config(menu=voice_menu)
        
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def show_recommendations(self):
        file_path = "recommendations.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            with open(file_path, 'w') as file:
                content = ""
        
        recommendations_window = tk.Toplevel(self)
        recommendations_window.title("Recommendations")
        
        text_widget = tk.Text(recommendations_window, wrap=tk.WORD)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar_x = tk.Scrollbar(recommendations_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y = tk.Scrollbar(recommendations_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        
        # Add voice menu to the recommendations window
        voice_menu = tk.Menu(recommendations_window, tearoff=0)
        voice_menu.add_command(label="Read Content", command=lambda: self.read_content_window(content))
        recommendations_window.config(menu=voice_menu)
        
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def display_content(self, title, content):
        top = tk.Toplevel(self)
        top.title(title)
        text_widget = tk.Text(top, wrap=tk.WORD)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        
        scrollbar_x = tk.Scrollbar(top, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y = tk.Scrollbar(top, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def clear_chat_display(self):
        self.chat_display.delete('1.0', tk.END)
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_display.insert(tk.END, f"User: {message}\n")
            self.ret_val = get_response(message)
            self.msg = f"{bot_name}: {self.ret_val[0]}\n"
            self.chat_display.insert(tk.END, f"{self.msg}\n")
            file_path = "history.txt"
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write(self.msg)
            else:
                with open(file_path, 'a') as file:
                    file.write(self.msg)
            file_path = "recommendations.txt"
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write(self.ret_val[1])
            else:
                with open(file_path, 'w') as file:
                    file.write(self.ret_val[1])

            self.message_entry.delete(0, tk.END)
    
    def read_content(self):
        content = self.chat_display.get('1.0', tk.END)
        self.speak_content(content)
    
    def read_content_window(self, content):
        self.speak_content(content)
    
    def speak_content(self, content):
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        engine.say(content)
        engine.runAndWait()
        
if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
