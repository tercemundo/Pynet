import requests
import re
import sys

def obtener_info_cuitonline(numero):
    url = f"https://www.cuitonline.com/search.php?q={numero}"
    response = requests.get(url)
    texto = response.text

    # Buscar el patrón específico: nombre y apellido seguido de guión y CUIT
    patron = r'([\w\s]+)\s*-\s*(\d+);'
    match = re.search(patron, texto)

    if match:
        nombre_apellido = match.group(1).strip()
        cuit = match.group(2).strip()
        
        # Separar nombre y apellido (asumiendo que el último espacio separa apellido de nombre)
        partes_nombre = nombre_apellido.rsplit(' ', 1)
        if len(partes_nombre) > 1:
            apellido = partes_nombre[0]
            nombre = partes_nombre[1]
        else:
            apellido = nombre_apellido
            nombre = ""

        return {
            "Apellido": apellido,
            "Nombre": nombre,
            "CUIT": cuit
        }
    else:
        return {
            "Apellido": "No encontrado",
            "Nombre": "No encontrado",
            "CUIT": "No encontrado"
        }

# Verificar si se proporcionó un argumento
if len(sys.argv) != 2:
    print("Uso: python script.py <numero>")
    sys.exit(1)

# Obtener el número del argumento de línea de comandos
numero = sys.argv[1]

# Obtener y mostrar la información
info = obtener_info_cuitonline(numero)

print("\nInformación encontrada:")
for clave, valor in info.items():
    print(f"{clave}: {valor}")
