import pygame
import random
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION = (GRID_WIDTH // 2, 0)
PIECES = [
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 1, 1], [0, 1, 0]],  
    [[1, 1, 1], [0, 0, 1]],  
    [[1, 1, 1], [1, 0, 0]]  
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_tetromino(tetromino, position):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                pygame.draw.rect(screen, tetromino_color, (position[0] * GRID_SIZE + x * GRID_SIZE,  position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision(tetromino, position, grid):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                if position[0] + x < 0 or position[0] + x >= GRID_WIDTH or \
                        position[1] + y >= GRID_HEIGHT or grid[position[1] + y][position[0] + x]:
                    return True
    return False

def merge_tetromino(tetromino, position, grid):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                grid[position[1] + y][position[0] + x] = 1

def remove_completed_rows(grid):
    completed_rows = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            completed_rows.append(y)
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
    return len(completed_rows)

grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
tetromino = random.choice(PIECES)
tetromino_color = random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
position = list(INITIAL_POSITION)
score = 0
start_time = pygame.time.get_ticks()

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                position[0] -= 1
                if check_collision(tetromino, position, grid):
                    position[0] += 1
            elif event.key == pygame.K_RIGHT:
                position[0] += 1
                if check_collision(tetromino, position, grid):
                    position[0] -= 1
            elif event.key == pygame.K_DOWN:
                position[1] += 1
                if check_collision(tetromino, position, grid):
                    position[1] -= 1
            elif event.key == pygame.K_UP:
                rotated_tetromino = list(zip(*reversed(tetromino)))
                if not check_collision(rotated_tetromino, position, grid):
                    tetromino = rotated_tetromino

    position[1] += 1
    if check_collision(tetromino, position, grid):
        position[1] -= 1
        merge_tetromino(tetromino, position, grid)
        completed_rows = remove_completed_rows(grid)
        score += completed_rows
        tetromino = random.choice(PIECES)
        tetromino_color = random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
        position = list(INITIAL_POSITION)
        if check_collision(tetromino, position, grid):
            game_over = True


    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(tetromino, position)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(2)  


elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
screen.fill(BLACK)
font = pygame.font.Font(None, 36)
score_text = font.render(f"Score: {score}", True, WHITE)
time_text = font.render(f"Time: {elapsed_time} seconds", True, WHITE)
screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()