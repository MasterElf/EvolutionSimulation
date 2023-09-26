import numpy as np
import math

def perspective_transform(world_coordinates, vision_pixels, vision_range):
    # Define the transformation matrix
    transform_matrix = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    # Apply the transformation
    screen_coordinates = world_coordinates @ transform_matrix
    if screen_coordinates[2] <= 0:
        return None, None, None

    perspective_x = screen_coordinates[0] / screen_coordinates[2] * vision_range
    perspective_y = screen_coordinates[2]
    pixel_idx = int((perspective_x + vision_range) / (2 * vision_range) * vision_pixels)

    # Check for valid pixel index
    if pixel_idx < 0 or pixel_idx >= vision_pixels:
        return None, None, None

    return pixel_idx, perspective_x, perspective_y

def get_frustum_coordinates(agent_x, agent_y, angle, vision_pixels, vision_range):
    # Calculate the angles for the leftmost and rightmost vision pixels
    half_fov = math.pi / vision_pixels
    left_angle = angle - half_fov
    right_angle = angle + half_fov

    # Calculate the coordinates for the leftmost and rightmost vision points in agent's coordinate system
    left_x = agent_x + vision_range * math.cos(left_angle)
    left_y = agent_y + vision_range * math.sin(left_angle)
    right_x = agent_x + vision_range * math.cos(right_angle)
    right_y = agent_y + vision_range * math.sin(right_angle)

    return int(left_x), int(left_y), int(right_x), int(right_y)
