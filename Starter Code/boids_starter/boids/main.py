import os
import sys
import random
import math
import pygame
import imageio.v2 as imageio

from datatypes import OrderedPair, Boid, Sky
from functions import simulate_boids
from drawing import animate_system

def main():
    # Get command-line arguments
    num_boids = int(sys.argv[1])
    sky_width = float(sys.argv[2])
    initial_speed = float(sys.argv[3])
    max_boid_speed = float(sys.argv[4])
    num_gens = int(sys.argv[5])
    proximity = float(sys.argv[6])
    separation_factor = float(sys.argv[7])
    alignment_factor = float(sys.argv[8])
    cohesion_factor = float(sys.argv[9])
    time_step = float(sys.argv[10])
    canvas_width = int(sys.argv[11])
    image_frequency = int(sys.argv[12])
    # Initialize pygame
    pygame.init()
    # Generate initial sky with random boids
    boids = []
    for _ in range(num_boids):
        position = OrderedPair(random.uniform(0, sky_width), random.uniform(0, sky_width))
        angle = random.uniform(0, 2 * math.pi)
        velocity = OrderedPair(initial_speed * math.cos(angle), initial_speed * math.sin(angle))
        acceleration = OrderedPair(0.0, 0.0)
        boids.append(Boid(position, velocity, acceleration))
    initial_sky = Sky(sky_width, boids, max_boid_speed, proximity, separation_factor, alignment_factor, cohesion_factor)
    # Call simulation
    time_points = simulate_boids(initial_sky, num_gens, time_step)
    # Call animate_system
    frames = animate_system(time_points, canvas_width, image_frequency)
    # Render MP4
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "boids_simulation.mp4")
    writer = imageio.get_writer(output_file, fps=30, codec="libx264", quality=8)
    for frame in frames:
        writer.append_data(frame)
    writer.close()
    pygame.quit()

if __name__ == "__main__":
    main()
