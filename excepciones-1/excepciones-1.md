# Excepciones en Python - Primera Parte: No las estás usando lo suficiente.

¿Alguna vez estuviste googleando durante horas cómo "hacer que funcione" una librería?
¿Te preguntaste cómo hacer que tu código quede un poco más fácil de leer y de modificar?
¿Te interesaría conocer más acerca de técnicas utilizadas en IA?

Para responder estas preguntas y, por qué no, generar otras, es que desde Ninja quisimos abrir un nuevo espacio de comunicación. 

Este artículo forma parte de una serie de conceptos que son, de cierta manera, periféricos a la Ciencia de Datos. Aprender estas cosas es necesario porque lo que vamos a ver en estos posts son conceptos bastante transversales a los proyectos que quieran hacer: permiten mejorar *un poquito todos los códigos*. Además, saber por qué se usan quizás nos ayude a entender mejor cuándo y por qué implementarlo.

Sin más introducciones, vamos ahora sí al tema que nos ocupa en este caso: las **excepciones en Python**.

## ¿Qué es "manejar los errores"?

Supongamos que alguien nos pide como tarea hacer una función que sume listas: es decir, dadas `lista1 = [1, 2, 3]` y `lista2 = [10, 20, 30]` nos devuelva `[11, 22, 33]`.
Para resolver este problema, hacemos una función[^1]:

```python
def sumar_listas(lista1, lista2):
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total
```

La probamos sobre nuestro ejemplo y :heart-eyes:

```python
>>> lista1 = [1, 2, 3]
>>> lista2 = [10, 20, 30]
>>> sumar_listas(lista1, lista2)
[11, 22, 33]
```

Pero en todas las historias hay un villano, y en este caso es alguien que quiere sumar la lista `lista1 = [1, 2, 3]` con `lista2 = [10, 20, 30, 40]` (es un villano bastante modesto[^2]).
Nosotros sabemos que sumar eso *no tiene sentido* porque las listas no tienen el mismo tamaño, pero nuestra función no:

```python
>>> lista1 = [1, 2, 3]
>>> lista2 = [10, 20, 30, 40]
>>> sumar_listas(lista1, lista2)
[11, 22, 33]
```

Queda claro que acá alguien está haciendo algo mal (nuestro villano) y nuestro programa no está preparado para lidiar con esto.
Pensamos una solución: como la suma de las listas tienen que ser una lista, podemos usar un entero como marca de que "algo anduvo mal".
Por ejemplo, si las listas son de distinto tamaño, devolvemos `-1`.
Entonces queda:

```
def sumar_listas_error(lista1, lista2):
    if len(lista1) != len(lista2):
        return -1
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total
>>> sumar_listas_error([1, 2, 3], [10, 20, 30])
[11, 22, 33]
>>> sumar_listas_error([1, 2, 3], [10, 20, 30, 40])
-1
```

Esta técnica que estamos usando es una implementación casera de manejo de errores, y no está nada mal.
Tiene algunas complicaciones y limitaciones, claro.
La primera es que tenemos que recordar que el `-1` quiere decir que hubo un error.
Y la segunda es que éste no es el único error que se puede generar.
También seguramente queramos decir que hubo un error si tratamos de sumar listas con `strings` adentro: `lista1 = ['uno', 2, 3]` y `lista2 = ['diez', 20, 30]`.
O sea que, con nuestra implementación casera, no sólo tenemos que chequear si está este error, sino además sería ideal elegir otro número (digamos `-2`) para avisar que el error es distinto.
Y hay que recordar qué significa ese número... y después elegir qué hacer si tenemos ese error!

Siempre es bueno tener un manejo de errores, y si eligen usar éste, ¡bienvenido sea![^3]
Es **claramente** mejor que nada.
Pero implica que tenemos que encargarnos *nosotros* como programadores de tres "problemas":

1. Recordar qué quieren decir `-1`, `-2`, etcétera.
2. Andar pasando el error de función en función. Además... ¿qué hacemos si `-1` o `-2` son resultados posibles de nuestra función?
3. Chequear a cada rato si la función tiró un error y decidir qué hacer.

Manejar errores de repente pone una montaña de cosas bajo nuestra responsabilidad.
En general, es mejor depender de soluciones usadas en la comunidad antes que crear la propia.
Hay una gran cantidad de motivos para justificar esto, algunos que todos tenemos presentes, otros que quizás no tanto.
Pero mejor que eso sea tarea de otro post.
Por lo pronto, en Python hay una forma mucho más linda, pensada desde el comienzo del lenguaje, que se comporta bien en todas las librerías.
En fin, más... *Pythónica*

## El manejo de las excepciones de Python. Lanzar y capturar.

Obviando los errores de sintaxis (como por ejemplo olvidarse un `:` después de un `if`), Python maneja los errores a través de las excepciones.
Qué pasa por ejemplo, si tratamos de sumar un `string` con un `int`?

```python
>>> '2' + 3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot concatenate 'str' and 'int' objects

```

Ese `TypeError` que aparece ahí es una de las *excepciones* estándar de Python (tiene unas cuantas decenas) de las que veníamos hablando.
Esto resuelve el primer problema: es un error de Tipo.
Hasta escribe en pantalla (más o menos) cuál es el problema.
Ahora, para explicar cómo resuelve los otros dos problemas tenemos que cambiar la mentalidad.
Vamos a responder al problema 2 (cómo pasar el error de función en función) respondiendo a una pregunta *similar*: cómo hago para alertar al programa **en general** de un error.

### Lanzar excepciones

Para esto, Python usa un carril paralelo al de los valores que devuelve en las funciones (fíjense que esto resuelve el bonus del problema `2.`: qué hacer si nuestro código de error es un valor esperado por la función).
Imaginen que cada vez que ejecutamos una función nos metemos "un paso más abajo" en el código.
En este caso, la excepción **frena todo y sube de golpe**.
Este proceso de "alertar" se llama en la jerga *lanzar una excepción* y, en Python, se lanzan con `raise`.
En nuestro ejemplo de `sumar_listas` podemos pedir que cuando las listas tienen distinto tamaño, se *lance la excepción* `ValueError` (es una de las excepciones estándar de Python).
En ese caso, nuestra función se vería
```python
def sumar_listas_lanza(lista1, lista2):
    if len(lista1) != len(lista2):
        raise ValueError("Las listas tienen distinto tamaño")
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total
```
y si ahí tratamos de sumar las listas que habíamos dicho antes, tenemos
```
>>> sumar_listas_lanza([1, 2, 3], [10, 20, 30, 40])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "sumar_listas.py", line 18, in sumar_listas_lanza
    raise ValueError("Las listas tienen distinto tamaño")
ValueError: Las listas tienen distinto tamaño
```

Fíjense que encima nos dice que el error está en `sumar_listas_lanza`, y hasta la línea del archivo! No podemos pedir mucho más.

## Capturar excepciones

Bueno, quizás sí podemos pedir un poco más... ¿qué pasa si queremos hacer algo cuando hay un error?
Muy bueno lo del error y eso, pero quizás no quiero que cuando pase algo que no esperaba el programa se detenga por completo y se ponga a gritar ERROR ERROR.
Supongamos que quiero llamar a esta función, pero que si ambas listas son de distinto tamaño, directamente me devuelva la primera de ambas.
Una posibilidad sería que en vez del `raise` que pusimos adentro, pogamos un `return` de la lista por defecto... pero medio que estamos tirando todo por la borda.
Estábamos conformes con que fuera un error, simplemente queremos tratar de intervenir mientras *va subiendo* antes de que detenga todo el programa.
Además, en ese caso, la función no debería llamarse `sumar_lista`, sino `sumar_lista_excepto_que_sean_de_distinto_tamano_etcétera` (más allá del nombre, la función ya no sólo "sumaría dos listas").

Lo que tenemos que hacer es **capturar la excepción**.
El ejemplo se ve más claro si imagináramos que una función está llamado a nuestro `sumar_listas_lanza` y, con el resultado, hace algo.
Por ejemplo, la función `maximo_suma` que ponemos aquí devuelve el máximo de la suma de las listas.

```python
def maximo_suma(lista1, lista2):
    suma = sumar_listas_lanza(lista1, lista2)
    maximo = max(suma)
    return maximo
```

Las excepciones se capturan con los bloques de `try`/`except`.
Como casi todo lo que está desarrollado en Python, se puede tratar de "leer" directamente: quiere decir *intentá* X, *excepto* que pase Y.
Nosotros podríamos *intentar* `sumar_listas_lanza`, *excepto* que haya un `ValueError` y, en ese caso, usamos la primera lista, `lista1`:

```python
def maximo_suma(lista1, lista2):
    try:
        resultado = sumar_listas_lanza(lista1, lista2)
    except ValueError:
        resultado = lista1
    maximo = max(resultado)
    return maximo
```

## En conclusión

Tener un sistema de manejo de errores es importante, y Python nos permite que las excepciones vayan por *un carril separado* a las funciones.
Aprovechando eso, los códigos quedan mucho más claros, tanto al leerlos como al ejecutarlos.
En la próxima edición, vamos a ver cómo usar las excepciones de Python para controlar el flujo de ejecución y cómo crear nuestras propias excepciones.

[^1]: El código que escribimos aquí no va a ser 100% "pythonico" (más de uno podría poner el grito en el cielo porque usemos `for i in range(len(a))`); pero priorizamos que se entienda el concepto.

[^2]: Está bueno pensar siempre en cómo se comporta nuestro código fuera del comportamiento que teníamos en mente; la técnica de pensar que estamos programando para evitar que un "villano" haga que nuestro código dé resultados incoherentes es bastante útil.

[^3]: De hecho, es parecido al que usa nada menos que el kernel de Linux. Claro, no tienen muchas más alternativas
