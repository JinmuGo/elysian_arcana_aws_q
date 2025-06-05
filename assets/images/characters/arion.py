import pygame

def create_arion_image():
    # Create a 100x150 pixel art image for Arion (The Fool)
    image = pygame.Surface((100, 150))
    image.fill((0, 0, 0))  # Black background
    
    # Body
    for y in range(50, 130):
        for x in range(35, 65):
            image.set_at((x, y), (65, 105, 225))  # Blue robe
    
    # Head
    for y in range(20, 50):
        for x in range(40, 60):
            image.set_at((x, y), (255, 223, 196))  # Skin tone
    
    # Hair
    for y in range(15, 30):
        for x in range(35, 65):
            image.set_at((x, y), (240, 220, 130))  # Blonde hair
    
    # Face details
    image.set_at((45, 35), (0, 0, 0))  # Left eye
    image.set_at((55, 35), (0, 0, 0))  # Right eye
    
    # Draw a smile
    for x in range(45, 56):
        image.set_at((x, 40), (0, 0, 0))
    
    # Arms
    for y in range(60, 100):
        for x in range(25, 35):
            image.set_at((x, y), (65, 105, 225))  # Left arm
        for x in range(65, 75):
            image.set_at((x, y), (65, 105, 225))  # Right arm
    
    # Legs
    for y in range(130, 150):
        for x in range(40, 50):
            image.set_at((x, y), (50, 50, 150))  # Left leg
        for x in range(50, 60):
            image.set_at((x, y), (50, 50, 150))  # Right leg
    
    # Staff (representing The Fool's walking stick)
    for y in range(40, 140):
        image.set_at((80, y), (139, 69, 19))  # Brown staff
    
    # The Fool's bag
    for y in range(70, 90):
        for x in range(20, 30):
            image.set_at((x, y), (139, 69, 19))  # Brown bag
    
    return image
