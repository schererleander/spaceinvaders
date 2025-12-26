import pygame
import os

class Extra(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.image = pygame.image.load(os.path.abspath('assets/img/extra.png'))
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)

    self.__pos_x = float(self.rect.x)
    # pixels/second (old: 2 px/frame @ 60 FPS)
    self.__geschwindigkeit = 120.0
  
  def bewegen(self, dt: float):
    self.__pos_x += self.__geschwindigkeit * dt
    self.rect.x = int(round(self.__pos_x))
  
  def einschraenken(self, screenLaenge):
    if self.rect.left >= screenLaenge:
      self.kill()