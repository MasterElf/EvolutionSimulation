import numpy as np
import math
from vision_transforms import perspective_transform

class Agent:
    def __init__(self, x, y, angle=0, energy=100):
        self.x = x
        self.y = y
        self.angle = angle
        self.energy = energy
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.vision_field = np.zeros((10, 3), dtype=int)
        self.z_buffer = np.full(10, np.inf)

    def move(self, screen_width, screen_height, agent_speed):
        self.x += agent_speed * math.cos(self.angle)
        self.y += agent_speed * math.sin(self.angle)
        self.x = int(self.x) % screen_width
        self.y = int(self.y) % screen_height

    def collect_resource(self, resources):
        for resource in resources:
            distance = math.sqrt((self.x - resource.x)**2 + (self.y - resource.y)**2)
            if distance < 15:
                self.energy += 50
                resources.remove(resource)
                return

    def update_vision(self, resources, agents, background_color, vision_pixels, vision_range):
        self.vision_field[:, :] = background_color  # This line replaces the fill function
        self.z_buffer.fill(np.inf)
        
        for obj_list in [resources, agents]:
            for obj in obj_list:
                if obj == self:
                    continue
                
                world_coordinates = np.array([obj.x - self.x, obj.y - self.y, 1])
                
                pixel_idx, perspective_x, perspective_y = perspective_transform(
                    world_coordinates, vision_pixels, vision_range
                )
                
                if pixel_idx is not None:
                    if perspective_y < self.z_buffer[pixel_idx]:
                        self.z_buffer[pixel_idx] = perspective_y
                        color = obj.color if hasattr(obj, 'color') else (255, 255, 255)
                        self.vision_field[pixel_idx] = color
