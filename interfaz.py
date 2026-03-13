import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime


class App:
	def __init__(self, root, registro):
		self.root = root
		self.registro = registro


		self.root.title("Pynanci Managed v1.0")
		self.root.geometry("420x525")	
		self.root.minsize(400,500)
		#self.root.resizable(False,False)

		self.balance_valor = tk.StringVar()
		self.balance_efectivo = tk.StringVar()
		self.balance_banco = tk.StringVar()

		style= ttk.Style()

		style.map(
			"Treeview",
			background=[("selected", "#6E7D4E")],
			foreground=[("selected", "#FFFFFF")]
		)

		style.configure(
			"Treeview.Heading",
			font=("Segoe UI", 10, "bold")
		)

		style.configure(
			"Treeview",
			font=("Segoe UI", 10),
			rowheight=25
		)

		style.configure(
			"Bg_mainframe.TFrame",
			background="#D8E0C7"
		)

		self.crear_frames()

		self.crear_widgets()

		self.cargar_tabla()

	def crear_frames(self):
		##Main Frame##
		self.main_frame = ttk.Frame(self.root, style="Bg_mainframe.TFrame")
		self.main_frame.pack(fill="both", expand=True,)
		self.main_frame.bind("<Button-1>", self.deseleccionar_tabla, add="+")


		##Balance Frame##
		self.balance_frame = ttk.Frame(self.main_frame, style="Bg_mainframe.TFrame")
		self.balance_frame.pack_propagate(False)
		self.balance_frame.pack(fill="x", expand=False)
		self.balance_frame.bind("<Button-1>", self.deseleccionar_tabla, add="+")

		self.balance_frame.columnconfigure(0, weight=1)
		self.balance_frame.columnconfigure(1, weight=1)
		self.balance_frame.columnconfigure(2, weight=1)

		##Entry Frame##
		self.entry_frame = ttk.Frame(self.main_frame, style="Bg_mainframe.TFrame")
		self.entry_frame.pack_propagate(False)
		self.entry_frame.pack(fill="x", expand=False)
		self.entry_frame.bind("<Button-1>", self.deseleccionar_tabla, add="+")

		self.entry_frame.columnconfigure(0, weight=1)
		self.entry_frame.columnconfigure(1, weight=1)

		##Treeview Frame##
		self.treeview_frame = ttk.Frame(self.main_frame, style="Bg_mainframe.TFrame")
		self.treeview_frame.pack_propagate(False)
		self.treeview_frame.pack(fill="both", expand=True)
		self.treeview_frame.bind("<Button-1>", self.deseleccionar_tabla, add="+")

		self.treeview_frame.columnconfigure(0, weight=1)
		self.treeview_frame.rowconfigure(0, weight=1)


	def crear_widgets(self):

		###Balance###
		self.label_balance_efectivo = tk.Label(
			self.balance_frame,
			text = "EFECTIVO",
			font=("Segoe UI", 8),
			background='#D8E0C7'
		)
		self.label_balance_efectivo.grid(row=0, column=0, pady=(20,0))

		self.label_balance_efectivo_valor = tk.Label(
			self.balance_frame,
			textvariable=self.balance_efectivo,
			font=("Arial",16),
			background='#D8E0C7'
		)
		self.label_balance_efectivo_valor.grid(row=1, column=0, pady=(0,15))

		self.label_balance_titulo = tk.Label(
			self.balance_frame,
			text = "BALANCE GENERAL",
			font=("Segoe UI", 13),
			background='#D8E0C7'
		)
		self.label_balance_titulo.grid(row=0, column=1, pady=(15,0))

		self.label_balance = tk.Label(
			self.balance_frame,
			textvariable=self.balance_valor,
			font=("Arial",18),
			background='#D8E0C7'
		)
		self.label_balance.grid(row=1, column=1, pady=(0,15))

		self.label_balance_banco = tk.Label(
			self.balance_frame,
			text = "BANCO",
			font=("Segoe UI", 8),
			background='#D8E0C7'
		)
		self.label_balance_banco.grid(row=0, column=2, pady=(20,0))

		self.label_balance_banco_valor = tk.Label(
			self.balance_frame,
			textvariable=self.balance_banco,
			font=("Arial",16),
			background='#D8E0C7'
		)
		self.label_balance_banco_valor.grid(row=1, column=2, pady=(0,15))


		###ENTRADA MONTO###
		vcmd = (self.entry_frame.register(self.validar_entero), "%P") #esta va con el validador de enteros

		self.entry_monto = ttk.Entry(
			self.entry_frame,
			validate="key",
			validatecommand=vcmd,
			justify="center",
		)
		self.entry_monto.grid(row=0, column=0, columnspan=2, padx=20, sticky="ew")


		###Switch maybe###
		self.metodo_pago = tk.StringVar(value="")
		billetera_button = tk.Radiobutton(
			self.entry_frame,
			text="Billetera",
			variable=self.metodo_pago,
            indicatoron=False,
			value="cash",
			bg="light steel blue",
			activebackground="steel blue",
			selectcolor="steel blue",
			activeforeground="#FFFFFF"

		)
		banco_button = tk.Radiobutton(
			self.entry_frame,
			text="Banco",
			variable=self.metodo_pago,
            indicatoron=False,
			value="bank",
			bg="light steel blue",
			activebackground="steel blue",
			selectcolor="steel blue",
			activeforeground="#FFFFFF"
		)
		
		billetera_button.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
		banco_button.grid(row=2, column=1, pady=5, padx=20, sticky="ew")


		###BOTONES_MONTO###
		self.boton_ingreso = tk.Button(
			self.entry_frame,
			text="INGRESO",
			background="#6E7D4E",
			activebackground="#6E7D4E",
			fg="LemonChiffon2",
			command=self.agregar_ingreso
		)
		self.boton_ingreso.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

		self.boton_egreso = tk.Button(
			self.entry_frame,
			text="EGRESO",
			background="#AA7229",
			activebackground="#AA7229",
			fg="LemonChiffon2",
			command=self.agregar_egreso
		)
		self.boton_egreso.grid(row=3, column=1, pady=5, padx=20, sticky="ew")
		

		###TABLA###
		self.tree = ttk.Treeview(
			self.treeview_frame,
			columns=("fecha", "tipo", "metodo", "monto"),
			show="headings",
			selectmode="browse",
		)

		self.actualizar_balance
		self.tree.heading("fecha", text="Fecha")
		self.tree.heading("tipo", text="Tipo")
		self.tree.heading("metodo", text="Método")
		self.tree.heading("monto", text="Monto")


		self.tree.tag_configure("ingreso", foreground="#6E7D4E")
		self.tree.tag_configure("egreso", foreground="#AA7229")


		self.tree.column("fecha", width=94, anchor="center")
		self.tree.column("tipo", width=70, anchor="center", stretch= False)
		self.tree.column("metodo", width=80, anchor="center", stretch= False)
		self.tree.column("monto", width=110, anchor="e")

		self.tree.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")


		self.tree.bind("<Button-1>", self.bloquear_ajuste)
		self.tree.bind("<<TreeviewSelect>>", self.habilitar_eliminar)


		###ELSCROLL_VERTICAL###
		self.scrollbar = ttk.Scrollbar(
			self.treeview_frame,
			orient="vertical",
			command=self.tree.yview
		)
		self.tree.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.grid(row=0, column=1, sticky="ns", pady=10)


		###BOTON_ELIMINAR###
		self.boton_eliminar = tk.Button(
			self.treeview_frame,
			font=("Segoe UI", 10),
			text="Eliminar",
			command=self.eliminar_movimiento,
			state="disabled",
			background="#F0C48C"
		)
		self.boton_eliminar.grid(row=1, column=0, pady=(0,10))

	


	def cargar_tabla(self):
		for elemento in self.tree.get_children():
			self.tree.delete(elemento)

		self.movimientos_ord = self.registro.obtener_movimientos_ordenados()

		for movimiento in self.movimientos_ord:
			fecha = datetime.strptime(movimiento.fecha, "%Y-%m-%dT%H:%M:%S.%f")
			fecha_con_formato = fecha.strftime("%d-%m-%Y")
			monto_f = (f"{movimiento.monto:,.0f}")
			if movimiento.tipo == "ingreso":
				tag_tipo = "ingreso"
			else:
				tag_tipo = "egreso"
			self.tree.insert(
				"",
				"end",
				iid=movimiento.id,
				values=(fecha_con_formato, movimiento.tipo, movimiento.metodo, monto_f),
				tags=(tag_tipo))

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
			print(f"Eliminando... {id_movimiento}")
			self.registro.eliminar(id_movimiento)
			self.cargar_tabla()


	def habilitar_eliminar(self, event=None): #se supone que desactiva el boton de eliminación hasta que se haya seleccionado un elemento
		seleccion = self.tree.selection()
		if seleccion:
			self.boton_eliminar.config(state="normal")
		else:
			self.boton_eliminar.config(state="disabled")

	
	def deseleccionar_tabla(self, event):
		widget = event.widget

		if widget != self.tree and widget != self.boton_eliminar:
			self.tree.selection_remove(self.tree.selection())


	def agregar_ingreso(self):
		valor = self.entry_monto.get().strip()

		metodo_valor = self.metodo_pago.get()

		if not valor:
			messagebox.showwarning("Campo vacio", "Ingrese un monto.")
			return
		
		if not metodo_valor:
			messagebox.showwarning("Sin Selección", "Seleccione un método de pago.")
			return

		try:
			monto = float(valor)
		except ValueError:
			messagebox.showerror("Error", "Ingrese un número válido.")
			return

		if monto <= 0:
			messagebox.showwarning("Valor inválido", "El monto debe ser mayor a cero.")
			return


		self.registro.agregar(monto, "ingreso", metodo_valor)
		self.cargar_tabla()
		self.entry_monto.delete(0, tk.END)
		self.entry_monto.focus()


	def agregar_egreso(self):
		valor = self.entry_monto.get().strip()

		metodo_valor = self.metodo_pago.get()

		if not valor:
			messagebox.showwarning("Campo vacio", "Ingrese un monto.")
			return
		
		if not metodo_valor:
			messagebox.showwarning("Sin Selección", "Seleccione un método de pago.")
			return

		try:
			monto = float(valor)
		except ValueError:
			messagebox.showerror("Error", "Ingrese un número válido.")
			return

		if monto <= 0:
			messagebox.showwarning("Valor inválido", "El monto debe ser mayor a cero.")
			return


		self.registro.agregar(monto, "egreso", metodo_valor)
		self.cargar_tabla()
		self.entry_monto.delete(0, tk.END)
		self.entry_monto.focus()	


	def validar_entero(self, valor):
		if valor == "":
			return True #Segun que para permitir borrar y eso

		return valor.isdigit()

		#Anotación: para que se pase este filtro solo debe devolver True en esta función, todo lo False es off


	def actualizar_balance(self):
		balance = self.registro.balance_general()
		self.balance_valor.set(f"{balance:,.0f}")

		balance_billetera = self.registro.balance_puntual("cash")
		self.balance_efectivo.set(f"{balance_billetera:,.0f}")

		balance_banco = self.registro.balance_puntual("bank")
		self.balance_banco.set(f"{balance_banco:,.0f}")


	def comprobacion(self):
		self.balance_valor += 1
		if self.tree.selection():
			print(f"ok, {self.tree.selection()}")
		else:
			print("not")