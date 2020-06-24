# funciones_bien_implementada.py
def agregar_a_lista(elemento, inicial=[]):
    inicial.append(elemento)
    return inicial

def agregar_a_lista_bien(elemento, inicial=None):
    if inicial is None:
        inicial = []
    inicial.append(elemento)
    return inicial

una_lista = agregar_a_lista(5)
otra_lista = agregar_a_lista(7)
print(f"Identidades: {id(una_lista)}, {id(otra_lista)}")

una_lista_bien = agregar_a_lista_bien(5)
otra_lista_bien = agregar_a_lista_bien(7)
print(f"Identidades: {id(una_lista_bien)}, {id(otra_lista_bien)}")
