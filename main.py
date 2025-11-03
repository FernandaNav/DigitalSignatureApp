from ui.main_window import App
import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
