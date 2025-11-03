import customtkinter as ctk
from tkinter import filedialog, messagebox
from crypto.key_manager import generate_rsa_keypair, save_private_key, save_public_key, load_private_key, load_public_key
import os

class KeysPage(ctk.CTkFrame):
    def __init__(self, parent, accent="#1fb6a8"):
        super().__init__(parent)
        self.configure(fg_color="#0f1112")
        self.accent = accent

        title = ctk.CTkLabel(self, text="Gestión de Claves", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(30,10))

        self.info = ctk.CTkLabel(
            self, 
            text="Genera, guarda o carga pares de claves RSA (se recomienda 2048 bits).", 
            wraplength=900, 
            justify="center"
        )
        self.info.pack(pady=(0,16), padx=30)

        btn_frame = ctk.CTkFrame(self, fg_color="#121213")
        btn_frame.pack(padx=40, pady=10, fill='x')

        self.btn_generate = ctk.CTkButton(
            btn_frame, 
            text="🔑 Generar par de claves (2048)", 
            fg_color=self.accent, 
            command=self.generate_keys
        )
        self.btn_generate.pack(padx=10, pady=12, side='left')

        self.btn_save_priv = ctk.CTkButton(
            btn_frame, 
            text="💾 Guardar clave privada...", 
            command=self.save_priv
        )
        self.btn_save_priv.pack(padx=10, pady=12, side='left')

        self.btn_save_pub = ctk.CTkButton(
            btn_frame, 
            text="💾 Guardar clave pública...", 
            command=self.save_pub
        )
        self.btn_save_pub.pack(padx=10, pady=12, side='left')

        load_frame = ctk.CTkFrame(self, fg_color="#121213")
        load_frame.pack(padx=40, pady=18, fill='x')

        self.btn_load_priv = ctk.CTkButton(
            load_frame, 
            text="📂 Cargar clave privada", 
            command=self.load_priv
        )
        self.btn_load_priv.pack(side='left', padx=10, pady=12)

        self.btn_load_pub = ctk.CTkButton(
            load_frame, 
            text="📂 Cargar clave pública", 
            command=self.load_pub
        )
        self.btn_load_pub.pack(side='left', padx=10, pady=12)

        # área de estado
        self.status_box = ctk.CTkTextbox(self, width=900, height=200)
        self.status_box.pack(padx=30, pady=(10,30))
        self.status_box.insert('1.0', "No hay claves cargadas en memoria.\n")

        # claves en memoria
        self._priv = None
        self._pub = None

    def _log(self, text):
        self.status_box.insert('end', text + "\n")
        self.status_box.see('end')

    def generate_keys(self):
        priv, pub = generate_rsa_keypair(2048)
        self._priv = priv
        self._pub = pub
        messagebox.showinfo("Completado", "Par de claves RSA generado en memoria.")
        self._log("✔ Claves RSA (2048) generadas.")

    def save_priv(self):
        if not self._priv:
            messagebox.showerror("Error", "No hay clave privada en memoria. Genera o carga una primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        save_private_key(self._priv, path)
        messagebox.showinfo("Guardado", f"Clave privada guardada en:\n{path}")
        self._log(f"💾 Clave privada guardada → {path}")

    def save_pub(self):
        if not self._pub:
            messagebox.showerror("Error", "No hay clave pública en memoria. Genera o carga una primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        save_public_key(self._pub, path)
        messagebox.showinfo("Guardado", f"Clave pública guardada en:\n{path}")
        self._log(f"💾 Clave pública guardada → {path}")

    def load_priv(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        try:
            self._priv = load_private_key(path)
            messagebox.showinfo("Cargada", "Clave privada cargada en memoria.")
            self._log(f"📂 Clave privada cargada → {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la clave privada:\n{e}")

    def load_pub(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        try:
            self._pub = load_public_key(path)
            messagebox.showinfo("Cargada", "Clave pública cargada en memoria.")
            self._log(f"📂 Clave pública cargada → {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la clave pública:\n{e}")
