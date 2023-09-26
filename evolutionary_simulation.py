import pygame
import random
import math
from agent import Agent
from vision_transforms import get_frustum_coordinates  # Import the function

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
RESOURCE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (128, 128, 128)
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

        left_x, left_y, right_x, right_y = get_frustum_coordinates(agent.x, agent.y, agent.angle, VISION_PIXELS, VISION_RANGE)  # Corrected this line
        pygame.draw.line(screen, (255, 255, 255), (agent.x, agent.y), (left_x, left_y), 1)
        pygame.draw.line(screen, (255, 255, 255), (agent.x, agent.y), (right_x, right_y), 1)

    for resource in resources:
        pygame.draw.circle(screen, RESOURCE_COLOR, (resource.x, resource.y), 5)

    for i, agent in enumerate(agents):
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
