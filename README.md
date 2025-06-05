# Elysian Arcana - Pygame Implementation

A roguelike card game based on the Elysian Arcana game design.

## Game Overview

This implementation captures the core mechanics of the Elysian Arcana game design:

- **Card-based Combat**: Use cards with different effects (damage, healing, defense)
- **Character System**: Play as Arion (The Fool) with Lylac as an ally
- **Elemental System**: Cards have different elements (fire, earth, arcana, physical)
- **Turn-based Strategy**: Clear turn structure with player and enemy phases
- **Multiple Stages**: Progress through 4 stages with different enemies
- **Card Rewards**: Earn new cards after defeating enemies
- **Enemy Variety**: Each enemy has unique behaviors and abilities

## How to Play

1. Run `python main.py` to start the game
2. In battle:
   - You control one character at a time (highlighted in gold)
   - **Step 1**: Select a card to play (follow the instruction at the top)
   - **Step 2**: Select a target (enemy for damage cards, character for healing)
   - Press TAB to switch between your characters
   - Press SPACE to end your turn
3. After defeating an enemy:
   - Choose a new card to add to your deck or skip
   - Progress to the next stage
4. Defeat all enemies across 4 stages to win!

## Controls

- **Mouse**: Select cards, targets, and rewards
- **TAB**: Switch between characters
- **SPACE**: End turn
- **ENTER**: Start game/Restart after game over

## Game Elements

### Characters
- **Arion**: The protagonist (The Fool), balanced character
- **Lylac**: Ally with fire and healing abilities

### Basic Cards
- **Slash**: Basic attack (1 mana, 6 damage)
- **Defend**: Block damage (1 mana)
- **Arcane Bolt**: Stronger attack (2 mana, 8 damage)
- **Fireball**: Fire attack (2 mana, 10 damage)
- **Heal**: Restore health (1 mana, 6 healing)
- **Earth Shield**: Strong defense (2 mana)

### Advanced Cards (Rewards)
- **Dual Strike**: Attack twice (2 mana, 4+4 damage)
- **Flame Wave**: Powerful fire attack (3 mana, 15 damage)
- **Rejuvenation**: Strong healing + draw (2 mana, 10 healing)
- **Stone Wall**: Strong defense (3 mana, block 12)
- **Lightning Bolt**: Quick attack + draw (1 mana, 5 damage)
- **Ice Spike**: Attack + slow enemy (1 mana, 7 damage)
- **Life Drain**: Damage + healing (2 mana, 8 damage, 4 healing)
- **Wind Slash**: Piercing attack (2 mana, 9 damage, ignores defense)

### Enemies
- **Stage 1**: Shadow Arcana - Basic attacks
- **Stage 2**: Reversed Magician - Alternates between attacks and buffs
- **Stage 3**: Corrupted Empress - Cycles between attack, heal, and debuff
- **Stage 4**: Tower Guardian - Can perform devastating big attacks

## Turn Structure

1. **Player Turn**:
   - Switch between characters with TAB
   - Play cards from your hand using mana
   - End turn when ready
   
2. **Enemy Turn**:
   - Enemy performs its action based on its intent
   - Game automatically transitions back to player turn

## Requirements

- Python 3.x
- Pygame library

## Installation

```
pip install pygame
python main.py
```
