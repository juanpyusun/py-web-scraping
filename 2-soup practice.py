# Librerias
from bs4 import BeautifulSoup
import requests

# Variables
URL = "https://www.ganarchance.com/resultados-loterias-colombia"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
LOTERIA_3 = "050"
LOTERIA_4 = "7678"

# Peticion
request = requests.get(URL, headers = headers)

# Parseo de html
html = request.text
soup = BeautifulSoup(html, "html.parser")

# Buscar divs con clase "clasesita" y extraer su contenido
divs_nombre = soup.find_all("div", class_="nombre")
divs_numero = soup.find_all("div", class_="numero")

numeros = []
loterias = []
print(" ")
for resultado, loteria in zip(divs_numero, divs_nombre):
    resultado = resultado.text.strip()
    loteria = loteria.text.strip()
    numeros.append(resultado)
    loterias.append(loteria)
    
    if resultado.endswith(LOTERIA_3):
        print("*************")
        print(f"Ganador con 3 CIFRAS en la loteria '{loteria}' con el numero {resultado}")
    if resultado == LOTERIA_4:
        print("*************")
        print(f"Ganador con 4 CIFRAS en la loteria '{loteria}' con el numero {resultado}")
    