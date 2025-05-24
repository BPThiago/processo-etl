import mysql.connector
import requests

def pais_para_continente(pais):
    url = f"https://restcountries.com/v3.1/translation/{pais.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()[0]
    continente = data['region']

    traducao = {
        'Africa': 'África',
        'Americas': 'América',
        'Europe': 'Europa',
        'Asia': 'Ásia',
        'Oceania': 'Oceania',
        'Antarctic': 'Antártida'
    }
    return traducao.get(continente, continente)

conn_relacional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="relacional",
)

conn_dimensional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="dimensional",
)

cursor_relacional = conn_relacional.cursor()
cursor_dimensional = conn_dimensional.cursor()

cursor_relacional.execute(
    "SELECT idPais, nmPais FROM pais"
)
paises = cursor_relacional.fetchall()

cursor_relacional.execute(
    "SELECT idEstado, nmEstado FROM estado"
)
estados = cursor_relacional.fetchall()

cursor_relacional.execute(
    "SELECT idCidade, nmCidade FROM cidade"
)
cidades = cursor_relacional.fetchall()

continentes = []
for id_pais, nome_pais in paises:
    continentes.append(pais_para_continente(nome_pais))

# Inserts
cursor_dimensional.executemany(
    "INSERT INTO d_localidade (idLocalidade, pais, estado, cidade, continente) VALUES (%s, %s, %s, %s, %s)",
    [(i+1, paises[0][1], estados[i][1], cidades[i][1], continentes[0]) for i in range(len(estados))],
)
conn_dimensional.commit()