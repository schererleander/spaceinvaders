import pygame
import os

class Spieler(pygame.sprite.Sprite):
  def __init__(self, position: tuple):
    super().__init__()
    self.image = pygame.image.load(os.path.abspath('assets/img/player.png'))
    self.rect = self.image.get_rect()
    self.rect.center = position

    self.__pos_x = float(self.rect.x)

    self.__leben = 3
    # pixels/second (old: 8 px/frame @ 60 FPS)
    self.__geschwindigkeit = 480.0

    self.__laserCoolDown = 300
    self.__zeitVonLetzenSchuss = 0
  
  def getLaserPostion(self) -> tuple:
    return (self.rect.centerx, self.rect.top)

  def getLeben(self) -> int:
    return self.__leben

  def bewegen(self, dt: float):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.__pos_x -= self.__geschwindigkeit * dt
    if keys[pygame.K_RIGHT]:
      self.__pos_x += self.__geschwindigkeit * dt

    self.rect.x = int(round(self.__pos_x))
  
  def einschraenken(self, screenLaenge):
    if self.rect.left <= 0:
      self.rect.x = 0
    if self.rect.right >= screenLaenge:
      self.rect.right = screenLaenge

    self.__pos_x = float(self.rect.x)
  
  def schuss(self):
    keys = pygame.key.get_pressed()
    jetzt = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and jetzt - self.__zeitVonLetzenSchuss >= self.__laserCoolDown:
      self.__zeitVonLetzenSchuss = jetzt
      return True
    else:
      return False

  def treffer(self):
    self.__leben -= 1

  def heilen(self):
    self.__leben += 1
  

