# ¿Cuánto tarda un borracho en ganar al Pacman?

En esta serie de artículos vamos a estudiar un aspecto de los más dinámicos de la inteligencia artificial: el desarrollo de robots.
No tanto como Skynet (todavía), pero sí que pueda realizar alguna tarea como un humano: jugar al Pacman.
Para eso necesitamos *armar un Pacman*; vamos a hacer un Pacman más sencillo, en el que no hay fantasmas.

Aprovechemos que no hay fantasmas para hacer jugar a un tipo de jugador que probablemente sobreviviría poco: un borracho jugando al Pacman.
El borracho jugando al pacman juega completamente *al azar*.
En cada momento elige de forma aleatoria para dónde va en el siguiente paso: para arriba, para abajo, para la izquierda o para la derecha.

Les pregunto entonces: en el nivel inicial (que estes que copiamos aquí) y sabiendo que el pacman se desplaza a una velocidad aproximada de 10 casilleros por segundo, **¿cuánto tiempo dicen que tardaría un borracho en comerse todas las bolitas?**

![Pacman](pacman_original.png)

En la sección que sigue vamos a describir un poco cómo fue el diseño y la implementación del Pacman en Python.
Si no les interesa tanto esto, pueden saltearla e ir directamente a la sección resultados.

## El Pacman

Vamos a describir el estado del juego Pacman en la clase `Estado`.
Esta clase va a tener (por ahora) los siguientes atributos:

- `mapa`: un array bidimensional que tiene `1` cuando hay una bolita, `0` cuando está vacío y `-1` cuando el lugar está prohibido.
- `posicion`: la posición en la que se encuentra el Pacman
- `puntaje`: cuántas bolitas comió
- `cantidad_pasos`: cuántos pasos hizo

