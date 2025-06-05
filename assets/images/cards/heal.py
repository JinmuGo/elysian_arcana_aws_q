import pygame

def create_heal_card_image():
    # Create a 130x100 pixel art image for the heal card
    image = pygame.Surface((130, 100))
    image.fill((0, 0, 0))  # Black background
    
    # Heart pixel art
    pixels = [
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
    
    # Draw the pixel art
    for y, row in enumerate(pixels):
        for x, col in enumerate(row):
            if col == '#':
                # Create a gradient from light to dark green
                green = min(255, 180 + y * 2)
                image.set_at((x + 25, y + 25), (100, green, 100))
    
    # Add some healing sparkles
    for i in range(15):
        x = 25 + (i * 8) % 80
        y = 25 + (i * 7) % 50
        size = (i % 3) + 1
        pygame.draw.circle(image, (200, 255, 200), (x, y), size)
    
    return image
