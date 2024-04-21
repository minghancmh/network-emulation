import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from processLogs import processLog

# Original data
x_drop_rates, y_redundancy_factors, z_prob_msg_decode = processLog("./logs/combined_logs.txt")
x = np.array(x_drop_rates)
y = np.array(y_redundancy_factors)
z = np.array(z_prob_msg_decode)

# Create grid coordinates
xi = np.linspace(min(x), max(x), 100)
yi = np.linspace(min(y), max(y), 100)
xi, yi = np.meshgrid(xi, yi)

# Interpolate z values on grid
zi = griddata((x, y), z, (xi, yi), method='linear') # cubic, linear, nearest

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface using interpolated grid data
ax.plot_surface(xi, yi, zi, cmap='viridis')

# Labels and title
ax.set_xlabel('Probability of Packet Drop per router')
ax.set_ylabel('Redundancy Factor, r')
ax.set_zlabel('Probability of Successful Decoding')
ax.set_title('Smoothed Surface Plot')

plt.show()
