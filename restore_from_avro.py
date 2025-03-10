import mysql.connector
import fastavro

# Conectar a la base de datos
connection = mysql.connector.connect(
    host="globant-db.chowq0ua2ted.us-east-2.rds.amazonaws.com",
    user="admin",
    password="mUmusa91_",
    database="globant_challenge"
)

cursor = connection.cursor()

def restore_table_from_avro(table_name):
    with open(f"{table_name}.avro", "rb") as avro_file:
        reader = fastavro.reader(avro_file)
        rows = [row for row in reader]

    if table_name == "departments":
        query = "INSERT INTO departments (id, department) VALUES (%s, %s) ON DUPLICATE KEY UPDATE department = VALUES(department)"

    elif table_name == "jobs":
        query = "INSERT INTO jobs (id, job) VALUES (%s, %s) ON DUPLICATE KEY UPDATE job = VALUES(job)"

    elif table_name == "hired_employees":
        query = """
        INSERT INTO hired_employees (id, name, datetime, department_id, job_id)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name), datetime = VALUES(datetime), 
        department_id = VALUES(department_id), job_id = VALUES(job_id)
        """

        for row in rows:
            row["datetime"] = row["datetime"][:19]  # 🔹 Evitar problemas con formatos ISO 8601

    cursor.executemany(query, [tuple(row.values()) for row in rows])
    connection.commit()
    print(f"✅ Datos restaurados en la tabla {table_name}.")

# Restaurar todas las tablas
restore_table_from_avro("departments")
restore_table_from_avro("jobs")
restore_table_from_avro("hired_employees")

# Cerrar conexión
cursor.close()
connection.close()