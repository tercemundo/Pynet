def generar_lista_dni(inicio, fin, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for numero in range(inicio, fin + 1):
            archivo.write(f"{numero}\n")

# Solicitar entrada del usuario
while True:
    try:
        inicio = int(input("Ingrese el número de inicio: "))
        fin = int(input("Ingrese el número de fin: "))
        if inicio > fin:
            print("El número de inicio debe ser menor o igual al número de fin.")
        else:
            break
    except ValueError:
        print("Por favor, ingrese números válidos.")
