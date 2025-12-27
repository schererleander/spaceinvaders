import asyncio
import pygame

from Szenen import Menue, Game, Benennung, Score


class Steuerung:
  def __init__(self):
    self.__szene = Menue()
    self.__szenenIndex = 0
    self.__verlasseSpiel = False
    self.__spielerListe = []

    self.__clock = pygame.time.Clock()

  def __sotiereSpielerListe(self):
    self.__spielerListe.sort(key=lambda spieler: spieler[1], reverse=True)

  def __addSpieler(self, spielerName: str, spielerScore: int):
    gibtSpieler = False
    for spieler in range(len(self.__spielerListe)):
      if self.__spielerListe[spieler][0] == spielerName:
        gibtSpieler = True
        self.__spielerListe[spieler] = (spielerName, spielerScore)
    if not gibtSpieler:
      self.__spielerListe.append((spielerName, spielerScore))

  def __wechselSzene(self):
    self.__szenenIndex += 1
    if self.__szenenIndex > 3:
      self.__szenenIndex = 0

    if self.__szenenIndex == 0:
      self.__szene = Menue()
    elif self.__szenenIndex == 1:
      self.__szene = Game()
    elif self.__szenenIndex == 2:
      score = self.__szene.getScore()
      self.__szene = Benennung(score)
    elif self.__szenenIndex == 3:
      score = self.__szene.getScore()
      name = self.__szene.getName()
      self.__addSpieler(name, score)
      self.__sotiereSpielerListe()
      self.__szene = Score(self.__spielerListe)

  async def loop(self):
    while not self.__szene == None and not self.__verlasseSpiel:
      dt = self.__clock.tick(60) / 1000.0

      key_events = []
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.__verlasseSpiel = True
        elif event.type == pygame.KEYDOWN:
          key_events.append(event)

      if key_events:
        self.__szene.beiEingabe(key_events)

      self.__szene.beiUpdate(dt)
      self.__szene.beiZeichne()

      if self.__szene.getWechselSzene():
        self.__wechselSzene()

      await asyncio.sleep(0)
