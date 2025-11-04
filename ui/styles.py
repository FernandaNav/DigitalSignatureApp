import customtkinter as ctk
import tkinter as tk

# Tipografías y tamaños para mejor legibilidad (ajustados a UI/UX más grande)
# He aumentado ligeramente las fuentes para mejor lectura en pantallas modernas.
HEADING_FONT = ("Segoe UI", 26, "bold")
SUBHEADING_FONT = ("Segoe UI", 16)
BUTTON_FONT = ("Segoe UI", 15, "bold")
BODY_FONT = ("Segoe UI", 12)

# Fuente central (la 'caja de enmedio') — ligeramente menor que antes ("un poquito" más pequeña).
# Antes era 3x el tamaño base; ahora reducimos a ~2.5x para mejor equilibrio.
CENTRAL_FONT = ("Segoe UI", int(BODY_FONT[1] * 2.5), "bold")

# Colores base — mantener la paleta original (no cambiar la sensación cromática)
ACCENT = "#12a892"
SIDEBAR_BG = "#16171a"
MAIN_BG = "#0f1112"
PANEL_BG = "#121213"

# Botones: borde y radio para mejor affordance
BUTTON_BORDER_WIDTH = 2
BUTTON_BORDER_COLOR = "#0f7f6e"  # tono ligeramente más oscuro del acento
BUTTON_CORNER_RADIUS = 12


def button_kwargs(accent=ACCENT):
    """Valores por defecto que pueden pasarse al crear CTkButton para homogeneizar el estilo."""
    return {
        "fg_color": accent,
        "hover_color": "#17a28f",
        "height": 44,
        "corner_radius": BUTTON_CORNER_RADIUS,
        "font": BUTTON_FONT,
        "border_width": BUTTON_BORDER_WIDTH,
        "border_color": BUTTON_BORDER_COLOR,
    }


class CardFrame(ctk.CTkFrame):
    """Un contenedor tipo 'card' con radio, borde y padding consistente.

    Uso: CardFrame(parent, fg_color=PANEL_BG, corner_radius=12, border_color=None)
    """
    def __init__(self, parent, fg_color=PANEL_BG, corner_radius=12, border_color=None, **kwargs):
        # border_color se puede usar para dar un ligero contorno
        super().__init__(parent, fg_color=fg_color, corner_radius=corner_radius, **kwargs)
        if border_color:
            try:
                # algunos CTkFrame acepat border_width/border_color
                self.configure(border_width=1, border_color=border_color)
            except Exception:
                pass



class StyledDialog(ctk.CTkToplevel):
    """Diálogo simple y accesible con estilo consistente.

    Uso: StyledDialog(parent, title, message, kind="info")
    Se muestra de forma modal y tiene un único botón Aceptar.
    """
    ICONS = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️"
    }

    def __init__(self, parent, title, message, kind="info", accent=ACCENT):
        super().__init__(parent)
        self.title(title)
        self.configure(fg_color=MAIN_BG)
        self.resizable(False, False)

        self.transient(parent)
        # Centro relativo
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 120, parent.winfo_rooty() + 120))

        icon = self.ICONS.get(kind, "ℹ️")

        frame = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=12)
        frame.pack(padx=16, pady=16, fill="both", expand=True)

        top = ctk.CTkFrame(frame, fg_color=PANEL_BG)
        top.pack(fill='x', padx=6, pady=(6, 2))

        lbl_icon = ctk.CTkLabel(top, text=icon, font=("Segoe UI", 20))
        lbl_icon.pack(side='left', padx=(6, 12))

        lbl_title = ctk.CTkLabel(top, text=title, font=HEADING_FONT, anchor='w')
        lbl_title.pack(side='left', fill='x', expand=True)

        msg = ctk.CTkLabel(frame, text=message, font=BODY_FONT, wraplength=560, justify='left')
        msg.pack(padx=8, pady=(6, 12))

        btn = ctk.CTkButton(frame, text="Aceptar", fg_color=accent, hover_color="#17a28f", font=BUTTON_FONT, command=self._close)
        btn.pack(pady=(4, 6))

        # Modal
        self.grab_set()
        self.wait_window(self)

    def _close(self):
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()


def show_info(parent, title, message):
    StyledDialog(parent, title, message, kind="info")


def show_success(parent, title, message):
    StyledDialog(parent, title, message, kind="success")


def show_error(parent, title, message):
    StyledDialog(parent, title, message, kind="error")


def show_warning(parent, title, message):
    StyledDialog(parent, title, message, kind="warning")


def style_textbox(tb: ctk.CTkTextbox):
    """Aplicar fuente y contraste a un CTkTextbox existente."""
    try:
        tb.configure(font=BODY_FONT, text_color="#e6eef0", fg_color=PANEL_BG)
    except Exception:
        # En caso de widgets personalizados que no acepten alguna opción
        pass


def style_central_textbox(tb: ctk.CTkTextbox):
    """Aplicar estilo especial para la caja central (texto grande)."""
    try:
        tb.configure(font=CENTRAL_FONT, text_color="#ffffff", fg_color=PANEL_BG)
    except Exception:
        pass
