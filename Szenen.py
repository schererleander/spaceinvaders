import pygame

class Szene():
  def __init__(self):
    self._wechselSzene = False

  def beiEingabe(self, events: list):
    pass

  def beiUpdate(self, dt: float):
    pass
  
  def beiZeichne(self):
    pass
  
  def getWechselSzene(self):
    return self._wechselSzene

from GUI import GUI

class Menue(Szene):
  def __init__(self, ):
    super().__init__()
    self.__screen = pygame.display.set_mode((600,700))
    pygame.display.set_caption('Space Invaders')
    self.__dieGUI = GUI(self.__screen)

    self.__background = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()))
    self.__background.fill((0,0,0))

  def beiEingabe(self, events: list):
    # Alle Tasten werden in eine Liste gespeichert, wenn eine Taste gedrueckt ist der Wert des Index der Taste 1
    keys = pygame.key.get_pressed()
    # Wenn die Leertaste gedrueckt ist starte das Spiel
    if keys[pygame.K_SPACE]:
      self._wechselSzene = True

  def beiUpdate(self, dt: float):
    pass

  def beiZeichne(self):
    # Der Hintergrund wird auf den Screen gezeichnet
    self.__screen.blit(self.__background, (0,0))

    self.__dieGUI.zeichneText('Space Invaders', 20, self.__screen.get_width()//2, int(self.__screen.get_height()*0.20), (255,255,255))
    self.__dieGUI.zeichneText('Um das Spiel zu starten druecke:', 16, self.__screen.get_width()//2, int(self.__screen.get_height()*0.40), (255,255,255))
    self.__dieGUI.zeichneRoundedButton('Space', 15, self.__screen.get_width()//2, int(self.__screen.get_height()*0.60), 120, 60, 10, (255,255,255), (0,0,0))
    
    # Das Bild wird refreshed
    pygame.display.flip()

from random import randrange
from Extra import Extra
from Bunker import Bunker
from Laser import Laser
from Spieler import Spieler
from Alien import Alien

class Game(Szene):
  def __init__(self):
    super().__init__()
    self.__screen = pygame.display.set_mode((600,700))

    self.__hintergrund = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()))
    self.__hintergrund.fill((0,0,0))

    self.__score = 0
    self.__alienUebrig = 0
    self.__alienSchussIntervall = 1000
    self.__zeitVonLetztenAlienSchuss = 0

    self.__extraSpawnIntervall = 40000
    self.__zeitvonLetztenExtra = 1

    self.__volume = 0.1
    self.__shootSound = pygame.mixer.Sound('assets/sound/shoot.wav')
    self.__shootSound.set_volume(self.__volume)
    self.__alienTodSound = pygame.mixer.Sound('assets/sound/invaderkilled.wav')
    self.__alienTodSound.set_volume(self.__volume)
    self.__spielerTodSound = pygame.mixer.Sound('assets/sound/explosion.wav')
    self.__spielerTodSound.set_volume(self.__volume)

    self.__derSpieler = Spieler((int(self.__screen.get_width()/2), int(self.__screen.get_height()*0.90)))

    self.__dieGUI = GUI(self.__screen)
    self.__spielerSpriteGruppe = pygame.sprite.GroupSingle(self.__derSpieler)
    self.__spielerLaserSpriteGruppe = pygame.sprite.Group()
    self.__alienSpriteGruppe = pygame.sprite.Group()
    self.__alienLaserSpriteGruppe = pygame.sprite.Group()
    self.__extraSpriteGruppe = pygame.sprite.GroupSingle()
    self.__bunkerSpriteGruppe = pygame.sprite.Group()

    self.__bunkerForm = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx',
    ]

    self.__erstelleAlleBunker(anzahl=4,groeße=7,startX=50,startY=int(self.__screen.get_width()*0.85), xOffset=80)
    self.__erstelleAliens(zeilen=6,spalten=8,startX=50, startY=100,xDistanz=20,yDistanz=20)

  def __erstelleBunker(self, groeße: int, startX: int, startY: int):
    for zeile in range(len(self.__bunkerForm)):
      for spalte in range(len(self.__bunkerForm[zeile])):
        if self.__bunkerForm[zeile][spalte] == 'x':
          x = startX + spalte * groeße
          y = startY + zeile * groeße
          derBlock = Bunker(x, y, groeße, (180,70,60))
          self.__bunkerSpriteGruppe.add(derBlock)

  def __erstelleAlleBunker(self, anzahl: int, groeße: int, startX: int, startY: int, xOffset: int):
    for spalte in range(anzahl):
      x = startX + (spalte * len(self.__bunkerForm[0]) * groeße) + (spalte * xOffset)
      y = startY
      self.__erstelleBunker(groeße,x,y)

  def __erstelleAliens(self, zeilen: int, spalten: int, startX: int, startY: int, xDistanz: int, yDistanz: int):
      beispielAlien = pygame.image.load('assets/img/red.png')
      weiteAlien = beispielAlien.get_width()
      hoeheAlien = beispielAlien.get_height()
      
      for zeile in range(zeilen):
        for spalte in range(spalten):
          x = startX + spalte *  weiteAlien + spalte * xDistanz
          y = startY + zeile * hoeheAlien + zeile * yDistanz
          if zeile == 0:
            dasAlien = Alien('assets/img/yellow.png', (x, y), 60)
          elif zeile == 1 or zeile == 2:
            dasAlien = Alien('assets/img/green.png', (x, y), 30)
          else:
            dasAlien = Alien('assets/img/red.png', (x, y), 20)
          self.__alienSpriteGruppe.add(dasAlien)
  
  def __bewegeAliens(self, dt: float):
    for alien in self.__alienSpriteGruppe:
      alien.bewegen(dt)
      if alien.getRect().right >= self.__screen.get_width():
        for alien in self.__alienSpriteGruppe:
          alien.aendereRichtung()
          alien.bewegeRunter(12)
      elif alien.getRect().left <= 0:
        for alien in self.__alienSpriteGruppe:
          alien.aendereRichtung()
          alien.bewegeRunter(12)
  
  def __alienSchuss(self):
    jetzt = pygame.time.get_ticks()
    if jetzt - self.__zeitVonLetztenAlienSchuss >= self.__alienSchussIntervall and len(self.__alienSpriteGruppe) > 0:
      alienListe = list(self.__alienSpriteGruppe)
      randomAlien = alienListe[randrange(len(alienListe))]
      self.__zeitVonLetztenAlienSchuss = pygame.time.get_ticks()
      self.__shootSound.play()
      self.__alienLaserSpriteGruppe.add(Laser((randomAlien.getRect().centerx, randomAlien.getRect().bottom), 120.0))

  def __erstelleExtra(self):
    jetzt = pygame.time.get_ticks()
    if jetzt - self.__zeitvonLetztenExtra >= self.__extraSpawnIntervall:
      self.__extraSpriteGruppe.add(Extra(-10, 50))
      self.__zeitvonLetztenExtra = jetzt
  
  def __bewegeExtra(self, dt: float):
    for extra in self.__extraSpriteGruppe:
      extra.bewegen(dt)
      extra.einschraenken(self.__screen.get_width())

  def __kollision(self):
    for laser in self.__alienLaserSpriteGruppe:
      # Wenn ein Laser von Alien Bunker soll der Laser und ein Teil des Bunker zerstört werden
      if pygame.sprite.spritecollide(laser,self.__bunkerSpriteGruppe,True):
        laser.kill()

      # Wenn ein Laser von einem Alien den Spieler trifft soll das Sprite vom Spieler nicht zerstört
      # werden der Laser schon und ein Leben des Spieler wird abgezogen
      if pygame.sprite.spritecollide(laser,self.__spielerSpriteGruppe,False):
        laser.kill()
        self.__derSpieler.treffer()
        if self.__derSpieler.getLeben() == 0:
          # Wenn der Spieler keine Leben hat Sound abspielen und zur nächsten Szene wechseln
          self.__spielerTodSound.play()
          self._wechselSzene = True

    for alien in self.__alienSpriteGruppe:
      # Wenn ein Alien einen Bunker berührt hat der Spieler es nicht geschaft die Welt zu beschützen
      if pygame.sprite.spritecollide(alien,self.__bunkerSpriteGruppe,False):
        self._wechselSzene = True

    for laser in self.__spielerLaserSpriteGruppe:
      # Wenn ein Laser vom Spieler, den Bunker trifft, soll nur der Laser zerstört werden
      if pygame.sprite.spritecollide(laser,self.__bunkerSpriteGruppe,False):
        laser.kill()
      
      # Wenn der Spieler das extra Leben trifft, soll der Laser zerstört und der Spieler geheilt werden
      if pygame.sprite.spritecollide(laser,self.__extraSpriteGruppe,True):
        self.__derSpieler.heilen()
        laser.kill()

      # Wenn ein Laser vom Spieler ein Alien trifft, soll das Alien und der Laser zerstört werden
      if pygame.sprite.spritecollide(laser,self.__alienSpriteGruppe,False):
        # Alle Alien die den Laser berühren werden in eine Liste gespeichert
        kollidierteAliens = pygame.sprite.spritecollide(laser,self.__alienSpriteGruppe,False)
        # ...
        for alien in kollidierteAliens:
          # Der Wert des Alien wird dem Score hinzugefügt
          self.__score += alien.getWert()
          # Lade und spiele Sound ab
          self.__alienTodSound.play()
          alien.kill()
        laser.kill()

      # Wenn ein Laser vom Spieler mit einem Laser vom Alien trifft, sollen beide zerstört werden
      if pygame.sprite.spritecollide(laser,self.__alienLaserSpriteGruppe,True):
        laser.kill()

  def getScore(self):
    return self.__score

  def beiUpdate(self, dt: float):

    if self.__derSpieler.schuss():
      self.__spielerLaserSpriteGruppe.add(Laser(self.__derSpieler.getLaserPostion(), -600.0))
      self.__shootSound.play()
    
    self.__derSpieler.bewegen(dt)
    self.__derSpieler.einschraenken(screenLaenge=self.__screen.get_width())

    self.__alienSchuss()
    self.__bewegeAliens(dt)

    for laser in self.__alienLaserSpriteGruppe:
      laser.bewegen(dt)
      laser.einschraenken(self.__screen.get_height())
    for laser in self.__spielerLaserSpriteGruppe:
      laser.bewegen(dt)
      laser.einschraenken(self.__screen.get_height())
    
    self.__kollision()
    self.__alienUebrig = len(self.__alienSpriteGruppe)

    self.__erstelleExtra()
    self.__bewegeExtra(dt)

    if self.__alienUebrig <= 0:
      self.__erstelleAliens(zeilen=6,spalten=8,startX=50, startY=100,xDistanz=20,yDistanz=20)
  
  def beiZeichne(self):
    self.__screen.blit(self.__hintergrund, (0,0))

    self.__spielerSpriteGruppe.draw(self.__screen)
    self.__spielerLaserSpriteGruppe.draw(self.__screen)

    self.__alienSpriteGruppe.draw(self.__screen)
    self.__alienLaserSpriteGruppe.draw(self.__screen)

    self.__extraSpriteGruppe.draw(self.__screen)

    self.__bunkerSpriteGruppe.draw(self.__screen)

    self.__dieGUI.zeichneText(f'Score: {self.__score}', 12, 100, int(self.__screen.get_height()*0.05), (255,255,255))
    self.__dieGUI.zeichneText(f'Leben: {self.__derSpieler.getLeben()}', 12, self.__screen.get_width()-100, int(self.__screen.get_height()*0.05), (255,255,255))
    pygame.display.flip()

class Benennung(Szene):
  def __init__(self, score: int):
    super().__init__()
    self.__screen = pygame.display.set_mode((600,800))
    
    self.__hintergrund = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()))
    self.__hintergrund.fill((0,0,0))

    self.__score = score
    self.__spielerName = ''

    self.__dieGUI = GUI(self.__screen)

  def getName(self):
    return self.__spielerName
  
  def getScore(self):
    return self.__score

  def beiEingabe(self, events: list):
    for event in events:
      if event.key == pygame.K_BACKSPACE:
        # Das letzte Zeichen (-1) wird weg gelassen/gelöscht
        self.__spielerName = self.__spielerName[:-1]
      
      elif event.key == pygame.K_RETURN and len(self.__spielerName) > 0:
        self._wechselSzene = True

      elif event.unicode != ' ' and not len(self.__spielerName) > 3:
        # Limitiere Spielername auf 3 Zeichen
        self.__spielerName += event.unicode

  def beiUpdate(self, dt: float):
    pass

  def beiZeichne(self):
    
    self.__screen.blit(self.__hintergrund, (0,0))

    self.__dieGUI.zeichneText(f'Bitte geben sie ihren Name ein!', 12, self.__screen.get_width()//2, self.__screen.get_height()//2-50, (255,255,255))
    self.__dieGUI.zeichneText(f'{self.__spielerName} : {self.__score}', 12, self.__screen.get_width()//2, self.__screen.get_height()//2, (255,255,255))

    pygame.display.flip()

class Score(Szene):
  def __init__(self, spielerListe):
    super().__init__()
    self.__screen = pygame.display.set_mode((600,700))
    self.__spielerListe = spielerListe
    self.__dieGUI = GUI(self.__screen)

    self.__zeichneHighScoreListe(self.__screen.get_width()//2, 100, 50)

    pygame.display.flip()

  def __zeichneHighScoreListe(self, startPosX, startPosY, offsetY):
    x = startPosX
    y = startPosY
    for i in range(9):
      if not i == 0:
        y += offsetY

      if len(self.__spielerListe)-1 >= i:
        self.__dieGUI.zeichneText(f'{i+1}. {self.__spielerListe[i][0]} : {self.__spielerListe[i][1]}', 12, x, y, (255,255,255))
      else:
        self.__dieGUI.zeichneText(f'{i+1}. ___ : ___', 12, x, y, (255,255,255))
    
    self.__dieGUI.zeichneRoundedButton('Retry Press Space', 8, self.__screen.get_width()//2, self.__screen.get_height()-30, 180, 20, 5, (255,255,255), (0,0,0))
  
  def beiEingabe(self, events: list):
    for event in events:
      if event.key == pygame.K_SPACE:
        self._wechselSzene = True

  def beiUpdate(self, dt: float):
    pass