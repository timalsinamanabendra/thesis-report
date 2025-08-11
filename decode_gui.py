# decode_gui.py
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os, sys, subprocess  # <-- added

from stego_core import decode_image

class DecodeApp:
    def __init__(self):
        self.wn = Tk()
        self.wn.title("Image Steganography - Decoder")
        self.wn.state("zoomed")
        self.wn.configure(bg="#FFF8DC")

        self.image_display_size = (400, 400)
        self.stego_path = None

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

    def _open_encoder(self):
        self._run_script("encode_gui.py")

    def _restart_decoder(self):
        # optional convenience to restart current app
        self.wn.destroy()
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])

    # ---------- Menubar ----------
    def _build_menu(self):
        menubar = Menu(self.wn)

        # File
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select Stego Image", command=self.select_stego)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.wn.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # Apps (NEW)
        apps_menu = Menu(menubar, tearoff=0)
        apps_menu.add_command(label="Open Encoder (new window)", command=self._open_encoder)
        apps_menu.add_command(label="Restart Decoder", command=self._restart_decoder)
        menubar.add_cascade(label="Apps", menu=apps_menu)

        # Help
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "Decoder\nLSB + XOR(PRNG) with numeric key")
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.wn.config(menu=menubar)

    def _build_layout(self):
        container = Frame(self.wn, bg="black", width=1200, height=600)
        container.pack(expand=True, fill=BOTH, padx=10, pady=10)

        right = Frame(container, bg="white")
        right.pack(side=RIGHT, expand=True, fill=BOTH, padx=5, pady=5)

        Label(right, text="Decode", font=("arial", 20, "bold"), bg="white").pack(pady=10)

        self.photo_frame = LabelFrame(right, text="Selected Stego Image", bg="white", width=400, height=400)
        self.photo_frame.pack(pady=10)

        Button(right, text="Select Stego Image", command=self.select_stego).pack(pady=5)

        Label(right, text="Decryption Key (numbers only):", bg="white").pack(pady=5)
        self.ent_key = Entry(right, width=30)
        self.ent_key.pack(pady=5)

        Button(right, text="Decode", command=self.decode).pack(pady=10)

        self.lbl_out = Label(right, text="Decrypted Message: ", bg="white", wraplength=600, justify=LEFT)
        self.lbl_out.pack(pady=8)

    def select_stego(self):
        path = filedialog.askopenfilename(title="Choose a stego image")
        if path:
            self.stego_path = path
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

    def decode(self):
        if not self.stego_path:
            messagebox.showerror("Error", "Please select a stego image to decode.")
            return

        key_text = self.ent_key.get().strip()
        if not key_text.isdigit():
            messagebox.showerror("Error", "Numeric decryption key required.")
            return
        key = int(key_text)

        try:
            self.lbl_out.config(text="Decrypted Message: (will be shown in 5 seconds...)")
            msg = decode_image(self.stego_path, key)
            self.wn.after(5000, lambda: self._show_message(msg))
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {e}")

    def _show_message(self, msg: str):
        self.lbl_out.config(text=f"Decrypted Message: {msg}")
        messagebox.showinfo("Success", "Message decrypted successfully!")

if __name__ == "__main__":
    DecodeApp()
