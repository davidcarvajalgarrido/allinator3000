class Horse:
	# Clase base: Pegasus y Unicorn heredarán de aquí.
	def __init__(self, name, age, color, max_speed, energy):
		self.name = name
		self.age = age
		self.color = color
		self.max_speed = max_speed
		self.energy = energy

	def neigh(self):
		return f"{self.name} dice: hiiiii"

	def run(self, km):
		cost = km * 5
		if cost > self.energy:
			return f"{self.name} no tiene energía suficiente para correr {km} km."

		self.energy -= cost
		return f"{self.name} corrió {km} km y le quedan {self.energy} puntos de energía."

	def eat(self, amount):
		self.energy += amount
		return f"{self.name} comió y ahora tiene {self.energy} puntos de energía."

	def rest(self, hours):
		recovery = hours * 10
		self.energy += recovery
		return f"{self.name} descansó {hours} horas y recuperó energía hasta {self.energy}."
