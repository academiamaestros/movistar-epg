import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Obtener la fecha y hora actual
fecha_actual = datetime.utcnow().strftime("%d/%m/%Y %H:%M")

# Crear la cabecera del XML con la fecha
cabecera = f'<?xml version="1.0" encoding="UTF-8"?>\n'
cabecera += f'<tv generator-info-name="Epg Movistar {fecha_actual}" generator-info-url="t.me/EPG_dobleM">\n'

# Abre el archivo para escribir la cabecera
with open('guiaiptv.xml', 'w', encoding='utf-8') as archivo:
    archivo.write(cabecera)

# Descargar los datos JSON desde la URL
url = 'https://ottcache.dof6.com/movistarplus/webplayer/DIFUSION/contents/epg'
response = requests.get(url)
programacion = response.json()

# Crear el árbol XML
root = ET.Element("tv")

# Iterar sobre los canales y la programación para crear los elementos XML
for canal in programacion:
    channel = ET.SubElement(root, "channel", id=canal["Nombre"])
    display_name = ET.SubElement(channel, "display-name")
    display_name.text = canal["Nombre"]

    for pase in canal["Pases"]:
        program = ET.SubElement(
            root, 
            "programme", 
            start=datetime.fromtimestamp(int(pase["FechaHoraInicio"]) / 1000).strftime('%Y%m%d%H%M%S') + " +0000",
            stop=datetime.fromtimestamp(int(pase["FechaHoraFin"]) / 1000).strftime('%Y%m%d%H%M%S') + " +0000",
            channel=canal["Nombre"]
        )
        title = ET.SubElement(program, "title")
        title.text = pase["Titulo"]
        desc = ET.SubElement(program, "desc")
        desc.text = pase["Descripcion"] if "Descripcion" in pase else ""
        category = ET.SubElement(program, "category")
        category.text = pase["GeneroComAntena"]

# Guardar el resto del archivo XML
tree = ET.ElementTree(root)
tree.write("guiaiptv.xml", encoding='utf-8', xml_declaration=True)

# Cerrar el XML correctamente
with open('guiaiptv.xml', 'a', encoding='utf-8') as archivo:
    archivo.write('</tv>\n')

print("EPG generada correctamente.")
