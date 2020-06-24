# Argumentos opcionales en Python: ¿por qué no hay que usar listas?

Imaginemos esta función (que, ustedes dirán, es bastante tonta) que agrega un elemento a una lista inicial, ambos argumentos de la función.
Pero además, queremos que *por defecto*, la lista inicial esté vacía, así que pasarle sólo un `elemento` a la función implique devolver una lista con únicamente ese elemento:
```python
def agregar_a_lista(elemento, inicial=[]):
    inicial.append(elemento)
    return inicial
```

Así que vamos a usar nuestra humilde, pero correcta función!
```python
>>> una_lista_larga = agregar_a_lista(5, [2, 3])
>>> print(una_lista_larga)
[2, 3, 5]
>>> una_lista_corta = agregar_a_lista(5)
>>> print(una_lista_corta)
>>> otra_lista_corta = agregar_a_lista(7)
```

Todo parece andar bien, y `otra_lista_corta` debería dar `[7]`.
Sin embargo...

```python
>>> print(otra_lista_corta)
[5, 7]
```

QUÉ!? ¿Qué pasó? ¿Se "acuerda" de que antes le había agregado un 5?

# ¿Cuándo se calculan los valores por defecto?

Esta es la primera pregunta que nos va a ayudar a entender lo que está sucediendo.
Para eso, vamos a usar: 1. el método `__defaults__`, que nos permite ver los valores por defecto de una función; y 2. el built-in `id` que nos devuelve una referencia única a cada objeto (es decir, dos objetos tienen el mismo `id` si y sólo si son el mismo objeto).
Ahora comenzamos de cero un 

```python
def agregar_a_lista(elemento, inicial=[]):
    inicial.append(elemento)
    return inicial


valores_por_defecto = agregar_a_lista.__defaults__
identidades = [id(valor) for valor in agregar_a_lista.__defaults__]
print(f"Valores por defecto: {valores_por_defecto}")
print(f"Identidades: {identidades}")

print("Ejecutando una_lista = agregar_a_lista(5)")
una_lista = agregar_a_lista(5)
print(f"Resultado: {una_lista}")

valores_por_defecto = agregar_a_lista.__defaults__
identidades = [id(valor) for valor in agregar_a_lista.__defaults__]
print(f"Valores por defecto: {valores_por_defecto}")
print(f"Identidades: {identidades}")

print("Ejecutando otra_lista = agregar_a_lista(7)")
otra_lista = agregar_a_lista(7)
print(f"Resultado: {otra_lista}")
```

Cuando ejecutamos ese script, obtenemos:

```
Valores por defecto: ([],)
Identidades: [140611099623168]
Ejecutando una_lista = agregar_a_lista(5)
Resultado: [5]
Valores por defecto: ([5],)
Identidades: [140611099623168]
Ejecutando otra_lista = agregar_a_lista(7)
Resultado: [5, 7]
```

Efectivamente, la función se *acuerda* de que le agregamos un 5, pero porque el objeto es el mismo (fíjense que las identidades concuerdan).
La primera vez que ejecutamos la función, modificamos su valor; entonces, la segunda vez que lo usamos, lo tomamos con el valor modificado.
La primera conclusión sería: no modifiquemos los valores por defecto dentro de una función de Python o, más general y más seguro, **no usemos objetos mutables como valores por defecto en una función**.

### Bueno, pero ¿qué está pasando?

Como pueden ver, el `__defaults__` de la función ya tiene un valor incluso antes de que la función se llame por primera vez.
Esto se debe a que los valores por defecto de la función se calculan cuando la función se define, no cuando se llama.
Este comportamiento se llama *early-binding*, y su contraparte (*late-binding*) calcula los valores por defecto en cada ejecución.

Podemos poner esto a prueba bastante fácilmente: ¿qué pasa si entre llamada y llamada volvemos a definir la función tal como estaba?

```python
def agregar_a_lista(elemento, inicial=[]):
    inicial.append(elemento)
    return inicial


valores_por_defecto = agregar_a_lista.__defaults__
identidades = [id(valor) for valor in agregar_a_lista.__defaults__]
print(f"Valores por defecto: {valores_por_defecto}")
print(f"Identidades: {identidades}")

print("Ejecutando una_lista = agregar_a_lista(5)")
una_lista = agregar_a_lista(5)
print(f"Resultado: {una_lista}")


def agregar_a_lista(elemento, inicial=[]):
    inicial.append(elemento)
    return inicial

valores_por_defecto = agregar_a_lista.__defaults__
identidades = [id(valor) for valor in agregar_a_lista.__defaults__]
print(f"Valores por defecto: {valores_por_defecto}")
print(f"Identidades: {identidades}")

print("Ejecutando otra_lista = agregar_a_lista(7)")
otra_lista = agregar_a_lista(7)
print(f"Resultado: {otra_lista}")
```

Al ejecutar este script obtenemos el resultado esperado:
```
Valores por defecto: ([],)
Identidades: [140438619595200]
Ejecutando una_lista = agregar_a_lista(5)
Resultado: [5]
Valores por defecto: ([],)
Identidades: [140438619595840]
Ejecutando otra_lista = agregar_a_lista(7)
Resultado: [7]
```
No sólo los valores por defecto se vuelven a calcular, sino que además fíjense que tienen dos identidades distintas; es decir, son dos objetos *distintos*.

## OK, entendido. Pero ¿cómo lo resuelvo?

La solución cuando no queremos este comportamiento (que es la mayoría de los casos) es utilizar lo que se llama un objeto *centinela*, para lo que generalmente se usa `None`:
```python
def agregar_a_lista_bien(elemento, inicial=None):
    if inicial is None:
        inicial = []
    inicial.append(elemento)
    return inicial
```

Fíjense la diferencia cuando usamos esta función, comparándola con la anterior

```python
una_lista = agregar_a_lista(5)
otra_lista = agregar_a_lista(7)
print(f"Identidades: {id(una_lista)}, {id(otra_lista)}")

una_lista_bien = agregar_a_lista_bien(5)
otra_lista_bien = agregar_a_lista_bien(7)
print(f"Identidades: {id(una_lista_bien)}, {id(otra_lista_bien)}")
```

```
Identidades: 139893270457152, 139893270457152
Identidades: 139893271721280, 139893270011200
```

En `agregar_a_lista` ambas listas son el mismo objeto (sus identidades son iguales), mientras que en `agregar_a_lista_bien` se crearon dos listas distintas: `[5]` y `[7]`.
La diferencia fundamental es que el uso del valor centinela `None` nos permitió definir `inicial` *dentro* de la función y, así, es `inicial = []` sucede *cada vez que llamamos la función* y no sólo al princiio como antes.

## Algunas aclaraciones extra (quizás un poco más avanzadas)

### Sobre los centinelas
No quiero ahondar mucho en este tema, pero hay veces que, en la función que usamos, el argumento por defecto podría ser `None`.
En ese caso, nuestra técnica del centinela interfiere con ese valor, porque lo considera simplemente el indicador de "acá va una lista vacía".
¿La solución? Usar centinelas únicos.
La explicación detallada quedará para más adelante, pero la idea es algo así:

```python
_CENTINELA = object()

def agregar_a_lista_bien_unico(elemento, inicial=_CENTINELA):
    if inicial is _CENTINELA:
        inicial = []
    inicial.append(elemento)
    return inicial
```

### Sobre el `is`
La *keyword* `is` en Python es para chequear identidades, no valores.
Es decir, `A is B` va a dar `True` si y sólo si `id(A) == id(B)`; es decir, si y sólo si `A` y `B` son el mismo objeto.
¿Por qué comparamos con `is` y no con `==`?
Porque en Python el comparador (`==`) se puede definir para cada clase a través del método `__eq__`; entonces, si creamos una clase que parece una lista, pero devuelve siempre `True` en las comparaciones:
```python
class MiLista(list):
    def __eq__(self, other):
        return True
```
sucede:

```python
>>> lista_prueba = MiLista([1, 2, 3, 4])
>>> lista_prueba == None
True
>>> lista_prueba is None
False
```

Así que nunca, *nunca*, **nunca** comparen valores centinela con `==`.
Lo que me lleva al tercer y último punto:

### Comparaciones implícitas
Python tiene conversiones implícitas de valores booleanos (`True`/`False`, bah).
Por ejemplo, las listas vacías, `None` y los números iguales a 0 se evalúan como `False`.
Así que, como `None` se evalúa a `False`, uno podría tentarse a escribir:

```
...
if not inicial:
    inicial = []
```
en vez del chequeo `inicial is None`.

A esto, además del problema de comparar con `==`, se le suma que quizás *sí* quermeos pasar una lista vacía y modificarla (con un `append`), pero este código nos fuerza a crear una lista nueva `inicial` dentro del *scope* de la función.

# Entonces...

 Estudiar cómo funciona el lenguaje nos puede ayudar a que comportamientos que antes nos parecían raros se vuelvan más intuitivos.
 En este caso en particular:

1. No usemos *mutables* como valores por defecto en Python.
2. `None` casi siempre es un buen valor centinela
3. Cuando no sirve como centinela, hay que arremangarse un poco; pero la lógica es la misma.
4. Los centinelas siempre se chequean con `is`, no con `==`.
