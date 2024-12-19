import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to simulate patient response
def simulate_patient_response(initial_tumor_size, drug_dosage, num_days, health_score, toxicity_threshold):
    """Simulate the response of a patient's tumor size and health score over time.

    Args:
        initial_tumor_size (float): Initial tumor size in cm³.
        drug_dosage (float): Drug dosage administered daily in mg.
        num_days (int): Number of days to simulate.
        health_score (float): Initial health score.
        toxicity_threshold (float): Maximum tolerable drug concentration.

    Returns:
        tuple: (time, tumor_sizes, drug_concentrations, health_scores)
    """
    time = np.arange(0, num_days, 1)
    tumor_sizes = []
    drug_concentrations = []
    health_scores = []

    tumor_size = initial_tumor_size
    drug_concentration = 0
    current_health_score = health_score

    for t in time:
        # Update drug concentration and decay over time
        if t % 30 == 0:  # Administer drug every 30 days
            drug_concentration += drug_dosage
        drug_concentration = max(0, drug_concentration - 5)  # Drug decay

        # Update tumor size based on drug concentration
        if drug_concentration > toxicity_threshold:
            tumor_size *= 0.9  # Reduce tumor size due to high drug concentration
            current_health_score -= 1  # Health score deteriorates
        else:
            tumor_size *= 1.01  # Tumor grows slightly without enough drug concentration

        # Update health score based on drug toxicity
        if drug_concentration > toxicity_threshold:
            current_health_score -= 2

        # Clamp health score to avoid going negative
        current_health_score = max(0, current_health_score)

        # Record the values
        tumor_sizes.append(tumor_size)
        drug_concentrations.append(drug_concentration)
        health_scores.append(current_health_score)

    return time, tumor_sizes, drug_concentrations, health_scores

# Load and preprocess the dataset
def preprocess_dataset(file_path):
    """Preprocess the dataset to extract relevant columns and clean data."""
    data = pd.read_csv(file_path)
    
    # Example preprocessing for Breast Cancer dataset
    # Drop unnecessary columns
    data = data.drop(columns=['id', 'Unnamed: 32'], errors='ignore')
    
    # Encode diagnosis as binary: M=1, B=0
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    
    # Fill or drop missing values
    data = data.dropna()
    
    return data

# Simulate treatment for a single patient
def simulate_treatment(row):
    """Simulate treatment for a single patient."""
    initial_tumor_size = row['radius_mean'] * 10  # Scale tumor size for simulation
    drug_dosage = 50                              # Fixed drug dosage (mg)
    num_days = 180                                # Simulate for 180 days
    health_score = 70                             # Initial health score
    toxicity_threshold = 40                       # Toxicity threshold

    # Run simulation
    time, tumor_sizes, drug_concentrations, health_scores = simulate_patient_response(
        initial_tumor_size, drug_dosage, num_days, health_score, toxicity_threshold
    )

    # Return the final tumor size and health score
    return tumor_sizes[-1], health_scores[-1]

# Visualize simulation results
def plot_simulation(time, tumor_sizes, drug_concentrations, health_scores):
    """Plot simulation results."""
    plt.figure(figsize=(12, 8))

    # Plot tumor sizes
    plt.subplot(3, 1, 1)
    plt.plot(time, tumor_sizes, color='red', label='Tumor Size (cm³)')
    plt.xlabel('Days')
    plt.ylabel('Tumor Size (cm³)')
    plt.title('Tumor Size Over Time')
    plt.legend()

    # Plot drug concentrations
    plt.subplot(3, 1, 2)
    plt.plot(time, drug_concentrations, color='blue', label='Drug Concentration (mg/m²)')
    plt.axhline(y=40, color='orange', linestyle='--', label='Toxicity Threshold')
    plt.xlabel('Days')
    plt.ylabel('Concentration (mg/m²)')
    plt.title('Drug Concentration Over Time')
    plt.legend()

    # Plot health scores
    plt.subplot(3, 1, 3)
    plt.plot(time, health_scores, color='green', label='Health Score')
    plt.xlabel('Days')
    plt.ylabel('Health Score')
    plt.title('Health Score Over Time')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main code
if __name__ == "__main__":
    # Load dataset (ensure file path is correct)
    file_path = "data.csv"  # Replace with your dataset path
    data = preprocess_dataset(file_path)
    
    # Print data preview
    print(data.head())
    
    # Simulate treatment for a random patient
    random_patient = data.sample(1).iloc[0]
    final_tumor_size, final_health_score = simulate_treatment(random_patient)
    
    print(f"Final Tumor Size: {final_tumor_size:.2f} cm³")
    print(f"Final Health Score: {final_health_score:.2f}")
    
    # Simulate patient response
    time, tumor_sizes, drug_concentrations, health_scores = simulate_patient_response(
        initial_tumor_size=random_patient['radius_mean'] * 10,
        drug_dosage=50,
        num_days=180,
        health_score=70,
        toxicity_threshold=40
    )

    # Plot the results
    plot_simulation(time, tumor_sizes, drug_concentrations, health_scores)
