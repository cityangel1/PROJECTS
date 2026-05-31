# ficha/gui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from .core import FichaCore
from .constants import BACKGROUND_COLOR, TEXT_COLOR

class FichaGUI:
    def __init__(self):
        self.core = FichaCore()
        self.root = ctk.CTk()
        self.root.title("Ficha - Advanced Steganography")
        self.root.geometry("950x720")
        self.root.configure(fg_color=BACKGROUND_COLOR)

        self.create_widgets()

    def create_widgets(self):
        # Title
        ctk.CTkLabel(self.root, text="FICHA", font=ctk.CTkFont(size=48, weight="bold"),
                     text_color=TEXT_COLOR).pack(pady=15)

        # Carrier Type
        self.carrier_type = ctk.StringVar(value="Image")
        ctk.CTkSegmentedButton(self.root, values=["Image", "Video", "Audio"],
                              variable=self.carrier_type).pack(pady=10)

        # File Selection
        self.carrier_var = ctk.StringVar()
        self.secret_var = ctk.StringVar()

        ctk.CTkButton(self.root, text="Select Carrier", command=self.select_carrier,
                      fg_color=TEXT_COLOR).pack(pady=8, padx=50, fill="x")
        ctk.CTkEntry(self.root, textvariable=self.carrier_var).pack(padx=50, pady=5)

        ctk.CTkButton(self.root, text="Select File to Hide", command=self.select_secret,
                      fg_color=TEXT_COLOR).pack(pady=8, padx=50, fill="x")
        ctk.CTkEntry(self.root, textvariable=self.secret_var).pack(padx=50, pady=5)

        # Passphrase
        self.pass1 = ctk.CTkEntry(self.root, placeholder_text="Passphrase", show="*")
        self.pass1.pack(pady=8, padx=50, fill="x")
        self.pass2 = ctk.CTkEntry(self.root, placeholder_text="Confirm Passphrase", show="*")
        self.pass2.pack(pady=8, padx=50, fill="x")

        # Buttons
        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=30)

        ctk.CTkButton(btn_frame, text="EMBED", width=200, height=50, fg_color="#8B4513",
                      command=self.embed_action).pack(side="left", padx=15)
        ctk.CTkButton(btn_frame, text="EXTRACT", width=200, height=50, fg_color="#8B4513",
                      command=self.extract_action).pack(side="left", padx=15)

    def select_carrier(self):
        types = [("All Supported", "*.png *.jpg *.jpeg *.mp4 *.wav")]
        path = filedialog.askopenfilename(filetypes=types)
        if path:
            self.carrier_var.set(path)

    def select_secret(self):
        path = filedialog.askopenfilename()
        if path:
            self.secret_var.set(path)

    def embed_action(self):
        if self.pass1.get() != self.pass2.get():
            messagebox.showerror("Error", "Passphrases do not match")
            return
        if not self.carrier_var.get() or not self.secret_var.get():
            messagebox.showerror("Error", "Select both files")
            return

        try:
            carrier = self.carrier_var.get()
            if self.carrier_type.get() == "Video":
                out = self.core.embed_video(carrier, self.secret_var.get(), self.pass1.get())
            elif self.carrier_type.get() == "Audio":
                out = self.core.embed_audio(carrier, self.secret_var.get(), self.pass1.get())
            else:
                out = self.core.embed_image(carrier, self.secret_var.get(), self.pass1.get())
            messagebox.showinfo("Success", f"Embedded successfully!\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_action(self):
        carrier = filedialog.askopenfilename()
        if not carrier:
            return
        output = filedialog.asksaveasfilename()
        if not output:
            return
        passphrase = ctk.CTkInputDialog(title="Passphrase", text="Enter passphrase:").get_input()

        try:
            result = self.core.extract(carrier, output, passphrase)
            messagebox.showinfo("Success", f"Extracted to: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()
