import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from processLogs import processLog

# Define arrays of x, y, and z coordinates
# x = np.array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
# y = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5])
# z = np.array([2, 3, 2, 3, 2, 3, 4, 3, 4, 3, 4, 5, 4, 5, 4, 5, 6, 5, 6, 5, 6, 7, 6, 7, 6])

x_drop_rates, y_redundancy_factors, z_prob_msg_decode = processLog("./logs/logs.txt")

x = np.array(x_drop_rates)
y = np.array(y_redundancy_factors)
z = np.array(z_prob_msg_decode)

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface using triangulation
ax.plot_trisurf(x, y, z, cmap='viridis')

# Labels and title
ax.set_ylabel('Redundancy Factor, r')
ax.set_xlabel('Probability of Packet Drop per router')
ax.set_zlabel('Probability of Successful Decoding')
ax.set_title('Surface Plot')

# Show plot
plt.show()
