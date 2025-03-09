from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "globant-db.chowq0ua2ted.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "mUmusa91_",
    "database": "globant_challenge"
}

# Inicializar la aplicación FastAPI
app = FastAPI()

# Modelo de datos para recibir nuevas contrataciones
class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

# Endpoint para insertar un nuevo empleado
@app.post("/hired_employees/")
def insert_hired_employee(employee: HiredEmployee):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar que department_id y job_id existen
        cursor.execute("SELECT COUNT(*) FROM departments WHERE id = %s", (employee.department_id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail="Department ID no válido")
        
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE id = %s", (employee.job_id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail="Job ID no válido")
        
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO hired_employees (id, name, datetime, department_id, job_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (employee.id, employee.name, employee.datetime, employee.department_id, employee.job_id))
        
        conn.commit()
        return {"message": "Empleado registrado correctamente"}
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Ruta de prueba
@app.get("/")
def home():
    return {"message": "API de contratación en ejecución"}
