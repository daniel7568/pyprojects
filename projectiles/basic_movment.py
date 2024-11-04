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

#def pos_after_a(a_mag,v_vec,p_vec):
#    angle = np.arctan2(v_vec[1], v_vec[0])
#    a_vec = np.array([a_mag * np.cos(angle), a_mag * np.sin(angle), 0])
#    a_vec += grav
#    final_vel = np.array([terminal_vel* np.cos(angle),terminal_vel * np.sin(angle), 0])
#    t =  np.abs(final_vel) / np.abs(a_vec)
#    ret_tuple = (p_vec + v_vec*t +0.5*a_vec*t**2,v_vec+a_vec*t,t)
#    return ret_tuple
#def equations(p_vec,v_vec):
#    x_coef = np.array([v_vec[0],p_vec[0]])
#    y_coef = np.array([-4.905,v_vec[1],p_vec[1]])
#    return (x_coef,y_coef)

def predict_intercept(target_pos, target_vel, missile_pos, missile_vel,missile_a):
    """Calculate predicted intercept point using closing velocity."""
    r = target_pos - missile_pos
    closing_velocity = target_vel - missile_vel
    angle = np.arctan2(missile_vel[1], missile_vel[0])
    missile_a_vec = np.array([missile_a * np.cos(angle), missile_a * np.sin(angle), 0])
    missile_a_vec += grav
    missile_x_eq = np.array([])








    # Quadratic equation coefficients
    a = np.dot(closing_velocity, closing_velocity) - missile_speed ** 2
    b = 2 * np.dot(r, closing_velocity)
    c = np.dot(r, r)

    # Solve quadratic equation
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None

    t_intercept = (-b - np.sqrt(discriminant)) / (2 * a)
    if t_intercept < 0:
        return None

    return target_pos + target_vel * t_intercept

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
                    x_time_eq = np.polyfit(normal_t_target_pos, normal_x_target_pos,1)
                    y_time_eq = np.polyfit(normal_t_target_pos, normal_y_target_pos,2)
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
                        if not hit:
                            for deg in range (170,90,-1):
                                if not hit:
                                    r_deg = deg*(pi/180)
                                    missile_vel = np.array([0.1*np.cos(r_deg),0.1*np.sin(r_deg),0])
                                    new_pos, new_vel, time_a = pos_after_a(a,missile_vel,missile_pos)
                                    x_eq, y_eq = equations(new_pos,new_vel)
                                    missile_x_values = np.polyval(x_eq, time_line+time_a)
                                    missile_y_values = np.polyval(y_eq, time_line+time_a)
                                    for i in range(len(time_line)):
                                        if np.abs(target_x_values[i] - missile_x_values[i]) < 0.1 and np.abs(
                                                target_y_values[i] - missile_y_values[i]) < 0.1:
                                            final_a = a
                                            hit = True
                                            break
                                else:
                                    break
                        else:
                            break
                    else:
                        print("can't hit the target")
        else:
            missile_pos = missile_pos +  missile_vel * dt + time_update
            if t -launched_time < 7:
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




