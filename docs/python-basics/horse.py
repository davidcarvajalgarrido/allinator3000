class Caballo:
	# Clase base: Pegaso y Unicornio heredarán de aquí.
	def __init__(self, nombre, edad, color, velocidad_maxima, energia):
		self.nombre = nombre
		self.edad = edad
		self.color = color
		self.velocidad_maxima = velocidad_maxima
		self.energia = energia

	def relinchar(self):
		return f"{self.nombre} dice: hiiiii"

	def correr(self, kilometros):
		gasto = kilometros * 5
		if gasto > self.energia:
			return f"{self.nombre} no tiene energía suficiente para correr {kilometros} km."

		self.energia -= gasto
		return f"{self.nombre} corrió {kilometros} km y le quedan {self.energia} puntos de energía."

	def comer(self, cantidad):
		self.energia += cantidad
		return f"{self.nombre} comió y ahora tiene {self.energia} puntos de energía."

	def descansar(self, horas):
		recuperacion = horas * 10
		self.energia += recuperacion
		return f"{self.nombre} descansó {horas} horas y recuperó energía hasta {self.energia}."
