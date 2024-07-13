import pygame
import sys
import time

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def update(self):

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, direction):
        if direction == 'up' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == 'down' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif direction == 'left' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == 'right' and self.direction != (-1, 0):
            self.direction = (1, 0)

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, WHITE, rect)

def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    snake = Snake()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('down')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('right')

        snake.update()

        screen.fill(BLACK)
        snake.draw(screen)
        pygame.display.flip()

        clock.tick(10)

if __name__ == '__main__':
    main()