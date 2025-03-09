from fastapi import FastAPI, HTTPException
import mysql.connector
from typing import List, Dict

# Conectar a MySQL
conn = mysql.connector.connect(
    host="globant-db.chowq0ua2ted.us-east-2.rds.amazonaws.com",
    user="admin",
    password="mUmusa91_",
    database="globant_challenge"
)
cursor = conn.cursor()

app = FastAPI()

@app.post("/insert_data/")
async def insert_data(data: Dict[str, List[Dict]]):
    tables = ["departments", "jobs", "hired_employees"]
    log_errors = []

    for table, rows in data.items():
        if table not in tables:
            return HTTPException(status_code=400, detail=f"Tabla {table} no permitida")
        
        if not rows:
            continue
        
        # Obtener columnas de la tabla
        cursor.execute(f"DESCRIBE {table}")
        columns = [col[0] for col in cursor.fetchall()]
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        valid_rows = []
        
        for row in rows:
            values = [row.get(col, None) for col in columns]
            if None in values:  # Si hay valores nulos, loguear error
                log_errors.append({"table": table, "row": row, "error": "Faltan datos"})
            else:
                valid_rows.append(tuple(values))
        
        if valid_rows:
            cursor.executemany(insert_query, valid_rows)
            conn.commit()
    
    return {"message": "Datos insertados", "log_errors": log_errors}
