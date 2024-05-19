import tkinter as tk
import os
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from PIL import Image, ImageTk

class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.listening = False  # Variable to track if listening is active
        self.initialize_components()
        
    def initialize_components(self):
        self.geometry("600x500")
        
        # Menu Bar
        self.menu_bar = tk.Menu(self, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.config(menu=self.menu_bar)
        
        # Home Menu Button
        home_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Arial", 10))
        home_menu.add_command(label="Home", command=self.show_home)
        self.menu_bar.add_cascade(label="Home", menu=home_menu)
        
        # History Menu Button
        history_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Arial", 10))
        history_menu.add_command(label="Show History", command=self.show_history)
        self.menu_bar.add_cascade(label="History", menu=history_menu)
        
        # Recommendations Menu Button
        recommendations_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Arial", 10))
        recommendations_menu.add_command(label="Show Recommendations", command=self.show_recommendations)
        self.menu_bar.add_cascade(label="Recommendations", menu=recommendations_menu)
        
        # Voice Menu Button
        voice_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Arial", 10))
        voice_menu.add_command(label="Read Content", command=self.read_content)
        self.menu_bar.add_cascade(label="Voice", menu=voice_menu)
        
        # Chat Frame
        self.chat_frame = tk.Frame(self, bg="#F0F0F0")
        self.chat_frame.pack(expand=True, fill=tk.BOTH)
        
        # Chat Display
        self.chat_display = tk.Text(self.chat_frame, width=60, wrap=tk.WORD, bg="white", fg="black")
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        scrollbar_y = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar_y.set)
        
        # Input Frame
        input_frame = tk.Frame(self, bg="#F0F0F0")
        input_frame.pack(fill=tk.X)
        
        # Input Label
        self.input_label = tk.Label(input_frame, text="Input:", font=("Helvetica", 12), bg="#F0F0F0")
        self.input_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        
        # Message Entry
        self.message_entry = tk.Entry(input_frame, bg="white", fg="black")
        self.message_entry.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
        
        # Send Button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message, bg="#007BFF", fg="white")
        self.send_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        # Microphone Button
        self.microphone_img = Image.open("microphone.png")  # Path to your microphone image
        self.microphone_img = self.microphone_img.resize((20, 20), Image.LANCZOS)
        self.microphone_img = ImageTk.PhotoImage(self.microphone_img)
        self.microphone_button = tk.Button(input_frame, image=self.microphone_img, command=self.toggle_listen, bg="#007BFF", fg="white")
        self.microphone_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
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
        text_widget = tk.Text(top, wrap=tk.WORD, bg="white", fg="black")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        
        scrollbar_y = tk.Scrollbar(top, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = tk.Scrollbar(top, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def clear_chat_display(self):
        self.chat_display.delete('1.0', tk.END)
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_display.insert(tk.END, f"User: {message}\n")
            self.message_entry.delete(0, tk.END)
    
    def toggle_listen(self):
        if self.listening:
            self.listening = False
        else:
            self.listening = True
            self.listen_and_translate()
    
    def listen_and_translate(self):
        recognizer = sr.Recognizer()
        translator = Translator()
        
       
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=5)
            audio = recognizer.listen(source)
            
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            translation = translator.translate(text, src='auto', dest='en')
            self.message_entry.insert(tk.END, translation.text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error with the service; {0}".format(e))
        
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
