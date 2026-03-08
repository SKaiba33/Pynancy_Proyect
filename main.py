import tkinter as tk
from modelo import RegistroFinanzas, Movimiento
from interfaz import App


if __name__ == "__main__":
	root = tk.Tk()
	registro = RegistroFinanzas()
	app = App(root, registro)

	root.mainloop()