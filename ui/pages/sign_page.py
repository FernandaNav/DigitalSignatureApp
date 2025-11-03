import customtkinter as ctk
from tkinter import filedialog, messagebox
from crypto.sign_manager import sign_file_with_private_key, verify_file_with_public_key

class SignPage(ctk.CTkFrame):
    def __init__(self, parent, accent="#1fb6a8"):
        super().__init__(parent)
        self.configure(fg_color="#0f1112")
        self.accent = accent

        title = ctk.CTkLabel(self, text="Firmar / Verificar", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(30,10))

        info = ctk.CTkLabel(
            self,
            text="Firma archivos (.txt) con RSA-PSS y verifica las firmas (.sig).",
            wraplength=900,
            justify="center"
        )
        info.pack(padx=30, pady=(0,12))

        frame = ctk.CTkFrame(self, fg_color="#121213")
        frame.pack(padx=30, pady=12, fill='x')

        btn_sign = ctk.CTkButton(frame, text="🖋 Firmar un archivo .txt", fg_color=self.accent, command=self.sign_file)
        btn_sign.pack(side='left', padx=12, pady=12)

        btn_verify = ctk.CTkButton(frame, text="🔎 Verificar archivo + firma", fg_color=self.accent, command=self.verify_file)
        btn_verify.pack(side='left', padx=12, pady=12)

        self.log = ctk.CTkTextbox(self, width=900, height=220)
        self.log.pack(padx=30, pady=(10,30))

    def sign_file(self):
        priv_path = filedialog.askopenfilename(title="Selecciona la clave privada (.pem)", filetypes=[("Archivos PEM","*.pem")])
        if not priv_path:
            return
        file_path = filedialog.askopenfilename(title="Selecciona el archivo a firmar (.txt)", filetypes=[("Archivos de texto","*.txt")])
        if not file_path:
            return
        try:
            out = sign_file_with_private_key(priv_path, file_path)
            self.log.insert('end', f"🖋 Firma generada → {out}\n")
            self.log.see('end')
            messagebox.showinfo("Archivo firmado", f"Se generó la firma correctamente:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo firmar el archivo:\n{e}")

    def verify_file(self):
        pub_path = filedialog.askopenfilename(title="Selecciona la clave pública (.pem)", filetypes=[("Archivos PEM","*.pem")])
        if not pub_path:
            return
        file_path = filedialog.askopenfilename(title="Selecciona el archivo original (.txt)", filetypes=[("Archivos de texto","*.txt")])
        if not file_path:
            return
        sig_path = filedialog.askopenfilename(title="Selecciona la firma (.sig)", filetypes=[("Archivos de firma","*.sig")])
        if not sig_path:
            return
        try:
            ok = verify_file_with_public_key(pub_path, file_path, sig_path)
            if ok:
                self.log.insert('end', "✅ Firma válida\n")
                messagebox.showinfo("Verificación exitosa", "La firma es válida y el archivo no fue modificado.")
            else:
                self.log.insert('end', "❌ Firma inválida\n")
                messagebox.showwarning("Firma inválida", "La firma no coincide o el archivo fue alterado.")
            self.log.see('end')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo verificar la firma:\n{e}")
