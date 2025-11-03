import customtkinter as ctk
from tkinter import filedialog, messagebox
from crypto.cipher_manager import hybrid_encrypt_file, hybrid_decrypt_file, load_public_key_from_file, load_private_key_from_file

class EncryptPage(ctk.CTkFrame):
    def __init__(self, parent, accent="#1fb6a8"):
        super().__init__(parent)
        self.configure(fg_color="#0f1112")
        self.accent = accent

        title = ctk.CTkLabel(self, text="Cifrar / Descifrar", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(30,10))

        self.info = ctk.CTkLabel(
            self,
            text="Usa RSA para proteger una clave AES y AES-GCM para cifrar el contenido del archivo (esquema híbrido).",
            wraplength=900,
            justify="center"
        )
        self.info.pack(padx=30, pady=(0,10))

        frame = ctk.CTkFrame(self, fg_color="#121213")
        frame.pack(padx=30, pady=12, fill='x')

        btn_load_pub = ctk.CTkButton(frame, text="📂 Cargar clave pública (para cifrar)", command=self.load_public_key)
        btn_load_pub.pack(side='left', padx=12, pady=12)

        btn_load_priv = ctk.CTkButton(frame, text="📂 Cargar clave privada (para descifrar)", command=self.load_private_key)
        btn_load_priv.pack(side='left', padx=12, pady=12)

        ops = ctk.CTkFrame(self, fg_color="#121213")
        ops.pack(padx=30, pady=12, fill='x')

        btn_encrypt = ctk.CTkButton(ops, text="🔒 Cifrar un archivo .txt", fg_color=self.accent, command=self.encrypt_file)
        btn_encrypt.pack(side='left', padx=12, pady=12)

        btn_decrypt = ctk.CTkButton(ops, text="🔓 Descifrar un archivo .enc", fg_color=self.accent, command=self.decrypt_file)
        btn_decrypt.pack(side='left', padx=12, pady=12)

        self.output = ctk.CTkTextbox(self, width=900, height=220)
        self.output.pack(padx=30, pady=(10,30))

        self._pub_path = None
        self._priv_path = None

    def load_public_key(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        self._pub_path = path
        self.output.insert('end', f"🔑 Clave pública cargada: {path}\n")
        self.output.see('end')

    def load_private_key(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos PEM","*.pem")])
        if not path:
            return
        self._priv_path = path
        self.output.insert('end', f"🔒 Clave privada cargada: {path}\n")
        self.output.see('end')

    def encrypt_file(self):
        if not self._pub_path:
            messagebox.showerror("Error", "Primero carga una clave pública.")
            return
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto","*.txt")])
        if not path:
            return
        try:
            out = hybrid_encrypt_file(self._pub_path, path)
            self.output.insert('end', f"✅ Archivo cifrado → {out}\n")
            self.output.see('end')
            messagebox.showinfo("Cifrado completo", f"El archivo fue cifrado con éxito:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cifrar el archivo:\n{e}")

    def decrypt_file(self):
        if not self._priv_path:
            messagebox.showerror("Error", "Primero carga una clave privada.")
            return
        path = filedialog.askopenfilename(filetypes=[("Archivos cifrados","*.enc")])
        if not path:
            return
        try:
            out = hybrid_decrypt_file(self._priv_path, path)
            self.output.insert('end', f"✅ Archivo descifrado → {out}\n")
            self.output.see('end')
            messagebox.showinfo("Descifrado completo", f"El archivo fue descifrado con éxito:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descifrar el archivo:\n{e}")
