import pygame
import random

# Initialize Pygame and set up window dimensions
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Set up display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class GameObject:
    """Base class for all game objects."""
    
    def __init__(self, position, body_color):
        """
        Initialize the game object with a position and color.
        
        :param position: Tuple of (x, y) coordinates
        :param body_color: RGB color tuple
        """
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
        """
        Draw the object on the game surface. Should be overridden.
        
        :param surface: Pygame surface where the object is drawn
        """
        pass

class Apple(GameObject):
    """Represents an apple in the game."""
    
    def __init__(self):
        """Initialize the apple with a random position and color (red)."""
        super().__init__(self.randomize_position(), (255, 0, 0))
    
    def randomize_position(self):
        """
        Randomize the position of the apple within the game field.
        
        :return: Tuple of (x, y) coordinates for the new position
        """
        x = random.randint(0, WINDOW_WIDTH // 20 - 1) * 20
        y = random.randint(0, WINDOW_HEIGHT // 20 - 1) * 20
        return (x, y)
    
    def draw(self, surface):
        """Draw the apple as a red square on the surface."""
        pygame.draw.rect(surface, self.body_color, (*self.position, 20, 20))

class Snake(GameObject):
    """Represents the snake and manages its movement and interactions."""
    
    def __init__(self):
        """Initialize the snake with a length of 1 and a default direction."""
        super().__init__((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = (20, 0)  # Moving right by default
        self.next_direction = None
    
    def update_direction(self, new_direction):
        """
        Update the direction of the snake based on user input.
        
        :param new_direction: Tuple representing new direction (dx, dy)
        """
        # Prevent reversing direction directly
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def move(self):
        """Move the snake based on its direction, add a new head and remove the tail if length unchanged."""
        if self.next_direction:
            self.direction = self.next_direction
        new_head = (self.positions[0][0] + self.direction[0],
                    self.positions[0][1] + self.direction[1])
        self.positions = [new_head] + self.positions[:self.length - 1]
    
    def grow(self):
        """Increase the length of the snake by one segment."""
        self.length += 1
    
    def reset(self):
        """Reset the snake to its initial length and position."""
        self.__init__()
    
    def get_head_position(self):
        """
        Get the current head position of the snake.
        
        :return: Tuple representing head coordinates
        """
        return self.positions[0]
    
    def draw(self, surface):
        """Draw the snake's body segments on the surface."""
        for segment in self.positions:
            pygame.draw.rect(surface, self.body_color, (*segment, 20, 20))

def handle_keys(snake):
    """
    Handle key presses to control the snake's movement.
    
    :param snake: Instance of the Snake class
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction((0, -20))
    elif keys[pygame.K_DOWN]:
        snake.update_direction((0, 20))
    elif keys[pygame.K_LEFT]:
        snake.update_direction((-20, 0))
    elif keys[pygame.K_RIGHT]:
        snake.update_direction((20, 0))

def main():
    """Main game loop handling initialization, events, updates, and rendering."""
    snake = Snake()
    apple = Apple()
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Control snake with keys
        handle_keys(snake)
        
        # Update snake direction and move
        snake.move()
        
        # Check if snake eats the apple
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()
        
        # Check for self-collision
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
        
        # Draw apple and snake
        apple.draw(screen)
        snake.draw(screen)
        
        # Refresh screen
        pygame.display.update()
        
        # Control game speed - set to 10 FPS
        clock.tick(10)

# Run the game
if __name__ == "__main__":
    main()


# Run the game
if __name__ == "__main__":
    main()