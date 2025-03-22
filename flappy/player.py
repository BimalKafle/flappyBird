import pygame
from flappy.config import (
    GROUNDY,
    PLAYER_VELOCITY_Y,
    PLAYER_MAX_VELOCITY_Y,
    PLAYER_MIN_VELOCITY_Y,
    PLAYER_ACC_Y,
    PLAYER_FLAP_ACC_V
)

class Player:
    def _init_(self,x,y,sprites,sounds):
        """
        Initialize the player 
        x= initial x position
        y initail y position
        sprites= refers to the dictionary that contains the image required for game
        sounds= refers to the dictionary that contains the sound required for game
        """
        self.x=x
        self.y=y
        self.sprites=sprites
        self.sounds=sounds

        self.vel_y=PLAYER_VELOCITY_Y
        self.max_vel_y=PLAYER_MAX_VELOCITY_Y
        self.min_vel_y=PLAYER_MIN_VELOCITY_Y
        self.acc_y=PLAYER_ACC_Y
        self.flap_accv=PLAYER_FLAP_ACC_V

        self.flapped=false

    def flap(self):
        self.vel_y=self.flap_accv
        self.flapped=True
        self.sounds['wing'].play()

    def move(self):
        if(self.vel_y<self.max_vel_y and not self.flapped):
            self.vel_y+=self.acc_y
        if self.flapped:
            self.flapped=False 

        player_height=self.sprites['player'].get_height()
        self.y+=min(self.vel_y,GROUNDY-self.y-player_height)


    def draw(self,screen):
        screen.blite(self.sprites['player'],(self.x,self.y))

    def get_rect(self):
        return self.sprites['player'].get_rect(topleft=(self.x,self.y)) 
