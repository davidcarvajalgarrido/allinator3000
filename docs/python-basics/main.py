from horse import Caballo
from pegaso import Pegaso
from unicornio import Unicornio

def main():
	# Objeto de la clase base.
	caballo = Caballo("Babieca", 6, "marron", 55, 80)
	# Objetos de clases derivadas.
	pegaso = Pegaso("Nube", 4, "blanco", 70, 90, 1200)
	unicornio = Unicornio("Destello", 5, "plateado", 60, 85, "dorado")

	# Polimorfismo por inclusión: distintas clases comparten el método heredado.
	print(caballo.relinchar())
	print(pegaso.relinchar())
	print(unicornio.relinchar())

	# Métodos propios de cada clase.
	print(caballo.comer(15))
	print(caballo.correr(8))
	print(pegaso.volar(300))
	print(unicornio.lanzar_magia())

if __name__ == "__main__":
	main()