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

def procesar_numero(numero):
    info = obtener_info_cuitonline(numero)
    print(f"\nInformación para DNI {numero}:")
    for clave, valor in info.items():
        print(f"{clave}: {valor}")

def procesar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            dnis = archivo.read().splitlines()
        
        for dni in dnis:
            dni = dni.strip()
            if dni:  # Ignorar líneas vacías
                procesar_numero(dni)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Obtener información de CUITonline")
    parser.add_argument("entrada", help="Número de DNI o nombre del archivo si se usa -l")
    parser.add_argument("-l", "--lista", action="store_true", help="Indica que la entrada es un archivo con lista de DNIs")
    
    args = parser.parse_args()

    if args.lista:
        procesar_archivo(args.entrada)
    else:
        procesar_numero(args.entrada)

if __name__ == "__main__":
    main()
