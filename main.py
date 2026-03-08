from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal
import re

app = FastAPI(
    title="AI Extract API",
    version="1.0"
)

# ----- MODELOS (VALIDACIÓN) -----

class ExtractRequest(BaseModel):
    text: str
    domain: str


class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORG", "DATE", "LOCATION", "OTHER"]


class ExtractResponse(BaseModel):
    summary: str
    entities: List[Entity]
    actions: List[str]
    confidence: float = Field(..., ge=0, le=1)
    needs_clarification: bool
    clarifying_questions: List[str]


# ----- FUNCIONES DE ANÁLISIS -----

def extract_entities(text: str):

    entities = []

    # fechas simples
    dates = re.findall(r"\d{1,2} de \w+", text)
    for d in dates:
        entities.append({"name": d, "type": "DATE"})

    # detectar nombres simples (dos palabras con mayúscula)
    persons = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", text)
    for p in persons:
        entities.append({"name": p, "type": "PERSON"})

    # detectar organización
    if "universidad" in text.lower():
        entities.append({"name": "Universidad", "type": "ORG"})

    return entities


def generate_summary(text: str):

    words = text.split()

    if len(words) <= 60:
        return text

    return " ".join(words[:60])


# ----- ENDPOINT PRINCIPAL -----

@app.post("/extract", response_model=ExtractResponse)
def extract(data: ExtractRequest):

    text = data.text

    entities = extract_entities(text)

    summary = generate_summary(text)

    # detectar ambigüedad
    needs_clarification = False
    questions = []

    if "próxima semana" in text.lower():
        needs_clarification = True
        questions.append("¿Cuál es la fecha exacta de la reunión?")
        questions.append("¿Dónde será la reunión?")
        questions.append("¿Quién presentará el proyecto?")

    actions = []

    if "confirmar" in text.lower():
        actions.append("Confirmar asistencia")

    confidence = 0.85

    if needs_clarification:
        confidence = 0.45
        actions = []

    return {
        "summary": summary,
        "entities": entities,
        "actions": actions,
        "confidence": confidence,
        "needs_clarification": needs_clarification,
        "clarifying_questions": questions
    }


@app.get("/")
def home():
    return {"message": "API funcionando"}