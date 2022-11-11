import pygame
import os

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Game")

GREEN = (120, 0, 255)
WHITE = (0, 0, 0)
# BORDER = pygame.Rect(0, 100, 10, 300)

# BUZZER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Buzzer_sound.mp3'))
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

FPS = 30
VEL = 5
GOALPOST_WIDTH, GOALPOST_HEIGHT = 900, 500
GOALIE_WIDTH, GOALIE_HEIGHT = 500, 400
BALL_WIDTH, BALL_HEIGHT = 100, 100
STAR_WIDTH, STAR_HEIGHT = 130, 130

GOALPOST_IMAGE = pygame.image.load(os.path.join('Assets', 'goalpost.jpg'))
GOALPOST = pygame.transform.scale(
    GOALPOST_IMAGE, (GOALPOST_WIDTH, GOALPOST_HEIGHT))

GOALIE_IMAGE = pygame.image.load(os.path.join('Assets', 'goalie.png'))
GOALIE = pygame.transform.scale(GOALIE_IMAGE, (GOALIE_WIDTH, GOALIE_HEIGHT))

BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'ball.png'))
BALL = pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

STAR_IMAGE = pygame.image.load(os.path.join('Assets', 'Star 1.png'))
STAR = pygame.transform.scale(STAR_IMAGE, (STAR_WIDTH, STAR_HEIGHT))


def draw_window(goalie, ball):
    WIN.fill(GREEN)
    WIN.blit(GOALPOST, (0, 0))
    score_text = SCORE_FONT.render("SCORE: " + str(), 1, WHITE)
    WIN.blit(score_text, (600, 12))
    # pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(GOALIE, (goalie.x, goalie.y))
    WIN.blit(BALL, (ball.x, ball.y))
   # WIN.blit(STAR, (pygame.mouse.get_pos()))
    pygame.display.update()


# def automatic_movements(goalie):
#     # goalie = GOALIE.goalie
#     # screen_rect = self.GOALIE.screen.get_rect()
#
#     if (goalie.x - VEL) > 15:
#         goalie.x -= VEL
#     # elif goalie.moving_right and goalie.x - VEL > 15:
#     #     goalie.moving_right = False
#     #     goalie.moving_left = True
#
#     elif (goalie.x + VEL + goalie.width) < (WIDTH - 50):
#         goalie.x += VEL
#         # goalie.moving_left = False
#         # goalie.moving_right = True
def goalie_movement(keys_pressed, goalie):
    if keys_pressed[pygame.K_a] and goalie.x - VEL > 15:
        goalie.x -= VEL
    if keys_pressed[pygame.K_d] and goalie.x + VEL + goalie.width < WIDTH - 50:
        goalie.x += VEL


def ball_movements(keys_pressed, ball):
    if keys_pressed[pygame.K_LEFT] and ball.y - VEL > 50:
        ball.y -= VEL

    if keys_pressed[pygame.K_RIGHT] and ball.x + VEL + ball.width < WIDTH:
        ball.x += VEL


def main():
    goalie = pygame.Rect(180, 40, GOALIE_WIDTH, GOALIE_HEIGHT)
    ball = pygame.Rect(400, 400, BALL_WIDTH, BALL_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    # BUZZER_SOUND.play()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                WIN.blit(STAR, (pygame.mouse.get_pos()))
            if event.type == pygame.QUIT:
                run = False
            pygame.display.flip()

        keys_pressed = pygame.key.get_pressed()
        goalie_movement(keys_pressed, goalie)
        # automatic_movements(goalie)
        ball_movements(keys_pressed, ball)
        draw_window(goalie, ball)

    pygame.quit()


if __name__ == "__main__":
    main()
