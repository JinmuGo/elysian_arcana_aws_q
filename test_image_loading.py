import pygame
import os
import sys

pygame.init()

# Create a simple window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Image Loading Test")

# Try to load an image
image_path = "assets/images/enemies/shadow_arcana.png"
print(f"Current working directory: {os.getcwd()}")
print(f"Looking for image at: {image_path}")
print(f"File exists: {os.path.exists(image_path)}")

try:
    if os.path.exists(image_path):
        image = pygame.image.load(image_path)
        print(f"Image loaded successfully: {image}")
    else:
        print(f"Image not found at {image_path}")
except Exception as e:
    print(f"Error loading image: {e}")

# Keep the window open for a bit
pygame.time.delay(3000)
pygame.quit()
