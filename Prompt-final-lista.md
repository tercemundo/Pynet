Necesito un script Python que:
- Acepte un DNI como argumento o una lista de DNIs desde archivo (-l archivo)
- Sin argumentos muestre error y salga
- Consulte CUIT online por cada DNI
- Extraiga nombre, apellido, CUIT, categoría monotributo y URL constancia
- Use regex para parsear respuestas
- Maneje errores de requests y archivo
- URL: https://www.cuitonline.com/search.php?q=<dni>
