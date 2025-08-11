from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import sys
import subprocess  
import os

class LoginForm:
    def __init__(self):
        self.wn = Tk()
        self.wn.title("Login Form")
        self.wn.attributes("-fullscreen", True)  
        self.wn.configure(bg='#FFF8DC')

        # Variables
        self.Username_value = StringVar()
        self.Password_value = StringVar()
        self.password_visible = False  # 

        # ================ CANVAS =====================
        self.canvas = Canvas(self.wn)
        self.canvas.pack(fill=BOTH, expand=True)

        # Ensure window is updated before getting size
        self.wn.update_idletasks()
        screen_width = self.wn.winfo_screenwidth()
        screen_height = self.wn.winfo_screenheight()

        # Load background image dynamically, with error handling
        if os.path.exists("background.jpg"):
            self.background_img = Image.open("background.jpg")
            self.background_img = self.background_img.resize((screen_width, screen_height))
            self.background_img = ImageTk.PhotoImage(self.background_img)
            self.canvas.create_image(0, 0, image=self.background_img, anchor=NW)
        else:
            # If image not found, fill with color
            self.canvas.create_rectangle(0, 0, screen_width, screen_height, fill="#FFF8DC", outline="")

        # ================ LABELS AND ENTRIES =====================
        self.canvas.create_text(screen_width // 2, 150, text="Login", fill='black', font=('times', 60, 'bold'))
        
        self.canvas.create_text(screen_width // 2 - 150, 300, text="Username", fill='black', font=('times', 30, 'bold'))
        self.canvas.create_text(screen_width // 2 - 150, 400, text="Password", fill='black', font=('times', 30, 'bold'))

        # Username Entry
        self.Username = Entry(self.wn, font=('bell mt', 20, 'bold'), textvariable=self.Username_value)
        self.Username.place(x=screen_width // 2, y=285, width=300, height=40)

        # Password Entry
        self.Password_Show = Entry(self.wn, font=('bell mt', 20, 'bold'), textvariable=self.Password_value, show="*")
        self.Password_Show.place(x=screen_width // 2, y=385, width=300, height=40)

        # Show/Hide Password Button
        self.hide_show_btn = Button(self.wn, text="Show", font=('bell mt', 14, 'bold'), height=1, width=6,
                                    command=self.toggle_password, bd=0)
        self.hide_show_btn.place(x=screen_width // 2 + 320, y=385)

        # ================ BUTTONS =====================
        self.Exit = Button(self.wn, text="EXIT", font=('bell mt', 15, 'bold'), bd=5, bg='red', fg='white',
                           command=self.exit_application)
        self.Exit.place(x=20, y=20)

        self.Login = Button(self.wn, text='Log In', font=('bell mt', 20, 'bold'), height=1, width=10, command=self.login_button)
        self.Login.place(x=screen_width // 2 - 50, y=480)

        self.wn.mainloop()

    # ================ METHODS =====================
    def toggle_password(self):
        """ Toggle Password Visibility """
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.Password_Show.config(show="")
            self.hide_show_btn.config(text="Hide")
        else:
            self.Password_Show.config(show="*")
            self.hide_show_btn.config(text="Show")

    def exit_application(self):
        """ Exit Application Completely """
        ask = messagebox.askyesno('Exit', 'Do you want to exit?')
        if ask:
            self.wn.quit()
            self.wn.destroy()
            sys.exit(0) 

    def login_button(self):
        """ Check username & password in MySQL Database """
        username = self.Username_value.get()
        password = self.Password_value.get()

        if not username or not password:
            messagebox.showerror('Error', 'Please fill in all fields')
            return

        try:
            # Connecting to MySQL Database (XAMPP)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="user_database"  
            )
            cursor = conn.cursor()

            # Query to check user login
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                if username == "admin":
                    messagebox.showinfo("Login Success", "Welcome Admin!")
                    self.wn.destroy() 
                    subprocess.Popen(["python", "user_add.py"])  
                else:
                    messagebox.showinfo("Login Success", f"Welcome, {username}!")
                    self.wn.destroy()  
                    subprocess.Popen(["python", "encode_gui.py"])  
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")

LoginForm()
