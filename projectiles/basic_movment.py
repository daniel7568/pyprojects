import numpy as np
import matplotlib.pyplot as plt

#conditions and vectors
target_pos = np.array([0, 0.01,0])
target_vel = np.array([0.433, 0.25,0])
missile_pos = np.array([3000, 0,0])
missile_vel = np.array([0, 0,0])
grav = np.array([0, -9.81,0])

#Lists
x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]
t_target_pos = [target_pos[2]]
normal_x_target_pos = []
normal_y_target_pos = []
normal_t_target_pos = []
x_missile_pos = []
y_missile_pos = []

#starting values
t = 0
acurate_count = 0
dt = 0.001
pi = np.pi
time_update = np.array([0,0,dt])
launched = False
hit = False
target_a = 20
terminal_vel = 100


def intercept_angle(missile_pos, missile_a,target_x_eq,target_y_eq):
    """Calculate predicted intercept point using closing velocity."""
    best_v = None
    for deg in np.arange(180,90,-0.1):
        r_deg = deg*(pi/180)
        missile_vel = np.array([0.1 * np.cos(r_deg), 0.1 * np.sin(r_deg), 0])
        missile_a_vec = np.array([missile_a * np.cos(r_deg), missile_a * np.sin(r_deg), 0]) + grav
        missile_x_eq = np.array([0.5*missile_a_vec[0],missile_vel[0],missile_pos[0]])
        missile_y_eq = np.array([0.5 * missile_a_vec[1], missile_vel[1], missile_pos[1]])
        x_intersect_t = np.roots(np.array(missile_x_eq) - np.array(target_x_eq))
        x_intersect_t = x_intersect_t[np.isreal(x_intersect_t)].real
        x_intersect_t = x_intersect_t[x_intersect_t > 0]

        y_intersect_t = np.roots(np.array(missile_y_eq) - np.array(target_y_eq))
        y_intersect_t = y_intersect_t[np.isreal(y_intersect_t)].real
        y_intersect_t = y_intersect_t[y_intersect_t > 0]

        intersection_times = np.intersect1d(x_intersect_t, y_intersect_t)
        if intersection_times.size > 0:
            best_v = missile_vel
        return best_v,missile_a_vec

def calculate_guidance(missile_pos, missile_vel, target_pos, target_vel):
    """Calculate proportional navigation guidance command."""
    r = target_pos - missile_pos
    v_closing = target_vel - missile_vel

    # Normalized line of sight vector
    los = r / np.linalg.norm(r)

    # Calculate line of sight rate
    los_rate = np.cross(los, np.cross(v_closing, los)) / np.linalg.norm(r)

    # Navigation constant
    N = 4

    # Calculate acceleration command (perpendicular to current velocity)
    if np.linalg.norm(missile_vel) > 0:  # Prevent division by zero
        v_missile_norm = missile_vel / np.linalg.norm(missile_vel)
        a_command = N * np.linalg.norm(v_closing) * np.cross(los_rate, v_missile_norm)
    else:
        a_command = np.zeros(3)

    return a_command

def apply_missile_acceleration(current_vel, desired_direction, acceleration, dt):
    """Apply acceleration to the missile while respecting maximum speed."""
    current_speed = np.linalg.norm(current_vel)

    # Calculate acceleration vector in desired direction
    accel_vector = acceleration * desired_direction

    # Apply acceleration
    new_vel = current_vel + accel_vector * dt
    new_speed = np.linalg.norm(new_vel)

    # Limit to maximum speed
    if new_speed > max_missile_speed:
        new_vel = max_missile_speed * new_vel / new_speed

    return new_vel

while target_pos[1] > 0:
    # Update target position
    target_pos = target_pos + target_vel * dt + time_update

    # Apply acceleration for the first 10 seconds
    if t < 10:
        v_angle = np.arctan2(target_vel[1], target_vel[0])
        a_vector = np.array([target_a * np.sin(v_angle), target_a * np.cos(v_angle),0])
        target_vel = target_vel + grav * dt + a_vector * dt
    else:
        target_vel = target_vel + grav * dt
        if not launched:
            normal_x_target_pos.append(target_pos[0])
            normal_y_target_pos.append(target_pos[1])
            normal_t_target_pos.append(target_pos[2])
            v_angle = np.arctan2(target_vel[1], target_vel[0])
            coef = np.polyfit(normal_x_target_pos, normal_y_target_pos, 2)
            if coef[0]<0:
                acurate_count += 1
                if acurate_count>20:
                    target_x_eq = np.polyfit(normal_t_target_pos, normal_x_target_pos,2)
                    target_y_eq = np.polyfit(normal_t_target_pos, normal_y_target_pos,2)
                    roots = np.roots(y_time_eq)
                    time_end = max(roots)
                    time_line = np.linspace(min(normal_t_target_pos), time_end, 5000)
                    target_y_values = np.polyval(y_time_eq, time_line)
                    target_x_values = np.polyval(x_time_eq, time_line)
                    plt.scatter(target_x_values, target_y_values , c="r", label="Normal Trajectory")
                    print(x_time_eq)
                    print(y_time_eq)
                    launched = True  # Launch the missile or mark as launched
                    launched_time = t
                    for a in range (14,60):
                        missile_vel,missile_vec = intercept_angle(missile_pos,a,target_x_eq,target_y_eq)
                        if missile_vel is not None:



                    else:
                        print("can't hit the target")
        else:
            missile_pos = missile_pos +  missile_vel * dt + time_update
            if t -launched_time < 10:
                angle = np.arctan2( missile_vel[1],  missile_vel[0])
                missile_a_vector = np.array([final_a * np.cos(angle), final_a * np.sin(angle), 0])
                missile_vel = missile_vel + grav * dt + missile_a_vector * dt
            else:
                missile_vel = missile_vel + grav*dt
            x_missile_pos.append(missile_pos[0])
            y_missile_pos.append(missile_pos[1])
    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])
    t_target_pos.append(target_pos[2])
    t += dt

plt.scatter(x_missile_pos,y_missile_pos,c="k")
plt.plot(x_target_pos, y_target_pos, label="Target Path" )
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.title("Target Trajectory with Normal Path")
plt.show()
print(target_pos[2])
print(hit)




