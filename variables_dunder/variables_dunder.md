# Qué son las variables "dunder"?

El término `dunder` viene de _double underscore_, es decir, doble guión bajo. En general, en Python, llamamos variables _dunder_ a las que empiezan y terminan con dos guiones bajos. Por ejemplo, si alguna vez programaron una clase en Python, seguramente hayan usado el método `__init__`, que es el inicializador del objeto, y es un método _dunder_.

Pero las variables _dunder_ son un poco más opcionales, y su uso es un poco más críptico a veces. En este artículo vamos a ver dos ejemplos de variables _dunder_ muy útiles, que quizás alguna vez hayas visto. Por ejemplo, alguna vez viste escrito esto en un código?

```python

def main():
    # Hace un montón de cosas
    ...

if __name__ == '__main__':
    main()
```

## Variable `__name__`

La variable `__name__` es una de las variables más raras de todas, porque depende de cómo se ejecuta el archivo. En un ejemplo muy sencillo, construyamos el archivo `archivo_de_prueba.py` con este contenido:

```python
print("Me llamo")
print({__name__})
```

Ahora abrimos una consola de python e importamos el archivo[^1]. El resultado:

```
>>> import archivo_de_prueba
Me llamo
archivo_de_prueba
>>>
```

Muy claro, y con total sentido, `__name__` es el nombre del archivo[^2]. Sin embargo, cuando ejecutamos el archivo directamente, resulta:

```
$ python archivo_de_prueba.py
Me llamo
__main__
```

¿¡Qué pasó!? En realidad, es un poco más complejo que `__name__` cambia de valor de acuerdo a cómo se ejecuta el archivo. `__name__` es el nombre del _módulo_ en el que está. Cuando importan `archivo_de_prueba`, ése es el nombre del módulo. Pero cuando lo ejecutan directamente, cómo se llama el módulo, si en realidad _no hay módulo_? Bueno, por convención, el módulo de "ejecución", es `__main__`.

Con esta información, entonces, ¿qué hace el `if __name__ == "__main__"`? Ahora es un poco más fácil, quiere decir que lo que está en ese bloque se va a ejecutar sólo si el archivo es el archivo principal. Es decir, si lo importamos como módulo, esa parte del texto se saltea. Me siento obligado a aclarar: esto no es _súper importante_. Al fin y al cabo, hay muy pocas veces que queremos que un archivo pueda ser usado como módulo Y como ejecutable _a la vez_. Pero lo que sí es importante es que, con esta variable, eso se puede hacer. Y se volvió una construcción idiomática usual en python. Por eso es que lo tienen tantos scripts.

## Variable `__file__`

La variable `__file__` es, en general, más útil y también más fácil de entender: siempre toma el valor de _ruta relativa que nos lleva al archivo_. Por ejemplo, ahora `archivo_de_prueba.py` es:

```python
print("Mi archivo es:")
print(__file__)
```

Cuando lo ejecutamos, obtenemos

```
$ python archivo_de_prueba.py
Mi archivo es:
archivo_de_prueba.py
```

Y si lo ejecutamos desde otra carpeta, por ejemplo, obtenemos:

```
$ cd ..
$ python variables_dunder/archivo_de_prueba.py
Mi archivo es:
variables_dunder/archivo_de_prueba.py
```

"¿Por qué es tan útil tener esto?", se preguntarán. Imaginen la siguiente estructura de directorios:

```
- paquete
  - bin/
    - script.py
  - carpeta_de_datos/
    - datos_muy_importantes.csv
```

Y el archivo `script.py` chequea que exista el archivo de datos muy importantes:

```python
import os

existe_el_archivo = os.path.exists('../datos/datos_muy_importantes.csv')

if existe_el_archivo:
    print("Tranquiles! Los datos muy importantes están!")
else:
    print("Ooops, creo que perdimos todos los datos")
```

Entonces, para nuestro reaseguro, ejecutamos `script.py` desde su carpeta, `paquete/bin/`:

```
(.../paquete) $ cd bin/
(.../paquete/bin) $ python script.py
Tranquiles! Los datos muy importantes están!
```

¿Pero qué habría pasado si lo ejecutábamos desde el directorio anterior?

```
(.../paquete) $ python bin/script.py
Ooops, creo que perdimos todos los datos
```

Porque, claro, los datos están en `../datos` relativo al archivo _script.py_; pero si ponemos `../datos` así nomás, lo va a buscar en la ruta relativa al directorio en el que estamos parados al ejecutarlo! Muchas veces esto se resuelve de una forma _muy_ poco portable: poniendo la ruta absoluta al archivo `datos_muy_importantes.csv`. Pero ahora sí, viene `__file__` al rescate! Porque lo podemos usar para elegir el directorio base respecto del cual elegimos los archivos. Para eso, usamos `os.path.dirname` (que, a partir de una ruta absoluta o relativa, devuelve el _directorio_ en el que está el archivo) y `os.path.abspath`, que a partir de una ruta relativa genera la ruta absoluta.

Entonces, modifiquemos un poquito el archivo `script.py`:

```python
import os

directorio_base = os.path.dirname(__file__)
ruta_absoluta = os.path.abspath(directorio_base)
ruta_donde_busco = ruta_absoluta + '/' + '../datos/datos_muy_importantes.csv'
print("Voy a buscar en:")
print(ruta_donde_busco)
existe_el_archivo = os.path.exists(ruta_donde_busco)

if existe_el_archivo:
    print("Tranquiles! Los datos muy importantes están!")
else:
    print("Ooops, creo que perdimos todos los datos")
```

 Y ahora...

```
(.../paquete) $ cd bin/
(.../paquete/bin) $ python script.py
Voy a buscar en:
/home/pablo/blog/variables_dunder/paquete/bin/../datos/datos_muy_importantes.csv
Tranquiles! Los datos muy importantes están!
(.../paquete/bin) $ cd ..
(.../paquete) $ python bin/script.py
Voy a buscar en:
/home/pablo/blog/variables_dunder/paquete/bin/../datos/datos_muy_importantes.csv
Tranquiles! Los datos muy importantes están!
```

Fíjense que en ambos casos busca en la misma carpeta y que, además, el sistema de archivos se da cuenta de que hacer `paquete/bin/../datos` es lo mismo que hacer directamente `paquete/datos`. Y así, gracias a la variable dunder `__file__` y la magia del sistema operativo, podemos poner direcciones _relativas al script_ en vez de que sean relativas al directorio en el que estamos trabajando.


## Más variables dunder

Y, la verdad es que hay un montón. Particularmente `__author__` y `__version__` sobresalen. Pero elegimos hablar de `__file__` y `__name__` porque son las dos más útiles dentro del código y además, si bien su uso es sencillo una vez que se entienden, resultan muchas veces demasiado oscuras las implementaciones.

Eso sí: hay otras cosas _dunder_: Los métodos _dunder_ (`__init__`, `__str__`, ...). Esos sí los vamos a ver con un poquito más de detalle en una próxima entrega. Pero esto fue todo por hoy, ¡nos vemos la próxima!

Pablo



[^1]: Recuerden que importar un archivo en `python` es, esencialmente, _ejecutarlo_


Porque las rutas _relativas_ en `python` no son relativas al archivo que están ejecutando, sino al directorio en el que están trabajando cuando lo ejecutan. Tratemos de ser un poco más concretos: i