import pygame

def create_slash_card_image():
    # Create a 130x100 pixel art image for the slash card
    image = pygame.Surface((130, 100))
    image.fill((0, 0, 0))  # Black background
    
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
    
    return image
