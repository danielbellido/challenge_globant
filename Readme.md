# Data Engineering Challenge - Globant

## 📌 Descripción del Proyecto
Este proyecto consiste en la migración de datos desde archivos CSV a una base de datos MySQL, la creación de una API REST para gestionar nuevas transacciones, la exportación de datos a formato AVRO y su restauración desde estos archivos.

## 📂 Estructura del Proyecto
```
/
├── api/
�?  ├── main.py  # Código de la API REST
�?  ├── database.py  # Conexión a MySQL
├── data/
�?  ├── departments.csv  # Datos de departamentos
�?  ├── jobs.csv  # Datos de trabajos
�?  ├── hired_employees.csv  # Datos de empleados
├── avro/
�?  ├── export_to_avro.py  # Script de exportación a AVRO
�?  ├── restore_from_avro.py  # Script de restauración desde AVRO
�?  ├── schemas/  # Definiciones de esquema AVRO
├── Dockerfile  # Configuración para Docker
├── README.md  # Documentación
└── requirements.txt  # Dependencias del proyecto
```

## 🚀 Instalación y Configuración
### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/nombre-repo.git
cd nombre-repo
```

### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
Crear un archivo `.env` con los datos de conexión a MySQL:
```plaintext
DB_HOST=tu-servidor-rds
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_NAME=tu-base-de-datos
```

## 📡 API REST
Ejecutar la API con:
```bash
python api/main.py
```

### 📝 Endpoints Disponibles
| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET    | `/departments` | Obtener todos los departamentos |
| GET    | `/jobs` | Obtener todos los trabajos |
| GET    | `/hired_employees` | Obtener todos los empleados |
| POST   | `/hired_employees` | Insertar un nuevo empleado |

### Ejemplo de solicitud POST
```json
{
  "id": 1001,
  "name": "John Doe",
  "datetime": "2025-03-08T10:00:00",
  "department_id": 2,
  "job_id": 5
}
```

## 📦 Exportación y Restauración de Datos con AVRO
### Exportar datos a AVRO
```bash
python avro/export_to_avro.py
```

### Restaurar datos desde AVRO
```bash
python avro/restore_from_avro.py
```

## 🐳 Despliegue con Docker
### Construir y ejecutar el contenedor
```bash
docker build -t data-engineer-api .
docker run -p 5000:5000 --env-file .env data-engineer-api
```

## �?Despliegue en AWS
- **Base de Datos:** Se usó **Amazon RDS** con MySQL.
- **API:** Puede desplegarse en **AWS Lambda** con API Gateway o en un **EC2**.
- **Archivos AVRO:** Se pueden almacenar en **Amazon S3**.

---

## 🔐 Seguridad en la API
- Se validan los datos de entrada en el `POST`.
- Se usa `.env` para evitar exponer credenciales.
- Se pueden agregar **tokens JWT** para autenticación.

## 📌 Contribuciones
Si deseas contribuir, por favor abre un **Pull Request** con tus cambios.

---

