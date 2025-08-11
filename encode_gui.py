# encode_gui.py
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os, sys, subprocess

from stego_core import encode_image


class EncodeApp:
    def __init__(self):
        self.wn = Tk()
        self.wn.title("Image Steganography - Encoder")
        self.wn.state("zoomed")
        self.wn.configure(bg="#FFF8DC")

        self.image_display_size = (400, 400)
        self.path_image = None

        self._build_menu()
        self._build_layout()

        self.wn.mainloop()

    # ---------- Apps menu helpers ----------
    def _run_script(self, filename: str):
        """Launch another script (encode_gui.py / decode_gui.py) with same Python."""
        here = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(here, filename)
        if not os.path.exists(target):
            messagebox.showerror("Not found", f"Could not locate: {target}")
            return
        try:
            subprocess.Popen([sys.executable, target])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {filename}:\n{e}")

    def _open_decoder(self):
        self._run_script("decode_gui.py")

    def _restart_encoder(self):
        self.wn.destroy()
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])

    # ---------- Menubar ----------
    def _build_menu(self):
        menubar = Menu(self.wn)

        # File
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select Image", command=self.select_image)
        file_menu.add_command(label="Encode & Save", command=self.encode_and_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.wn.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # Apps (NEW)
        apps_menu = Menu(menubar, tearoff=0)
        apps_menu.add_command(label="Open Decoder (new window)", command=self._open_decoder)
        apps_menu.add_command(label="Restart Encoder", command=self._restart_encoder)
        menubar.add_cascade(label="Apps", menu=apps_menu)

        # Help
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About", "Encoder\nLSB + XOR(PRNG) with numeric key"
            ),
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.wn.config(menu=menubar)

    def _build_layout(self):
        container = Frame(self.wn, bg="black", width=1200, height=600)
        container.pack(expand=True, fill=BOTH, padx=10, pady=10)

        left = Frame(container, bg="white")
        left.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        Label(left, text="Encode", font=("arial", 20, "bold"), bg="white").pack(pady=10)

        self.photo_frame = LabelFrame(left, text="Selected Image", bg="white", width=400, height=400)
        self.photo_frame.pack(pady=10)

        Button(left, text="Select Image", command=self.select_image).pack(pady=5)

        Label(left, text="Message to Encode:", bg="white").pack(pady=5)
        self.ent_msg = Text(left, width=60, height=6)
        self.ent_msg.pack(pady=5)

        Label(left, text="Encryption Key (numbers only):", bg="white").pack(pady=5)
        self.ent_key = Entry(left, width=30)
        self.ent_key.pack(pady=5)

        Button(left, text="Encode & Save", command=self.encode_and_save).pack(pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(title="Choose a cover image")
        if path:
            self.path_image = path
            self._display_image(path, self.photo_frame)

    def _display_image(self, image_path, frame):
        for w in frame.winfo_children():
            w.destroy()
        try:
            img = Image.open(image_path)
            img.thumbnail(self.image_display_size)
            render = ImageTk.PhotoImage(img)
            lbl = Label(frame, image=render, bg="white")
            lbl.image = render
            lbl.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image: {e}")

    def encode_and_save(self):
        if not self.path_image:
            messagebox.showerror("Error", "Please select an image to encode.")
            return

        key_text = self.ent_key.get().strip()
        if not key_text.isdigit():
            messagebox.showerror("Error", "Numeric encryption key required.")
            return
        key = int(key_text)

        message = self.ent_msg.get("1.0", "end-1c")
        if not message:
            messagebox.showerror("Error", "Message is empty.")
            return

        try:
            stego = encode_image(self.path_image, message, key)
            initial_name = f"stego_{os.path.basename(self.path_image)}"
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=initial_name,
                title="Save stego image as..."
            )
            if save_path:
                cv2.imwrite(save_path, stego)
                messagebox.showinfo("Success", "Image encoded and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {e}")


if __name__ == "__main__":
    EncodeApp()
