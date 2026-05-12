# Python basico para gente que viene de JavaScript

Este apunte resume equivalencias utiles entre Python y JavaScript y prepara el terreno para tres temas que suelen marcar un antes y un despues al empezar con Python: decoradores, iteradores y generadores.

La idea no es memorizar sintaxis aislada, sino entender el modelo mental de Python.

## 1. Variables y tipos: parecido, pero mas explicito

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
- La indentacion forma parte de la sintaxis.

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

Python tambien tiene ternario, pero el orden cambia respecto a JavaScript.

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

Nota importante: dentro de la expresion del f-string conviene usar comillas simples si el string exterior usa comillas dobles.

## 5. Bucles: recorrer valores e indices

Una diferencia habitual al venir de JavaScript es querer sacar indice y valor directamente de una lista.

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

Sin `enumerate()`, un `for item in fruits` solo te da el valor, no el indice.

## 6. Alcance de variables y cierres

Python tambien tiene closures, igual que JavaScript.

```python
x = 300

def show_value():
    print(x)

show_value()  # 300
```

La funcion puede leer una variable definida fuera de ella, siempre que este en un alcance accesible.

Esto es importante porque los decoradores se apoyan precisamente en funciones que devuelven otras funciones.

## 7. Decoradores

### Que es un decorador

Un decorador es una funcion que recibe otra funcion y devuelve una nueva funcion con comportamiento extra.

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

La forma comun en Python usa `@`:

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

### Como leer mentalmente `@decorator`

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

### Para que sirven

Casos tipicos:

- logging
- medir tiempo
- validaciones
- control de acceso
- reutilizar comportamiento sin ensuciar la logica principal

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

- El iterable es la coleccion recorrible.
- El iterador es el mecanismo que va avanzando por esa coleccion.

## 9. Generadores

### Que es un generador

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

Con `return`, la funcion termina.
Con `yield`, la funcion se pausa y puede continuar despues.

Eso hace que los generadores sean utiles cuando:

- hay muchos datos
- no quieres cargarlos todos en memoria
- quieres producir resultados bajo demanda

### Paralelismo con JavaScript

JavaScript tambien tiene generadores:

```javascript
function* myGenerator() {
  yield 1;
  yield 2;
  yield 3;
}
```

La idea es la misma, aunque en Python esta mucho mas integrada en el dia a dia.

## 10. Relacion entre iteradores y generadores

Un generador es un iterador.

Eso significa que puedes hacer esto:

```python
generator = my_generator()

print(next(generator))
print(next(generator))
print(next(generator))
```

Y obtendras los valores uno a uno, igual que con cualquier iterador.

La diferencia es que el generador no lo has construido a mano: Python lo crea a partir de una funcion con `yield`.

## 11. Resumen rapido para gente que viene de JS

| Idea | JavaScript | Python |
| --- | --- | --- |
| Variable | `const x = 8` | `x = 8` |
| Longitud | `arr.length` | `len(arr)` |
| Ternario | `cond ? a : b` | `a if cond else b` |
| Template string | `` `Hola ${x}` `` | `f"Hola {x}"` |
| Array con indice | `forEach((item, i) => ...)` | `for i, item in enumerate(lista):` |
| Funcion que envuelve otra | funcion de orden superior | decorador |
| Produccion perezosa de valores | generator function | funcion con `yield` |

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

## 13. Ideas clave para cerrar

- Python busca legibilidad antes que ruido sintactico.
- `enumerate()` es tu amigo cuando necesitas indice y valor.
- Un decorador envuelve funciones.
- Un iterador entrega valores de uno en uno.
- Un generador es la forma mas comoda de crear iteradores con `yield`.

Si entiendes bien esas cinco ideas, ya tienes una base muy solida para seguir profundizando.