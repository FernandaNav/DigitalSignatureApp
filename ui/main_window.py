import customtkinter as ctk
from ui.pages.key_page import KeysPage
from ui.pages.encrypt_page import EncryptPage
from ui.pages.sign_page import SignPage
from ui.styles import HEADING_FONT, BUTTON_FONT, button_kwargs
import os

# Apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#1fb6a8"   # acento verde-azulado suave
SIDEBAR_BG = "#16171a"
MAIN_BG = "#0f1112"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CryptoDesk — Cifrado Asimétrico y Firma Digital")
        self.after(80, lambda: self.state('zoomed'))  # maximizar con retraso para compatibilidad

        # Panel lateral
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=SIDEBAR_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.sidebar, text="🔐 CryptoDesk", font=HEADING_FONT)
        self.logo.pack(pady=(30, 20))

        # estilo consistente para botones (con borde)
        btn_style = button_kwargs(ACCENT)

        self.btn_keys = ctk.CTkButton(self.sidebar, text="🔑 Generar Claves", command=self.show_keys, **btn_style)
        self.btn_keys.pack(fill="x", padx=20, pady=(8, 6))

        self.btn_encrypt = ctk.CTkButton(self.sidebar, text="🔒 Cifrar / Descifrar", command=self.show_encrypt, **btn_style)
        self.btn_encrypt.pack(fill="x", padx=20, pady=6)

        self.btn_sign = ctk.CTkButton(self.sidebar, text="🖋 Firmar / Verificar", command=self.show_sign, **btn_style)
        self.btn_sign.pack(fill="x", padx=20, pady=6)

        # Contenedor principal
        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color=MAIN_BG)
        self.container.pack(side="left", fill="both", expand=True)

        # Inicializar páginas (lazy)
        self.pages = {}
        self.show_keys()

    def hide_all(self):
        for p in self.pages.values():
            p.pack_forget()

    def show_keys(self):
        self.hide_all()
        if 'keys' not in self.pages:
            self.pages['keys'] = KeysPage(self.container, accent=ACCENT)
        self.pages['keys'].pack(fill='both', expand=True)

    def show_encrypt(self):
        self.hide_all()
        if 'encrypt' not in self.pages:
            self.pages['encrypt'] = EncryptPage(self.container, accent=ACCENT)
        self.pages['encrypt'].pack(fill='both', expand=True)

    def show_sign(self):
        self.hide_all()
        if 'sign' not in self.pages:
            self.pages['sign'] = SignPage(self.container, accent=ACCENT)
        self.pages['sign'].pack(fill='both', expand=True)
