import random
import sys

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки:
FPS = 20

# Настройка игрового окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Изгиб Питона")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект (заглушка для переопределения)."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, position=None, body_color=(255, 0, 0)):
        """Инициализирует яблоко."""
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, position=None, body_color=(0, 255, 0)):
        """Инициализирует змейку в начальном состоянии."""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        super().__init__((start_x, start_y), body_color)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()

        # Запоминаем хвост до движения, чтобы потом затереть его на экране
        old_tail = snake.positions[-1] if len(snake.positions) > 1 else None
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while True:
                apple.randomize_position()
                if apple.position not in snake.positions:
                    break

        # Проверка на столкновение с собой
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
            apple.randomize_position()
            continue

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)

        if old_tail and old_tail not in snake.positions:
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                (*old_tail, GRID_SIZE, GRID_SIZE)
            )

        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
