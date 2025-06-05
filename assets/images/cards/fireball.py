import pygame

def create_fireball_card_image():
    # Create a 130x100 pixel art image for the fireball card
    image = pygame.Surface((130, 100))
    image.fill((0, 0, 0))  # Black background
    
    # Fireball pixel art
    pixels = [
        "      ###      ",
        "    #######    ",
        "   #########   ",
        "  ###########  ",
        " ############# ",
        " ############# ",
        "###############",
        "###############",
        "###############",
        " ############# ",
        " ############# ",
        "  ###########  ",
        "   #########   ",
        "    #######    ",
        "      ###      ",
    ]
    
    # Draw the pixel art
    for y, row in enumerate(pixels):
        for x, col in enumerate(row):
            if col == '#':
                # Create a gradient from yellow to red
                red = min(255, 200 + y * 3)
                green = max(0, 150 - y * 10)
                image.set_at((x + 30, y + 30), (red, green, 0))
    
    # Add some flame particles
    for i in range(20):
        x = 30 + (i * 7) % 70
        y = 30 + (i * 5) % 40
        size = (i % 3) + 1
        pygame.draw.circle(image, (255, 200, 0), (x, y), size)
    
    return image
