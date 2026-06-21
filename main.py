import random
from pathlib import Path

import pygame

try:
    from snake import Snake
except ImportError:
    from .snake import Snake


CELL_SIZE = 24
COLUMNS = 30
ROWS = 22
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60
MOVE_DELAY_MS = 115

BACKGROUND = (18, 22, 26)
GRID_COLOR = (27, 33, 38)
TEXT_COLOR = (232, 238, 224)
APPLE_COLOR = (220, 45, 55)
APPLE_HIGHLIGHT = (255, 135, 140)
LEAF_COLOR = (78, 180, 90)

ASSET_DIR = Path(__file__).resolve().parent / "assets"
APPLE_SPRITE = ASSET_DIR / "apple.png"


class Apple:
    def __init__(self, sprite, snake_body):
        self.sprite = sprite
        self.position = (0, 0)
        self.respawn(snake_body)

    def respawn(self, snake_body):
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(COLUMNS)
            for y in range(ROWS)
            if (x, y) not in occupied
        ]
        self.position = random.choice(free_cells) if free_cells else (-1, -1)

    def draw(self, surface):
        x, y = self.position
        surface.blit(self.sprite, (x * CELL_SIZE, y * CELL_SIZE))


def create_apple_sprite(path):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    sprite = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(sprite, APPLE_COLOR, (12, 14), 8)
    pygame.draw.circle(sprite, APPLE_HIGHLIGHT, (9, 11), 3)
    pygame.draw.ellipse(sprite, LEAF_COLOR, pygame.Rect(13, 3, 8, 5))
    pygame.draw.line(sprite, (95, 58, 35), (12, 7), (13, 3), 2)
    pygame.image.save(sprite, str(path))


def load_apple_sprite():
    if not APPLE_SPRITE.exists():
        create_apple_sprite(APPLE_SPRITE)
    return pygame.image.load(str(APPLE_SPRITE)).convert_alpha()


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_score(surface, font, score):
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    surface.blit(text, (12, 10))


def draw_game_over(surface, font, small_font, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    title = font.render("Game Over", True, TEXT_COLOR)
    score_text = small_font.render(f"Final score: {score}", True, TEXT_COLOR)
    restart = small_font.render("Press SPACE to restart or ESC to quit", True, TEXT_COLOR)

    surface.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 44)))
    surface.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    surface.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 38)))


def new_game(apple_sprite):
    snake = Snake(
        start_pos=(COLUMNS // 2, ROWS // 2),
        cell_size=CELL_SIZE,
        color=(55, 196, 96),
        head_color=(35, 145, 75),
    )
    apple = Apple(apple_sprite, snake.body)
    return snake, apple, 0, False


def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 30)
    apple_sprite = load_apple_sprite()

    snake, apple, score, game_over = new_game(apple_sprite)
    last_move_time = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snake, apple, score, game_over = new_game(apple_sprite)
                last_move_time = pygame.time.get_ticks()
            elif not game_over:
                snake.handle_event(event)

        now = pygame.time.get_ticks()
        if not game_over and now - last_move_time >= MOVE_DELAY_MS:
            snake.move()
            last_move_time = now

            if snake.head == apple.position:
                score += 1
                snake.grow()
                apple.respawn(snake.body)

            if snake.hits_self() or snake.out_of_bounds(COLUMNS, ROWS):
                game_over = True

        screen.fill(BACKGROUND)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)
        draw_score(screen, small_font, score)

        if game_over:
            draw_game_over(screen, font, small_font, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
