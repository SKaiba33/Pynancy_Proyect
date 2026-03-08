import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime


class App:
	def __init__(self, root, registro):
		self.root = root
		self.registro = registro


		self.root.title("Pynanci Managed v1.0")
		self.root.geometry("400x500")	
		self.root.resizable(False,False)

		self.balance_valor = tk.StringVar()

		self.crear_widgets()

		self.cargar_tabla()



	def crear_widgets(self):

		###Balance###

		self.label_balance_titulo = tk.Label(
			self.root,
			text = "BALANCE ACTUAL",
			font = ("Arial", 12)
		)
		self.label_balance_titulo.grid(row=0, column=0, columnspan=2, pady=(15,0))

		self.label_balance = tk.Label(
			self.root,
			textvariable=self.balance_valor,
			font=("Arial",18)
		)
		self.label_balance.grid(row=1, column=0, columnspan=2, pady=(0,15))



		###ENTRADA MONTO###
		vcmd = (self.root.register(self.validar_entero), "%P") #esta va con el validador de enteros

		self.entry_monto = ttk.Entry(
			self.root,
			validate="key",
			validatecommand=vcmd
		)
		self.entry_monto.grid(row=2, column= 0, columnspan=2, padx=20, sticky="ew")


		###BOTONES_MONTO###

		self.boton_ingreso = tk.Button(
			self.root,
			text="+",
			command=self.agregar_ingreso
		)
		self.boton_ingreso.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

		self.boton_egreso = tk.Button(
			self.root,
			text="-",
			command=self.agregar_egreso
		)
		self.boton_egreso.grid(row=3, column=1, pady=10, padx=20, sticky="ew")


		###TABLA###

		self.tree = ttk.Treeview(
			self.root,
			columns=("fecha", "tipo", "monto"),
			show="headings",
			selectmode="browse"
		)


		self.tree.heading("fecha", text="Fecha")
		self.tree.heading("tipo", text="Tipo")
		self.tree.heading("monto", text="Monto")


		self.tree.column("fecha", width=120, anchor="center", stretch=False)
		self.tree.column("tipo", width=104, anchor="center", stretch=False)
		self.tree.column("monto", width=120, anchor="e", stretch=False)

		self.tree.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")


		self.tree.bind("<Button-1>", self.bloquear_ajuste)
		self.tree.bind("<<TreeviewSelect>>", self.habilitar_eliminar)

		###ELSCROLL_VERTICAL###

		self.scrollbar = ttk.Scrollbar(
			self.root,
			orient="vertical",
			command=self.tree.yview
		)
		self.tree.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.grid(row=4, column=2, sticky="ns", pady=10)


		###BOTON_ELIMINAR###
		self.boton_eliminar = tk.Button(
			self.root,
			text="Eliminar",
			command=self.eliminar_movimiento,
			state="disabled"
		)
		self.boton_eliminar.grid(row=5, column=0,columnspan=2, pady=10)



		###AJUSTAR_TABLA###
		self.root.grid_rowconfigure(4, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_columnconfigure(1, weight=1)
	


	def cargar_tabla(self):
		for elemento in self.tree.get_children():
			self.tree.delete(elemento)

		self.movimientos_ord = self.registro.obtener_movimientos_ordenados()

		for movimiento in self.movimientos_ord:
			fecha = datetime.strptime(movimiento.fecha, "%Y-%m-%dT%H:%M:%S.%f")
			fecha_con_formato = fecha.strftime("%d-%m-%Y")
			self.tree.insert(
				"",
				"end",
				iid=movimiento.id,
				values=(fecha_con_formato, movimiento.tipo, movimiento.monto))

		self.actualizar_balance()


	def bloquear_ajuste(self, event): #Bloquea el ajuste de la tabla por parte del usuario
			if self.tree.identify_region(event.x,event.y) == "separator":
				return "break"


	def eliminar_movimiento(self):
		seleccion = self.tree.selection()


		if not seleccion:
			messagebox.showwarning("Atención", "Selecciona una nota para eliminarla.")
			return


		confirmar = messagebox.askyesno(
			"Confirmar eliminación",
			"¿Estás seguro de eliminar el registro?"

		)

		if not confirmar:
			print("no confirmado")
			return
		else:
			id_movimiento = seleccion[0]
			print(f"Eliminando...{id_movimiento}")
			self.registro.eliminar(id_movimiento)
			self.cargar_tabla()


	def habilitar_eliminar(self, event=None): #se supone que desactiva el boton de eliminación hasta que se haya seleccionado un elemento
		seleccion = self.tree.selection()
		if seleccion:
			self.boton_eliminar.config(state="normal")
		else:
			self.boton_eliminar.config(state="disabled")


	def agregar_ingreso(self):
		valor = self.entry_monto.get().strip()

		if not valor:
			messagebox.showwarning("Campo vacio", "Ingrese un monto.")
			return

		try:
			monto = float(valor)
		except ValueError:
			messagebox.showerror("Error", "Ingrese un número válido.")
			return

		if monto <= 0:
			messagebox.showwarning("Valor inválido", "El monto debe ser mayor a cero.")
			return


		self.registro.agregar(monto, "ingreso")
		self.cargar_tabla()
		self.entry_monto.delete(0, tk.END)
		self.entry_monto.focus()

	def agregar_egreso(self):
		valor = self.entry_monto.get().strip()

		if not valor:
			messagebox.showwarning("Campo vacio", "Ingrese un monto.")
			return

		try:
			monto = float(valor)
		except ValueError:
			messagebox.showerror("Error", "Ingrese un número válido.")
			return

		if monto <= 0:
			messagebox.showwarning("Valor inválido", "El monto debe ser mayor a cero.")
			return


		self.registro.agregar(monto, "egreso")
		self.cargar_tabla()
		self.entry_monto.delete(0, tk.END)
		self.entry_monto.focus()	

	def validar_entero(self, valor):
		if valor == "":
			return True #Segun que para permitir borrar y eso

		return valor.isdigit()

		#Anotación: para que se pase este filtro solo debe devolver True en esta función, todo lo False es off

	def actualizar_balance(self):
		balance = self.registro.balance()
		self.balance_valor.set(f"{balance:,.0f}")


	def comprobacion(self):
		self.balance_valor += 1
		if self.tree.selection():
			print(f"ok, {self.tree.selection()}")
		else:
			print("not")





