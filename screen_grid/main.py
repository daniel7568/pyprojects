import matplotlib.pyplot as plt
import numpy as np



class ScreenGrid:
    def __init__(self,name, width, height, zone_size):
        self.width = width
        self.height = height
        self.zone_size = zone_size
        self.zone_width = width // zone_size
        self.zone_height = height // zone_size
        self.grid = np.zeros((height, width))
        self.name = name
        self.zones = [[(i,j) for j in range(zone_size)] for i in range(zone_size)]

        self.zones_dict = {}
        for ls in self.zones:
            for zone in ls:
                self.zones_dict[zone] = []

    def draw(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title(self.name)
        ax.imshow(self.grid, cmap='Greys', interpolation='nearest', origin='lower',)
        plt.show()
    def add_object(self, obj):
        self.grid[obj.dl[1]:obj.ur[1]+1, obj.dl[0]:obj.ur[0]+1] = obj.color
        self.addToZones(obj)
    def addToZones(self, obj):
        for ls in self.zones:
            for zone in ls:
                zone_x = zone[0]*self.zone_width
                zone_y = zone[1]*self.zone_height
                if not (obj.ur[0]<zone_x or obj.dl[0]>zone_x+self.zone_width or obj.ur[1]<zone_y or obj.dl[1]>zone_y+self.zone_height):
                    self.zones_dict[zone].append(obj)
    def show_zones_of_object(self, obj):
        zones_in = []
        for zone, objects in self.zones_dict.items():
            if obj in objects:
                zones_in.append(zone)
        for zone in zones_in:
            self.grid[zone[1]*self.zone_height:(zone[1]+1)*self.zone_height,zone[0]*self.zone_width:(zone[0]+1)*self.zone_width] += 0.1
    def zones_of_object(self, obj):
        zones_in = []
        for zone, objects in self.zones_dict.items():
            if obj in objects:
                zones_in.append(zone)
        return zones_in
    def remove_object(self, obj):
        self.grid[obj.dl[1]:obj.ur[1]+1, obj.dl[0]:obj.ur[0]+1] = 0
        self.removeFromZones(obj)
    def removeFromZones(self, obj):
        for zone, objects in self.zones_dict.items():
            if obj in objects:
                objects.remove(obj)
    def draw_zones_checkboard(self):
        # Create a copy so we don't overwrite objects
        grid_copy = np.zeros_like(self.grid)

        # Loop over zones and fill alternating ones
        for i in range(self.zone_size):
            for j in range(self.zone_size):
                # Checkerboard pattern (sum even -> light shade, odd -> dark)
                if (i + j) % 2 == 0:
                    x0 = int(i * self.zone_width)
                    y0 = int(j * self.zone_height)
                    x1 = int((i + 1) * self.zone_width)
                    y1 = int((j + 1) * self.zone_height)
                    grid_copy[y0:y1, x0:x1] = 0.2  # light gray fill

        # Plot
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title(self.name + " (Zones Checkerboard)")
        ax.imshow(grid_copy, cmap='Greys', interpolation='nearest', origin='lower')
        plt.show()
    def clear(self):
        self.grid = np.zeros((self.height, self.width))
        self.zones_dict = {zone: [] for zone in self.zones_dict}
    def get_objects_in_zone(self, zone):
        return self.zones_dict.get(zone, [])
    def get_all_objects(self):
        all_objects = set()
        for objects in self.zones_dict.values():
            all_objects.update(objects)
        return list(all_objects)



class ScreenObject:
    def __init__(self, points,color, screen: ScreenGrid):
        self.dl = min(points,key=lambda p: p[0]+p[1])
        self.ur = max(points,key=lambda p: p[0]+p[1])
        self.screen = screen
        self.color = color
        self.screen_grid = screen
        self.screen.add_object(self)

w,h = 160,90
zone_size = 5
screen = ScreenGrid("Test Screen", w, h, zone_size)
obj1 = ScreenObject([(13,20),(23,20),(13,25),(23,25)], 0.5, screen)

screen.draw()

screen.show_zones_of_object(obj1)

screen.draw()
screen.draw_zones_checkboard()
# print(screen.zones_dict)
# # screen.remove_object(obj2)
# screen.draw()
# print(screen.zones_dict)