import pygame
from flappy.config import GROUNDY

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

        