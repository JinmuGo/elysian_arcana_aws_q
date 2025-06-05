import pygame
import random

def create_reversed_magician_image():
    """Create pixel art for Reversed Magician enemy."""
    # Create a 120x180 surface
    image = pygame.Surface((120, 180), pygame.SRCALPHA)
    
    # Dark blue robe
    for y in range(60, 160):
        for x in range(30, 90):
            # Create a robe shape
            if ((x - 60)**2) / 900 + ((y - 110)**2) / 2500 <= 1:
                # Add some texture to the robe
                blue_value = 100 + (x * y) % 50
                image.set_at((x, y), (0, 0, blue_value))
    
    # Magician's hat
    for y in range(20, 60):
        for x in range(40, 80):
            # Hat shape
            if 40 <= x <= 80 and 50 <= y <= 60:  # Hat brim
                image.set_at((x, y), (0, 0, 80))
            elif 45 <= x <= 75 and 20 <= y <= 50:  # Hat top
                image.set_at((x, y), (0, 0, 60))
    
    # Face (shadowed)
    for y in range(60, 80):
        for x in range(50, 70):
            # Oval face shape
            if ((x - 60)**2) / 100 + ((y - 70)**2) / 100 <= 1:
                image.set_at((x, y), (50, 50, 100))
    
    # Glowing eyes (reversed/corrupted)
    for i in range(2):
        image.set_at((55 - i, 70), (0, 200, 255))  # Left eye
        image.set_at((55, 70 - i), (0, 200, 255))
        image.set_at((55 + i, 70), (0, 200, 255))
        
        image.set_at((65 - i, 70), (0, 200, 255))  # Right eye
        image.set_at((65, 70 - i), (0, 200, 255))
        image.set_at((65 + i, 70), (0, 200, 255))
    
    # Staff
    for y in range(40, 160):
        for x in range(90, 95):
            image.set_at((x, y), (100, 50, 0))  # Brown staff
    
    # Magic orb on staff
    for y in range(30, 50):
        for x in range(85, 105):
            # Circular orb
            if ((x - 95)**2 + (y - 40)**2) <= 100:
                # Swirling magic effect
                blue = (x * y) % 255
                image.set_at((x, y), (0, blue, 255))
    
    # Magical effects around the magician
    for _ in range(50):
        x = random.randint(20, 100)
        y = random.randint(20, 160)
        size = random.randint(1, 2)
        
        # Small magical particles
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                if i*i + j*j <= size*size:
                    px, py = x + i, y + j
                    if 0 <= px < 120 and 0 <= py < 180:
                        image.set_at((px, py), (0, 150, 255))
    
    return image
