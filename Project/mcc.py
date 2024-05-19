import tkinter as tk
import os
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from PIL import Image, ImageTk
from chat import get_response, bot_name
import customtkinter as ctk
import threading
class ChatApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.initialize_components()
        self.reading_thread = None
        self.engine= None 
        
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
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)
        
        
        # Chat Display
        self.chat_display = ctk.CTkTextbox(self.chat_frame, width=60, wrap=tk.WORD, fg_color="#121212", text_color="white")
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
       
        
        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill=tk.X)
        
        # Input Label
        self.input_label = ctk.CTkLabel(input_frame, text="Input:", font=("Helvetica", 12, "bold"))
        self.input_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        
        # Message Entry
        self.message_entry = ctk.CTkEntry(input_frame)
        self.message_entry.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
        
        # Send Button
        self.send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        # Microphone Button
        self.microphone_img = Image.open("microphone.png")  # Path to your microphone image
        self.microphone_img = self.microphone_img.resize((20, 20), Image.LANCZOS)
        self.microphone_img = ImageTk.PhotoImage(self.microphone_img)
        self.microphone_button = tk.Button(input_frame, image=self.microphone_img, command=self.listen_and_translate)
        self.microphone_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        self.show_home()
        
    def show_home(self):
        self.clear_chat_display()
        self.chat_display.insert(tk.END, "Welcome to the Home Page!\n\n")
    
    def show_history(self):
        file_path = "history.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            with open(file_path, 'w') as file:
                content = ""
        
        history_window = ctk.CTkToplevel(self)
        history_window.title("History")
        history_window.geometry("600x500")
        
        text_widget = ctk.CTkTextbox(history_window, wrap=tk.WORD, fg_color="#121212", text_color="white")
        text_widget.insert(tk.END, content)
        text_widget.configure(state=tk.DISABLED)
        '''
        scrollbar_x = ctk.CTkScrollbar(history_window, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.configure(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y = ctk.CTkScrollbar(history_window,  command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar_y.set)
        '''
        # Add voice menu to the history window
        voice_menu = tk.Menu(history_window, tearoff=0)
        voice_menu.add_command(label="Read Content", command=lambda: self.read_content_window(content))
        voice_menu.add_command(label="Stop Reading", command=lambda: self.stop_speaking)
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
        
        recommendations_window = ctk.CTkToplevel(self)
        recommendations_window.title("Recommendations")
        recommendations_window.geometry("600x500")
        
        text_widget = ctk.CTkTextbox(recommendations_window, wrap=tk.WORD, fg_color="#121212", text_color="white")
        text_widget.insert(tk.END, content)
        text_widget.configure(state=tk.DISABLED)
        '''
        scrollbar_x = ctk.CTkScrollbar(recommendations_window,  command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.configure(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y = ctk.CTkScrollbar(recommendations_window,  command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar_y.set)
        '''
        # Add voice menu to the recommendations window
        voice_menu = tk.Menu(recommendations_window, tearoff=0)
        voice_menu.add_command(label="Read Content", command=lambda: self.read_content_window(content))
        voice_menu.add_command(label="Stop Reading", command=lambda: self.stop_speaking)
        recommendations_window.config(menu=voice_menu)

  
        
        text_widget.pack(expand=True, fill=tk.BOTH)
    
    def display_content(self, title, content):
        top = ctk.CTkToplevel(self)
        top.title(title)
        text_widget = ctk.CTkText(top, wrap=tk.WORD, bg_color="white", fg_color="black")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make text widget uneditable
        '''
        scrollbar_y = ctk.CTkScrollbar(top,  command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ctk.CTkScrollbar(top,  command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        '''
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
            self.msg=f"{self.ret_val[1]}\n"
            if not os.path.exists(file_path):
                
                with open(file_path, 'w') as file:
                    file.write(self.msg)
            else:
                with open(file_path, 'w') as file:
                    file.write(self.msg)

            self.message_entry.delete(0, tk.END)
    
    def listen_and_translate(self):
        
        recognizer = sr.Recognizer()
        translator = Translator()
        
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
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
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140)
        self.reading_thread = threading.Thread(target=self.speak_content, args=(content,))
        self.reading_thread.start()
        
    def read_content_window(self, content):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140)
        self.reading_thread = threading.Thread(target=self.speak_content, args=(content,))
        self.reading_thread.start()
        #self.speak_content(content)
    
    def speak_content(self, content):
        '''
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        '''
        self.engine.say(content)
        self.engine.runAndWait()
    def stop_speaking(self):
        self.reading_thread.join()
        self.engine.stop()

            
        
if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
