import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.special

# Constants
AVERAGE_NUM_HOPS = 2
NUM_PACKETS_PER_PAYLOAD = 21

# Generate grid of drop rates and redundancy factors
x_drop_rates = np.linspace(0, 1, 100)  # More practical resolution for plotting
y_redundancy_factors = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x_drop_rates, y_redundancy_factors)

# Probability calculation
# Assuming that z should depend both on X and Y through some theoretical model
Z = np.zeros(X.shape)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        p_drop = X[i, j]
        redundancy = Y[i, j]
        effective_packets = (1 + redundancy) * NUM_PACKETS_PER_PAYLOAD
        # Assuming the chance of receiving enough packets despite the drop
        p_success = 0
        for k in range(NUM_PACKETS_PER_PAYLOAD, int(effective_packets) + 1):
            p_success += scipy.special.comb(effective_packets, k) * (1 - p_drop)**k * p_drop**(effective_packets - k)
        Z[i, j] = p_success

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Labels and title
ax.set_xlabel('Packet Drop Rate')
ax.set_ylabel('Redundancy Factor')
ax.set_zlabel('Probability of Successful Decoding')
ax.set_title('Theoretical Probability Surface (h=2)')

# Colorbar

plt.show()
