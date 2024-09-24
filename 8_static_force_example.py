import numpy as np
import matplotlib.pyplot as pl

L1 = 1.0
L2 = 1.0

theta1 = np.pi / 4  # Example joint value
theta2 = np.pi / 4  # Example joint value

def jacobian(theta1, theta2):
    j11 = -L1 * np.sin(theta1) - L2 * np.sin(theta1 + theta2)
    j12 = -L2 * np.sin(theta1 + theta2)
    j21 = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    j22 = L2 * np.cos(theta1 + theta2)
    return np.array([[j11, j12], [j21, j22]])


def jacobian_T(theta1, theta2):
    j11 = -L1 * np.sin(theta1) - L2 * np.sin(theta1 + theta2)
    j12 = -L2 * np.sin(theta1 + theta2)
    j21 = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    j22 = L2 * np.cos(theta1 + theta2)
    return np.array([[j11, j21], [j12, j22]])

def forward_kinematics(theta1, theta2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, y

def compute_ellipse(matrix, scale=1.0):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    axis_lengths = scale * np.sqrt(eigenvalues)

    theta = np.linspace(0, 2 * np.pi, 100)
    x = axis_lengths[0] * np.cos(theta)
    y = axis_lengths[1] * np.sin(theta)

    R = eigenvectors
    return R @ np.array([x, y])

# Compute end-effector position
x_end, y_end = forward_kinematics(theta1, theta2)

# Compute ellipsoids
J = jacobian(theta1, theta2)
J_T = jacobian_T(theta1, theta2)
velocity_ellipse = compute_ellipse(J @ J.T)
force_ellipse = compute_ellipse(np.linalg.pinv(J).T @ np.linalg.pinv(J), scale=0.2)  # Scaled for visualization
J_Vel_1 = J[:, 0]
J_Vel_2 = J[:, 1]
J_Force_1 = J_T[:, 0]
J_Force_2 = J_T[:, 1]
# Plot robot, velocity and force ellipsoids
plt.figure()
# Plot robot
plt.plot([0, L1 * np.cos(theta1), x_end], [0, L1 * np.sin(theta1), y_end], '-o', label='Robot', color='blue')
# Plot velocity ellipsoid
plt.plot(velocity_ellipse[0, :] + x_end, velocity_ellipse[1, :] + y_end, label='Velocity Ellipsoid', color='red')
# Plot force ellipsoid
plt.plot(force_ellipse[0, :] + x_end, force_ellipse[1, :] + y_end, label='Force Ellipsoid', color='green')

# plt.quiver(x_end, y_end, J_Vel_1[0], J_Vel_1[1], color='r')  # Plot velocity vector
# plt.quiver(x_end, y_end, J_Vel_2[0], J_Vel_2[1], color='b')  # Plot velocity vector


# plt.quiver(x_end, y_end, J_Vel_1, J_Vel_2, color='g')  # Plot velocity vector
# plt.quiver(x_end, y_end, J_Force_2[0], J_Force_2[1], color='y')  # Plot velocity vector

plt.title("Robot with Velocity and Force Ellipsoids")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()
