import pygame

def create_lylac_image():
    # Create a 100x150 pixel art image for Lylac (Tower Arcana)
    image = pygame.Surface((100, 150))
    image.fill((0, 0, 0))  # Black background
    
    # Body - purple robe (representing transformation magic)
    for y in range(50, 130):
        for x in range(35, 65):
            image.set_at((x, y), (128, 0, 128))  # Purple robe
    
    # Head
    for y in range(20, 50):
        for x in range(40, 60):
            image.set_at((x, y), (255, 223, 196))  # Skin tone
    
    # Hair - white/silver hair
    for y in range(15, 35):
        for x in range(35, 65):
            image.set_at((x, y), (220, 220, 255))  # Silver hair
    
    # Face details
    image.set_at((45, 35), (0, 0, 0))  # Left eye
    image.set_at((55, 35), (0, 0, 0))  # Right eye
    
    # Serious expression
    for x in range(45, 56):
        image.set_at((x, 42), (0, 0, 0))
    
    # Arms
    for y in range(60, 100):
        for x in range(25, 35):
            image.set_at((x, y), (128, 0, 128))  # Left arm
        for x in range(65, 75):
            image.set_at((x, y), (128, 0, 128))  # Right arm
    
    # Legs
    for y in range(130, 150):
        for x in range(40, 50):
            image.set_at((x, y), (80, 0, 80))  # Left leg
        for x in range(50, 60):
            image.set_at((x, y), (80, 0, 80))  # Right leg
    
    # Magic wand
    for y in range(60, 100):
        image.set_at((75, y), (200, 200, 200))  # Silver wand
    
    # Magic sparkles around the character
    sparkle_positions = [(30, 30), (70, 30), (30, 120), (70, 120), (50, 15)]
    for pos in sparkle_positions:
        for i in range(3):
            image.set_at((pos[0] + i, pos[1]), (255, 255, 100))
            image.set_at((pos[0] - i, pos[1]), (255, 255, 100))
            image.set_at((pos[0], pos[1] + i), (255, 255, 100))
            image.set_at((pos[0], pos[1] - i), (255, 255, 100))
    
    return image
