from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess  
import sys

class UserAdd:
    def __init__(self):
        self.wn = Tk()
        self.wn.title("Admin Panel - Add User")
        self.wn.geometry("500x400")  
        self.wn.configure(bg='#FFF8DC')

        # ========== Title ==========
        Label(self.wn, text="Admin Panel", font=("Arial", 20, "bold"), bg='#FFF8DC').pack(pady=20)

        # ========== Username Input ==========
        Label(self.wn, text="Username:", font=("Arial", 14), bg='#FFF8DC').pack(pady=5)
        self.username_entry = Entry(self.wn, font=("Arial", 14))
        self.username_entry.pack(pady=5, ipady=3, ipadx=50)  # Bigger input field

        # ========== Password Input ==========
        Label(self.wn, text="Password:", font=("Arial", 14), bg='#FFF8DC').pack(pady=5)
        self.password_entry = Entry(self.wn, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5, ipady=3, ipadx=50)  # Bigger input field

        # ========== Buttons ==========
        self.add_button = Button(self.wn, text="Add User", font=("Arial", 14, "bold"), bg="green", fg="white",
                                 command=self.add_user, width=15)
        self.add_button.pack(pady=10)

        self.exit_button = Button(self.wn, text="Exit", font=("Arial", 14), bg="red", fg="white",
                                  command=self.exit_application, width=15)
        self.exit_button.pack(pady=5)

        self.wn.mainloop()

    # ========== Methods ==========
    def add_user(self):
        """ Add new user to MySQL Database if username is unique """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            # Connect to MySQL (XAMPP)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="user_database"
            )
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already used! Choose a different one.")
                conn.close()
                return

            # Insert new user into database
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"User '{username}' added successfully!")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")

    def exit_application(self):
        """ Exit & Redirect Admin to HomePage.py """
        ask = messagebox.askyesno('Exit', 'Do you want to return to Home?')
        if ask:
            self.wn.destroy() 
            subprocess.Popen(["python", "HomePage.py"])  
            sys.exit(0) 

UserAdd()
