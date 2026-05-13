from horse import Caballo

class Pegaso(Caballo):
	def __init__(self, nombre, edad, color, velocidad_maxima, energia, altura_de_vuelo):
		# Herencia: reutilizamos los atributos comunes del caballo.
		super().__init__(nombre, edad, color, velocidad_maxima, energia)

		# Atributo propio de Pegaso.
		self.altura_de_vuelo = altura_de_vuelo

	# Método específico de la subclase.
	def volar(self, metros):
		gasto = metros // 10
		if gasto > self.energia:
			return f"{self.nombre} no tiene energía suficiente para volar {metros} metros."

		self.energia -= gasto
		return (
			f"{self.nombre} voló a {self.altura_de_vuelo} metros de altura "
			f"durante {metros} metros y ahora tiene {self.energia} de energía."
		)