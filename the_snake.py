import pygame
import random

# Инициализация Pygame и задание размеров окна
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_COLOR = (0, 0, 0)  # Черный цвет фона

# Настройка отображения
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, body_color):
        """
        Инициализация игрового объекта с позицией и цветом.

        :param position: Кортеж координат (x, y)
        :param body_color: Кортеж RGB цвета
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Отрисовка объекта на игровой поверхности. Метод должен быть переопределен.

        :param surface: Поверхность Pygame для рисования объекта
        """
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока со случайной позицией и цветом (красный)."""
        super().__init__(self.randomize_position(), (255, 0, 0))

    def randomize_position(self):
        """
        Случайным образом задает позицию яблока внутри игрового поля.

        :return: Кортеж координат (x, y) для новой позиции
        """
        x = random.randint(0, (WINDOW_WIDTH // 20) - 1) * 20
        y = random.randint(0, (WINDOW_HEIGHT // 20) - 1) * 20
        return (x, y)

    def draw(self, surface):
        """Отрисовка яблока в виде красного квадрата на поверхности."""
        pygame.draw.rect(surface, self.body_color, (*self.position, 20, 20))


class Snake(GameObject):
    """Класс, представляющий змею, и управляющий ее движением и взаимодействиями."""

    def __init__(self):
        """Инициализация змеи с длиной 1 и направлением по умолчанию."""
        super().__init__((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = (20, 0)  # Движение вправо по умолчанию
        self.next_direction = None

    def update_direction(self, new_direction):
        """
        Обновление направления змеи на основе пользовательского ввода.

        :param new_direction: Кортеж, представляющий новое направление (dx, dy)
        """
        # Запрет на изменение направления на противоположное
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        """
        Движение змеи в соответствии с ее направлением, добавление новой
        головы и удаление хвоста, если длина не изменилась.
        """
        if self.next_direction:
            self.direction = self.next_direction
        new_head = (
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        )
        self.positions = [new_head] + self.positions[:self.length - 1]

    def grow(self):
        """Увеличение длины змеи на один сегмент."""
        self.length += 1

    def reset(self):
        """Сброс змеи до начальной длины и позиции."""
        self.__init__()

    def get_head_position(self):
        """
        Получить текущую позицию головы змеи.

        :return: Кортеж координат головы
        """
        return self.positions[0]

    def draw(self, surface):
        """Отрисовка сегментов тела змеи на поверхности."""
        for segment in self.positions:
            pygame.draw.rect(surface, self.body_color, (*segment, 20, 20))


def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления движением змеи.

    :param snake: Экземпляр класса Snake
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
    """Главный игровой цикл, который управляет инициализацией, событиями, обновлениями и отрисовкой."""
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление змеей с помощью клавиш
        handle_keys(snake)

        # Обновление направления змеи и движение
        snake.move()

        # Проверка, ест ли змея яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        # Проверка на самопересечение
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()

        # Отрисовка яблока и змеи
        apple.draw(screen)
        snake.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Задание скорости игры - 10 кадров в секунду
        clock.tick(10)

    pygame.quit()


# Запуск игры
if __name__ == "__main__":
    main()
