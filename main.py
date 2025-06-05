import pygame
import sys
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()

# Print current working directory for debugging
print(f"Current working directory: {os.getcwd()}")
print(f"Assets directory exists: {os.path.exists('assets')}")
print(f"Images directory exists: {os.path.exists('assets/images')}")
print(f"Enemies directory exists: {os.path.exists('assets/images/enemies')}")
print(f"Enemy images: {os.listdir('assets/images/enemies') if os.path.exists('assets/images/enemies') else 'directory not found'}")

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (218, 165, 32)
BLUE = (65, 105, 225)
RED = (178, 34, 34)
GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)

# Game states
MAIN_MENU = 0
BATTLE = 1
DECK_BUILDING = 2
GAME_OVER = 3
VICTORY = 4
REWARD_SCREEN = 5
STAGE_TRANSITION = 6

# Turn states
PLAYER_TURN = 0
ENEMY_TURN = 1
TURN_TRANSITION = 2

# Action states - for clear instruction flow
WAITING_FOR_CARD = 0
WAITING_FOR_TARGET = 1
EXECUTING_ACTION = 2

class Card:
    def __init__(self, name, cost, damage, healing, effect_text, element):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.healing = healing
        self.effect_text = effect_text
        self.element = element
        self.rect = pygame.Rect(0, 0, 150, 200)
        self.selected = False
        
        # Try to load card image from preloaded images
        self.image = None
        if hasattr(pygame.app, 'game') and hasattr(pygame.app.game, 'card_images'):
            card_name = self.name.lower().replace(' ', '_')
            if card_name in pygame.app.game.card_images:
                self.image = pygame.app.game.card_images[card_name]
                print(f"Using preloaded image for card {self.name}")
        
        # If no preloaded image, try to load directly
        if self.image is None:
            image_path = os.path.join("assets", "images", "cards", f"{self.name.lower().replace(' ', '_')}.png")
            try:
                if os.path.exists(image_path):
                    self.image = pygame.image.load(image_path)
                    self.image = pygame.transform.scale(self.image, (130, 100))
                    print(f"Loaded image for card {self.name} from {image_path}")
            except Exception as e:
                print(f"Error loading card image: {e}")
                self.image = None
            
        # If no image, create a colored surface
        if self.image is None:
            self.image = pygame.Surface((130, 100))
            if self.element == "fire":
                self.image.fill(RED)
            elif self.element == "earth":
                self.image.fill(GREEN)
            elif self.element == "arcana":
                self.image.fill(PURPLE)
            else:
                self.image.fill(BLUE)
            print(f"Created fallback image for card {self.name}")
        
    def draw(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        
        # Card background
        color = BLUE
        if self.element == "fire":
            color = RED
        elif self.element == "earth":
            color = GREEN
        elif self.element == "arcana":
            color = PURPLE
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, GOLD, self.rect, 3)
        
        # Card image
        screen.blit(self.image, (x + 10, y + 40))
        
        # Card content
        font = pygame.font.SysFont('Arial', 16)
        name_text = font.render(self.name, True, WHITE)
        cost_text = font.render(f"Cost: {self.cost}", True, WHITE)
        
        effect_lines = []
        if self.damage > 0:
            effect_lines.append(f"Damage: {self.damage}")
        if self.healing > 0:
            effect_lines.append(f"Heal: {self.healing}")
        if self.effect_text:
            effect_lines.append(self.effect_text)
            
        # Draw text
        screen.blit(name_text, (x + 10, y + 10))
        screen.blit(cost_text, (x + 10, y + 30))
        
        for i, line in enumerate(effect_lines):
            effect_text = font.render(line, True, WHITE)
            screen.blit(effect_text, (x + 10, y + 150 + i * 20))
            
        # Highlight if selected
        if self.selected:
            pygame.draw.rect(screen, WHITE, self.rect, 5)

class Character:
    def __init__(self, name, max_hp, deck):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.deck = deck
        self.hand = []
        self.discard_pile = []
        self.mana = 3
        self.max_mana = 3
        self.active = False  # Indicates if this character is currently being played
        self.block = 0  # Amount of damage that can be blocked
        
        # Character progression stats
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.strength = 0  # Bonus damage
        self.dexterity = 0  # Bonus block
        self.intelligence = 0  # Bonus healing
        
        # Try to load character image
        self.image = None
        image_path = os.path.join("assets", "images", "characters", f"{self.name.lower()}.png")
        try:
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (100, 150))
        except:
            self.image = None
            
        # If no image, create a colored surface
        if self.image is None:
            self.image = pygame.Surface((100, 150))
            if self.name == "Arion":
                self.image.fill(BLUE)
            elif self.name == "Lylac":
                self.image.fill(PURPLE)
            else:
                self.image.fill(GREEN)
                
        self.rect = self.image.get_rect()
        
    def draw_card(self, count=1):
        for _ in range(count):
            if not self.deck:
                # Reshuffle discard pile into deck
                if self.discard_pile:
                    self.deck = self.discard_pile.copy()
                    self.discard_pile = []
                    random.shuffle(self.deck)
                else:
                    return  # No cards left
                    
            if self.deck:
                self.hand.append(self.deck.pop())
                
    def discard_hand(self):
        self.discard_pile.extend(self.hand)
        self.hand = []
        
    def reset_mana(self):
        self.mana = self.max_mana
        
    def gain_exp(self, amount):
        """Add experience to the character and level up if needed."""
        self.exp += amount
        
        # Check for level up
        if self.exp >= self.exp_to_level:
            self.level_up()
            
    def level_up(self):
        """Level up the character and increase stats."""
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)  # Increase exp needed for next level
        
        # Increase stats
        self.max_hp += 10
        self.current_hp = self.max_hp  # Heal to full on level up
        self.max_mana += 1
        self.mana = self.max_mana
        
        # Increase combat stats based on character
        if self.name == "Arion":
            self.strength += 2
            self.dexterity += 1
            self.intelligence += 1
        elif self.name == "Lylac":
            self.strength += 1
            self.dexterity += 1
            self.intelligence += 2
        else:
            self.strength += 1
            self.dexterity += 1
            self.intelligence += 1
        
    def draw(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        
        # Highlight active character
        if self.active:
            highlight = pygame.Surface((110, 160))
            highlight.fill(GOLD)
            screen.blit(highlight, (x - 5, y - 5))
            
        screen.blit(self.image, self.rect)
        
        # Draw health bar
        health_percent = self.current_hp / self.max_hp
        health_width = 100 * health_percent
        
        pygame.draw.rect(screen, RED, (x, y - 20, 100, 15))
        pygame.draw.rect(screen, GREEN, (x, y - 20, health_width, 15))
        
        # Draw name and HP
        font = pygame.font.SysFont('Arial', 16)
        name_text = font.render(f"{self.name} Lv.{self.level}", True, WHITE)
        hp_text = font.render(f"{self.current_hp}/{self.max_hp}", True, WHITE)
        
        screen.blit(name_text, (x, y - 40))
        screen.blit(hp_text, (x + 30, y - 18))
        
        # Draw block if any
        if self.block > 0:
            block_text = font.render(f"Block: {self.block}", True, LIGHT_BLUE)
            screen.blit(block_text, (x, y - 60))
            
        # Draw stats if active
        if self.active:
            stats_text = font.render(f"STR:{self.strength} DEX:{self.dexterity} INT:{self.intelligence}", True, GOLD)
            screen.blit(stats_text, (x, y + 160))
            
            # Draw EXP bar
            exp_percent = self.exp / self.exp_to_level
            exp_width = 100 * exp_percent
            pygame.draw.rect(screen, GRAY, (x, y + 180, 100, 10))
            pygame.draw.rect(screen, GOLD, (x, y + 180, exp_width, 10))
            exp_text = font.render(f"EXP: {self.exp}/{self.exp_to_level}", True, WHITE)
            screen.blit(exp_text, (x, y + 195))

class Enemy:
    def __init__(self, name, hp, attack_damage, preloaded_image=None):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack_damage = attack_damage
        self.intent = "Attack"  # Shows what the enemy will do next
        self.intent_damage = attack_damage
        self.status_effects = []  # List of status effects like "Weak", "Vulnerable", etc.
        
        # Use preloaded image if available
        image_name = self.name.lower().replace(' ', '_')
        if preloaded_image is not None:
            print(f"Using preloaded image for {self.name}")
            self.image = preloaded_image
        else:
            # Try to load enemy image with multiple paths
            self.image = None
            
            # Try multiple possible paths
            possible_paths = [
                os.path.join("assets", "images", "enemies", f"{image_name}.png"),
                os.path.join("..", "assets", "images", "enemies", f"{image_name}.png"),
                os.path.join(os.getcwd(), "assets", "images", "enemies", f"{image_name}.png"),
                os.path.join(os.getcwd(), "..", "assets", "images", "enemies", f"{image_name}.png")
            ]
            
            for path in possible_paths:
                print(f"Trying path: {path}")
                try:
                    if os.path.exists(path):
                        print(f"Found image for {self.name} at {path}")
                        self.image = pygame.image.load(path)
                        self.image = pygame.transform.scale(self.image, (120, 180))
                        break
                except Exception as e:
                    print(f"Error loading image at {path}: {e}")
                    
            if self.image is None:
                print(f"Could not find image for {self.name} in any location")
            
        # If no image, create a colored surface
        if self.image is None:
            print(f"Using fallback color for {self.name}")
            self.image = pygame.Surface((120, 180))
            
            # Different colors for different enemies
            if "Shadow" in name:
                self.image.fill((100, 0, 100))  # Dark purple
            elif "Magician" in name:
                self.image.fill((0, 0, 150))  # Dark blue
            elif "Empress" in name:
                self.image.fill((150, 0, 0))  # Dark red
            elif "Tower" in name:
                self.image.fill((100, 100, 0))  # Dark yellow
            else:
                self.image.fill(RED)
            
        self.rect = self.image.get_rect()
        
    def decide_action(self):
        # More complex enemy AI based on name
        if "Shadow" in self.name:
            # Shadow Arcana just attacks
            self.intent = "Attack"
            self.intent_damage = self.attack_damage
        elif "Magician" in self.name:
            # Magician alternates between attack and buff
            if self.intent == "Attack":
                self.intent = "Buff"
                self.intent_damage = 0
            else:
                self.intent = "Attack"
                self.intent_damage = self.attack_damage + 2  # Buffed attack
        elif "Empress" in self.name:
            # Empress has a 3-turn pattern: attack, heal, debuff
            if self.intent == "Attack":
                self.intent = "Heal"
                self.intent_damage = 10  # Heal amount
            elif self.intent == "Heal":
                self.intent = "Debuff"
                self.intent_damage = 0
            else:
                self.intent = "Attack"
                self.intent_damage = self.attack_damage
        elif "Tower" in self.name:
            # Tower Guardian has a special pattern
            if random.random() < 0.3:
                self.intent = "Big Attack"
                self.intent_damage = self.attack_damage * 2
            else:
                self.intent = "Attack"
                self.intent_damage = self.attack_damage
        
    def perform_action(self, targets):
        """Perform the intended action on targets."""
        result = {"damage": 0, "target": None, "message": ""}
        
        if self.intent == "Attack" or self.intent == "Big Attack":
            # Choose a random target
            if targets:
                target = random.choice([t for t in targets if t.current_hp > 0])
                result["damage"] = self.intent_damage
                result["target"] = target
                result["message"] = f"{self.name} attacks {target.name} for {self.intent_damage} damage!"
                
        elif self.intent == "Heal":
            # Heal self
            heal_amount = self.intent_damage
            self.current_hp = min(self.current_hp + heal_amount, self.max_hp)
            result["message"] = f"{self.name} heals for {heal_amount} HP!"
            
        elif self.intent == "Buff":
            # Buff attack
            self.attack_damage += 2
            result["message"] = f"{self.name} increases its attack power!"
            
        elif self.intent == "Debuff":
            # Debuff a random target
            if targets:
                target = random.choice([t for t in targets if t.current_hp > 0])
                result["target"] = target
                result["message"] = f"{self.name} weakens {target.name}!"
                # In a full game, would apply a status effect here
                
        return result
        
    def attack(self):
        return self.intent_damage
        
    def draw(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)
        
        # Draw health bar
        health_percent = self.current_hp / self.max_hp
        health_width = 120 * health_percent
        
        pygame.draw.rect(screen, RED, (x, y - 20, 120, 15))
        pygame.draw.rect(screen, GREEN, (x, y - 20, health_width, 15))
        
        # Draw name and HP
        font = pygame.font.SysFont('Arial', 16)
        name_text = font.render(self.name, True, WHITE)
        hp_text = font.render(f"{self.current_hp}/{self.max_hp}", True, WHITE)
        
        screen.blit(name_text, (x, y - 40))
        screen.blit(hp_text, (x + 40, y - 18))
        
        # Draw intent
        intent_color = WHITE
        if self.intent == "Attack":
            intent_color = RED
        elif self.intent == "Big Attack":
            intent_color = (255, 50, 50)  # Brighter red
        elif self.intent == "Heal":
            intent_color = GREEN
        elif self.intent == "Buff":
            intent_color = GOLD
        elif self.intent == "Debuff":
            intent_color = PURPLE
            
        intent_text = font.render(f"Intent: {self.intent} {self.intent_damage if self.intent_damage > 0 else ''}", True, intent_color)
        pygame.draw.rect(screen, BLACK, (x, y - 70, intent_text.get_width() + 10, 25))
        screen.blit(intent_text, (x + 5, y - 65))
        
        # Draw status effects
        if self.status_effects:
            status_text = font.render(" ".join(self.status_effects), True, WHITE)
            screen.blit(status_text, (x, y - 90))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Elysian Arcana")
        self.clock = pygame.time.Clock()
        self.state = MAIN_MENU
        self.turn_state = PLAYER_TURN
        self.action_state = WAITING_FOR_CARD
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 32)
        
        # Game progression
        self.current_stage = 1
        self.max_stages = 4
        self.difficulty_multiplier = 1.0  # Increases enemy stats
        
        # Enhanced enemy stats with scaling difficulty
        self.stage_enemies = {
            1: {"name": "Shadow Arcana", "hp": 80, "attack": 10},
            2: {"name": "Reversed Magician", "hp": 120, "attack": 15},
            3: {"name": "Corrupted Empress", "hp": 180, "attack": 20},
            4: {"name": "Tower Guardian", "hp": 250, "attack": 25}
        }
        
        # Preload enemy images to avoid loading issues during gameplay
        self.enemy_images = {}
        for enemy_name in ["shadow_arcana", "reversed_magician", "corrupted_empress", "tower_guardian"]:
            self.preload_enemy_image(enemy_name)
            
        # Preload card images
        self.preload_card_images()
            
        # Create cards
        self.create_cards()
        
        # Create initial cards
        self.create_cards()
        
        # Create characters
        arion_deck = [
            self.cards["slash"], self.cards["slash"], 
            self.cards["defend"], self.cards["defend"],
            self.cards["arcane_bolt"]
        ]
        
        lylac_deck = [
            self.cards["fireball"], self.cards["fireball"],
            self.cards["heal"], self.cards["heal"],
            self.cards["earth_shield"]
        ]
        
        self.player_characters = [
            Character("Arion", 50, arion_deck.copy()),
            Character("Lylac", 40, lylac_deck.copy())
        ]
        
        # Set the active character
        self.active_character_index = 0
        self.player_characters[self.active_character_index].active = True
        
        # Create enemy based on current stage
        enemy_data = self.stage_enemies[self.current_stage]
        self.enemy = Enemy(enemy_data["name"], enemy_data["hp"], enemy_data["attack"])
        
        # Game variables
        self.current_turn = 0
        self.selected_card = None
        self.selected_target = None
        self.battle_message = ""
        self.battle_message_timer = 0
        self.transition_timer = 0
        self.instruction_text = "Select a card to play"
        
        # Card rewards
        self.available_rewards = []
        self.reward_selection = False
        
        # Initialize battle
        self.start_battle()
        
    def preload_enemy_image(self, enemy_name):
        """Preload enemy images to avoid loading issues during gameplay."""
        # Try multiple possible paths
        possible_paths = [
            os.path.join("assets", "images", "enemies", f"{enemy_name}.png"),
            os.path.join("..", "assets", "images", "enemies", f"{enemy_name}.png"),
            os.path.join(os.getcwd(), "assets", "images", "enemies", f"{enemy_name}.png"),
            os.path.join(os.getcwd(), "..", "assets", "images", "enemies", f"{enemy_name}.png")
        ]
        
        for path in possible_paths:
            print(f"Preloading enemy image from: {path}")
            try:
                if os.path.exists(path):
                    print(f"Found image for {enemy_name} at {path}")
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (120, 180))
                    self.enemy_images[enemy_name] = image
                    return
            except Exception as e:
                print(f"Error loading image at {path}: {e}")
                
        print(f"Could not preload image for {enemy_name}, will use fallback color")
        # Create a fallback colored surface
        image = pygame.Surface((120, 180))
        if "shadow" in enemy_name:
            image.fill((100, 0, 100))  # Dark purple
        elif "magician" in enemy_name:
            image.fill((0, 0, 150))  # Dark blue
        elif "empress" in enemy_name:
            image.fill((150, 0, 0))  # Dark red
        elif "tower" in enemy_name:
            image.fill((100, 100, 0))  # Dark yellow
        else:
            image.fill((178, 34, 34))  # Default red
            
        self.enemy_images[enemy_name] = image
        
    def preload_card_images(self):
        """Preload all card images."""
        self.card_images = {}
        card_names = [
            "slash", "defend", "arcane_bolt", "fireball", "heal", "earth_shield",
            "dual_strike", "flame_wave", "rejuvenation", "stone_wall",
            "lightning_bolt", "ice_spike", "life_drain", "wind_slash"
        ]
        
        for card_name in card_names:
            # Try multiple possible paths
            possible_paths = [
                os.path.join("assets", "images", "cards", f"{card_name}.png"),
                os.path.join("..", "assets", "images", "cards", f"{card_name}.png"),
                os.path.join(os.getcwd(), "assets", "images", "cards", f"{card_name}.png"),
                os.path.join(os.getcwd(), "..", "assets", "images", "cards", f"{card_name}.png")
            ]
            
            for path in possible_paths:
                print(f"Preloading card image from: {path}")
                try:
                    if os.path.exists(path):
                        print(f"Found image for {card_name} at {path}")
                        image = pygame.image.load(path)
                        image = pygame.transform.scale(image, (130, 100))
                        self.card_images[card_name] = image
                        break
                except Exception as e:
                    print(f"Error loading card image at {path}: {e}")
            
            # If image wasn't found, create a fallback
            if card_name not in self.card_images:
                print(f"Creating fallback image for {card_name}")
                image = pygame.Surface((130, 100))
                
                # Color based on card type
                if card_name in ["slash", "defend", "dual_strike", "wind_slash", "ice_spike"]:
                    image.fill((65, 105, 225))  # Blue for physical
                elif card_name in ["fireball", "flame_wave"]:
                    image.fill((178, 34, 34))  # Red for fire
                elif card_name in ["arcane_bolt", "heal", "rejuvenation", "lightning_bolt", "life_drain"]:
                    image.fill((128, 0, 128))  # Purple for arcana
                elif card_name in ["earth_shield", "stone_wall"]:
                    image.fill((34, 139, 34))  # Green for earth
                else:
                    image.fill((100, 100, 100))  # Gray for unknown
                    
                self.card_images[card_name] = image
        
    def create_cards(self):
        # Store reference to game for preloaded images
        pygame.app = type('', (), {})()
        pygame.app.game = self
        
        # Create cards
        self.cards = {
            # Basic cards
            "slash": Card("Slash", 1, 6, 0, "", "physical"),
            "defend": Card("Defend", 1, 0, 0, "Block 5 damage", "physical"),
            "arcane_bolt": Card("Arcane Bolt", 2, 8, 0, "", "arcana"),
            "fireball": Card("Fireball", 2, 10, 0, "", "fire"),
            "heal": Card("Heal", 1, 0, 6, "", "arcana"),
            "earth_shield": Card("Earth Shield", 2, 0, 0, "Block 8 damage", "earth"),
            
            # Advanced cards for rewards
            "dual_strike": Card("Dual Strike", 2, 4, 0, "Attack twice", "physical"),
            "flame_wave": Card("Flame Wave", 3, 15, 0, "", "fire"),
            "rejuvenation": Card("Rejuvenation", 2, 0, 10, "Draw a card", "arcana"),
            "stone_wall": Card("Stone Wall", 3, 0, 0, "Block 12 damage", "earth"),
            "lightning_bolt": Card("Lightning Bolt", 1, 5, 0, "Draw a card", "arcana"),
            "ice_spike": Card("Ice Spike", 1, 7, 0, "Slow enemy", "water"),
            "life_drain": Card("Life Drain", 2, 8, 4, "", "arcana"),
            "wind_slash": Card("Wind Slash", 2, 9, 0, "Ignore defense", "wind")
        }
        
    def start_battle(self):
        self.state = BATTLE
        self.turn_state = PLAYER_TURN
        self.action_state = WAITING_FOR_CARD
        self.current_turn = 1
        
        # Reset characters
        for character in self.player_characters:
            character.hand = []
            character.discard_pile = []
            character.deck = character.deck.copy()
            random.shuffle(character.deck)
            character.draw_card(5)
            character.reset_mana()
            
        # Set active character
        for i, character in enumerate(self.player_characters):
            character.active = (i == self.active_character_index)
            
        # Reset enemy with difficulty scaling
        enemy_data = self.stage_enemies[self.current_stage]
        scaled_hp = int(enemy_data["hp"] * self.difficulty_multiplier)
        scaled_attack = int(enemy_data["attack"] * self.difficulty_multiplier)
        
        # Use preloaded image if available
        enemy_name = enemy_data["name"].lower().replace(' ', '_')
        preloaded_image = self.enemy_images.get(enemy_name)
        
        self.enemy = Enemy(enemy_data["name"], scaled_hp, scaled_attack, preloaded_image)
        self.enemy.decide_action()
        
        # Increase difficulty for next battles
        self.difficulty_multiplier += 0.1
        
        # Set instruction
        self.instruction_text = "Select a card to play (or press 1-5)"
        
    def generate_rewards(self):
        """Generate card rewards after defeating an enemy."""
        self.available_rewards = []
        
        # Get all advanced cards
        advanced_cards = [card for name, card in self.cards.items() 
                         if name not in ["slash", "defend", "arcane_bolt", "fireball", "heal", "earth_shield"]]
        
        # Choose 3 random cards as rewards
        if advanced_cards:
            self.available_rewards = random.sample(advanced_cards, min(3, len(advanced_cards)))
            
    def next_stage(self):
        """Advance to the next stage."""
        # Award experience for completing the stage
        exp_reward = 50 * self.current_stage
        for character in self.player_characters:
            if character.current_hp > 0:  # Only award exp to living characters
                character.gain_exp(exp_reward)
                print(f"{character.name} gained {exp_reward} exp!")
        
        # Heal characters a bit between stages
        for character in self.player_characters:
            heal_amount = character.max_hp // 4  # Heal 25% of max HP
            character.current_hp = min(character.current_hp + heal_amount, character.max_hp)
        
        # Increment stage
        self.current_stage += 1
        print(f"Advancing to stage {self.current_stage}")
        
        # Create new enemy based on current stage
        enemy_data = self.stage_enemies[self.current_stage]
        self.enemy = Enemy(enemy_data["name"], enemy_data["hp"], enemy_data["attack"])
        
        # Reset for new battle
        self.state = BATTLE
        self.turn_state = PLAYER_TURN
        self.action_state = WAITING_FOR_CARD
        self.current_turn = 1
        
        # Reset characters for new battle but preserve their decks
        for character in self.player_characters:
            # Save the current deck before resetting
            current_deck = character.deck.copy() + character.hand.copy() + character.discard_pile.copy()
            print(f"{character.name}'s deck size before reset: {len(current_deck)}")
            
            # Reset hand and discard pile
            character.hand = []
            character.discard_pile = []
            
            # Restore the full deck including any new cards
            character.deck = current_deck
            print(f"{character.name}'s deck size after reset: {len(character.deck)}")
            random.shuffle(character.deck)
            character.draw_card(5)
            character.reset_mana()
            
        # Set active character
        for i, character in enumerate(self.player_characters):
            character.active = (i == self.active_character_index)
            
        # Enemy decides action
        self.enemy.decide_action()
        
        # Set instruction
        self.instruction_text = "Select a card to play"
        
    def switch_character(self):
        # Switch to the next character
        self.player_characters[self.active_character_index].active = False
        self.active_character_index = (self.active_character_index + 1) % len(self.player_characters)
        self.player_characters[self.active_character_index].active = True
        
        # Clear selected card
        if self.selected_card:
            self.selected_card.selected = False
            self.selected_card = None
            
        # Reset action state
        self.action_state = WAITING_FOR_CARD
        self.instruction_text = "Select a card to play"
            
    def start_enemy_turn(self):
        self.turn_state = TURN_TRANSITION
        self.transition_timer = 60  # 1 second at 60 FPS
        self.battle_message = "Enemy Turn"
        
    def process_enemy_turn(self):
        # Get enemy action result
        action_result = self.enemy.perform_action(self.player_characters)
        
        # Apply damage if any, considering block
        if action_result["damage"] > 0 and action_result["target"]:
            target = action_result["target"]
            damage = action_result["damage"]
            
            # Apply block if available
            if target.block > 0:
                blocked_damage = min(target.block, damage)
                damage -= blocked_damage
                target.block -= blocked_damage
                self.battle_message = f"{self.enemy.name} attacks {target.name} for {action_result['damage']} damage, {blocked_damage} blocked!"
            
            # Apply remaining damage
            target.current_hp -= damage
            if target.block == 0 and damage > 0:
                self.battle_message = f"{self.enemy.name} attacks {target.name} for {damage} damage!"
            
        # If no damage was dealt, use the original message
        elif not action_result["damage"] > 0:
            self.battle_message = action_result["message"]
            
        self.battle_message_timer = 120
            
        # Check for game over
        all_dead = True
        for character in self.player_characters:
            if character.current_hp > 0:
                all_dead = False
                break
                
        if all_dead:
            self.state = GAME_OVER
            return
            
        # Start next player turn
        self.turn_state = TURN_TRANSITION
        self.transition_timer = 60
        self.battle_message = "Player Turn"
        self.current_turn += 1
        
        # Reset all characters for the new turn
        for character in self.player_characters:
            if character.current_hp > 0:  # Only reset living characters
                character.discard_hand()
                character.draw_card(5)
                character.reset_mana()
                
        # Enemy decides next action
        self.enemy.decide_action()
        
        # Reset action state
        self.action_state = WAITING_FOR_CARD
        self.instruction_text = "Select a card to play"
        
    def end_player_turn(self):
        # Reset block for all characters (block only lasts one turn)
        for character in self.player_characters:
            character.block = 0
            
        # Start enemy turn
        self.start_enemy_turn()
            
    def play_card(self, card, character, target):
        if card.cost > character.mana:
            self.battle_message = "Not enough mana!"
            self.battle_message_timer = 60
            self.action_state = WAITING_FOR_CARD
            self.instruction_text = "Select a card to play"
            return False
            
        # Apply card effects
        if card.damage > 0:
            # Apply strength bonus to damage
            total_damage = card.damage + character.strength
            target.current_hp -= total_damage
            self.battle_message = f"{character.name} uses {card.name} for {total_damage} damage!"
            
            # Special card effects
            if card.name == "Dual Strike":
                target.current_hp -= total_damage  # Second hit
                self.battle_message = f"{character.name} uses {card.name} for {total_damage * 2} damage!"
            elif card.name == "Wind Slash":
                self.battle_message = f"{character.name} uses {card.name} for {total_damage} damage, ignoring defense!"
            
        if card.healing > 0:
            # Apply intelligence bonus to healing
            total_healing = card.healing + character.intelligence
            # Healing targets the selected character
            target.current_hp = min(target.current_hp + total_healing, target.max_hp)
            self.battle_message = f"{character.name} heals {target.name} for {total_healing} HP!"
            
        # Special effects
        if "Block" in card.effect_text:
            # Extract the block amount from the effect text
            block_text = card.effect_text
            block_amount = int(''.join(filter(str.isdigit, block_text)))
            
            # Apply dexterity bonus to block
            total_block = block_amount + character.dexterity
            
            # Apply block to the target character
            target.block += total_block
            self.battle_message = f"{character.name} gives {target.name} {total_block} block!"
            
        # Card-specific effects
        if "Draw a card" in card.effect_text:
            character.draw_card(1)
            self.battle_message += " Drew a card!"
        if "Slow enemy" in card.effect_text and hasattr(target, 'status_effects'):
            target.status_effects.append("Slowed")
            self.battle_message += " Enemy slowed!"
            
        # Remove card from hand and add to discard pile
        character.hand.remove(card)
        character.discard_pile.append(card)
        
        # Reduce mana
        character.mana -= card.cost
        
        self.battle_message_timer = 60
        
        # Reset action state
        self.action_state = WAITING_FOR_CARD
        self.instruction_text = "Select a card to play"
        
        # Check if enemy is defeated
        if target == self.enemy and target.current_hp <= 0:
            if self.current_stage < self.max_stages:
                # Go to reward screen
                self.state = REWARD_SCREEN
                self.generate_rewards()
            else:
                # Final victory
                self.state = VICTORY
            
        return True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if self.state == MAIN_MENU:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.start_battle()
                    
            elif self.state == BATTLE:
                if self.turn_state == PLAYER_TURN:
                    if event.type == MOUSEBUTTONDOWN:
                        active_character = self.player_characters[self.active_character_index]
                        
                        # WAITING_FOR_CARD state - select a card
                        if self.action_state == WAITING_FOR_CARD:
                            for card in active_character.hand:
                                if card.rect.collidepoint(event.pos):
                                    # Select card
                                    if self.selected_card:
                                        self.selected_card.selected = False
                                    self.selected_card = card
                                    card.selected = True
                                    
                                    # Update action state
                                    self.action_state = WAITING_FOR_TARGET
                                    if card.damage > 0:
                                        self.instruction_text = "Select an enemy to attack"
                                    elif card.healing > 0:
                                        self.instruction_text = "Select a character to heal"
                                    else:
                                        self.instruction_text = "Select a target for this card"
                        
                        # WAITING_FOR_TARGET state - select a target
                        elif self.action_state == WAITING_FOR_TARGET:
                            # Check if enemy was clicked and a damage card is selected
                            if self.selected_card and self.selected_card.damage > 0 and self.enemy.rect.collidepoint(event.pos):
                                self.play_card(self.selected_card, active_character, self.enemy)
                                self.selected_card = None
                                
                            # Check if player character was clicked and a healing card is selected
                            for character in self.player_characters:
                                if self.selected_card and self.selected_card.healing > 0 and character.rect.collidepoint(event.pos):
                                    self.play_card(self.selected_card, active_character, character)
                                    self.selected_card = None
                                    
                            # If clicked elsewhere, cancel the selection
                            if self.selected_card:
                                self.selected_card.selected = False
                                self.selected_card = None
                                self.action_state = WAITING_FOR_CARD
                                self.instruction_text = "Select a card to play"
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            self.end_player_turn()
                        elif event.key == K_TAB:
                            self.switch_character()
                        # Number keys for card selection (1-5)
                        elif K_1 <= event.key <= K_5:
                            active_character = self.player_characters[self.active_character_index]
                            card_index = event.key - K_1  # Convert key to 0-based index
                            
                            if self.action_state == WAITING_FOR_CARD and card_index < len(active_character.hand):
                                # Select the card
                                if self.selected_card:
                                    self.selected_card.selected = False
                                self.selected_card = active_character.hand[card_index]
                                self.selected_card.selected = True
                                
                                # Update action state
                                self.action_state = WAITING_FOR_TARGET
                                if self.selected_card.damage > 0:
                                    self.instruction_text = "Select an enemy to attack"
                                elif self.selected_card.healing > 0:
                                    self.instruction_text = "Select a character to heal"
                                else:
                                    self.instruction_text = "Select a target for this card"
                            
            elif self.state == REWARD_SCREEN:
                if event.type == MOUSEBUTTONDOWN:
                    # Check if a reward card was clicked
                    for i, card in enumerate(self.available_rewards):
                        card_x = SCREEN_WIDTH // 2 - 250 + i * 250
                        card_y = SCREEN_HEIGHT // 2 - 100
                        card_rect = pygame.Rect(card_x, card_y, 150, 200)
                        
                        if card_rect.collidepoint(event.pos):
                            # Add a copy of the selected card to the active character's deck
                            active_character = self.player_characters[self.active_character_index]
                            
                            # Create a new instance of the card to avoid reference issues
                            new_card = Card(card.name, card.cost, card.damage, card.healing, 
                                           card.effect_text, card.element)
                            active_character.deck.append(new_card)
                            print(f"Added {new_card.name} to {active_character.name}'s deck")
                            print(f"Deck now has {len(active_character.deck)} cards")
                            
                            # Proceed to next stage
                            self.next_stage()
                            break
                            
                    # Skip button
                    skip_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 40)
                    if skip_rect.collidepoint(event.pos):
                        self.next_stage()
                            
            elif self.state == GAME_OVER or self.state == VICTORY:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.__init__()  # Reset the game
                    
    def draw(self):
        self.screen.fill(GRAY)
        
        if self.state == MAIN_MENU:
            title_text = self.large_font.render("ELYSIAN ARCANA", True, GOLD)
            start_text = self.font.render("Press ENTER to start", True, WHITE)
            
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 300))
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 350))
            
            # Add controls info
            controls_text = [
                "Controls:",
                "- Mouse: Select cards and targets",
                "- 1-5: Select cards by number",
                "- TAB: Switch characters",
                "- SPACE: End turn"
            ]
            
            for i, text in enumerate(controls_text):
                info_text = self.small_font.render(text, True, WHITE)
                self.screen.blit(info_text, (SCREEN_WIDTH // 2 - 100, 400 + i * 25))
            
        elif self.state == BATTLE:
            # Draw turn indicator
            turn_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
            pygame.draw.rect(self.screen, (30, 30, 50), turn_bg)
            
            # Draw stage indicator
            stage_text = self.font.render(f"Stage {self.current_stage}/{self.max_stages}", True, GOLD)
            self.screen.blit(stage_text, (SCREEN_WIDTH - stage_text.get_width() - 20, 20))
            
            # Draw turn number
            turn_text = self.font.render(f"Turn {self.current_turn}", True, WHITE)
            self.screen.blit(turn_text, (20, 20))
            
            # Draw whose turn it is
            if self.turn_state == PLAYER_TURN:
                state_text = self.font.render("Player Turn - Press SPACE to end turn, TAB to switch character", True, LIGHT_BLUE)
            elif self.turn_state == ENEMY_TURN:
                state_text = self.font.render("Enemy Turn", True, RED)
            else:
                state_text = self.font.render(self.battle_message, True, GOLD)
                
            self.screen.blit(state_text, (SCREEN_WIDTH // 2 - state_text.get_width() // 2, 20))
            
            # Draw instruction text
            instruction_bg = pygame.Rect(0, 80, SCREEN_WIDTH, 40)
            pygame.draw.rect(self.screen, (50, 50, 70), instruction_bg)
            instruction_text = self.font.render(self.instruction_text, True, WHITE)
            self.screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 90))
            
            # Draw characters
            for i, character in enumerate(self.player_characters):
                character.draw(self.screen, 150 + i * 200, 300)
                
                # Draw mana for active character
                if character.active:
                    mana_text = self.font.render(f"Mana: {character.mana}/{character.max_mana}", True, LIGHT_BLUE)
                    self.screen.blit(mana_text, (150 + i * 200, 460))
                    
                    # Draw deck/discard info
                    deck_text = self.small_font.render(f"Deck: {len(character.deck)} | Discard: {len(character.discard_pile)}", True, WHITE)
                    self.screen.blit(deck_text, (150 + i * 200, 490))
                
            # Draw enemy
            self.enemy.draw(self.screen, 700, 300)
            
            # Draw cards in hand for active character
            active_character = self.player_characters[self.active_character_index]
            for i, card in enumerate(active_character.hand):
                card.draw(self.screen, 50 + i * 160, 550)
                
                # Draw card number for keyboard selection
                if i < 5:  # Only show numbers for first 5 cards
                    num_bg = pygame.Rect(50 + i * 160, 550, 25, 25)
                    pygame.draw.rect(self.screen, GOLD, num_bg)
                    num_text = self.font.render(str(i + 1), True, BLACK)
                    self.screen.blit(num_text, (50 + i * 160 + 8, 550 + 2))
                card.draw(self.screen, 50 + i * 160, 550)
                
            # Draw battle message
            if self.battle_message_timer > 0:
                message_bg = pygame.Rect(SCREEN_WIDTH // 2 - 200, 130, 400, 40)
                pygame.draw.rect(self.screen, (50, 50, 70), message_bg)
                pygame.draw.rect(self.screen, GOLD, message_bg, 2)
                
                message_text = self.font.render(self.battle_message, True, WHITE)
                self.screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 140))
                
        elif self.state == REWARD_SCREEN:
            # Draw reward screen
            title_text = self.large_font.render("Choose a Card Reward", True, GOLD)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            
            # Draw available rewards
            for i, card in enumerate(self.available_rewards):
                card_x = SCREEN_WIDTH // 2 - 250 + i * 250
                card_y = SCREEN_HEIGHT // 2 - 100
                card.draw(self.screen, card_x, card_y)
                
            # Draw skip button
            skip_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 40)
            pygame.draw.rect(self.screen, GRAY, skip_rect)
            skip_text = self.font.render("Skip", True, WHITE)
            self.screen.blit(skip_text, (SCREEN_WIDTH // 2 - skip_text.get_width() // 2, SCREEN_HEIGHT - 90))
            
            # Draw stage info
            stage_text = self.font.render(f"Completed Stage {self.current_stage}/{self.max_stages}", True, WHITE)
            self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 50))
                
        elif self.state == GAME_OVER:
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press ENTER to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 300))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
            
            # Show stage reached
            stage_text = self.font.render(f"Reached Stage {self.current_stage}/{self.max_stages}", True, WHITE)
            self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 400))
            
        elif self.state == VICTORY:
            victory_text = self.large_font.render("VICTORY!", True, GREEN)
            restart_text = self.font.render("Press ENTER to restart", True, WHITE)
            
            self.screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 300))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
            
            # Show completion message
            complete_text = self.font.render("You have completed all stages!", True, GOLD)
            self.screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 400))
            
        pygame.display.flip()
        
    def update(self):
        if self.battle_message_timer > 0:
            self.battle_message_timer -= 1
            
        if self.turn_state == TURN_TRANSITION:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                if self.battle_message == "Enemy Turn":
                    self.turn_state = ENEMY_TURN
                    self.process_enemy_turn()
                else:
                    self.turn_state = PLAYER_TURN
            
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
