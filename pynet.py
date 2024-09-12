import requests

# Banner en ASCII
def mostrar_banner():
    banner = """
 ███████████                                  █████   
░░███░░░░░███                                ░░███    
 ░███    ░███ █████ ████ ████████    ██████  ███████  
 ░██████████ ░░███ ░███ ░░███░░███  ███░░███░░░███░   
 ░███░░░░░░   ░███ ░███  ░███ ░███ ░███████   ░███    
 ░███         ░███ ░███  ░███ ░███ ░███░░░    ░███ ███
 █████        ░░███████  ████ █████░░██████   ░░█████ 
░░░░░          ░░░░░███ ░░░░ ░░░░░  ░░░░░░     ░░░░░  
               ███ ░███                               
              ░░██████                                
               ░░░░░░  
        Un poco de Python con Mucho Fernet               
    ===========================================
    OSINT al 70% 30% by Un Hacker En Capital
    """
    print(banner)

# Simula un campo de entrada
def pedir_datos():
    print("***********************************")
    nombre_apellido_dni = input("Ingrese un nombre y apellido o un DNI: ")
    print("***********************************")
    return nombre_apellido_dni

# Enviar solicitud POST real
def enviar_solicitud(dato):
    url = "https://informes.nosis.com/Home/Buscar"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Cookie': '<INSERTAR_COOKIES_AQUÍ>'  # Las cookies necesarias, debes insertar las correctas aquí
    }
    data = f"Texto={dato.replace(' ', '+')}&Tipo=-1&EdadDesde=-1&EdadHasta=-1&IdProvincia=-1&Localidad=&recaptcha_response_field=enganio+al+captcha&recaptcha_challenge_field=enganio+al+captcha&encodedResponse="
    
    response = requests.post(url, headers=headers, data=data)

    # Si el código de estado es exitoso, devolvemos la respuesta en formato JSON
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al realizar la solicitud: {response.status_code}")
        return None

# Mostrar la tabla con los resultados
def mostrar_tabla(resultados):
    if resultados and "EntidadesEncontradas" in resultados:
        print("+--------------------+-------------------------------+-------------------------------------+----------------+")
        print("| Documento          | Nombre                        | Actividad                           | Provincia      |")
        print("+--------------------+-------------------------------+-------------------------------------+----------------+")
        for entidad in resultados['EntidadesEncontradas']:
            doc = entidad['Documento']
            nombre = entidad['RazonSocial']
            actividad = entidad['Actividad']
            provincia = entidad['Provincia']
            print(f"| {doc:<18} | {nombre:<30} | {actividad:<35} | {provincia:<14} |")
        print("+--------------------+-------------------------------+-------------------------------------+----------------+")
        
    else:
        print("No se encontraron resultados.")

# Ejecución principal del script
def main():
    mostrar_banner()
    dato = pedir_datos()
    respuesta = enviar_solicitud(dato)
    mostrar_tabla(respuesta)

if __name__ == "__main__":
    main()
