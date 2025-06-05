import pygame

def create_shadow_arcana_image():
    """Create pixel art for Shadow Arcana enemy."""
    # Create a 120x180 surface
    image = pygame.Surface((120, 180), pygame.SRCALPHA)
    
    # Shadowy body
    for y in range(40, 160):
        for x in range(40, 80):
            # Create a gradient effect for the shadowy body
            darkness = max(0, 100 - abs(y - 100) - abs(x - 60))
            if darkness > 20:  # Only draw if dark enough
                image.set_at((x, y), (darkness, 0, darkness))
    
    # Glowing eyes
    for i in range(3):
        image.set_at((50 - i, 70), (255, 0, 0))  # Left eye
        image.set_at((50, 70 - i), (255, 0, 0))
        image.set_at((50 + i, 70), (255, 0, 0))
        image.set_at((50, 70 + i), (255, 0, 0))
        
        image.set_at((70 - i, 70), (255, 0, 0))  # Right eye
        image.set_at((70, 70 - i), (255, 0, 0))
        image.set_at((70 + i, 70), (255, 0, 0))
        image.set_at((70, 70 + i), (255, 0, 0))
    
    # Shadowy tendrils
    for i in range(30):
        x = 40 + i
        y = 160 + int(10 * pygame.math.sin(i * 0.2))
        for j in range(5):
            image.set_at((x, y + j), (50, 0, 50))
    
    for i in range(30):
        x = 50 + i
        y = 160 + int(8 * pygame.math.sin(i * 0.3 + 2))
        for j in range(5):
            image.set_at((x, y + j), (50, 0, 50))
    
    # Dark aura effect
    for i in range(360):
        angle = i * 3.14159 / 180
        radius = 50 + (i % 10)
        x = int(60 + radius * pygame.math.cos(angle))
        y = int(100 + radius * pygame.math.sin(angle))
        if 0 <= x < 120 and 0 <= y < 180:
            image.set_at((x, y), (20, 0, 20))
    
    return image
