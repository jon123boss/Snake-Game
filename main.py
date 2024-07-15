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

SNAKE_HEAD_IMAGE = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
pygame.draw.rect(SNAKE_HEAD_IMAGE, (0, 255, 0), (0, 0, GRID_SIZE, GRID_SIZE))
FOOD_IMAGE = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
pygame.draw.circle(FOOD_IMAGE, (255, 0, 0), (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)
BACKGROUND_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_IMAGE.fill((100, 100, 100))

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
            surface.blit(SNAKE_HEAD_IMAGE, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE))

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
        self.position = self.randomize_position()

    def randomize_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        surface.blit(FOOD_IMAGE, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE))

def draw_score(surface, score):
    font = pygame.font.SysFont('Arial', 24, bold=True)
    score_text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(score_text, (10, 10))

def draw_menu(surface, font):
    surface.fill(BLACK)
    title_text = font.render('Snake Game', True, WHITE)
    start_text = font.render('Press ENTER to Start', True, WHITE)
    quit_text = font.render('Press ESC to Quit', True, WHITE)

    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    surface.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def handle_playing_state(surface, clock, snake, food, score, level):
    snake_speed = 8 + level * 2

    snake.update()

    if snake.collides_with(food):
        snake.grow_snake()
        food = Food()
        score += 1

        if score >= 10 + level * 5:
            level += 1
            if level >= len(LEVELS):
                level = len(LEVELS) - 1

    if snake.collides_with_self() or snake.collides_with_boundaries():
        return False, score, level

    surface.blit(BACKGROUND_IMAGE, (0, 0))
    snake.draw(surface)
    food.draw(surface)
    draw_score(surface, score)

    return True, score, level

def handle_game_over(surface, font, score):
    surface.fill(BLACK)
    game_over_text = font.render('Game Over', True, RED)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    restart_text = font.render('Press ENTER to Restart', True, WHITE)
    quit_text = font.render('Press ESC to Quit', True, WHITE)

    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

def restart_game():
    return Snake(), Food(), 0

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24, bold=True)

    level = 0
    snake, food, score = None, None, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and level == 0:
                    snake, food, score = restart_game()
                    level = 1

                if level > 0:
                    if event.key == pygame.K_UP:
                        snake.change_direction('up')
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction('down')
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction('left')
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction('right')

        if level > 0:
            game_over, score, level = handle_playing_state(screen, clock, snake, food, score, level)
            if not game_over:
                handle_game_over(screen, font, score)
                level = 0

        else:
            screen.fill(BLACK)
            draw_menu(screen, font)

        pygame.display.flip()
        clock.tick(10 + level * 2)

if __name__ == '__main__':
    main()

