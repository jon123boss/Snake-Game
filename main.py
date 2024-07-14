import pygame
import sys
import random
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
        self.grow = False

    def update(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
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

    def grow_snake(self):
        self.grow = True

    def collides_with(self, obj):
        return self.positions[0] == obj.position

    def collides_with_self(self):
        return self.positions[0] in self.positions[1:]

    def collides_with_boundaries(self):
        head_x, head_y = self.positions[0]
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)

def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    snake = Snake()
    food = Food()
    score = 0

    def draw_score(surface, score):
        score_text = font.render(f'Score: {score}', True, WHITE)
        surface.blit(score_text, (10, 10))

    def game_over(surface):
        game_over_text = font.render('Game Over', True, RED)
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

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

        if snake.collides_with(food):
            snake.grow_snake()
            food = Food()
            score += 1

        if snake.collides_with_self() or snake.collides_with_boundaries():
            game_over(screen)

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, score)
        pygame.display.flip()

        clock.tick(10)

if __name__ == '__main__':
    main()

_____

Collision and gam over