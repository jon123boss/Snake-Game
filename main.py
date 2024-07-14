import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SNAKE_IMAGE = pygame.image.load('Snake head illustration.png')
FOOD_IMAGE = pygame.image.load('Ice cream gelato apple.png')
BACKGROUND_IMAGE = pygame.image.load('pngtree-top-down-view-of-a-rough-granular-dark-asphalt-road-texture-image_13806719.png')

SNAKE_IMAGE = pygame.transform.scale(SNAKE_IMAGE, (GRID_SIZE, GRID_SIZE))
FOOD_IMAGE = pygame.transform.scale(FOOD_IMAGE, (GRID_SIZE, GRID_SIZE))

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
            surface.blit(SNAKE_IMAGE, rect)

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
        surface.blit(FOOD_IMAGE, rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36, bold=True)

    def draw_score(surface, score):
        score_text = font.render(f'Score: {score}', True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH - 120, 10))

    def game_over(surface):
        game_over_text = font.render('Game Over', True, RED)
        restart_text = font.render('Press R to Restart', True, RED)
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))
        pygame.display.flip()

    def restart_game():
        return Snake(), Food(), 0

    snake, food, score = restart_game()
    game_over_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over_flag and event.key == pygame.K_r:
                    snake, food, score = restart_game()
                    game_over_flag = False
                elif event.key == pygame.K_UP:
                    snake.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('down')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('right')

        if not game_over_flag:
            snake.update()

            if snake.collides_with(food):
                snake.grow_snake()
                food = Food()
                score += 1

            if snake.collides_with_self() or snake.collides_with_boundaries():
                game_over(screen)
                game_over_flag = True

            screen.blit(BACKGROUND_IMAGE, (0, 0))
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
            pygame.display.flip()

        clock.tick(10)

if __name__ == '__main__':
    main()