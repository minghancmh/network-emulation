import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.special

# Constants
NUM_PACKETS_PER_PAYLOAD = 21
hops_values = [1, 2, 3, 4, 5, 8, 10, 16, 20, 25]

# Generate grid of drop rates and redundancy factors
x_drop_rates = np.linspace(0, 1, 50)  # Reduce resolution for performance
y_redundancy_factors = np.linspace(0, 1, 50)
X, Y = np.meshgrid(x_drop_rates, y_redundancy_factors)

# Create a full-screen figure
plt.figure(figsize=(16, 8))

for index, AVERAGE_NUM_HOPS in enumerate(hops_values):
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            p_drop = X[i, j]
            redundancy = Y[i, j]
            effective_packets = (1 + redundancy) * NUM_PACKETS_PER_PAYLOAD
            p_survival_per_hop = 1 - p_drop
            p_survival_all_hops = p_survival_per_hop ** AVERAGE_NUM_HOPS
            p_success = 0
            for k in range(NUM_PACKETS_PER_PAYLOAD, int(effective_packets) + 1):
                p_success += scipy.special.comb(effective_packets, k) * p_survival_all_hops**k * (1 - p_survival_all_hops)**(effective_packets - k)
            Z[i, j] = p_success

    # Plot configuration
    ax = plt.subplot(2, 5, index + 1, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title(f'Hops = {AVERAGE_NUM_HOPS}')
    ax.set_xlabel('Drop Rate')
    ax.set_ylabel('Redundancy')
    ax.set_zlabel('Success Prob.')

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
