import numpy as np
import math
import random
from vision_transforms import perspective_transform, get_frustum_coordinates

class Agent:
    def __init__(self, x, y, angle=0, energy=100, vision_pixels=10, vision_range=100):
        self.x = x
        self.y = y
        self.angle = angle
        self.energy = energy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.vision_field = np.full((vision_pixels, 3), [128, 128, 128], dtype=np.uint8)  # Initialize to gray
        self.z_buffer = np.full(vision_pixels, np.inf)  # Initialize z-buffer

    def move(self):
        self.x += 2 * math.cos(self.angle)
        self.y += 2 * math.sin(self.angle)
        self.x = int(self.x) % 800
        self.y = int(self.y) % 600

    def collect_resource(self, resources):
        for resource in resources:
            distance = math.sqrt((self.x - resource.x)**2 + (self.y - resource.y)**2)
            if distance < 15:
                self.energy += 50
                resources.remove(resource)
                return

    def update_vision(self, resources, agents):
        self.vision_field.fill(128)  # Reset to gray
        self.z_buffer.fill(np.inf)  # Reset z-buffer

        for obj_list, color in [(resources, [0, 255, 0]), (agents, [0, 0, 255])]:
            for obj in obj_list:
                if obj == self:
                    continue
                dx = obj.x - self.x
                dy = obj.y - self.y
                world_coordinates = np.array([dx, dy, 1])
                pixel_idx, _, perspective_y = perspective_transform(world_coordinates, 10, 100)
                if pixel_idx is not None and perspective_y < self.z_buffer[pixel_idx]:
                    self.vision_field[pixel_idx] = color
                    self.z_buffer[pixel_idx] = perspective_y
