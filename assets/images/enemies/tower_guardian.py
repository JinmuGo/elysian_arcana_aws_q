import pygame

def create_tower_guardian_image():
    """Create pixel art for Tower Guardian enemy."""
    # Create a 120x180 surface
    image = pygame.Surface((120, 180), pygame.SRCALPHA)
    
    # Stone body
    for y in range(40, 160):
        for x in range(30, 90):
            # Create a golem-like shape
            in_body = False
            
            # Torso (rectangular)
            if 40 <= x <= 80 and 70 <= y <= 130:
                in_body = True
                
            # Head (circular)
            elif ((x - 60)**2 + (y - 55)**2) <= 225:  # radius 15
                in_body = True
                
            # Arms (rectangular)
            elif (30 <= x <= 40 and 70 <= y <= 120) or (80 <= x <= 90 and 70 <= y <= 120):
                in_body = True
                
            # Legs (rectangular)
            elif (45 <= x <= 55 and 130 <= y <= 160) or (65 <= x <= 75 and 130 <= y <= 160):
                in_body = True
                
            if in_body:
                # Stone texture
                noise = (x * y) % 30
                gray = 100 + noise
                image.set_at((x, y), (gray, gray, 0))  # Yellowish stone
    
    # Cracks in the stone (representing damage/age)
    for i in range(5):
        start_x = 50 + i * 5
        start_y = 80
        
        for j in range(20):
            x = start_x + j % 3 - 1
            y = start_y + j
            
            if 0 <= x < 120 and 0 <= y < 180:
                image.set_at((x, y), (50, 50, 0))
    
    # Glowing eyes
    for i in range(3):
        image.set_at((53 - i, 55), (255, 255, 0))  # Left eye
        image.set_at((53, 55 - i), (255, 255, 0))
        image.set_at((53 + i, 55), (255, 255, 0))
        
        image.set_at((67 - i, 55), (255, 255, 0))  # Right eye
        image.set_at((67, 55 - i), (255, 255, 0))
        image.set_at((67 + i, 55), (255, 255, 0))
    
    # Tower symbol on chest
    for y in range(90, 110):
        for x in range(55, 65):
            # Tower base
            if 55 <= x <= 65 and 100 <= y <= 110:
                image.set_at((x, y), (50, 50, 0))
                
            # Tower top
            if 57 <= x <= 63 and 90 <= y <= 100:
                image.set_at((x, y), (50, 50, 0))
    
    # Lightning effect around the guardian
    for i in range(0, 360, 45):
        angle = i * 3.14159 / 180
        length = 30
        
        start_x = int(60 + 40 * pygame.math.cos(angle))
        start_y = int(100 + 40 * pygame.math.sin(angle))
        
        for j in range(length):
            # Create jagged lightning effect
            offset = (j % 3) - 1
            x = int(start_x + j * pygame.math.cos(angle) + offset)
            y = int(start_y + j * pygame.math.sin(angle) + offset)
            
            if 0 <= x < 120 and 0 <= y < 180:
                image.set_at((x, y), (255, 255, 0))  # Yellow lightning
    
    return image
