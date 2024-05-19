import tkinter as tk

class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.geometry("500x500")
        
        self.initialize_components()
        
    def initialize_components(self):
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
        self.chat_frame.pack(pady=10)
        
        # Chat Display
        self.chat_display = tk.Text(self.chat_frame, height=20, width=60)
        self.chat_display.pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(self.chat_frame, height=20)
        input_frame.pack(pady=5, padx=5,  fill=tk.BOTH)
        
        
        
        # Message Entry
        self.message_entry = tk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, ipadx=100, expand=True, fill=tk.BOTH)  # Adjusted width horizontally
        
        # Send Button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 0))
        
        self.show_home()
        
    def show_home(self):
        self.clear_chat_display()
        self.chat_display.insert(tk.END, "Welcome to the Home Page!\n")
    
    def show_history(self):
        self.clear_chat_display()
        self.chat_display.insert(tk.END, "History will be displayed here.\n")
    
    def show_recommendations(self):
        self.clear_chat_display()
        self.chat_display.insert(tk.END, "Recommendations will be displayed here.\n")
    
    def clear_chat_display(self):
        self.chat_display.delete('1.0', tk.END)
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_display.insert(tk.END, f"User: {message}\n")
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
