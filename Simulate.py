import numpy as np
import matplotlib.pyplot as plt

# Parameters for the tumor growth model
initial_tumor_size = 1  # initial tumor size (in arbitrary units)
max_tumor_size = 1000  # max possible tumor size (carrying capacity)
base_growth_rate = 0.1  # base growth rate (without therapy)

# Therapy parameters (how much each therapy reduces the growth rate)
chemotherapy_effect = 0.02  # chemotherapy reduces growth rate by 2%
immunotherapy_effect = 0.01  # immunotherapy reduces growth rate by 1%
radiation_effect = 0.05  # radiation reduces growth rate by 5%

# Time parameters
time_steps = 100  # total number of time steps (days, weeks, etc.)

# Function to simulate tumor growth
def simulate_tumor_growth(therapy_effect=0.0):
    tumor_size = initial_tumor_size
    tumor_sizes = [tumor_size]
    
    for t in range(1, time_steps):
        # Apply logistic growth model: dN/dt = r * N * (1 - N/K)
        growth_rate_effective = base_growth_rate * (1 - tumor_size / max_tumor_size) - therapy_effect
        tumor_size += growth_rate_effective * tumor_size
        tumor_size = max(tumor_size, 0)  # Ensure tumor size doesn't go negative
        tumor_size = min(tumor_size, max_tumor_size)  # Ensure it doesn't exceed the max size
        tumor_sizes.append(tumor_size)
    
    return tumor_sizes

# Simulate tumor growth for each therapy
chemotherapy_tumor_growth = simulate_tumor_growth(chemotherapy_effect)
immunotherapy_tumor_growth = simulate_tumor_growth(immunotherapy_effect)
radiation_tumor_growth = simulate_tumor_growth(radiation_effect)
no_therapy_tumor_growth = simulate_tumor_growth(0.0)

# Plot the results
plt.figure(figsize=(10, 6))

plt.plot(chemotherapy_tumor_growth, label='Chemotherapy', color='red')
plt.plot(immunotherapy_tumor_growth, label='Immunotherapy', color='blue')
plt.plot(radiation_tumor_growth, label='Radiation', color='green')
plt.plot(no_therapy_tumor_growth, label='No Therapy', color='black', linestyle='--')

plt.title('Tumor Growth with Different Therapies')
plt.xlabel('Time (days or weeks)')
plt.ylabel('Tumor Size (arbitrary units)')
plt.legend()
plt.grid(True)
plt.show()

# Conclusion: Print out final tumor sizes after treatment
print(f"Final tumor size with chemotherapy: {chemotherapy_tumor_growth[-1]:.2f}")
print(f"Final tumor size with immunotherapy: {immunotherapy_tumor_growth[-1]:.2f}")
print(f"Final tumor size with radiation: {radiation_tumor_growth[-1]:.2f}")
print(f"Final tumor size with no therapy: {no_therapy_tumor_growth[-1]:.2f}")
