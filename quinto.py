import requests
import re
import sys
import argparse
import sqlite3

def crear_tabla(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personas (
        dni TEXT PRIMARY KEY,
        apellido TEXT,
        nombre TEXT,
        cuit TEXT
    )
    ''')
    conn.commit()

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

def guardar_en_db(conn, info):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO personas (dni, apellido, nombre, cuit)
    VALUES (?, ?, ?, ?)
    ''', (info['DNI'], info['Apellido'], info['Nombre'], info['CUIT']))
    conn.commit()

def procesar_numero(conn, numero):
    info = obtener_info_cuitonline(numero)
    guardar_en_db(conn, info)
    print(f"\nInformación para DNI {numero}:")
    for clave, valor in info.items():
        print(f"{clave}: {valor}")

def procesar_archivo(conn, nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            dnis = archivo.read().splitlines()
        for dni in dnis:
            dni = dni.strip()
            if dni:  # Ignorar líneas vacías
                procesar_numero(conn, dni)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Obtener información de CUITonline y guardar en SQLite")
    parser.add_argument("entrada", help="Número de DNI o nombre del archivo si se usa -l")
    parser.add_argument("-l", "--lista", action="store_true", help="Indica que la entrada es un archivo con lista de DNIs")
    parser.add_argument("-d", "--database", default="cuitonline.db", help="Nombre de la base de datos SQLite")
    args = parser.parse_args()

    conn = sqlite3.connect(args.database)
    crear_tabla(conn)

    try:
        if args.lista:
            procesar_archivo(conn, args.entrada)
        else:
            procesar_numero(conn, args.entrada)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
