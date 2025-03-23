import pygame
from flappy.config import(
    SCREENWIDTH,
    GROUNDY,
    BASE_VELOCITY_X
)

class Base:
    def _init_(self,sprites):
        self.x1=0
        self.x2=sprites['base'].get_width()
        self.y=GROUNDY
        self.velocity_x=BASE_VELOCITY_X
        self.sprites=sprites

    def move(self):
        self.x1+=self.velocity_x
        self.x2+=self.velocity_x

        base_width=self.sprites['base'].get_width()

        if self.x1+base_width<0:
            self.x1=self.x2+base_width

        if self.x2+base_width<0:
            self.x2=self.x1+base_width

    def draw(self,screen):
        screen.blit(self.sprites['base'],(self.x1,self.y))
        screen.blit(self.sprites['base'],(self.x2,self.y))
