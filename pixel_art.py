import pygame
import os

def create_pixel_art():
    """Create pixel art for characters and cards and save them as PNG files."""
    # Initialize pygame
    pygame.init()
    
    # Create directories if they don't exist
    os.makedirs("assets/images/characters", exist_ok=True)
    os.makedirs("assets/images/cards", exist_ok=True)
    os.makedirs("assets/images/enemies", exist_ok=True)
    
    # Create character pixel art
    create_arion_image()
    create_lylac_image()
    
    # Create enemy pixel art
    create_shadow_arcana_image()
    
    # Create card pixel art
    create_slash_card()
    create_defend_card()
    create_arcane_bolt_card()
    create_fireball_card()
    create_heal_card()
    create_earth_shield_card()
    
    print("All pixel art created successfully!")

def create_arion_image():
    """Create pixel art for Arion (The Fool)."""
    # Create a 100x150 surface
    image = pygame.Surface((100, 150), pygame.SRCALPHA)
    
    # Blue robe (representing The Fool)
    for y in range(50, 130):
        for x in range(35, 65):
            # Add some shading
            blue = max(65, 105 - abs(x - 50) * 2)
            image.set_at((x, y), (blue, blue, 225))
    
    # Head
    for y in range(20, 50):
        for x in range(40, 60):
            if (x - 50)**2 + (y - 35)**2 < 100:  # Circular head
                image.set_at((x, y), (255, 223, 196))  # Skin tone
    
    # Hair (blonde for The Fool)
    for y in range(15, 30):
        for x in range(35, 65):
            if (x - 50)**2 + (y - 25)**2 < 120:  # Hair shape
                image.set_at((x, y), (240, 220, 130))
    
    # Face details
    image.set_at((45, 35), (0, 0, 0))  # Left eye
    image.set_at((55, 35), (0, 0, 0))  # Right eye
    
    # Smile
    for x in range(45, 56):
        if 45 <= x <= 47 or 53 <= x <= 55:
            image.set_at((x, 40), (0, 0, 0))
        else:
            image.set_at((x, 42), (0, 0, 0))
    
    # Arms
    for y in range(60, 100):
        # Left arm
        for x in range(25, 35):
            if 25 <= x <= 30 and 60 <= y <= 100:
                image.set_at((x, y), (65, 105, 225))
        # Right arm
        for x in range(65, 75):
            if 70 <= x <= 75 and 60 <= y <= 100:
                image.set_at((x, y), (65, 105, 225))
    
    # Legs
    for y in range(130, 150):
        # Left leg
        for x in range(40, 50):
            image.set_at((x, y), (50, 50, 150))
        # Right leg
        for x in range(50, 60):
            image.set_at((x, y), (50, 50, 150))
    
    # Staff (The Fool's walking stick)
    for y in range(40, 140):
        for x in range(79, 82):
            image.set_at((x, y), (139, 69, 19))
    
    # The Fool's bag
    for y in range(70, 90):
        for x in range(20, 30):
            image.set_at((x, y), (139, 69, 19))
    
    # Save the image
    pygame.image.save(image, "assets/images/characters/arion.png")
    print("Created Arion character image")

def create_lylac_image():
    """Create pixel art for Lylac (Tower Arcana)."""
    # Create a 100x150 surface
    image = pygame.Surface((100, 150), pygame.SRCALPHA)
    
    # Purple robe (representing Tower Arcana)
    for y in range(50, 130):
        for x in range(35, 65):
            # Add some shading
            purple = max(80, 128 - abs(x - 50) * 2)
            image.set_at((x, y), (purple, 0, purple))
    
    # Head
    for y in range(20, 50):
        for x in range(40, 60):
            if (x - 50)**2 + (y - 35)**2 < 100:  # Circular head
                image.set_at((x, y), (255, 223, 196))  # Skin tone
    
    # Hair (silver for magical character)
    for y in range(15, 35):
        for x in range(35, 65):
            if (x - 50)**2 + (y - 25)**2 < 120:  # Hair shape
                image.set_at((x, y), (220, 220, 255))
    
    # Face details
    image.set_at((45, 35), (0, 0, 0))  # Left eye
    image.set_at((55, 35), (0, 0, 0))  # Right eye
    
    # Serious expression
    for x in range(45, 56):
        image.set_at((x, 42), (0, 0, 0))
    
    # Arms
    for y in range(60, 100):
        # Left arm
        for x in range(25, 35):
            if 25 <= x <= 30 and 60 <= y <= 100:
                image.set_at((x, y), (128, 0, 128))
        # Right arm
        for x in range(65, 75):
            if 70 <= x <= 75 and 60 <= y <= 100:
                image.set_at((x, y), (128, 0, 128))
    
    # Legs
    for y in range(130, 150):
        # Left leg
        for x in range(40, 50):
            image.set_at((x, y), (80, 0, 80))
        # Right leg
        for x in range(50, 60):
            image.set_at((x, y), (80, 0, 80))
    
    # Magic wand
    for y in range(60, 100):
        for x in range(74, 77):
            image.set_at((x, y), (200, 200, 200))
    
    # Magic sparkles
    sparkle_positions = [(30, 30), (70, 30), (30, 120), (70, 120), (50, 15)]
    for pos in sparkle_positions:
        for i in range(3):
            image.set_at((pos[0] + i, pos[1]), (255, 255, 100))
            image.set_at((pos[0] - i, pos[1]), (255, 255, 100))
            image.set_at((pos[0], pos[1] + i), (255, 255, 100))
            image.set_at((pos[0], pos[1] - i), (255, 255, 100))
    
    # Save the image
    pygame.image.save(image, "assets/images/characters/lylac.png")
    print("Created Lylac character image")

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
        y = 160 + int(10 * ((i % 10) / 10))
        for j in range(5):
            image.set_at((x, y + j), (50, 0, 50))
    
    for i in range(30):
        x = 50 + i
        y = 160 + int(8 * ((i % 8) / 8))
        for j in range(5):
            image.set_at((x, y + j), (50, 0, 50))
    
    # Dark aura effect
    for i in range(0, 360, 10):
        angle = i * 3.14159 / 180
        radius = 50 + (i % 10)
        x = int(60 + radius * pygame.math.cos(angle))
        y = int(100 + radius * pygame.math.sin(angle))
        if 0 <= x < 120 and 0 <= y < 180:
            image.set_at((x, y), (20, 0, 20))
    
    # Save the image
    pygame.image.save(image, "assets/images/enemies/shadow_arcana.png")
    print("Created Shadow Arcana enemy image")

def create_slash_card():
    """Create pixel art for Slash card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Blue sword pixel art
    pixels = [
        "              ",
        "      ##      ",
        "     ####     ",
        "      ##      ",
        "      ##      ",
        "      ##      ",
        "     ####     ",
        "    ######    ",
        "   ## ## ##   ",
        "  ##  ##  ##  ",
        " ##   ##   ## ",
        "##    ##    ##",
        "      ##      ",
        "     ####     ",
    ]
    
    # Draw the pixel art
    for y, row in enumerate(pixels):
        for x, col in enumerate(row):
            if col == '#':
                image.set_at((x + 30, y + 30), (65, 105, 225))  # Blue
    
    # Add some slash effect lines
    for i in range(5):
        pygame.draw.line(image, (200, 200, 255), (20 + i*20, 20), (40 + i*20, 80), 2)
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/slash.png")
    print("Created Slash card image")

def create_defend_card():
    """Create pixel art for Defend card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Shield pixel art
    shield_color = (65, 105, 225)  # Blue
    
    # Draw shield outline
    for x in range(30, 100):
        for y in range(20, 80):
            # Shield shape
            if ((x - 65)**2) / 900 + ((y - 50)**2) / 400 <= 1:
                # Border
                if ((x - 65)**2) / 800 + ((y - 50)**2) / 300 >= 0.9:
                    image.set_at((x, y), shield_color)
                # Inner shield
                elif ((x - 65)**2) / 600 + ((y - 50)**2) / 200 <= 0.8:
                    image.set_at((x, y), shield_color)
    
    # Draw shield emblem
    for x in range(55, 75):
        for y in range(40, 60):
            if abs(x - 65) + abs(y - 50) < 10:
                image.set_at((x, y), (200, 200, 255))
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/defend.png")
    print("Created Defend card image")

def create_arcane_bolt_card():
    """Create pixel art for Arcane Bolt card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Purple arcane bolt
    for i in range(20):
        # Main bolt
        x1 = 30 + i * 3
        y1 = 50 + int(10 * pygame.math.sin(i * 0.5))
        
        # Bolt thickness
        for j in range(-3, 4):
            y = y1 + j
            if 0 <= y < 100:
                # Gradient from white center to purple edges
                color_intensity = max(0, 255 - abs(j) * 60)
                if abs(j) < 2:
                    image.set_at((x1, y), (color_intensity, color_intensity, 255))
                else:
                    image.set_at((x1, y), (color_intensity // 2, 0, color_intensity))
    
    # Arcane sparkles
    for _ in range(20):
        x = 30 + (_ * 7) % 70
        y = 30 + (_ * 5) % 40
        size = (_ % 3) + 1
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                if i*i + j*j <= size*size:
                    px, py = x + i, y + j
                    if 0 <= px < 130 and 0 <= py < 100:
                        image.set_at((px, py), (200, 100, 255))
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/arcane_bolt.png")
    print("Created Arcane Bolt card image")

def create_fireball_card():
    """Create pixel art for Fireball card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Fireball pixel art
    center_x, center_y = 65, 50
    radius = 25
    
    # Draw the fireball
    for x in range(center_x - radius, center_x + radius):
        for y in range(center_y - radius, center_y + radius):
            distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
            if distance <= radius:
                # Create a gradient from yellow to red
                red = min(255, int(255 - distance * 3))
                green = max(0, int(150 - distance * 6))
                if 0 <= x < 130 and 0 <= y < 100:
                    image.set_at((x, y), (red, green, 0))
    
    # Add flame particles
    for i in range(30):
        angle = i * 12
        distance = radius - 5 + (i % 10)
        x = int(center_x + distance * pygame.math.cos(angle * 3.14159 / 180))
        y = int(center_y + distance * pygame.math.sin(angle * 3.14159 / 180))
        
        if 0 <= x < 130 and 0 <= y < 100:
            # Small flame
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx*dx + dy*dy <= 4:
                        px, py = x + dx, y + dy
                        if 0 <= px < 130 and 0 <= py < 100:
                            image.set_at((px, py), (255, 200, 0))
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/fireball.png")
    print("Created Fireball card image")

def create_heal_card():
    """Create pixel art for Heal card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Heart pixel art
    heart_pixels = [
        "    #####  #####    ",
        "   ####### #######   ",
        "  ##################  ",
        " #################### ",
        " #################### ",
        "######################",
        "######################",
        "######################",
        " #################### ",
        "  ##################  ",
        "   ################   ",
        "    ##############    ",
        "     ############     ",
        "      ##########      ",
        "       ########       ",
        "        ######        ",
        "         ####         ",
        "          ##          ",
    ]
    
    # Draw the heart
    for y, row in enumerate(heart_pixels):
        for x, col in enumerate(row):
            if col == '#':
                # Create a gradient from light to dark green
                green = min(255, 180 + y * 2)
                image.set_at((x + 25, y + 25), (100, green, 100))
    
    # Add healing sparkles
    for i in range(15):
        x = 25 + (i * 8) % 80
        y = 25 + (i * 7) % 50
        size = (i % 3) + 1
        
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                if dx*dx + dy*dy <= size*size:
                    px, py = x + dx, y + dy
                    if 0 <= px < 130 and 0 <= py < 100:
                        image.set_at((px, py), (200, 255, 200))
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/heal.png")
    print("Created Heal card image")

def create_earth_shield_card():
    """Create pixel art for Earth Shield card."""
    # Create a 130x100 surface
    image = pygame.Surface((130, 100), pygame.SRCALPHA)
    
    # Earth shield pixel art
    center_x, center_y = 65, 50
    
    # Draw rocky shield
    for x in range(30, 100):
        for y in range(20, 80):
            # Shield shape
            if ((x - center_x)**2) / 900 + ((y - center_y)**2) / 400 <= 1:
                # Create rocky texture
                noise = (x * y) % 10
                brown = min(139 + noise, 200)
                green = min(69 + noise, 100)
                image.set_at((x, y), (brown, green, 19))
    
    # Add rocky details
    for i in range(20):
        x = 40 + (i * 13) % 50
        y = 30 + (i * 11) % 40
        size = (i % 3) + 2
        
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                if dx*dx + dy*dy <= size*size:
                    px, py = x + dx, y + dy
                    if 0 <= px < 130 and 0 <= py < 100:
                        image.set_at((px, py), (100, 80, 0))
    
    # Save the image
    pygame.image.save(image, "assets/images/cards/earth_shield.png")
    print("Created Earth Shield card image")

if __name__ == "__main__":
    create_pixel_art()
