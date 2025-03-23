import sys
import pygame
from flappy.player import Player
from flappy.pipe import Pipe
from flappy.base import Base
from flappy.config import (
    FPS,
    SCREENWIDTH,
    SCREENHEIGHT,
    PLAYER_START_X,
    PLAYER_START_Y,
    PIPE_DISTANCE_X,
    GROUNDY
)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.clock=pygame.time.Clock()
        self.screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

        self.sprites=self.load_sprites()
        self.sounds=self.load_sounds()

        self.player=None
        self.base=None
        self.pipes=[]
        self.score=0



    def load_sprites(self):
        return {
            'numbers':tuple(
                pygame.image.load(f'gallery/sprites/{i}.png').convert_alpha() for i in range(10)
            ),
            'message':pygame.image.load('gallery/sprites/welcome.png').convert_alpha(),
            'base':pygame.image.load('gallery/sprites/base.png').convert_alpha(),
            'pipe': (
                pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(), 180),
                pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
            ),
            'background': pygame.image.load('gallery/sprites/background.png').convert(),
            'player': pygame.image.load('gallery/sprites/bird.png').convert_alpha()
        }
    
    def load_sounds(self):
         return {
            'die': pygame.mixer.Sound('gallery/audio/die.wav'),
            'hit': pygame.mixer.Sound('gallery/audio/hit.wav'),
            'point': pygame.mixer.Sound('gallery/audio/point.wav'),
            'swoosh': pygame.mixer.Sound('gallery/audio/swoosh.wav'),
            'wing': pygame.mixer.Sound('gallery/audio/wing.wav')
        }
    
    def spawn_pipe(self, offset_x=0):
        """Spawn a new pipe at the given offset from SCREENWIDTH."""
        new_pipe_x = SCREENWIDTH + offset_x
        return Pipe(new_pipe_x, sprites=self.sprites)
    
    def reset(self):
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, sprites=self.sprites, sounds=self.sounds)
        self.base = Base(sprites=self.sprites)

        first_pipe = self.spawn_pipe(offset_x=200)
        second_pipe = self.spawn_pipe(offset_x=200 + PIPE_DISTANCE_X)

        self.pipes = [first_pipe, second_pipe]

        self.score = 0

    def welcome_screen(self):
        player_x=PLAYER_START_X
        player_y=PLAYER_START_Y
        message_x=(SCREENWIDTH-self.sprites['message'].get_width())/2
        message_y=SCREENHEIGHT*0.13

        while True:
            for event in pygame.event.get():
                if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    return 
            self.screen.blit(self.sprites['background'], (0, 0))
            self.screen.blit(self.sprites['message'], (message_x, message_y))
            self.screen.blit(self.sprites['base'], (0, GROUNDY))
            self.screen.blit(self.sprites['player'], (player_x, player_y))

            pygame.display.update()
            self.clock.tick(FPS)

    def run(self):
        """
        Start the game loop.
        """
        while True:
            self.welcome_screen()
            self.reset()
            self.main_game()

    def main_game(self):
        """
        Main gameplay loop.
        """
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

            if self.check_collision():
                self.sounds['hit'].play()
                return  # Exit the current game and show welcome screen again

    def handle_events(self):
        """
        Handle user input.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                self.player.flap()

    def update_game_state(self):
        self.player.move()
        self.base.move()

        for pipe in self.pipes:
            pipe.move()

        # Get the last pipe in the list
        last_pipe = self.pipes[-1]

        # Check if the last pipe has moved far enough to spawn a new one
        if last_pipe.x < SCREENWIDTH - PIPE_DISTANCE_X:
            new_pipe = self.spawn_pipe(offset_x=0)  # Spawn just off the right edge
            self.pipes.append(new_pipe)

        # Remove the pipe if it's off-screen
        if self.pipes[0].is_off_screen():
            self.pipes.pop(0)

        self.update_score()

    def update_score(self):
        player_mid_x=self.player.x+self.sprites['player'].get_width()/2

        for pipe in self.pipes:
            pipe_mid_x=pipe.x+self.sprites['pipe'][0].get_width()/2
            if(pipe_mid_x<=player_mid_x<pipe_mid_x+4):
                self.score+=1
                self.sounds['point'].play()

    def check_collision(self):
        """
        Check for collision with pipes or ground.
        """
        player_rect = self.player.get_rect()

        # Ground and ceiling collision
        if self.player.y > GROUNDY - 25 or self.player.y < 0:
            return True

        # Pipe collision
        for pipe in self.pipes:
            if player_rect.colliderect(pipe.get_upper_rect()) or player_rect.colliderect(pipe.get_lower_rect()):
                return True

        return False

    def draw(self):
        """
        Draw all game objects on the screen.
        """
        self.screen.blit(self.sprites['background'], (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.base.draw(self.screen)
        self.player.draw(self.screen)
        
        # Draw score
        score_str = str(self.score)
        total_width = 0
        number_height = self.sprites['numbers'][0].get_height()

        # Calculate total width of the score to center it
        for digit in score_str:
            total_width += self.sprites['numbers'][int(digit)].get_width()

        x_offset = (SCREENWIDTH - total_width) / 2

        for digit in score_str:
            digit_surface = self.sprites['numbers'][int(digit)]
            self.screen.blit(digit_surface, (x_offset, SCREENHEIGHT * 0.12))
            x_offset += digit_surface.get_width()


