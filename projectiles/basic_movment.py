import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
target_pos = np.array([0, 0.01])
target_vel = np.array([0, 0])
missile_pos = np.array([8.66, 5])
missile_vel = np.array([8.66, 5])
target_a = 20
grav = np.array([0, -9.81])
dt = 0.001
pi = np.pi
launched = False

# Lists to store positions
x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]
normal_x_target_pos = []
normal_y_target_pos = []
t = 0

# Main simulation loop for target movement
while target_pos[1] > 0:
    # Update target position
    target_pos = target_pos + target_vel * dt

    # Apply acceleration for the first 10 seconds
    if t < 10:
        v_angle = np.arctan2(target_vel[1], target_vel[0])
        a_vector = np.array([target_a * np.sin(v_angle), target_a * np.cos(v_angle)])
        target_vel = target_vel + grav * dt + a_vector * dt
    else:
        target_vel = target_vel + grav * dt

        # Begin analyzing the normal trajectory if missile not launched
        if not launched:
            v_angle = np.arctan2(target_vel[1], target_vel[0])
            if v_angle < -pi / 6:
                # Fit a quadratic to the normal path
                coef = np.polyfit(normal_x_target_pos, normal_y_target_pos, 2)
                x_quad = np.linspace(min(normal_x_target_pos), min(normal_x_target_pos) + 1000, 200)
                y_quad = np.polyval(coef, x_quad)
                plt.plot(x_quad, y_quad, c="r", label="Normal Trajectory")
                launched = True  # Launch the missile or mark as launched
            else:
                # Collect points for normal trajectory
                normal_x_target_pos.append(target_pos[0])
                normal_y_target_pos.append(target_pos[1])

    # Append positions for plotting
    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])

    t += dt

# Plotting the target's path and normal trajectory
plt.plot(x_target_pos, y_target_pos, label="Target Path")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.title("Target Trajectory with Normal Path")
plt.show()





