import networkx as nx
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch_geometric.data import Data

# Create the graph with detailed health metrics
def create_graph():
    G = nx.Graph()

    # Add patient nodes with detailed metrics
    G.add_node("patient_1", type="patient", 
               age=55, sex="male", prior_treatments="none", 
               concurrent_malignancies=False, 
               performance_status=1,  # ECOG performance score (0 = fully active, 5 = dead)
               anc=2000, platelets=150000, bilirubin=1.0, ast=30, alt=25, creatinine=1.2, 
               creatinine_clearance=70, cancer_type="lung", cancer_stage="II", 
               comorbidities=[], weight_loss=False, nutritional_status="good", 
               mental_health="stable", tumor_marker=None)

    G.add_node("patient_2", type="patient", 
               age=70, sex="female", prior_treatments="chemotherapy", 
               concurrent_malignancies=False, 
               performance_status=2, 
               anc=1600, platelets=120000, bilirubin=1.6, ast=50, alt=45, creatinine=1.8, 
               creatinine_clearance=50, cancer_type="breast", cancer_stage="III", 
               comorbidities=["diabetes"], weight_loss=True, nutritional_status="moderate", 
               mental_health="anxious", tumor_marker="CA-125")

    G.add_node("patient_3", type="patient", 
               age=40, sex="male", prior_treatments="immunotherapy", 
               concurrent_malignancies=True, 
               performance_status=0, 
               anc=1800, platelets=130000, bilirubin=0.9, ast=20, alt=18, creatinine=1.0, 
               creatinine_clearance=80, cancer_type="colon", cancer_stage="I", 
               comorbidities=[], weight_loss=False, nutritional_status="excellent", 
               mental_health="stable", tumor_marker=None)

    # Add treatment nodes
    G.add_node("chemotherapy", type="treatment")
    G.add_node("immunotherapy", type="treatment")
    G.add_node("radiation", type="treatment")

    # Add parameter nodes
    G.add_node("tumor_size", type="parameter")
    G.add_node("health_score", type="parameter")

    # Add edges between patients and their parameters
    G.add_edge("patient_1", "tumor_size", weight=0.7)
    G.add_edge("patient_1", "health_score", weight=0.8)
    G.add_edge("patient_1", "chemotherapy", weight=0.5)

    G.add_edge("patient_2", "tumor_size", weight=0.9)
    G.add_edge("patient_2", "health_score", weight=0.4)
    G.add_edge("patient_2", "immunotherapy", weight=0.3)

    G.add_edge("patient_3", "tumor_size", weight=0.6)
    G.add_edge("patient_3", "health_score", weight=0.9)
    G.add_edge("patient_3", "radiation", weight=0.8)

    return G

# Visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    node_colors = []
    for node, data in G.nodes(data=True):
        if data.get("type") == "patient":
            node_colors.append("lightblue")
        elif data.get("type") == "treatment":
            node_colors.append("lightgreen")
        elif data.get("type") == "parameter":
            node_colors.append("orange")
        else:
            node_colors.append("grey")

    nx.draw(
        G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=10
    )
    plt.show()

# Compare treatments considering detailed health metrics
def compare_treatments(G):
    for patient in [node for node, data in G.nodes(data=True) if data.get("type") == "patient"]:
        print(f"\nPatient: {patient}")
        patient_data = G.nodes[patient]

        # Patient-specific metrics
        age = patient_data.get("age")
        sex = patient_data.get("sex")
        anc = patient_data.get("anc")
        platelets = patient_data.get("platelets")
        bilirubin = patient_data.get("bilirubin")
        ast = patient_data.get("ast")
        alt = patient_data.get("alt")
        creatinine = patient_data.get("creatinine")
        creatinine_clearance = patient_data.get("creatinine_clearance")
        performance_status = patient_data.get("performance_status")
        cancer_stage = patient_data.get("cancer_stage")
        comorbidities = patient_data.get("comorbidities")
        mental_health = patient_data.get("mental_health")
        weight_loss = patient_data.get("weight_loss")
        nutritional_status = patient_data.get("nutritional_status")

        print(f"  Age: {age}, Sex: {sex}, Performance Status: {performance_status}")
        print(f"  ANC: {anc}, Platelets: {platelets}, Bilirubin: {bilirubin}")
        print(f"  AST: {ast}, ALT: {alt}, Creatinine: {creatinine}, Creatinine Clearance: {creatinine_clearance}")
        print(f"  Cancer Stage: {cancer_stage}, Comorbidities: {comorbidities}, Mental Health: {mental_health}")

        treatment_scores = []
        for treatment in [node for node, data in G.nodes(data=True) if data.get("type") == "treatment"]:
            effectiveness = G.edges.get((patient, treatment), {}).get("weight", 0)

            # Adjust effectiveness based on patient metrics
            if anc < 1500 or platelets < 100000:
                effectiveness -= 0.3  # Low blood counts reduce tolerance for most treatments
            if bilirubin > 1.5 or (ast > 40 and alt > 40):
                effectiveness -= 0.2  # Impaired liver function limits many treatments
            if creatinine_clearance < 60:
                effectiveness -= 0.3  # Reduced kidney function limits treatment options
            if performance_status > 2:
                effectiveness -= 0.4  # Poor performance status affects all treatments
            if "diabetes" in comorbidities and treatment == "chemotherapy":
                effectiveness -= 0.2  # Chemotherapy risk for diabetic patients
            if weight_loss or nutritional_status == "poor":
                effectiveness -= 0.3  # Weakened patients handle aggressive treatments poorly

            treatment_scores.append((treatment, max(effectiveness, 0)))  # No negative scores

        # Rank and recommend treatments
        treatment_scores.sort(key=lambda x: x[1], reverse=True)
        for treatment, score in treatment_scores:
            print(f"  Treatment: {treatment}, Score: {score:.2f}")
        best_treatment = treatment_scores[0][0] if treatment_scores else None
        print(f"  Recommended Treatment: {best_treatment}" if best_treatment else "  No suitable treatment found")

# Main function
if __name__ == "__main__":
    G = create_graph()
    visualize_graph(G)

    # Compare treatments for all patients
    compare_treatments(G)
