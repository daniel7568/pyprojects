import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

#conditions and vectors
target_pos = np.array([0, 0.01,0])
target_vel = np.array([0.433, 0.25,0])
missile_pos = np.array([4000, 0,0])
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
terminal_speed = 200

def solve_quadratic(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float]]:
    """
    Solve quadratic equation ax^2 + bx + c = 0
    Returns tuple of solutions (t1, t2), where None indicates no real solution
    """
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None, None

    sqrt_disc = np.sqrt(discriminant)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    return t1, t2

def find_intercept_time(missile_pos: np.ndarray,
                        direction: np.ndarray,
                        missile_accel_mag: float,
                        max_speed: float,
                        target_pos: np.ndarray,
                        target_vel: np.ndarray,
                        target_accel: np.ndarray,
                        grav: np.ndarray) -> Optional[float]:
    """
    Find the intercept time for a given launch direction
    Returns the earliest positive intercept time, or None if no intercept exists
    """
    time_to_max_speed = max_speed / missile_accel_mag

    intercept_times = []

    a = 0.5 * missile_accel_mag * direction[i] - 0.5 * (target_accel[i] + grav[i])
    b = -target_vel[i]
    c = missile_pos[i] - target_pos[i]

    t1, t2 = solve_quadratic(a, b, c)
        if t1 is not None and 0 <= t1 <= time_to_max_speed:
            intercept_times.append(t1)
        if t2 is not None and 0 <= t2 <= time_to_max_speed:
            intercept_times.append(t2)

    if intercept_times:
        for t in sorted(intercept_times):
            missile_pos_t = missile_pos + direction * (0.5 * missile_accel_mag * t ** 2)
            target_pos_t = target_pos + target_vel * t + 0.5 * (target_accel + grav) * t ** 2
            if np.allclose(missile_pos_t, target_pos_t):
                return t

    intercept_times = []
    pos_at_max_speed = missile_pos + direction * (0.5 * missile_accel_mag * time_to_max_speed ** 2)

    for i in range(3):
        a = -0.5 * (target_accel[i] + grav[i])
        b = direction[i] * max_speed - target_vel[i]
        c = pos_at_max_speed[i] - target_pos[i] - direction[i] * max_speed * time_to_max_speed

        t1, t2 = solve_quadratic(a, b, c)
        if t1 is not None and t1 > time_to_max_speed:
            intercept_times.append(t1)
        if t2 is not None and t2 > time_to_max_speed:
            intercept_times.append(t2)

    # Check if any time satisfies all dimensions
    for t in sorted(intercept_times):
        missile_pos_t = pos_at_max_speed + direction * max_speed * (t - time_to_max_speed)
        target_pos_t = target_pos + target_vel * t + 0.5 * (target_accel + grav) * t ** 2
        if np.allclose(missile_pos_t, target_pos_t):
            return t

    return None


def intercept_angle(missile_pos: np.ndarray,
                    missile_accel_mag: float,
                    max_speed: float,
                    target_pos: np.ndarray,
                    target_vel: np.ndarray,
                    target_accel: np.ndarray,
                    grav: np.ndarray) -> Optional[float]:
    """
    Calculate optimal launch angle considering missile acceleration from 0 to max speed
    Returns the optimal angle in radians, or None if no intercept is possible
    """
    best_angle = None
    min_intercept_time = float('inf')
    for angle in np.arange(0, np.pi, 0.01):
        # Unit vector in launch direction
        direction = np.array([np.cos(angle), np.sin(angle), 0])

        intercept_time = find_intercept_time(
            missile_pos, direction, missile_accel_mag, max_speed,
            target_pos, target_vel, target_accel, grav
        )
        if intercept_time is not None and intercept_time < min_intercept_time:
            min_intercept_time = intercept_time
            best_angle = angle

    return best_angle


while target_pos[1] > 0:
    target_pos = target_pos + target_vel * dt + time_update
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
                    launched = True
                    launched_time = t
                    for a in range (60,110):
                        launch_angle = intercept_angle(missile_pos,a,terminal_speed,target_pos,target_vel,np.array([0,0,0]),grav)
                        if launch_angle is not None:
                            time_to_max_speed = terminal_speed / a
                            missile_a_vec = np.array([a * np.cos(launch_angle),a * np.sin(launch_angle), 0])
                            break
                    else:
                        print("can't hit the target")
        else:
            missile_pos = missile_pos +  missile_vel * dt + time_update
            if t -launched_time < time_to_max_speed:
                missile_vel = missile_vel + grav * dt + missile_a_vec * dt
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


