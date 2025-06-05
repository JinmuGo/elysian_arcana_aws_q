import pygame
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enemies.shadow_arcana import create_shadow_arcana_image
from enemies.reversed_magician import create_reversed_magician_image
from enemies.corrupted_empress import create_corrupted_empress_image
from enemies.tower_guardian import create_tower_guardian_image

def generate_enemy_images():
    """Generate all enemy pixel art assets and save them as PNG files."""
    pygame.init()
    
    # Create directory if it doesn't exist
    os.makedirs("enemies", exist_ok=True)
    
    # Generate and save enemy images
    enemies = {
        "shadow_arcana": create_shadow_arcana_image(),
        "reversed_magician": create_reversed_magician_image(),
        "corrupted_empress": create_corrupted_empress_image(),
        "tower_guardian": create_tower_guardian_image()
    }
    
    for name, image in enemies.items():
        pygame.image.save(image, f"enemies/{name}.png")
        print(f"Generated enemy image: enemies/{name}.png")
    
    print("All enemy images generated successfully!")

if __name__ == "__main__":
    generate_enemy_images()
