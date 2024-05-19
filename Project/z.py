import tkinter as tk
from tkinter import filedialog
import os
from chat import get_response, bot_name

class ChatApplication(tk.Tk):

    
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.initialize_components()
        
        # Bind the Configure event to handle resizing
        #self.bind("<Configure>", self.resize_window)
        
    def initialize_components(self):
        self.geometry("500x500")
        
        # Menu Bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
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
        self.chat_frame.pack(expand=True, fill=tk.BOTH)
        
        # Chat Display
        self.chat_display = tk.Text(self.chat_frame, height=20, width=60, wrap=tk.WORD)
        #self.chat_display.config(state=tk.DISABLED)
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        
        
        scrollbar_y = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar_y.set)
        
        
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
        
        self.display_content("History", content)
    
    def show_recommendations(self):
        file_path = "recommendations.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            with open(file_path, 'w') as file:
                content = ""
        
        self.display_content("Recommendations", content)
    
    def display_content(self, title, content):
        top = tk.Toplevel(self)
        top.title(title)
        text_widget = tk.Text(top, wrap=tk.WORD)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        #text_widget = tk.Text(top, wrap=tk.WORD)  # Enable word wrapping
        
        scrollbar_x = tk.Scrollbar(top, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        
        # Add vertical scroll bar to text widget
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
            self.ret_val=get_response(message)
            self.msg=f"{bot_name}: {self.ret_val[0]}\n"
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
    
    def resize_window(self, event):
        self.geometry(f"{event.width}x{event.height}")

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
