import pygame
import random

# Constants for screen and grid dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Background color of the game board

# Constants for movement directions
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Display setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Initialize a game object with a position and color.

        :param position: Tuple of coordinates (x, y), default is (0, 0)
        :param body_color: Tuple of RGB color, default is (255, 255, 255) (white)
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Draw the object on the game surface."""
        pass

class Apple(GameObject):
    """Class representing the apple in the game."""

    def __init__(self):
        """Initialize the apple with a random position and color (red)."""
        super().__init__(self.randomize_position(), (255, 0, 0))

    def randomize_position(self):
        """Set the apple's position within the game grid."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self, surface):
        """Draw the apple as a red square on the surface."""
        pygame.draw.rect(surface, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE))

class Snake(GameObject):
    """Class representing the snake, handling its movement and interactions."""

    def __init__(self):
        """Initialize the snake with a length of 1 and a default direction."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT  # Default movement is to the right
        self.next_direction = None

    def update_direction(self, new_direction):
        """Update the snake's direction based on player input."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        """Move the snake according to its direction."""
        if self.next_direction:
            self.direction = self.next_direction
        new_head = (
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        )
        self.positions = [new_head] + self.positions[:self.length - 1]

    def grow(self):
        """Increase the snake's length by one segment."""
        self.length += 1

    def reset(self):
        """Reset the snake to its initial length and position."""
        self.__init__()

    def get_head_position(self):
        """Get the current position of the snake's head."""
        return self.positions[0]

    def draw(self, surface):
        """Draw the snake's body segments on the surface."""
        for segment in self.positions:
            pygame.draw.rect(surface, self.body_color, (*segment, GRID_SIZE, GRID_SIZE))

def handle_keys(snake):
    """Handle key presses to control the snake's movement."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction(UP)
    elif keys[pygame.K_DOWN]:
        snake.update_direction(DOWN)
    elif keys[pygame.K_LEFT]:
        snake.update_direction(LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.update_direction(RIGHT)

def main():
    """Main game loop managing initialization, events, updates, and rendering."""
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()

        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
