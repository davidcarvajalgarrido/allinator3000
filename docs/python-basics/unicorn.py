from horse import Horse


class Unicorn(Horse):
	def __init__(self, name, age, color, max_speed, energy, horn_color):
		# Herencia: Unicorn parte de la clase base Horse.
		super().__init__(name, age, color, max_speed, energy)
		# Atributo propio de Unicorn.
		self.horn_color = horn_color

	# Método específico de la subclase.
	def cast_magic(self):
		if self.energy < 15:
			return f"{self.name} no tiene energía suficiente para usar su magia."

		self.energy -= 15
		return (
			f"{self.name} lanzó un brillo mágico con su cuerno {self.horn_color} "
			f"y le quedan {self.energy} puntos de energía."
		)