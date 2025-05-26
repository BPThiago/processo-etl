import mysql.connector
import pandas as pd

conn_dimensional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="dimensional",
)
cursor_dimensional = conn_dimensional.cursor()

excel_path = 'Ch3-SampleDateDim.xls'

df = pd.read_excel(excel_path)

for i, row in df.iterrows():
    day = row['day num in month']
    month = row['month']
    year = row['year']
    quarter = row['quarter']
    semester = quarter // 3 + 1
    
    cursor_dimensional.execute(
        "INSERT INTO d_data (idData, dia, mes, ano, trimestre, semestre) VALUES (%s, %s, %s, %s, %s, %s)",
        (i, day, month, year, quarter, semester)
    )

conn_dimensional.commit()
