import json
import requests
import xml.etree.ElementTree as ET
import datetime

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
        program = ET.SubElement(root, "programme", start=datetime.datetime.fromtimestamp(int(pase["FechaHoraInicio"])/1000).strftime('%Y%m%d%H%M%S') + " +0000",
                                stop=datetime.datetime.fromtimestamp(int(pase["FechaHoraFin"])/1000).strftime('%Y%m%d%H%M%S') + " +0000",
                                channel=canal["Nombre"])
        title = ET.SubElement(program, "title")
        title.text = pase["Titulo"]
        desc = ET.SubElement(program, "desc")
        desc.text = pase["Descripcion"] if "Descripcion" in pase else ""
        category = ET.SubElement(program, "category")
        category.text = pase["GeneroComAntena"]

# Guardar el archivo XML
tree = ET.ElementTree(root)
tree.write("guiaiptv.xml", encoding='utf-8', xml_declaration=True)

print("EPG generada correctamente.")
