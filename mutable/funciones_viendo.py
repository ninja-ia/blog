# funciones_viendo.py
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
