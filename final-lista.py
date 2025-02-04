import requests
import re
import sys

def obtener_info_cuitonline(cuit):
   url = f"https://www.cuitonline.com/search.php?q={cuit}"
   try:
       response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
       response.raise_for_status()
       texto = response.text

       patron_info = r'([\w\s]+)\s*-\s*(\d+);'
       patron_constancia = r'href="(//www\.cuitonline\.com/constancia/inscripcion/\d+)"'
       patron_categoria = r'Monotributista.*?CATEGOR.A\s+([A-Z])'

       match_info = re.search(patron_info, texto)
       match_constancia = re.search(patron_constancia, texto)
       match_categoria = re.search(patron_categoria, texto)

       if match_info:
           nombre_apellido = match_info.group(1).strip()
           cuit_encontrado = match_info.group(2).strip()
           
           partes_nombre = nombre_apellido.split()
           apellido = partes_nombre[0]
           nombre = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""

           return {
               "DNI": cuit,
               "Apellido": apellido,
               "Nombre": nombre,
               "CUIT": cuit_encontrado,
               "URL_Constancia": f"https:{match_constancia.group(1)}" if match_constancia else None,
               "Categoria": match_categoria.group(1) if match_categoria else "No encontrada"
           }
       return None
   except requests.exceptions.RequestException as e:
       print(f"Error consultando DNI {cuit}: {e}")
       return None

def procesar_lista_dnis(filename):
   try:
       with open(filename) as f:
           dnis = f.read().splitlines()
           return [dni.strip() for dni in dnis if dni.strip()]
   except:
       print(f"Error leyendo archivo {filename}")
       sys.exit(1)

if __name__ == "__main__":
   if len(sys.argv) < 2:
       print("Uso: python script.py <dni> o python script.py -l <archivo>")
       sys.exit(1)

   if sys.argv[1] == '-l':
       if len(sys.argv) != 3:
           print("Falta nombre de archivo")
           sys.exit(1)
       dnis = procesar_lista_dnis(sys.argv[2])
   else:
       dnis = [sys.argv[1]]

   for dni in dnis:
       info = obtener_info_cuitonline(dni)
       if info:
           print("\nDNI:", dni)
           for key, value in info.items():
               if key != "DNI":
                   print(f"{key}: {value}")
