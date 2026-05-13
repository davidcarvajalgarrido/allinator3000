# Python básico para gente que viene de JavaScript

Este apunte resume equivalencias útiles entre Python y JavaScript y prepara el terreno para varios temas que suelen marcar un antes y un después al empezar con Python: decoradores, iteradores, generadores y una primera base de POO.

La idea no es memorizar sintaxis aislada, sino entender el modelo mental de Python.

## 1. Variables y tipos: parecido, pero más explícito

En Python no se declaran variables con `let` o `const`.
Se asignan directamente:

```python
my_number = 8
my_age = 12
```

Equivalencia mental:

```javascript
const myNumber = 8;
const myAge = 12;
```

Diferencias importantes:

- Python suele usar `snake_case` en nombres de variables y funciones.
- No hay llaves ni punto y coma.
- La indentación forma parte de la sintaxis.

## 2. Tuplas, listas y longitud

En JavaScript solemos pensar en arrays. En Python hay varios tipos de colecciones.

### Lista

Una lista es lo mas parecido a un array mutable de JavaScript:

```python
fruits = ["apple", "banana", "cherry"]
```

```javascript
const fruits = ["apple", "banana", "cherry"];
```

### Tupla

Una tupla se parece a una lista, pero no se modifica:

```python
coords = (3, 4, 5)
```

La longitud se obtiene con `len()`:

```python
coords = (3, 4, 5)
total_positions = len(coords)

print(total_positions)  # 3
```

```javascript
const coords = [3, 4, 5];
const totalPositions = coords.length;
```

## 3. Condicionales y ternario

Python también tiene ternario, pero el orden cambia respecto a JavaScript.

### JavaScript

```javascript
const label = myAge > 17 ? "mayor" : "menor";
```

### Python

```python
label = "mayor" if my_age > 17 else "menor"
```

Observa la estructura:

```python
valor_si_true if condicion else valor_si_false
```

## 4. f-strings: el equivalente a template literals

Si en JavaScript usas template literals con backticks, en Python lo normal son los f-strings:

```python
my_age = 12
print(f"Hola, soy {'mayor' if my_age > 17 else 'menor'} de edad")
```

```javascript
const myAge = 12;
console.log(`Hola, soy ${myAge > 17 ? "mayor" : "menor"} de edad`);
```

Nota importante: dentro de la expresión del f-string conviene usar comillas simples si el string exterior usa comillas dobles.

## 5. Bucles: recorrer valores e índices

Una diferencia habitual al venir de JavaScript es querer sacar índice y valor directamente de una lista.

### JavaScript

```javascript
const fruits = ["apple", "banana", "cherry"];

fruits.forEach((item, index) => {
  console.log(`El elemento ${index} es ${item}`);
});
```

### Python

En Python usamos `enumerate()`:

```python
fruits = ["apple", "banana", "cherry"]

for index, item in enumerate(fruits):
    print(f"El elemento {index} es {item}")
```

Sin `enumerate()`, un `for item in fruits` solo te da el valor, no el índice.

## 6. Alcance de variables y cierres

Python también tiene closures, igual que JavaScript.

```python
x = 300

def show_value():
    print(x)

show_value()  # 300
```

La función puede leer una variable definida fuera de ella, siempre que esté en un alcance accesible.

Esto es importante porque los decoradores se apoyan precisamente en funciones que devuelven otras funciones.

## 7. Decoradores

### Qué es un decorador

Un decorador es una función que recibe otra función y devuelve una nueva función con comportamiento extra.

Idea mental en JavaScript:

```javascript
function wrap(fn) {
  return function () {
    return fn().toUpperCase();
  };
}
```

En Python:

```python
def uppercase_decorator(func):
    def wrapper():
        return func().upper()

    return wrapper
```

### Uso sin arroba

```python
def say_hi():
    return "hola"

decorated = uppercase_decorator(say_hi)
print(decorated())  # HOLA
```

### Uso con sintaxis de decorador

La forma común en Python usa `@`:

```python
def uppercase_decorator(func):
    def wrapper():
        return func().upper()

    return wrapper


@uppercase_decorator
def my_function():
    return "Hello Sally"


@uppercase_decorator
def say_goodbye():
    return "Ciao Sally"


print(my_function())
print(say_goodbye())
```

Salida:

```text
HELLO SALLY
CIAO SALLY
```

### Cómo leer mentalmente `@decorator`

Esto:

```python
@uppercase_decorator
def my_function():
    return "Hello Sally"
```

Equivale a esto:

```python
def my_function():
    return "Hello Sally"

my_function = uppercase_decorator(my_function)
```

### Para qué sirven

Casos típicos:

- logging
- medir tiempo
- validaciones
- control de acceso
- reutilizar comportamiento sin ensuciar la lógica principal

## 8. Iterables, iteradores e `iter()`

Estos tres conceptos suelen mezclarse al principio. Conviene separarlos.

### Iterable

Un iterable es algo que puedes recorrer con `for`.

Ejemplos:

- listas
- tuplas
- strings
- diccionarios
- generadores

```python
my_tuple = ("apple", "banana", "cherry")
```

Una tupla es iterable.

### Iterador

Un iterador es un objeto que sabe devolver el siguiente elemento uno a uno.

Lo obtenemos con `iter()`:

```python
my_tuple = ("apple", "banana", "cherry")
my_iterator = iter(my_tuple)

print(next(my_iterator))
print(next(my_iterator))
print(next(my_iterator))
```

Salida:

```text
apple
banana
cherry
```

Cuando ya no quedan elementos, `next()` lanza `StopIteration`.

### Idea mental

- El iterable es la colección recorrible.
- El iterador es el mecanismo que va avanzando por esa colección.

## 9. Generadores

### Qué es un generador

Un generador es una forma sencilla de crear iteradores.

En lugar de construir todos los valores de golpe y devolverlos con `return`, los produce poco a poco con `yield`.

```python
def my_generator():
    yield 1
    yield 2
    yield 3
```

Uso:

```python
for value in my_generator():
    print(value)
```

Salida:

```text
1
2
3
```

### Diferencia clave con `return`

Con `return`, la función termina.
Con `yield`, la función se pausa y puede continuar después.

Eso hace que los generadores sean útiles cuando:

- hay muchos datos
- no quieres cargarlos todos en memoria
- quieres producir resultados bajo demanda

### Paralelismo con JavaScript

JavaScript también tiene generadores:

```javascript
function* myGenerator() {
  yield 1;
  yield 2;
  yield 3;
}
```

La idea es la misma, aunque en Python está mucho más integrada en el día a día.

## 10. Relación entre iteradores y generadores

Un generador es un iterador.

Eso significa que puedes hacer esto:

```python
generator = my_generator()

print(next(generator))
print(next(generator))
print(next(generator))
```

Y obtendrás los valores uno a uno, igual que con cualquier iterador.

La diferencia es que el generador no lo has construido a mano: Python lo crea a partir de una función con `yield`.

## 11. Resumen rápido para gente que viene de JS

| Idea | JavaScript | Python |
| --- | --- | --- |
| Variable | `const x = 8` | `x = 8` |
| Longitud | `arr.length` | `len(arr)` |
| Ternario | `cond ? a : b` | `a if cond else b` |
| Template string | `` `Hola ${x}` `` | `f"Hola {x}"` |
| Array con índice | `forEach((item, i) => ...)` | `for i, item in enumerate(lista):` |
| Función que envuelve otra | función de orden superior | decorador |
| Producción perezosa de valores | generator function | función con `yield` |

## 12. Ejemplo final compacto

Este ejemplo junta varias ideas:

```python
def uppercase_decorator(func):
    def wrapper():
        return func().upper()

    return wrapper


@uppercase_decorator
def describe_age(age):
    label = "mayor" if age > 17 else "menor"
    return f"Hola, soy {label} de edad"


def countdown(limit):
    current = limit
    while current > 0:
        yield current
        current -= 1


print(describe_age(12))

for index, value in enumerate(countdown(3)):
    print(f"Paso {index}: {value}")
```

## 13. Ideas clave para cerrar esta primera parte

- Python busca legibilidad antes que ruido sintáctico.
- `enumerate()` es tu amigo cuando necesitas índice y valor.
- Un decorador envuelve funciones.
- Un iterador entrega valores de uno en uno.
- Un generador es la forma más cómoda de crear iteradores con `yield`.

Si entiendes bien esas cinco ideas, ya tienes una base muy sólida para seguir profundizando.

## 14. Clases y objetos: pasar de funciones a entidades con estado

Cuando entras en POO, la pregunta deja de ser solo "qué hace esta función" y pasa a ser también "quién tiene estos datos y estos comportamientos".

Una clase define una plantilla. Un objeto es una instancia concreta de esa plantilla.

```python
class Horse:
    def __init__(self, name, energy):
        self.name = name
        self.energy = energy

    def neigh(self):
        return f"{self.name} dice: hiiiii"
```

Uso:

```python
horse = Horse("Babieca", 80)
print(horse.neigh())
```

Idea mental:

- la clase es el molde
- el objeto es el valor real que vive en memoria
- `self` es la referencia al objeto actual

Si vienes de JavaScript, piensa en esto como una mezcla entre una `class` y un objeto con métodos, pero con una convención mucho más explícita alrededor de `self`.

## 15. `__init__` y `self`: las dos piezas que más se repiten al empezar

El método `__init__` se ejecuta al crear un objeto.

Sirve para inicializar sus atributos:

```python
class Horse:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

`self` no es una palabra reservada, pero en Python se usa siempre por convención.

Cuando escribes:

```python
horse = Horse("Babieca", 6)
```

Python crea el objeto y se lo pasa como primer argumento al método.

Por eso dentro de la clase escribimos `self.name`, `self.age`, etc.

## 16. Herencia: reutilizar una clase base

La herencia permite crear una clase nueva a partir de otra.

En nuestro ejemplo, `Pegasus` y `Unicorn` heredan de `Horse`.

```python
class Pegasus(Horse):
    def __init__(self, name, age, color, max_speed, energy, flight_height):
        super().__init__(name, age, color, max_speed, energy)
        self.flight_height = flight_height
```

`super()` sirve para reutilizar la lógica de la clase padre sin tener que copiarla.

La idea práctica es simple:

- `Horse` define lo común
- `Pegasus` añade lo que solo tiene un pegaso
- `Unicorn` añade lo que solo tiene un unicornio

## 17. Polimorfismo por inclusión

Este es el polimorfismo clásico de herencia.

Distintas clases comparten una interfaz común porque vienen de la misma base o porque redefinen el mismo método.

Con nuestro ejemplo, `Horse`, `Pegasus` y `Unicorn` pueden responder a `neigh()`:

```python
print(horse.neigh())
print(pegasus.neigh())
print(unicorn.neigh())
```

La gracia no es que hagan algo muy distinto, sino que desde fuera los tratas de forma uniforme.

Eso es exactamente la idea de polimorfismo por inclusión: varios objetos pueden entrar en el mismo hueco conceptual porque comparten contrato.

## 18. Juntando herencia y polimorfismo por inclusión en el mismo ejemplo

En el código que hemos montado hoy aparecen esas dos ideas de forma bastante limpia:

- `Pegasus` y `Unicorn` heredan de `Horse`: eso es herencia.
- Los tres pueden usar `neigh()`: eso es polimorfismo por inclusión.

Visto desde fuera:

```python
horse = Horse("Babieca", 6, "marrón", 55, 80)
pegasus = Pegasus("Nube", 4, "blanco", 70, 90, 1200)
unicorn = Unicorn("Destello", 5, "plateado", 60, 85, "dorado")

print(horse.neigh())
print(pegasus.neigh())
print(unicorn.neigh())

print(horse.eat(15))

print(pegasus.fly(300))
print(unicorn.cast_magic())
```

Fíjate en la diferencia:

- `neigh()` es común a las tres clases porque `Pegasus` y `Unicorn` lo heredan.
- `fly()` solo tiene sentido en `Pegasus`.
- `cast_magic()` solo tiene sentido en `Unicorn`.

Eso deja bastante clara la separación entre lo común y lo específico.

## 19. Resumen rápido de POO para quedarte con lo importante

| Idea | Traducción práctica |
| --- | --- |
| Clase | El molde |
| Objeto | Una instancia concreta |
| Atributo | Un dato guardado en el objeto |
| Método | Una función dentro de la clase |
| Herencia | Reutilizar una clase base |
| Polimorfismo por inclusión | Distintos objetos responden al mismo mensaje |

## 20. Ideas clave para cerrar

- Una clase junta datos y comportamiento.
- `__init__` prepara el estado inicial del objeto.
- `self` apunta al objeto actual.
- La herencia evita duplicar lo común.
- El polimorfismo por inclusión te deja tratar varios objetos de forma uniforme.

Si entiendes estas ideas y las relacionas con el ejemplo de `Horse`, `Pegasus` y `Unicorn`, ya tienes una base muy útil para empezar a leer y escribir POO en Python con criterio.