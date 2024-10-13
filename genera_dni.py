def generar_lista_dni(inicio, fin, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for numero in range(inicio, fin + 1):
            archivo.write(f"{numero}\n")

# Definir el rango
inicio = 25070000
fin = 25070999

# Nombre del archivo de salida
nombre_archivo = "lista_dni.txt"

# Generar la lista
generar_lista_dni(inicio, fin, nombre_archivo)

print(f"Se ha generado la lista de DNIs en el archivo '{nombre_archivo}'")
