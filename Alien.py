import pygame
import os

class Alien(pygame.sprite.Sprite):
  def __init__(self, bildDateipfad: str, position: tuple, wert: int):
    super().__init__()
    self.image = pygame.image.load(os.path.abspath(bildDateipfad))
    self.rect = self.image.get_rect()
    self.rect.center = position

    self.__pos_x = float(self.rect.x)
    self.__pos_y = float(self.rect.y)
    
    self.__wert = wert
    # pixels/second (old: 1 px/frame @ 60 FPS)
    self.__geschwindigkeit = 60.0
  
  def getRect(self):
    return self.rect

  def getWert(self) -> int:
    return self.__wert
  
  def aendereRichtung(self):
    self.__geschwindigkeit *= -1
 
  def bewegen(self, dt: float):
    self.__pos_x += self.__geschwindigkeit * dt
    self.rect.x = int(round(self.__pos_x))
  
  def bewegeRunter(self, y):
    self.__pos_y += y
    self.rect.y = int(round(self.__pos_y))