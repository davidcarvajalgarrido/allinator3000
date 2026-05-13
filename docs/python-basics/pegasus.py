from horse import Horse


class Pegasus(Horse):
	def __init__(self, name, age, color, max_speed, energy, flight_height):
		# Herencia: reutilizamos los atributos comunes del caballo.
		super().__init__(name, age, color, max_speed, energy)

		# Atributo propio de Pegasus.
		self.flight_height = flight_height

	# Método específico de la subclase.
	def fly(self, meters):
		cost = meters // 10
		if cost > self.energy:
			return f"{self.name} no tiene energía suficiente para volar {meters} metros."

		self.energy -= cost
		return (
			f"{self.name} voló a {self.flight_height} metros de altura "
			f"durante {meters} metros y ahora tiene {self.energy} de energía."
		)