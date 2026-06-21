import pygame


class Snake:
    """Grid-based snake for the classic Snake game."""

    def __init__(
        self,
        start_pos=(10, 10),
        cell_size=20,
        color=(45, 180, 80),
        head_color=(30, 130, 60),
    ):
        self.cell_size = cell_size
        self.color = color
        self.head_color = head_color
        self.body = [start_pos]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow_pending = 0

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, direction):
        """Queue a direction change unless it would reverse into the body."""
        if direction == (0, 0):
            return

        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.next_direction = direction

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        key_directions = {
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
        }

        if event.key in key_directions:
            self.set_direction(key_directions[event.key])

    def move(self):
        self.direction = self.next_direction
        next_head = (
            self.head[0] + self.direction[0],
            self.head[1] + self.direction[1],
        )

        self.body.insert(0, next_head)
        if self.grow_pending:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def hits_self(self):
        return self.head in self.body[1:]

    def out_of_bounds(self, columns, rows):
        x, y = self.head
        return x < 0 or y < 0 or x >= columns or y >= rows

    def draw(self, surface):
        for index, (x, y) in enumerate(self.body):
            rect = pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(
                surface,
                self.head_color if index == 0 else self.color,
                rect,
                border_radius=4,
            )
