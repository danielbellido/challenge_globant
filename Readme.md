# Data Engineering Challenge - Globant

## 馃搶 Descripci贸n del Proyecto
Este proyecto consiste en la migraci贸n de datos desde archivos CSV a una base de datos MySQL, la creaci贸n de una API REST para gestionar nuevas transacciones, la exportaci贸n de datos a formato AVRO y su restauraci贸n desde estos archivos.

## 馃搨 Estructura del Proyecto
```
/
鈹溾攢鈹� api/
鈹?  鈹溾攢鈹� main.py  # C贸digo de la API REST
鈹?  鈹溾攢鈹� database.py  # Conexi贸n a MySQL
鈹溾攢鈹� data/
鈹?  鈹溾攢鈹� departments.csv  # Datos de departamentos
鈹?  鈹溾攢鈹� jobs.csv  # Datos de trabajos
鈹?  鈹溾攢鈹� hired_employees.csv  # Datos de empleados
鈹溾攢鈹� avro/
鈹?  鈹溾攢鈹� export_to_avro.py  # Script de exportaci贸n a AVRO
鈹?  鈹溾攢鈹� restore_from_avro.py  # Script de restauraci贸n desde AVRO
鈹?  鈹溾攢鈹� schemas/  # Definiciones de esquema AVRO
鈹溾攢鈹� Dockerfile  # Configuraci贸n para Docker
鈹溾攢鈹� README.md  # Documentaci贸n
鈹斺攢鈹� requirements.txt  # Dependencias del proyecto
```

## 馃殌 Instalaci贸n y Configuraci贸n
### 1锔忊儯 Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/nombre-repo.git
cd nombre-repo
```

### 2锔忊儯 Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3锔忊儯 Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4锔忊儯 Configurar variables de entorno
Crear un archivo `.env` con los datos de conexi贸n a MySQL:
```plaintext
DB_HOST=tu-servidor-rds
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_NAME=tu-base-de-datos
```

## 馃摗 API REST
Ejecutar la API con:
```bash
python api/main.py
```

### 馃摑 Endpoints Disponibles
| M茅todo | Endpoint | Descripci贸n |
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

## 馃摝 Exportaci贸n y Restauraci贸n de Datos con AVRO
### Exportar datos a AVRO
```bash
python avro/export_to_avro.py
```

### Restaurar datos desde AVRO
```bash
python avro/restore_from_avro.py
```

## 馃惓 Despliegue con Docker
### Construir y ejecutar el contenedor
```bash
docker build -t data-engineer-api .
docker run -p 5000:5000 --env-file .env data-engineer-api
```

## 鈽?Despliegue en AWS
- **Base de Datos:** Se us贸 **Amazon RDS** con MySQL.
- **API:** Puede desplegarse en **AWS Lambda** con API Gateway o en un **EC2**.
- **Archivos AVRO:** Se pueden almacenar en **Amazon S3**.

---

## 馃攼 Seguridad en la API
- Se validan los datos de entrada en el `POST`.
- Se usa `.env` para evitar exponer credenciales.
- Se pueden agregar **tokens JWT** para autenticaci贸n.

## 馃搶 Contribuciones
Si deseas contribuir, por favor abre un **Pull Request** con tus cambios.

---

