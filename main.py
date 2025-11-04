import sys
import os

# Agregar el directorio raíz del proyecto al path antes de importar paquetes internos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import App


if __name__ == "__main__":
    app = App()
    app.mainloop()
