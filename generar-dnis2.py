import argparse
import sys

def generar_lista_dni(inicio, fin, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for numero in range(inicio, fin + 1):
            archivo.write(f"{numero}\n")
    print(f"Lista de DNI generada y guardada en {nombre_archivo}")

def main():
    parser = argparse.ArgumentParser(description="Generar lista de DNI y guardar en un archivo")
    parser.add_argument("-f", "--file", required=True, help="Nombre del archivo de salida")
    args = parser.parse_args()

    if not args.file:
        print("Error: Debe especificar un archivo de salida usando el argumento -f")
        sys.exit(1)

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

    generar_lista_dni(inicio, fin, args.file)

if __name__ == "__main__":
    main()
