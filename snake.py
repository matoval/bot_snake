import pygame
import random
import sys

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

# initialize pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

# create a clock to control the frame rate
clock = pygame.time.Clock()

# initialize snake position and direction
snake_pos = [100, 60]
snake_body = [[100, 60], [90, 60], [80, 60]]
direction = "RIGHT"
change_to = direction

# initialize food position
food_pos = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
food_spawn = True

score = 0

# game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your score was: ' + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

while True:
    # event handling and input processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    # make sure the snake cannot move in the opposite direction instantaneously
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # check for game over conditions
    if (
        snake_pos[0] > SCREEN_WIDTH or snake_pos[0] < 0
        or snake_pos[1] > SCREEN_HEIGHT or snake_pos[1] < 0
        or snake_pos in snake_body[1:]
    ):
        game_over()

    # update snake position
    if direction == "UP":
        snake_pos[1] -= BLOCK_SIZE
    if direction == "DOWN":
        snake_pos[1] += BLOCK_SIZE
    if direction == "LEFT":
        snake_pos[0] -= BLOCK_SIZE
    if direction == "RIGHT":
        snake_pos[0] += BLOCK_SIZE

    # snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                    random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        food_spawn = True

    screen.fill(BLACK)

    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # draw score
    score_font = pygame.font.SysFont('times new roman', 35)
    score_surface = score_font.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (SCREEN_WIDTH / 2, 10)
    screen.blit(score_surface, score_rect)

    pygame.display.update()
    clock.tick(20)

