import random
import pygame
from flappy.config import(
    SCREENWIDTH,
    SCREENHEIGHT,
    PIPE_VELOCITY_X,
    PIPE_GAP_SIZE
)

class Pipe:
    def __init__(self,x,sprites):
        self.x=x
        self.sprites=sprites
        self.pipe_height=self.sprites['pipe'][0].get_height()

        self.upper_y,self.lower_y=self.generate_y_positions()

    def generate_y_positions(self):
        offset=PIPE_GAP_SIZE
        base_height=self.sprites['base'].get_height()

        y2=offset+random.randrange(
            0,int(SCREENHEIGHT-base_height-1.2*offset)
        )
        y1=self.pipe_height-y2+offset
        return -y1,y2
    
    def move(self):
        self.x+=PIPE_VELOCITY_X
    
    def draw(self,screen):
        screen.blit(self.sprites['pipe'][0],(self.x,self.upper_y))

        screen.blit(self.sprites['pipe'][1],(self.x,self.lower_y))
 

    
    def is_off_screen(self):
        return self.x<-self.sprites['pipe'][0].get_width()

    def get_upper_rect(self):
        pipe_surface = self.sprites['pipe'][0]
        return pipe_surface.get_rect(topleft=(self.x, self.upper_y))

    def get_lower_rect(self):
        pipe_surface=self.sprites['pipe'][1]
        return pipe_surface.get_rect(topleft=(self.x,self.lower_y))