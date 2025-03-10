from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class Department(BaseModel):
    id: int
    department: str

class Job(BaseModel):
    id: int
    job: str

@app.post("/hired_employees/")
def create_hired_employee(employee: HiredEmployee):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s)",
            (employee.id, employee.name, employee.datetime, employee.department_id, employee.job_id)
        )
        conn.commit()
        return {"message": "Hired employee inserted successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

@app.post("/departments/")
def create_department(department: Department):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO departments (id, department) VALUES (%s, %s)",
            (department.id, department.department)
        )
        conn.commit()
        return {"message": "Department inserted successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

@app.post("/jobs/")
def create_job(job: Job):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jobs (id, job) VALUES (%s, %s)",
            (job.id, job.job)
        )
        conn.commit()
        return {"message": "Job inserted successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/hired_employees/by_month/")
def get_hired_employees_by_month():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT MONTH(datetime) AS month, COUNT(*) AS total_hired
            FROM hired_employees
            WHERE YEAR(datetime) = 2021
            GROUP BY MONTH(datetime)
            ORDER BY month;
        """)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/departments/below_average/")
def get_departments_below_average():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id, d.department, COUNT(he.id) AS total_hired
            FROM departments d
            LEFT JOIN hired_employees he ON d.id = he.department_id
            GROUP BY d.id, d.department
            HAVING total_hired < (SELECT AVG(count) FROM (SELECT COUNT(id) AS count FROM hired_employees GROUP BY department_id) AS subquery)
            ORDER BY total_hired ASC;
        """)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/departments/total_hired/")
def get_total_hired_by_department():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id, d.department, COUNT(he.id) AS total_hired
            FROM departments d
            LEFT JOIN hired_employees he ON d.id = he.department_id
            GROUP BY d.id, d.department
            ORDER BY total_hired DESC;
        """)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()
