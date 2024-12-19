# Cancer Tumor Growth Simulation and Therapy Effect Testing

## Overview

This project simulates cancer tumor growth and tests the effects of various therapies (e.g., chemotherapy, immunotherapy, radiation) on the tumor size over time. The simulation uses a logistic growth model to represent the tumor's natural growth and incorporates therapy effects that reduce the tumor's growth rate.

## Key Features
- Simulate tumor growth without therapy and with different therapies.
- Compare the effects of chemotherapy, immunotherapy, and radiation on tumor size.
- Visualize the tumor size progression over time under different treatment scenarios.
- Easily modify parameters such as growth rate, therapy effects, and carrying capacity to customize the simulation.

## Requirements

- Python 3.x
- `numpy` for numerical computations.
- `matplotlib` for plotting graphs.

You can install the required packages using `pip`:

```bash
pip install numpy matplotlib
```

## Project Files

- **tumor_simulation.py**: The Python script containing the tumor growth model, simulation logic, and therapy effects.
- **README.md**: This file.

## Tumor Growth Model

The model uses a logistic growth equation to simulate tumor growth:

\[
\frac{dN}{dt} = r \cdot N \cdot \left(1 - \frac{N}{K}\right)
\]

Where:
- \( N \) is the tumor size at time \( t \).
- \( r \) is the growth rate of the tumor (base growth rate without therapy).
- \( K \) is the maximum possible tumor size (carrying capacity).
- Therapy effects modify the growth rate to reduce tumor size growth.

## Therapy Effects

- **Chemotherapy**: Reduces tumor growth rate by a fixed percentage (e.g., 2% reduction in growth rate).
- **Immunotherapy**: Reduces tumor growth rate by a fixed percentage (e.g., 1% reduction in growth rate).
- **Radiation**: Reduces tumor growth rate by a fixed percentage (e.g., 5% reduction in growth rate).

Each therapy reduces the tumor growth rate in a gradual manner, and the final tumor size is calculated after a set number of time steps (e.g., 100 steps).

## How It Works

1. **Simulation Setup**:
   - Set the initial tumor size and the maximum possible tumor size (carrying capacity).
   - Define base growth rate and therapy effectiveness (for chemotherapy, immunotherapy, and radiation).

2. **Tumor Growth Simulation**:
   - Simulate tumor growth without therapy, with chemotherapy, with immunotherapy, and with radiation.
   - Apply the logistic growth model at each time step to calculate the tumor size.
   - Adjust the growth rate according to the therapy effects.

3. **Results**:
   - Plot the tumor size over time for each therapy scenario.
   - Print the final tumor size for each therapy.

## Running the Simulation

1. Clone or download the repository.
2. Navigate to the project directory.
3. Run the simulation script:

```bash
python tumor_simulation.py
```

This will execute the tumor growth simulation with different therapies and display the results as a graph.

### Example Output:

```plaintext
Final tumor size with chemotherapy: 41.62
Final tumor size with immunotherapy: 128.48
Final tumor size with radiation: 34.12
Final tumor size with no therapy: 752.39
```

A plot will be generated that shows the tumor size progression over time for each therapy.

## Customizing the Simulation

You can customize the simulation by modifying the following parameters in the `tumor_simulation.py` script:

- **Initial tumor size**: Change the initial size of the tumor at the beginning of the simulation.
- **Max tumor size (Carrying Capacity)**: Set the maximum size the tumor can reach.
- **Base growth rate**: Adjust the rate at which the tumor grows when no therapy is applied.
- **Therapy effects**: Modify how much each therapy reduces the growth rate (e.g., chemotherapy can have a stronger effect than immunotherapy).
- **Time steps**: Set the number of time steps for the simulation (e.g., days or weeks).

## Future Improvements

- Add more therapies (e.g., targeted therapies, combination therapies).
- Incorporate variability in patient responses to treatment.
- Simulate side effects of therapies, such as immune suppression or tissue damage.
- Include a more complex growth model that takes into account the interactions between the tumor and the immune system.
