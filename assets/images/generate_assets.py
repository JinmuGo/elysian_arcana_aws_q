import pygame
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from images.cards.slash import create_slash_card_image
from images.cards.fireball import create_fireball_card_image
from images.cards.heal import create_heal_card_image
from images.characters.arion import create_arion_image
from images.characters.lylac import create_lylac_image
from images.enemies.shadow_arcana import create_shadow_arcana_image

def generate_all_assets():
    """Generate all pixel art assets and save them as PNG files."""
    pygame.init()
    
    # Create directories if they don't exist
    os.makedirs("cards", exist_ok=True)
    os.makedirs("characters", exist_ok=True)
    os.makedirs("enemies", exist_ok=True)
    
    # Generate and save card images
    cards = {
        "slash": create_slash_card_image(),
        "fireball": create_fireball_card_image(),
        "heal": create_heal_card_image()
    }
    
    for name, image in cards.items():
        pygame.image.save(image, f"cards/{name}.png")
        print(f"Generated card image: cards/{name}.png")
    
    # Generate and save character images
    characters = {
        "arion": create_arion_image(),
        "lylac": create_lylac_image()
    }
    
    for name, image in characters.items():
        pygame.image.save(image, f"characters/{name}.png")
        print(f"Generated character image: characters/{name}.png")
    
    # Generate and save enemy images
    enemies = {
        "shadow_arcana": create_shadow_arcana_image()
    }
    
    for name, image in enemies.items():
        pygame.image.save(image, f"enemies/{name}.png")
        print(f"Generated enemy image: enemies/{name}.png")
    
    print("All assets generated successfully!")

if __name__ == "__main__":
    generate_all_assets()
