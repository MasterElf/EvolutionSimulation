import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
RESOURCE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (128, 128, 128)  # Gray background for vision field
ENERGY_FROM_RESOURCE = 50
AGENT_SPEED = 2
RESOURCE_SPAWN_RATE = 100
VISION_PIXELS = 10
VISION_RANGE = 100

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Agent:
    def __init__(self, x, y, angle=0, energy=100):
        self.x = x
        self.y = y
        self.angle = angle
        self.energy = energy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.vision_field = [BACKGROUND_COLOR] * VISION_PIXELS
        self.z_buffer = [float('inf')] * VISION_PIXELS

    def move(self):
        self.x += AGENT_SPEED * math.cos(self.angle)
        self.y += AGENT_SPEED * math.sin(self.angle)
        self.x = int(self.x) % SCREEN_WIDTH
        self.y = int(self.y) % SCREEN_HEIGHT

    def collect_resource(self, resources):
        for resource in resources:
            distance = math.sqrt((self.x - resource.x)**2 + (self.y - resource.y)**2)
            if distance < 15:
                self.energy += ENERGY_FROM_RESOURCE
                resources.remove(resource)
                return

    def update_vision(self, resources, agents):
        self.vision_field = [BACKGROUND_COLOR] * VISION_PIXELS
        self.z_buffer = [float('inf')] * VISION_PIXELS

        for object_list, color in [(resources, RESOURCE_COLOR), (agents, self.color)]:
            for obj in object_list:
                if obj == self:
                    continue

                # Relative coordinates to the agent
                dx = obj.x - self.x
                dy = obj.y - self.y

                # Rotate coordinates to align with agent's orientation
                rotated_x = dx * math.cos(-self.angle) - dy * math.sin(-self.angle)
                rotated_y = dx * math.sin(-self.angle) + dy * math.cos(-self.angle)

                # Perspective transformation
                if rotated_y <= 0:
                    continue

                perspective_x = rotated_x / rotated_y * VISION_RANGE
                perspective_y = rotated_y

                # Calculate which vision pixel this corresponds to
                pixel_idx = int((perspective_x + VISION_RANGE) / (2 * VISION_RANGE) * VISION_PIXELS)

                # Update vision_field and z_buffer
                if 0 <= pixel_idx < VISION_PIXELS:
                    if perspective_y < self.z_buffer[pixel_idx]:
                        self.vision_field[pixel_idx] = color
                        self.z_buffer[pixel_idx] = perspective_y

# Create resources
resources = [Resource(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(20)]

# Create agents
agents = [Agent(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.uniform(0, 2*math.pi)) for _ in range(10)]

# Main game loop
running = True
frame_count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_count += 1
    if frame_count % RESOURCE_SPAWN_RATE == 0:
        resources.append(Resource(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

    for agent in agents:
        agent.move()
        agent.collect_resource(resources)
        agent.update_vision(resources, agents)

    for resource in resources:
        pygame.draw.circle(screen, RESOURCE_COLOR, (resource.x, resource.y), 5)

    for i, agent in enumerate(agents):
        # Draw vision lines and sector
        angle1 = agent.angle - math.pi / VISION_PIXELS
        angle2 = agent.angle + math.pi / VISION_PIXELS
        end_x1 = agent.x + VISION_RANGE * math.cos(angle1)
        end_y1 = agent.y + VISION_RANGE * math.sin(angle1)
        end_x2 = agent.x + VISION_RANGE * math.cos(angle2)
        end_y2 = agent.y + VISION_RANGE * math.sin(angle2)
        pygame.draw.line(screen, (255, 255, 255), (agent.x, agent.y), (end_x1, end_y1), 1)
        pygame.draw.line(screen, (255, 255, 255), (agent.x, agent.y), (end_x2, end_y2), 1)
        pygame.draw.arc(screen, (255, 255, 255), (agent.x - VISION_RANGE, agent.y - VISION_RANGE, 2 * VISION_RANGE, 2 * VISION_RANGE), angle1, angle2, 1)

        pygame.draw.circle(screen, agent.color, (agent.x, agent.y), 10)
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(f"{i+1}", True, (255, 255, 255))
        screen.blit(text, (agent.x - 4, agent.y - 4))

    for i, agent in enumerate(agents):
        pygame.draw.rect(screen, (255, 255, 255), (650, 10 + i*40, 140, 38))
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(f"Agent {i+1}: E={agent.energy}", True, agent.color)
        screen.blit(text, (655, 10 + i*40))
        pygame.draw.rect(screen, (0, 0, 0), (660, 35 + i*40, VISION_PIXELS*3, 10))
        for j, color in enumerate(agent.vision_field):
            pygame.draw.rect(screen, color, (660 + j*3, 35 + i*40, 3, 10))

    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
