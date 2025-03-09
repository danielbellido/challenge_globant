import mysql.connector
import pandas as pd

# Conectar a la base de datos
conn = mysql.connector.connect(
    host="globant-db.chowq0ua2ted.us-east-2.rds.amazonaws.com",
    user="admin",
    password="mUmusa91_",
    database="globant_challenge"
)
cursor = conn.cursor()

# 🔹 Habilitar archivo de logs
log_file = "log.txt"

# Función para registrar errores en el log
def log_error(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)  # También mostrar en consola

# 🔹 Deshabilitar claves foráneas temporalmente
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
conn.commit()

# 🔹 Eliminar datos previos en orden correcto
tables = ["hired_employees", "departments", "jobs"]
for table in tables:
    cursor.execute(f"DELETE FROM {table};")
    conn.commit()
    print(f"⚠️ Datos eliminados de {table}")

# 🔹 Habilitar claves foráneas nuevamente
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
conn.commit()

# Función para cargar un CSV sin cabecera con validaciones y logging de errores
def load_csv_to_mysql(file_name, table_name, columns):
    df = pd.read_csv(file_name, names=columns, header=None, encoding="utf-8")

    # ✅ Reemplazar NaN con None (para que MySQL lo interprete como NULL)
    df = df.astype(object).where(pd.notna(df), None)

    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

    for row in df.itertuples(index=False, name=None):
        # 🔹 Validar que no haya valores nulos
        if None in row:
            log_error(f"❌ ERROR: Fila rechazada en {table_name}: {row}")
            continue  # Saltar esta fila y pasar a la siguiente

        try:
            cursor.execute(insert_query, row)
        except mysql.connector.Error as err:
            log_error(f"❌ ERROR insertando en {table_name}: {err} | Fila: {row}")
    
    conn.commit()
    print(f"✅ Datos insertados en {table_name} desde {file_name}")

# 🔹 Cargar cada CSV en orden correcto (SIN CABECERA)
load_csv_to_mysql("departments.csv", "departments", ["id", "department"])
load_csv_to_mysql("jobs.csv", "jobs", ["id", "job"])
load_csv_to_mysql("hired_employees.csv", "hired_employees", ["id", "name", "datetime", "department_id", "job_id"])

# Cerrar conexión
cursor.close()
conn.close()

print("🚀 Proceso completado. Revisa el archivo log.txt para errores.")
