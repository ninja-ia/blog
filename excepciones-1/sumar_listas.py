def sumar_listas(lista1, lista2):
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total


def sumar_listas_error(lista1, lista2):
    if len(lista1) != len(lista2):
        return -1
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total


def sumar_listas_lanza(lista1, lista2):
    if len(lista1) != len(lista2):
        raise ValueError("Las listas tienen distinto tamaño")
    lista_total = []
    for i in range(len(lista1)):
        lista_total.append(lista1[i] + lista2[i])
    return lista_total


def maximo_suma(lista1, lista2):
    suma = sumar_listas_lanza(lista1, lista2)
    maximo = max(suma)
    return maximo
