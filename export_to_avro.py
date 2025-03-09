import mysql.connector
import fastavro
from fastavro.schema import load_schema

# Conectar a la base de datos
connection = mysql.connector.connect(
    host="globant-db.chowq0ua2ted.us-east-2.rds.amazonaws.com",
    user="admin",
    password="mUmusa91_",
    database="globant_challenge"
)

# Cargar los esquemas Avro
avro_schemas = {
    "departments": load_schema("departments.avsc"),
    "jobs": load_schema("jobs.avsc"),
    "hired_employees": load_schema("hired_employees.avsc"),
}

def export_table_to_avro(table_name):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if table_name == "departments":
        rows = [{"id": row["id"], "name": row["department"]} for row in rows]  # 🔹 Usa "department"

    elif table_name == "jobs":
        rows = [{"id": row["id"], "name": row["job"]} for row in rows]  # 🔹 Usa "job"

    elif table_name == "hired_employees":
        rows = [
            {
                "id": row["id"],
                "name": row["name"],
                "datetime": row["datetime"].isoformat(),
                "department_id": row["department_id"],
                "job_id": row["job_id"]
            }
            for row in rows
        ]

    with open(f"{table_name}.avro", "wb") as avro_file:
        fastavro.writer(avro_file, avro_schemas[table_name], rows)

    print(f"✅ Datos exportados correctamente a {table_name}.avro")

# Ejecutar la exportación
export_table_to_avro("departments")
export_table_to_avro("jobs")
export_table_to_avro("hired_employees")
