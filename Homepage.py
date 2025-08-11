from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import cv2
import threading
import numpy as np
import random
import sys
import subprocess

class DashBoard:
    def __init__(self):
        self.wn = Tk()
        self.wn.title("Image Steganography")
        self.wn.state("zoomed")
        self.wn.configure(bg='#FFF8DC')

        # Variables
        self.image_display_size = (400, 400)
        self.path_image = None
        self.decode_path_image = None

        # Create Menu Bar
        self.create_menu()

        # Layout Frames
        self.Frame = Frame(self.wn, bg='black', width=1200, height=600)
        self.Frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        self.EncryptionFrame = Frame(self.Frame, bg='white', width=600, height=600)
        self.EncryptionFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        self.DecryptionFrame = Frame(self.Frame, bg='white', width=600, height=600)
        self.DecryptionFrame.pack(side=RIGHT, expand=True, fill=BOTH, padx=5, pady=5)

        self.create_encryption_widgets()
        self.create_decryption_widgets()

        self.wn.mainloop()

    def create_menu(self):
        menubar = Menu(self.wn)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear", command=self.clear_dashboard)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.wn.config(menu=menubar)

    def create_encryption_widgets(self):
        Label(self.EncryptionFrame, text='Encode', font=('arial', 20, 'bold'), bg='white').pack(pady=10)

        self.Encode_Photo_Frame = LabelFrame(self.EncryptionFrame, text="Selected Image", bg='white', width=400, height=400)
        self.Encode_Photo_Frame.pack(pady=10)

        Button(self.EncryptionFrame, text="Select Image", command=self.select_image).pack(pady=5)

        Label(self.EncryptionFrame, text="Message to Encode:", bg='white').pack(pady=5)
        self.ent_encode_msg = Text(self.EncryptionFrame, width=60, height=5)
        self.ent_encode_msg.pack(pady=5)

        Label(self.EncryptionFrame, text="Encryption Key:", bg='white').pack(pady=5)
        self.ent_encode_key = Entry(self.EncryptionFrame, width=30)
        self.ent_encode_key.pack(pady=5)

        Button(self.EncryptionFrame, text="Encode", command=self.encrypt_data_into_image).pack(pady=5)

    def create_decryption_widgets(self):
        Label(self.DecryptionFrame, text='Decode', font=('arial', 20, 'bold'), bg='white').pack(pady=10)

        self.Decode_Photo_Frame = LabelFrame(self.DecryptionFrame, text="Selected Stego Image", bg='white', width=400, height=400)
        self.Decode_Photo_Frame.pack(pady=10)

        Button(self.DecryptionFrame, text="Select Stego Image", command=self.select_stego_image).pack(pady=5)

        Label(self.DecryptionFrame, text="Decryption Key:", bg='white').pack(pady=5)
        self.ent_decode_key = Entry(self.DecryptionFrame, width=30)
        self.ent_decode_key.pack(pady=5)

        Button(self.DecryptionFrame, text="Decode", command=lambda: threading.Thread(target=self.decrypt).start()).pack(pady=5)

        self.lbl_decrypted_message = Label(self.DecryptionFrame, text="Decrypted Message: ", bg='white', wraplength=500)
        self.lbl_decrypted_message.pack(pady=5)

    def select_image(self):
        self.path_image = filedialog.askopenfilename()
        if self.path_image:
            self.display_image(self.path_image, self.Encode_Photo_Frame)

    def select_stego_image(self):
        self.decode_path_image = filedialog.askopenfilename()
        if self.decode_path_image:
            self.display_image(self.decode_path_image, self.Decode_Photo_Frame)

    def display_image(self, image_path, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            img = Image.open(image_path)
            img.thumbnail(self.image_display_size)
            render = ImageTk.PhotoImage(img)
            img_label = Label(frame, image=render, bg='white')
            img_label.image = render
            img_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image: {e}")

    def encrypt_data_into_image(self):
        if not self.path_image:
            messagebox.showerror("Error", "Please select an image to encode.")
            return

        key = self.ent_encode_key.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Numeric encryption key required.")
            return

        key = int(key)

        try:
            img = cv2.imread(self.path_image)
            if img is None:
                messagebox.showerror("Error", "Unable to read image. Please select a valid image file.")
                return
            message = self.ent_encode_msg.get("1.0", "end-1c") + "#####"
            # Encode message as UTF-8 bytes
            message_bytes = message.encode('utf-8')
            binary_data = ''.join([format(byte, '08b') for byte in message_bytes])
            max_capacity = img.shape[0] * img.shape[1] * 3
            if len(binary_data) > max_capacity:
                messagebox.showerror("Error", "Message too long for selected image. Please use a larger image or shorter message.")
                return

            random.seed(key)
            encrypted_data = ''.join([str(int(bit) ^ random.randint(0, 1)) for bit in binary_data])

            data_index = 0
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(3):
                        if data_index < len(encrypted_data):
                            img[i, j, k] = (img[i, j, k] & 0b11111110) | int(encrypted_data[data_index])
                            data_index += 1

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, img)
                messagebox.showinfo("Success", "Image encoded and saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt(self):
        if not self.decode_path_image:
            messagebox.showerror("Error", "Please select a stego image to decode.")
            return

        key = self.ent_decode_key.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Numeric decryption key required.")
            return

        key = int(key)

        try:
            img = cv2.imread(self.decode_path_image)
            if img is None:
                messagebox.showerror("Error", "Unable to read stego image. Please select a valid image file.")
                return
            binary_data = ""
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(3):
                        binary_data += str(img[i, j, k] & 1)

            random.seed(key)
            decrypted_data = ''.join(str(int(binary_data[i]) ^ random.randint(0, 1)) for i in range(len(binary_data)))

            # Convert binary string to bytes
            byte_list = [int(decrypted_data[i:i+8], 2) for i in range(0, len(decrypted_data), 8)]
            try:
                message = bytes(byte_list).decode('utf-8', errors='ignore')
            except Exception:
                message = ""
            message = message.split("#####")[0]

            self.lbl_decrypted_message.config(text="Decrypted Message: (will be shown in 5 seconds...)")
            self.wn.after(5000, lambda: self.show_decrypted_message(message))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decoding: {e}")

    def show_decrypted_message(self, message):
        self.lbl_decrypted_message.config(text=f"Decrypted Message: {message}")
        messagebox.showinfo("Success", "Message decrypted successfully!")

    def clear_dashboard(self):
        self.wn.destroy()
        DashBoard()

    def exit_application(self):
        ask = messagebox.askyesno('Exit', 'Do you want to return to Home?')
        if ask:
            self.wn.destroy()
            subprocess.Popen(["python", "HomePage.py"])
            sys.exit(0)

    def show_about(self):
        messagebox.showinfo("About", "Image Steganography Tool\nVersion 1.0\nCreated by Sudip")

DashBoard()
