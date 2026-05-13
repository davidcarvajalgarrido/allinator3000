from horse import Horse
from pegasus import Pegasus
from unicorn import Unicorn


def main():
	# Objeto de la clase base.
	horse = Horse("Babieca", 6, "marrón", 55, 80)
	# Objetos de clases derivadas.
	pegasus = Pegasus("Nube", 4, "blanco", 70, 90, 1200)
	unicorn = Unicorn("Destello", 5, "plateado", 60, 85, "dorado")

	# Polimorfismo por inclusión: distintas clases comparten el método heredado.
	print(horse.neigh())
	print(pegasus.neigh())
	print(unicorn.neigh())

	# Métodos propios de cada clase.
	print(horse.eat(15))
	print(horse.run(8))
	print(pegasus.fly(300))
	print(unicorn.cast_magic())


if __name__ == "__main__":
	main()