import tkinter as tk
from tkinter import messagebox
import os
import random
import string
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
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(50, 50))
        
        # Username Label and Entry
        username_label = tk.Label(self, text="Username:", bg="#f0f0f0")
        username_label.grid(row=1, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(self, bg="white", fg="black", relief=tk.FLAT)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Password Label and Entry
        password_label = tk.Label(self, text="Password:", bg="#f0f0f0")
        password_label.grid(row=2, column=0, padx=10, pady=5)

        self.password_entry = tk.Entry(self, bg="white", fg="black", show="*", relief=tk.FLAT)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Login Button
        login_button = tk.Button(self, text="Login", command=self.login, bg="#007BFF", fg="white", relief=tk.FLAT)
        login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Check if credentials file exists
        if not os.path.exists("credentials.txt"):
            # Signup Link
            signup_link = tk.Label(self, text="Don't have an account? Sign Up", fg="blue", cursor="hand2")
            signup_link.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
            signup_link.bind("<Button-1>", self.signup)
        else:
            # Forgot Password Link
            forgot_password_link = tk.Label(self, text="Forgot Password?", fg="blue", cursor="hand2")
            forgot_password_link.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
            forgot_password_link.bind("<Button-1>", self.forgot_password)

        # Centering the widgets
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Fetch username and password from credentials file
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            stored_username = lines[0].strip().split(": ")[1]
            stored_password = lines[1].strip().split(": ")[1]

        # Perform validation
        if username == stored_username and password == stored_password:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            self.destroy()  # Close the login window
            app = mic.ChatApplication()
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self, event):
        self.withdraw()  # Hide the login window
        signup_page = SignupPage(self)

    def forgot_password(self, event):
        self.withdraw()  # Hide the login window
        forgot_password_page = ForgotPasswordPage(self)

class SignupPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Signup Page")
        self.geometry("500x400")
        self.initialize_components()

    def initialize_components(self):
        # Create a label for the title
        title_label = tk.Label(self, text="Sign Up", font=("Arial", 20))
        title_label.pack(pady=(20, 10))

        # Username Label and Entry
        username_label = tk.Label(self, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(ipadx=20, ipady=5)

        # Password Label and Entry
        password_label = tk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=(0, 20), ipadx=20, ipady=5)

        # Signup Button
        signup_button = tk.Button(self, text="Sign Up", command=self.signup)
        signup_button.pack(ipadx=10, ipady=5)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Store the username and password in a file
        with open("credentials.txt", "w") as file:
            file.write(f"Username: {username}\nPassword: {password}")

        # Destroy the signup window
        app = mic.ChatApplication()
            
        app.mainloop()        
        self.destroy()

class ForgotPasswordPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Forgot Password")
        self.geometry("500x400")
        self.initialize_components()

    def initialize_components(self):
        # Create a label for the title
        title_label = tk.Label(self, text="Forgot Password?", font=("Arial", 20))
        title_label.pack(pady=(20, 10))

        # Username Label and Entry
        username_label = tk.Label(self, text="Enter your Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(ipadx=20, ipady=5)

        # Reset Password Button
        reset_button = tk.Button(self, text="Reset Password", command=self.reset_password)
        reset_button.pack(ipadx=10, ipady=5, pady=20)

    def reset_password(self):
        stored_username=""
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            stored_username = lines[0].strip().split(": ")[1]
        username = self.username_entry.get()

        # Generate a random password
        if(stored_username != username):
            messagebox.showinfo("Wrong Username", f"Please re-enter correct username.")
            return

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Update the password in the credentials file
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("Username:"):
                    if line.strip().split(": ")[1] == username:
                        lines[i+1] = f"Password: {new_password}\n"

        with open("credentials.txt", "w") as file:
            file.writelines(lines)

        # Notify the user about the new password
        messagebox.showinfo("Password Reset", f"New password generated: {new_password}. Please note your password for future purposes.")

        # Destroy the forgot password window
        self.destroy()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
