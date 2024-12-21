from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the graph globally
G = None


class PatientRequest(BaseModel):
    age: int
    sex: str
    prior_treatments: Optional[str]
    concurrent_malignancies: bool
    performance_status: int
    anc: int
    platelets: int
    bilirubin: float
    ast: int
    alt: int
    creatinine: float
    creatinine_clearance: int
    cancer_type: str
    cancer_stage: str
    comorbidities: List[str]
    weight_loss: bool
    nutritional_status: str
    mental_health: str
    tumor_marker: Optional[str]


# Helper functions
def create_graph():
    G = nx.Graph()

    # Add pre-defined nodes and relationships
    G.add_node("chemotherapy", type="treatment")
    G.add_node("immunotherapy", type="treatment")
    G.add_node("radiation", type="treatment")
    G.add_node("tumor_size", type="parameter")
    G.add_node("health_score", type="parameter")
    return G


def add_patient_to_graph(patient_data: dict):
    global G
    patient_id = f"patient_{len([n for n, d in G.nodes(data=True) if d.get('type') == 'patient']) + 1}"
    G.add_node(patient_id, type="patient", **patient_data)

    # Add example edges to parameters or treatments
    G.add_edge(patient_id, "tumor_size", weight=0.7)
    G.add_edge(patient_id, "health_score", weight=0.8)
    G.add_edge(patient_id, "chemotherapy", weight=0.5)
    return patient_id


def recommend_treatments(patient_id):
    global G
    patient_data = G.nodes[patient_id]
    anc = patient_data.get("anc")
    platelets = patient_data.get("platelets")
    bilirubin = patient_data.get("bilirubin")
    ast = patient_data.get("ast")
    alt = patient_data.get("alt")
    creatinine_clearance = patient_data.get("creatinine_clearance")
    performance_status = patient_data.get("performance_status")
    comorbidities = patient_data.get("comorbidities")
    weight_loss = patient_data.get("weight_loss")
    nutritional_status = patient_data.get("nutritional_status")

    treatment_scores = []
    for treatment in [node for node, data in G.nodes(data=True) if data.get("type") == "treatment"]:
        effectiveness = G.edges.get((patient_id, treatment), {}).get("weight", 0)

        # Adjust effectiveness based on patient metrics
        if anc < 1500 or platelets < 100000:
            effectiveness -= 0.3
        if bilirubin > 1.5 or (ast > 40 and alt > 40):
            effectiveness -= 0.2
        if creatinine_clearance < 60:
            effectiveness -= 0.3
        if performance_status > 2:
            effectiveness -= 0.4
        if "diabetes" in comorbidities and treatment == "chemotherapy":
            effectiveness -= 0.2
        if weight_loss or nutritional_status == "poor":
            effectiveness -= 0.3

        treatment_scores.append((treatment, max(effectiveness, 0)))

    treatment_scores.sort(key=lambda x: x[1], reverse=True)
    return treatment_scores


# API Endpoints
@app.on_event("startup")
def startup_event():
    global G
    G = create_graph()


@app.post("/add_patient/")
def add_patient(patient: PatientRequest):
    patient_data = patient.dict()
    patient_id = add_patient_to_graph(patient_data)
    return {"message": "Patient added", "patient_id": patient_id}


@app.get("/recommend_treatments/{patient_id}")
def get_recommendations(patient_id: str):
    if patient_id not in G.nodes:
        return {"error": "Patient not found"}
    treatments = recommend_treatments(patient_id)
    return {"patient_id": patient_id, "recommended_treatments": treatments}
