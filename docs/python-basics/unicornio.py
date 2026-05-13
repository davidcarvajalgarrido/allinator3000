from horse import Caballo

class Unicornio(Caballo):
	def __init__(self, nombre, edad, color, velocidad_maxima, energia, color_del_cuerno):
		# Herencia: Unicornio parte de la clase base Caballo.
		super().__init__(nombre, edad, color, velocidad_maxima, energia)
		# Atributo propio de Unicornio.
		self.color_del_cuerno = color_del_cuerno

	# Método específico de la subclase.
	def lanzar_magia(self):
		if self.energia < 15:
			return f"{self.nombre} no tiene energía suficiente para usar su magia."

		self.energia -= 15
		return (
			f"{self.nombre} lanzó un brillo mágico con su cuerno {self.color_del_cuerno} "
			f"y le quedan {self.energia} puntos de energía."
		)