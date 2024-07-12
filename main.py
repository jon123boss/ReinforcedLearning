import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 182, 193)
RADIUS = 10
PADDING = 20
NUM_ROWS = 5
NUM_COLS = 5

square_width = (SCREEN_WIDTH - (NUM_COLS + 1) * PADDING) // NUM_COLS
square_height = (SCREEN_HEIGHT - (NUM_ROWS + 1) * PADDING) // NUM_ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplying game")

blob_size = min(square_width, square_height) / 2
dot_radius = 8
turn = 0
player_turn = 0

blobs = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
dots = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

explosions = []

def animate_explosion(row, col):
    explosions.append({'row': row, 'col': col, 'radius': 0, 'max_radius': square_width // 2})

def check_win():
    blue_count = sum(blob == 0 for row in blobs for blob in row)
    red_count = sum(blob == 1 for row in blobs for blob in row)
    if blue_count == 0:
        return "Red wins!"
    elif red_count == 0:
        return "Blue wins!"
    return None

def reset_game():
    global blobs, dots, turn, player_turn
    blobs = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    dots = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    turn = 0
    player_turn = 0

running = True
win_message = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and win_message is None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    x = PADDING + col * (square_width + PADDING)
                    y = PADDING + row * (square_height + PADDING)
                    if x <= mouse_x <= x + square_width and y <= mouse_y <= y + square_height:
                        if blobs[row][col] is None and (turn == 0 or turn == 1):
                            if player_turn == turn % 2:
                                blobs[row][col] = turn % 2
                                dots[row][col] = 3
                                turn += 1
                                player_turn = 1 - player_turn
                        elif blobs[row][col] == turn % 2 and dots[row][col] < 3:
                            turn += 1
                            dots[row][col] += 1
                        elif blobs[row][col] == turn % 2 and dots[row][col] == 3:
                            explode(row, col, turn % 2)
                            turn += 1
                            player_turn = 1 - player_turn
                        if turn != 0 and turn != 1: win_message = check_win()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                win_message = None

    screen.fill(LIGHT_BLUE if turn % 2 == 0 else LIGHT_RED)

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = PADDING + col * (square_width + PADDING)
            y = PADDING + row * (square_height + PADDING)

            pygame.draw.rect(screen, GRAY, (x, y, square_width, square_height), border_radius=RADIUS)

            if blobs[row][col] is not None:
                blob_color = LIGHT_BLUE if blobs[row][col] == 0 else LIGHT_RED
                blob_x = x + (square_width - blob_size) // 2
                blob_y = y + (square_height - blob_size) // 2
                pygame.draw.rect(screen, blob_color, (blob_x, blob_y, blob_size, blob_size), border_radius=RADIUS)

                dot_positions = []
                if dots[row][col] == 1:
                    dot_positions = [(blob_x + blob_size // 2, blob_y + blob_size // 2)]
                elif dots[row][col] == 2:
                    dot_positions = [
                        (blob_x + blob_size // 2 - 10, blob_y + blob_size // 2),
                        (blob_x + blob_size // 2 + 10, blob_y + blob_size // 2)
                    ]
                elif dots[row][col] == 3:
                    dot_positions = [
                        (blob_x + blob_size // 2 - 10, blob_y + blob_size // 2 + 5),
                        (blob_x + blob_size // 2 + 10, blob_y + blob_size // 2 + 5),
                        (blob_x + blob_size // 2, blob_y + blob_size // 2 - 10)
                    ]

                for pos in dot_positions:
                    pygame.draw.circle(screen, WHITE, pos, dot_radius)

    # Handle and render explosion animations
    for explosion in explosions[:]:
        x = PADDING + explosion['col'] * (square_width + PADDING) + square_width // 2
        y = PADDING + explosion['row'] * (square_height + PADDING) + square_height // 2
        pygame.draw.circle(screen, WHITE, (x, y), explosion['radius'], 2)
        explosion['radius'] += 5
        if explosion['radius'] > explosion['max_radius']:
            explosions.remove(explosion)

    if win_message:
        font = pygame.font.SysFont(None, 75)
        text = font.render(win_message, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        sub_font = pygame.font.SysFont(None, 50)
        sub_text = sub_font.render("Press R to restart", True, BLACK)
        sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(sub_text, sub_text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()