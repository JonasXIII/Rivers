import pygame
import random
import noise

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 1200
TILE_SIZE = 5
NUM_TILES_X = WIDTH // TILE_SIZE
NUM_TILES_Y = HEIGHT // TILE_SIZE
FPS = 30
scale = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

#Tile Types
GRASS = 2
DIRT = 1
WATER = 0

# Set the seed for noise generation
seed_value = 42  # Change this to any integer value to use a different seed
random.seed(seed_value)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terrain Generation")

# Function to generate random terrain
def generate_terrain():
    terrain = []

    for x in range(NUM_TILES_X):
        column = []
        for y in range(NUM_TILES_Y):
            nx = x / NUM_TILES_X - 0.5
            ny = y / NUM_TILES_Y - 0.5
            value = noise.snoise2(nx * scale, ny * scale, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed_value)
            column.append(value)
        terrain.append(column)
    
    # Normalize values to the range [0, 1]
    min_value = min(min(row) for row in terrain)
    max_value = max(max(row) for row in terrain)
    terrain = [[(value - min_value) / (max_value - min_value) for value in row] for row in terrain]
    for x in range(NUM_TILES_X):
        for y in range(NUM_TILES_Y):
            if terrain[x][y] < 0.5:
                terrain[x][y] = DIRT
            else:
                terrain[x][y] = GRASS



    return terrain

# Main game loop
def main():
    terrain = generate_terrain()
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Draw the terrain
        for x in range(NUM_TILES_X):
            for y in range(NUM_TILES_Y):
                if terrain[x][y] == GRASS:
                    color = GREEN
                elif terrain[x][y] == WATER:
                    color = BLUE
                elif terrain[x][y] == DIRT:
                    color = BROWN
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Update the display
        pygame.display.flip()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
