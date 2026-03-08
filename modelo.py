import os, json
from datetime import datetime


class Movimiento:
	def __init__(self, id, monto, tipo):
		self.id = id
		self.fecha = datetime.now().isoformat()
		self.monto = float(monto)
		self.tipo = tipo  #solo "ingreso" o "egreso"


	def to_dict(self):
		return {
		"id": self.id,
		"fecha": self.fecha,
		"monto": self.monto,
		"tipo": self.tipo

		}

	@staticmethod
	def from_dict(data):
		obj = Movimiento(data["id"], data["monto"], data["tipo"])
		obj.fecha = data["fecha"]
		return obj

	def __repr__(self):
		return f"[{self.id}] {self.fecha} | {self.tipo.upper()} | {self.monto}"

class RegistroFinanzas:
	def __init__(self):
		self.movimientos = []
		self._ultimo_id = 0
		self.archivo = "data.json"
		self.cargar()

			

	def cargar(self):
		if not os.path.exists(self.archivo):
			return

		if os.path.getsize(self.archivo) == 0:
			return

		try:	
			with open(self.archivo, "r") as f:	
				datos = json.load(f)
				for item in datos:
					movimiento = Movimiento.from_dict(item)
					self.movimientos.append(movimiento)
					self._ultimo_id = max(self._ultimo_id, movimiento.id)
		except json.JSONDecodeError:
			print("Advertencia: archivo JSON corrupto o inválido.")			

	def guardar(self):
		with open(self.archivo, "w") as f:
			json.dump(
				[mov.to_dict() for mov in self.movimientos],
				f,
				indent=4
			)


	def agregar(self, monto, tipo):
		self._ultimo_id += 1
		movimiento = Movimiento(self._ultimo_id, monto, tipo)
		self.movimientos.append(movimiento)
		self.guardar()

	def eliminar(self, id):
		id = int(id)
		self.movimientos = [
			mov for mov in self.movimientos if mov.id != id
		]	#esto es elegante como el infierrrrno
		self.guardar()


	def balance(self):
		return sum(
			mov.monto if mov.tipo == "ingreso" else -mov.monto
			for mov in self.movimientos
			)

	def mostrar(self):
		for mov in self.movimientos:
			print(mov)

	def obtener_movimientos_ordenados(self): #de más nuevo a más viejo, por el reverse
		return sorted(
			self.movimientos,
			key=lambda n: n.fecha,
			reverse=True
		)

###PRUEBAS###

if __name__ == "__main__":

	registro = RegistroFinanzas()


	registro.agregar(500000, "ingreso")
	registro.agregar(1200000, "ingreso")
	registro.agregar(700000, "egreso")

	print("Movimiento:")
	registro.mostrar()

	print("\nBalance actual: ", registro.balance())


	print("\nEliminando ID 2...\n")
	registro.eliminar(2)

	registro.mostrar()
	print("\nBalance actual:", registro.balance())


