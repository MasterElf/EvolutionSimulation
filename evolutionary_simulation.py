import pygame
import random
import math
from agent import Agent
from config import *

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RESOURCE_COLOR

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
        agent.move(SCREEN_WIDTH, SCREEN_HEIGHT, AGENT_SPEED)
        agent.collect_resource(resources)
        agent.update_vision(resources, agents)

    for resource in resources:
        pygame.draw.circle(screen, RESOURCE_COLOR, (resource.x, resource.y), 5)

    for i, agent in enumerate(agents):
        pygame.draw.circle(screen, agent.color, (agent.x, agent.y), 10)
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(f"{i+1}", True, (255, 255, 255))
        screen.blit(text, (agent.x - 4, agent.y - 4))

    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
