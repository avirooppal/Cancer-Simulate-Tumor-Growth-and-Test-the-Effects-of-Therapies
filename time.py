import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the simulation parameters
days = 90  # Total simulation period in days

# Initial patient parameters
initial_tumor_size = 5.0  # cm
initial_wbc_count = 5000  # cells/mm³
initial_creatinine = 1.0  # mg/dL

# Define the treatment effects over time
def apply_chemotherapy(day):
    # Chemotherapy decreases tumor size, suppresses immune system, impacts kidneys
    tumor_size = initial_tumor_size - (0.05 * day)  # Tumor shrinks 0.05 cm per day
    wbc_count = initial_wbc_count - (50 * day)  # WBC drops by 50 cells/mm³ per day
    creatinine = initial_creatinine + (0.005 * day)  # Creatinine increases by 0.005 mg/dL per day
    return tumor_size, wbc_count, creatinine

def apply_immunotherapy(day):
    # Immunotherapy boosts immune system, gradually decreases tumor size
    tumor_size = initial_tumor_size - (0.02 * day)  # Tumor shrinks slower than chemotherapy
    wbc_count = initial_wbc_count + (60 * day)  # WBC increases by 60 cells/mm³ per day
    creatinine = initial_creatinine + (0.002 * day)  # Minimal creatinine increase
    return tumor_size, wbc_count, creatinine

def apply_radiation(day):
    # Radiation targets tumor directly, affects immune function and kidneys
    tumor_size = initial_tumor_size - (0.07 * day)  # Tumor shrinks faster than immunotherapy
    wbc_count = initial_wbc_count - (20 * day)  # WBC decreases moderately
    creatinine = initial_creatinine + (0.003 * day)  # Creatinine increases mildly
    return tumor_size, wbc_count, creatinine

# Run simulations for each treatment
def simulate_treatment(treatment_type):
    results = {
        "day": [],
        "tumor_size": [],
        "wbc_count": [],
        "creatinine": []
    }
    
    for day in range(1, days + 1):
        if treatment_type == "chemotherapy":
            tumor_size, wbc_count, creatinine = apply_chemotherapy(day)
        elif treatment_type == "immunotherapy":
            tumor_size, wbc_count, creatinine = apply_immunotherapy(day)
        elif treatment_type == "radiation":
            tumor_size, wbc_count, creatinine = apply_radiation(day)
        
        results["day"].append(day)
        results["tumor_size"].append(tumor_size)
        results["wbc_count"].append(wbc_count)
        results["creatinine"].append(creatinine)
    
    return pd.DataFrame(results)

# Simulate each treatment
chemotherapy_results = simulate_treatment("chemotherapy")
immunotherapy_results = simulate_treatment("immunotherapy")
radiation_results = simulate_treatment("radiation")

# Plot the results
plt.figure(figsize=(12, 8))

# Tumor Size
plt.subplot(2, 2, 1)
plt.plot(chemotherapy_results['day'], chemotherapy_results['tumor_size'], label='Chemotherapy', color='r')
plt.plot(immunotherapy_results['day'], immunotherapy_results['tumor_size'], label='Immunotherapy', color='b')
plt.plot(radiation_results['day'], radiation_results['tumor_size'], label='Radiation', color='g')
plt.title('Tumor Size Over Time')
plt.xlabel('Days')
plt.ylabel('Tumor Size (cm)')
plt.legend()

# White Blood Cell Count
plt.subplot(2, 2, 2)
plt.plot(chemotherapy_results['day'], chemotherapy_results['wbc_count'], label='Chemotherapy', color='r')
plt.plot(immunotherapy_results['day'], immunotherapy_results['wbc_count'], label='Immunotherapy', color='b')
plt.plot(radiation_results['day'], radiation_results['wbc_count'], label='Radiation', color='g')
plt.title('WBC Count Over Time')
plt.xlabel('Days')
plt.ylabel('WBC Count (cells/mm³)')
plt.legend()

# Creatinine
plt.subplot(2, 2, 3)
plt.plot(chemotherapy_results['day'], chemotherapy_results['creatinine'], label='Chemotherapy', color='r')
plt.plot(immunotherapy_results['day'], immunotherapy_results['creatinine'], label='Immunotherapy', color='b')
plt.plot(radiation_results['day'], radiation_results['creatinine'], label='Radiation', color='g')
plt.title('Creatinine Levels Over Time')
plt.xlabel('Days')
plt.ylabel('Creatinine (mg/dL)')
plt.legend()

plt.tight_layout()
plt.show()

# Output the final results after 90 days
final_results = {
    "Treatment": ["Chemotherapy", "Immunotherapy", "Radiation"],
    "Final Tumor Size (cm)": [
        chemotherapy_results["tumor_size"].iloc[-1],
        immunotherapy_results["tumor_size"].iloc[-1],
        radiation_results["tumor_size"].iloc[-1]
    ],
    "Final WBC Count (cells/mm³)": [
        chemotherapy_results["wbc_count"].iloc[-1],
        immunotherapy_results["wbc_count"].iloc[-1],
        radiation_results["wbc_count"].iloc[-1]
    ],
    "Final Creatinine (mg/dL)": [
        chemotherapy_results["creatinine"].iloc[-1],
        immunotherapy_results["creatinine"].iloc[-1],
        radiation_results["creatinine"].iloc[-1]
    ]
}

final_df = pd.DataFrame(final_results)
print(final_df)
