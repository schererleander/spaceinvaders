import pygame

class Laser(pygame.sprite.Sprite):
  def __init__(self, position: tuple, geschwindigkeit: float):
    super().__init__()
    self.image = pygame.Surface((3,10))
    self.image.fill((255,255,255)) # Farbe
    self.rect = self.image.get_rect()
    self.rect.center = position

    self.__pos_y = float(self.rect.y)
    self.__geschwindigkeit = float(geschwindigkeit)

  def getRect(self):
    return self.rect

  def bewegen(self, dt: float):
    self.__pos_y += self.__geschwindigkeit * dt
    self.rect.y = int(round(self.__pos_y))

  def einschraenken(self, screenHoehe: int):
    if self.rect.bottom < 0 or self.rect.top > screenHoehe:
      self.kill()
