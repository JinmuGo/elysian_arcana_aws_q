import pygame

def create_corrupted_empress_image():
    """Create pixel art for Corrupted Empress enemy."""
    # Create a 120x180 surface
    image = pygame.Surface((120, 180), pygame.SRCALPHA)
    
    # Empress dress (dark red)
    for y in range(60, 170):
        for x in range(30, 90):
            # Create a dress shape (wider at bottom)
            width_factor = (y - 60) / 110  # 0 at top, 1 at bottom
            dress_width = 30 + int(width_factor * 20)
            
            if 60 - dress_width <= x <= 60 + dress_width:
                # Add some texture to the dress
                red_value = 150 - (x * y) % 50
                image.set_at((x, y), (red_value, 0, 0))
    
    # Crown
    for y in range(20, 35):
        for x in range(45, 75):
            # Crown base
            if 45 <= x <= 75 and 30 <= y <= 35:
                image.set_at((x, y), (200, 150, 0))  # Gold
                
            # Crown points
            if ((x == 50 or x == 60 or x == 70) and 20 <= y <= 30) or \
               ((x == 55 or x == 65) and 25 <= y <= 30):
                image.set_at((x, y), (200, 150, 0))  # Gold
    
    # Face
    for y in range(35, 55):
        for x in range(50, 70):
            # Oval face shape
            if ((x - 60)**2) / 100 + ((y - 45)**2) / 100 <= 1:
                image.set_at((x, y), (200, 150, 150))  # Pale skin
    
    # Corrupted eyes (red)
    for i in range(2):
        image.set_at((55 - i, 45), (255, 0, 0))  # Left eye
        image.set_at((55, 45 - i), (255, 0, 0))
        image.set_at((55 + i, 45), (255, 0, 0))
        
        image.set_at((65 - i, 45), (255, 0, 0))  # Right eye
        image.set_at((65, 45 - i), (255, 0, 0))
        image.set_at((65 + i, 45), (255, 0, 0))
    
    # Scepter
    for y in range(60, 150):
        for x in range(90, 95):
            image.set_at((x, y), (150, 100, 0))  # Golden scepter
    
    # Scepter top
    for y in range(50, 60):
        for x in range(85, 100):
            # Circular orb
            if ((x - 92)**2 + (y - 55)**2) <= 49:
                image.set_at((x, y), (200, 0, 0))  # Red orb
    
    # Corruption effect (dark tendrils)
    for i in range(0, 360, 20):
        angle = i * 3.14159 / 180
        for r in range(5, 20, 2):
            x = int(60 + r * 2 * pygame.math.cos(angle))
            y = int(100 + r * pygame.math.sin(angle))
            
            if 0 <= x < 120 and 0 <= y < 180:
                for j in range(3):
                    px = x + j - 1
                    py = y
                    if 0 <= px < 120 and 0 <= py < 180:
                        image.set_at((px, py), (100, 0, 0))
    
    return image
