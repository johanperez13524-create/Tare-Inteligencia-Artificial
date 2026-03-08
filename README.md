# AI Extract API

Microservicio desarrollado con **FastAPI** para analizar texto y devolver información estructurada en formato JSON.

El sistema recibe texto y un dominio de contexto, y devuelve:

* Un resumen del texto
* Entidades detectadas
* Acciones sugeridas
* Nivel de confianza
* Si se necesita aclaración adicional

---

# Tecnologías utilizadas

* Python
* FastAPI
* Pydantic
* Uvicorn

---

# Instalación

1. Clonar el repositorio o descargar el proyecto.

2. Crear un entorno virtual:

```
python -m venv venv
```

3. Activar el entorno virtual.

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

4. Instalar dependencias:

```
pip install fastapi uvicorn pydantic
```

---

# Ejecutar la API

En la carpeta del proyecto ejecutar:

```
uvicorn main:app --reload
```

El servidor iniciará en:

```
http://127.0.0.1:8000
```

Documentación interactiva:

```
http://127.0.0.1:8000/docs
```

---

# Endpoint principal

POST `/extract`

Analiza el texto enviado y devuelve información estructurada.

---

# Ejemplo de request

```
POST /extract
```

Body JSON:

```
{
 "text": "La Universidad organizará una reunión el 10 de abril en el auditorio. María López coordinará el evento.",
 "domain": "universidad"
}
```

---

# Ejemplo de respuesta

```
{
 "summary": "La Universidad organizará una reunión el 10 de abril en el auditorio. María López coordinará el evento.",
 "entities": [
  {"name": "10 de abril", "type": "DATE"},
  {"name": "María López", "type": "PERSON"},
  {"name": "Universidad", "type": "ORG"}
 ],
 "actions": [],
 "confidence": 0.85,
 "needs_clarification": false,
 "clarifying_questions": []
}
```

---

# Ejemplo usando curl

```
curl -X POST "http://127.0.0.1:8000/extract" \
-H "Content-Type: application/json" \
-d '{
"text":"Hay una reunión la próxima semana para revisar el proyecto.",
"domain":"universidad"
}'
```

---

# Autor

Proyecto académico desarrollado para practicar:

* APIs con FastAPI
* validación con Pydantic
* diseño de contratos de salida
* procesamiento de texto
