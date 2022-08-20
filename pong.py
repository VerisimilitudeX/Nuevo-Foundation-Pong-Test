import pygame
import random
import sys
from screen import Screen

from paddle import Paddle
from ball import Ball


class Pong:
    BALL_WIDTH = 10
    BALL_VELOCITY = 6
    BALL_ANGLE = 0

    COLOUR = (255, 255, 255)

    LEFTSCORE = 0
    RIGHTSCORE = 0

    BALLXSTARTPOSITION = Screen.WIDTH / 2 - BALL_WIDTH / 2
    BALLYSTARTPOSITION = Screen.HEIGHT / 2 - BALL_WIDTH / 2

    def __init__(self):
        pygame.init()

        # Setup the screen
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        self.clock = pygame.time.Clock()

        # Create the player objects.

        self.paddles = []
        self.balls = []
        self.paddles.append(Paddle(  # The left paddle
            self.BALL_VELOCITY,
            pygame.K_w,
            pygame.K_s,
            0,
            Screen.HEIGHT / 2 - Paddle.HEIGHT / 2,
            Paddle.WIDTH,
            Paddle.HEIGHT
        ))

        self.paddles.append(Paddle(  # The right paddle
            self.BALL_VELOCITY,
            pygame.K_UP,
            pygame.K_DOWN,
            Screen.WIDTH - Paddle.WIDTH,
            Screen.HEIGHT / 2 - Paddle.HEIGHT / 2,
            Paddle.WIDTH,
            Paddle.HEIGHT
        ))

        self.balls.append(Ball(
            self.BALL_VELOCITY,
            self.BALLXSTARTPOSITION,
            self.BALLYSTARTPOSITION,
            self.BALL_WIDTH,
            self.BALL_WIDTH
        ))

        self.central_line = pygame.Rect(Screen.WIDTH/2, 0, 1, Screen.HEIGHT)

    def draw_text(self, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, self.COLOUR)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def check_ball_hits_wall(self):
        for ball in self.balls:
            if ball.x > Screen.WIDTH:
                self.LEFTSCORE = self.LEFTSCORE + 1
                ball.x = self.BALLXSTARTPOSITION
                ball.y = self.BALLYSTARTPOSITION
                ball.velocity = -1 * self.BALL_VELOCITY
                ball.angle = self.BALL_ANGLE

            if ball.x < 0:
                self.RIGHTSCORE = self.RIGHTSCORE + 1
                ball.x = self.BALLXSTARTPOSITION
                ball.y = self.BALLYSTARTPOSITION
                ball.velocity = self.BALL_VELOCITY
                ball.angle = self.BALL_ANGLE

            if ball.y > Screen.HEIGHT - self.BALL_WIDTH or ball.y < 0:
                ball.angle = -ball.angle

    def check_ball_hits_paddle(self):
        for ball in self.balls:
            for paddle in self.paddles:
                if ball.colliderect(paddle):
                    ball.velocity = -ball.velocity
                    ball.angle = random.randint(-10, 10)
                    break

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                # Add some extra ways to exit the game.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.check_ball_hits_paddle()
            self.check_ball_hits_wall()

            # Redraw the screen.
            self.screen.fill((0, 0, 0))

            for paddle in self.paddles:
                paddle.move_paddle(Screen.HEIGHT)
                pygame.draw.rect(self.screen, self.COLOUR, paddle)

            # We know we're not ending the game so lets move the ball here.
            for ball in self.balls:
                ball.move_ball()
                pygame.draw.rect(self.screen, self.COLOUR, ball)

            pygame.draw.rect(self.screen, self.COLOUR, self.central_line)

            self.draw_text(str(self.LEFTSCORE), 36, 350, 10)
            self.draw_text(str(self.RIGHTSCORE), 36, 450, 10)

            pygame.display.flip()
            self.clock.tick(90)
