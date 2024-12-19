import numpy as np
import matplotlib.pyplot as plt

# Parameters for Doxorubicin simulation
time_steps = 180  # Simulation for 180 days
dt = 1  # Time step in days
dose = 60  # Dose of Doxorubicin in mg/m²
dose_interval = 21  # Administered every 21 days
elimination_rate = np.log(2) / 1.25  # Elimination rate (half-life = 30 hours)
therapeutic_effect_rate = 0.05  # Tumor reduction rate
side_effect_rate = -0.03  # Health reduction rate due to toxicity
toxicity_threshold = 10  # Drug concentration threshold for toxicity effects

# Initial conditions
tumor_size = np.zeros(time_steps)
tumor_size[0] = 100  # Starting tumor size in cm³
health_score = np.zeros(time_steps)
health_score[0] = 70  # Initial health score
concentration = np.zeros(time_steps)

# Dosing schedule
doses = np.zeros(time_steps)
for day in range(0, time_steps, dose_interval):
    doses[day] = dose

# Simulate drug dynamics and effects
for t in range(1, time_steps):
    # Drug concentration
    concentration[t] = max(0, concentration[t - 1] * np.exp(-elimination_rate * dt) + doses[t])
    
    # Tumor reduction if drug concentration is above therapeutic level
    if concentration[t] > 0:
        tumor_size[t] = max(0, tumor_size[t - 1] - therapeutic_effect_rate * concentration[t] * dt)
    else:
        tumor_size[t] = tumor_size[t - 1]
    
    # Health score adjustment (toxicity and side effects)
    if concentration[t] > toxicity_threshold:
        health_score[t] = max(0, health_score[t - 1] + side_effect_rate * (concentration[t] - toxicity_threshold) * dt)
    else:
        health_score[t] = health_score[t - 1]

# Plot results
plt.figure(figsize=(12, 8))

# Tumor size plot
plt.subplot(3, 1, 1)
plt.plot(range(time_steps), tumor_size, label="Tumor Size (cm³)", color="red")
plt.title("Tumor Size Over Time")
plt.xlabel("Days")
plt.ylabel("Tumor Size (cm³)")
plt.legend()

# Drug concentration plot
plt.subplot(3, 1, 2)
plt.plot(range(time_steps), concentration, label="Drug Concentration (mg/m²)", color="blue")
plt.axhline(y=toxicity_threshold, color="orange", linestyle="--", label="Toxicity Threshold")
plt.title("Drug Concentration Over Time")
plt.xlabel("Days")
plt.ylabel("Concentration (mg/m²)")
plt.legend()

# Health score plot
plt.subplot(3, 1, 3)
plt.plot(range(time_steps), health_score, label="Health Score", color="green")
plt.title("Health Score Over Time")
plt.xlabel("Days")
plt.ylabel("Health Score")
plt.legend()

plt.tight_layout()
plt.show()

# Print final results
print(f"Final Tumor Size: {tumor_size[-1]:.2f} cm³")
print(f"Final Health Score: {health_score[-1]:.2f}")

if tumor_size[-1] < 50:
    print("Tumor has significantly reduced. Treatment is effective.")
else:
    print("Tumor reduction is minimal. Consider alternative treatments.")

if health_score[-1] < 50:
    print("Patient's health score is critically low. Consider modifying treatment plan.")
else:
    print("Patient's health score is stable.")
