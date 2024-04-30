import tkinter as tk
from tkinter import messagebox
import mic 
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")
        self.initialize_components()
        
    def initialize_components(self):
        # Create a label for the title
        title_label = tk.Label(self, text="Welcome to HealthBot", font=("Arial", 20), bg="#f0f0f0")
        title_label.pack(pady=(20, 10))
        
        # Username Label and Entry
        username_label = tk.Label(self, text="Username:", bg="#f0f0f0")
        username_label.pack(pady=(10, 0))
        
        self.username_entry = tk.Entry(self, bg="white", fg="black", relief=tk.FLAT)
        self.username_entry.pack(pady=(0, 10), ipadx=20, ipady=5)
        
        # Password Label and Entry
        password_label = tk.Label(self, text="Password:", bg="#f0f0f0")
        password_label.pack()
        
        self.password_entry = tk.Entry(self, bg="white", fg="black", show="*", relief=tk.FLAT)
        self.password_entry.pack(pady=(0, 20), ipadx=20, ipady=5)
        
        # Login Button
        login_button = tk.Button(self, text="Login", command=self.login, bg="#007BFF", fg="white", relief=tk.FLAT)
        login_button.pack(ipadx=10, ipady=5)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Perform validation, here you can add your authentication logic
        if username == "admin" and password != "admin":
            messagebox.showinfo("Login Unuccessful", "Please Retry!")
        else:
            self.destroy()
                
            app = mic.ChatApplication()
            
            app.mainloop()
            

        
if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
