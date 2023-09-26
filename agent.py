import numpy as np
import math
import random
from vision_transforms import perspective_transform
from config import VISION_PIXELS, VISION_RANGE, BACKGROUND_COLOR

class Agent:
    def __init__(self, x, y, angle=0, energy=100):
        self.x = x
        self.y = y
        self.angle = angle
        self.energy = energy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.vision_field = np.empty([VISION_PIXELS, 3], dtype=int)
        self.vision_field[:] = BACKGROUND_COLOR
        self.z_buffer = np.full(VISION_PIXELS, np.inf)

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, AGENT_SPEED):
        self.x = (self.x + AGENT_SPEED * math.cos(self.angle)) % SCREEN_WIDTH
        self.y = (self.y + AGENT_SPEED * math.sin(self.angle)) % SCREEN_HEIGHT

    def collect_resource(self, resources):
        for resource in resources:
            distance = math.sqrt((self.x - resource.x)**2 + (self.y - resource.y)**2)
            if distance < 15:
                self.energy += 50  # Amount of energy obtained from a resource
                resources.remove(resource)
                return

    def update_vision(self, resources, agents):
        self.vision_field[:] = BACKGROUND_COLOR
        self.z_buffer[:] = np.inf

        for object_list in [resources, agents]:
            for obj in object_list:
                if obj == self:
                    continue
                pixel_idx, perspective_x, perspective_y = perspective_transform(np.array([obj.x, obj.y, 1]), VISION_PIXELS, VISION_RANGE)
                
                if pixel_idx is None:
                    continue

                if perspective_y < self.z_buffer[pixel_idx]:
                    self.z_buffer[pixel_idx] = perspective_y
                    self.vision_field[pixel_idx] = obj.color if isinstance(obj, Agent) else RESOURCE_COLOR
