import matplotlib.pyplot as plt
import math
def seconds_to_hours(seconds):
    h = seconds//3600
    left = seconds%3600
    m  = left//60
    left = left%60
    return(h,"Hours",m,"Minutes",left,"Seconds")
def torpedo_hit2(ship_velocity, torpedo_velocity, ax, ay):
    def relative_angle(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return math.atan2(dy, dx)

    def calculate_new_cartesian_point(x, y, angle, distance):
        x = x + distance * math.cos(angle)
        y = y + distance * math.sin(angle)
        return x, y

    ship_velocity /= 3.6
    torpedo_velocity /= 3.6
    dt = 0.01

    ship_x = [0]
    ship_y = [0]

    torpedo_x = [ax]
    torpedo_y = [ay]
    time = 0
    while True:
        time += dt
        ship_x.append(ship_x[-1] + ship_velocity * dt)
        ship_y.append(ship_y[-1]+math.cos(ship_x[-1]))

        angle = relative_angle(torpedo_x[-1], torpedo_y[-1], ship_x[-1], ship_y[-1])
        distance = torpedo_velocity * dt
        mx, my = calculate_new_cartesian_point(torpedo_x[-1], torpedo_y[-1], angle, distance)
        torpedo_x.append(mx)
        torpedo_y.append(my)

        if math.hypot(ship_x[-1] - torpedo_x[-1], ship_y[-1] - torpedo_y[-1]) < 1:
            plt.scatter(torpedo_x[-1],torpedo_y[-1],c="r", label = f"Intersect in {seconds_to_hours(time)} ")
            print(f"Hit at time: {seconds_to_hours(time)} ")
            break

    plt.plot(ship_x, ship_y, label='Ship')
    plt.plot(torpedo_x, torpedo_y, label='Torpedo')
    plt.legend()
    plt.title('Torpedo Hit Simulation')
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.grid(True)
    plt.axis('equal')
    plt.show()


torpedo_hit2(70, 150, 2000, -5000)