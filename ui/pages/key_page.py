import customtkinter as ctk
from tkinter import filedialog
from ui.styles import show_error, show_info, show_warning, style_textbox, HEADING_FONT, SUBHEADING_FONT, BUTTON_FONT, button_kwargs, CardFrame, style_central_textbox
from crypto.key_manager import generate_rsa_keypair, save_private_key, save_public_key, load_private_key, load_public_key
import os


class KeysPage(ctk.CTkFrame):
    def __init__(self, parent, accent="#1fb6a8"):
        super().__init__(parent)
        self.configure(fg_color="#0f1112")
        self.accent = accent

        title = ctk.CTkLabel(self, text="Gestión de Claves", font=HEADING_FONT)
        title.pack(pady=(30, 10))

        self.info = ctk.CTkLabel(
            self,
            text="Genera, guarda o carga pares de claves RSA (se recomienda 2048 bits).",
            wraplength=900,
            justify="center",
            font=SUBHEADING_FONT,
        )
        self.info.pack(pady=(0, 16), padx=30)

        btn_frame = CardFrame(self, fg_color="#121213", corner_radius=14, border_color="#1b1c1f")
        btn_frame.pack(padx=40, pady=10, fill="x")

        btn_style = button_kwargs(self.accent)

        self.btn_generate = ctk.CTkButton(
            btn_frame,
            text="🔑 Generar par de claves (2048)",
            command=self.generate_keys,
            **btn_style,
        )
        self.btn_generate.pack(padx=10, pady=12, side="left")

        self.btn_save_priv = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar clave privada...",
            command=self.save_priv,
            **btn_style,
        )
        self.btn_save_priv.pack(padx=10, pady=12, side="left")

        self.btn_save_pub = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar clave pública...",
            command=self.save_pub,
            **btn_style,
        )
        self.btn_save_pub.pack(padx=10, pady=12, side="left")

        load_frame = CardFrame(self, fg_color="#121213", corner_radius=14, border_color="#1b1c1f")
        load_frame.pack(padx=40, pady=18, fill="x")

        self.btn_load_priv = ctk.CTkButton(
            load_frame,
            text="📂 Cargar clave privada",
            command=self.load_priv,
            **btn_style,
        )
        self.btn_load_priv.pack(side="left", padx=10, pady=12)

        self.btn_load_pub = ctk.CTkButton(
            load_frame,
            text="📂 Cargar clave pública",
            command=self.load_pub,
            **btn_style,
        )
        self.btn_load_pub.pack(side="left", padx=10, pady=12)

        # área de estado dentro de una tarjeta
        state_card = CardFrame(self, fg_color="#121213", corner_radius=14, border_color="#1b1c1f")
        state_card.pack(padx=30, pady=(10, 30), fill="both", expand=False)
        self.status_box = ctk.CTkTextbox(state_card, width=900, height=200)
        self.status_box.pack(padx=6, pady=8)
        # caja central con letra mucho más grande
        style_central_textbox(self.status_box)
        self.status_box.insert("1.0", "No hay claves cargadas en memoria.\n")

        # claves en memoria
        self._priv = None
        self._pub = None

    def _log(self, text):
        self.status_box.insert("end", text + "\n")
        self.status_box.see("end")

    def generate_keys(self):
        priv, pub = generate_rsa_keypair(2048)
        self._priv = priv
        self._pub = pub
        show_info(self, "Completado", "Par de claves RSA generado en memoria.")
        self._log("✔ Claves RSA (2048) generadas.")

    def save_priv(self):
        if not self._priv:
            show_error(self, "Error", "No hay clave privada en memoria. Genera o carga una primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("Archivos PEM", "*.pem")])
        if not path:
            return
        save_private_key(self._priv, path)
        show_info(self, "Guardado", f"Clave privada guardada en:\n{path}")
        self._log(f"💾 Clave privada guardada → {path}")

    def save_pub(self):
        if not self._pub:
            show_error(self, "Error", "No hay clave pública en memoria. Genera o carga una primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("Archivos PEM", "*.pem")])
        if not path:
            return
        save_public_key(self._pub, path)
        show_info(self, "Guardado", f"Clave pública guardada en:\n{path}")
        self._log(f"💾 Clave pública guardada → {path}")

    def load_priv(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM", "*.pem")])
        if not path:
            return
        try:
            self._priv = load_private_key(path)
            show_info(self, "Cargada", "Clave privada cargada en memoria.")
            self._log(f"📂 Clave privada cargada → {path}")
        except Exception as e:
            show_error(self, "Error", f"No se pudo cargar la clave privada:\n{e}")

    def load_pub(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM", "*.pem")])
        if not path:
            return
        try:
            self._pub = load_public_key(path)
            show_info(self, "Cargada", "Clave pública cargada en memoria.")
            self._log(f"📂 Clave pública cargada → {path}")
        except Exception as e:
            show_error(self, "Error", f"No se pudo cargar la clave pública:\n{e}")
