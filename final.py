import requests
import re

def obtener_info_cuitonline(cuit):
   url = f"https://www.cuitonline.com/search.php?q={cuit}"
   
   try:
       response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
       response.raise_for_status()
       texto = response.text

       patron_info = r'([\w\s]+)\s*-\s*(\d+);'
       patron_constancia = r'href="(//www\.cuitonline\.com/constancia/inscripcion/\d+)"'
       patron_categoria = r'Monotributista&nbsp;CATEGOR.A\s+([A-Z])'

       match_info = re.search(patron_info, texto)
       match_constancia = re.search(patron_constancia, texto)
       match_categoria = re.search(patron_categoria, texto)

       if match_info:
           nombre_apellido = match_info.group(1).strip()
           cuit_encontrado = match_info.group(2).strip()
           
           partes_nombre = nombre_apellido.split()
           apellido = partes_nombre[0]
           nombre = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""

           resultado = {
               "Apellido": apellido,
               "Nombre": nombre,
               "CUIT": cuit_encontrado,
               "URL_Constancia": f"https:{match_constancia.group(1)}" if match_constancia else None,
               "Categoria": match_categoria.group(1).strip() if match_categoria else "No encontrada"
           }
       else:
           resultado = {
               "Apellido": "No encontrado",
               "Nombre": "No encontrado",
               "CUIT": "No encontrado",
               "URL_Constancia": None,
               "Categoria": "No encontrada"
           }

       return resultado
   
   except requests.exceptions.RequestException as e:
       print(f"Error al realizar la solicitud: {e}")
       return None

if __name__ == "__main__":
   cuit = input("Por favor, ingrese el número de CUIT a buscar: ")
   info = obtener_info_cuitonline(cuit)
   if info:
       for key, value in info.items():
           print(f"{key}: {value}")
