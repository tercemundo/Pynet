import requests
import re
import sys
import argparse

def obtener_info_cuitonline(numero):
    url = f"https://www.cuitonline.com/search.php?q={numero}"
    response = requests.get(url)
    texto = response.text
    patron = r'([\w\s]+)\s*-\s*(\d+);'
    match = re.search(patron, texto)
    if match:
        nombre_apellido = match.group(1).strip()
        cuit = match.group(2).strip()
        partes_nombre = nombre_apellido.rsplit(' ', 1)
        if len(partes_nombre) > 1:
            apellido = partes_nombre[0]
            nombre = partes_nombre[1]
        else:
            apellido = nombre_apellido
            nombre = ""
        return {
            "DNI": numero,
            "Apellido": apellido,
            "Nombre": nombre,
            "CUIT": cuit
        }
    else:
        return {
            "DNI": numero,
            "Apellido": "No encontrado",
            "Nombre": "No encontrado",
            "CUIT": "No encontrado"
        }

def procesar_numero(numero, file=None):
    info = obtener_info_cuitonline(numero)
    output = f"\nInformación para DNI {numero}:\n"
    for clave, valor in info.items():
        output += f"{clave}: {valor}\n"
    
    print(output, end='')
    if file:
        file.write(output)

def procesar_archivo(nombre_archivo, output_file=None):
    try:
        with open(nombre_archivo, 'r') as archivo:
            dnis = archivo.read().splitlines()
        for dni in dnis:
            dni = dni.strip()
            if dni:  # Ignorar líneas vacías
                procesar_numero(dni, output_file)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Obtener información de CUITonline")
    parser.add_argument("entrada", help="Número de DNI o nombre del archivo si se usa -l")
    parser.add_argument("-l", "--lista", action="store_true", help="Indica que la entrada es un archivo con lista de DNIs")
    parser.add_argument("-o", "--output", help="Nombre del archivo de salida")
    args = parser.parse_args()

    output_file = None
    if args.output:
        try:
            output_file = open(args.output, 'w')
        except Exception as e:
            print(f"Error al abrir el archivo de salida: {str(e)}")
            return

    try:
        if args.lista:
            procesar_archivo(args.entrada, output_file)
        else:
            procesar_numero(args.entrada, output_file)
    finally:
        if output_file:
            output_file.close()

if __name__ == "__main__":
    main()
