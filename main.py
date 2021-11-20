import pygame
from pygame.version import PygameVersion
import os
from random import randint
import sys

#Einstellungen von PyGame
class settings:
    window_width =1000
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image= os.path.join(path_file,"images")
    fps=60
    caption = "Meteoritenschauer"
    nof_meteors = 15
    points=0
    lifes=3

#Background Klasse
class background:
    def __init__(self,filename="background.png"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert()
        self.image = pygame.transform.scale(self.image,(settings.window_width,settings.window_height))


    def draw(self,screen):
        screen.blit(self.image,(0,0))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        points_text=font.render(f"Points:{settings.points}",1,(255,255,255))
        lifes_text=font.render(f"Lifes:{settings.lifes}",1,(255,255,255))
        screen.blit(points_text,(10,10))
        screen.blit(lifes_text,(10,50))

#Alien sprite klasse
class alien(pygame.sprite.Sprite):
    def __init__(self,picturefile) -> object:
        super().__init__()
        self.image=pygame.image.load(os.path.join(settings.path_image,picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect=self.image.get_rect()
        #Alien spawn
        self.rect.left=400
        self.rect.top=600
        self.speed_h = 0
        self.speed_v = 0

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.rect.right + self.speed_h > settings.window_width:       # Läuft rechts raus
            self.speed_h *= 0
        if self.rect.bottom + self.speed_v > settings.window_height:     # Läuft unten raus
            self.speed_v *= 0
        if self.rect.left + self.speed_h < 0:            # Läuft links raus
            self.speed_h *= 0
        if self.rect.top + self.speed_v < 0:             # Läuft oben raus
            self.speed_v *= 0
        self.rect.move_ip((self.speed_h, self.speed_v))

    def stop(self):
        self.speed_v = self.speed_h = 0

    def down(self):
        self.speed_v = 6

    def up(self):
        self.speed_v = -6

    def left(self):
        self.speed_h = -6

    def right(self):
        self.speed_h = 6

#Meteorit sprite klasse
class meteorit(pygame.sprite.Sprite):
    def __init__(self,filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150))
        self.rect=self.image.get_rect()
        #Zufälliger meteoriten spawn
        self.rect.centerx=randint(10,990)
        self.rect.centery=randint(-990,-10)
        self.directiony=1
        #Zufalls Geschwindigkeit
        self.speed=randint(1,10)
        #Zufalls Größe
        scale_ratio = randint(2, 6) / 4
        self.image = pygame.transform.scale(self.image, ( int(self.image.get_rect().width * scale_ratio),int(self.image.get_rect().height * scale_ratio)))

    def draw(self,screen):
        screen.blit(self.image_1,self.rect)

    def update(self):
        self.rect.move_ip(0,self.directiony * self.speed)
        if self.rect.top >= settings.window_height:
            self.rect.centerx = randint(0,settings.window_width)
            self.rect.centery = randint(0,0)
            settings.points = settings.points + 1

#Game Klasse
#Diese Klasse verwaltet alle Komponenten und Logiken des Spiels.
class Game(object):
    def __init__(self,)-> None:
        super().__init__()
        #Fenster größe
        os.environ['SDL_VIDEO_WINDOW_POS'] = "380,100"
        pygame.init()
        pygame.display.set_caption(settings.caption)
        self.screen=pygame.display.set_mode((settings.window_width,settings.window_height))
        self.clock=pygame.time.Clock()
        self.background= background()
        self.meteorit=meteorit("meteorit.png")
        self.alien=alien("alien.png")
        self.all_meteor=pygame.sprite.Group()
        self.all_meteor.add(self.meteorit)



        self.running= False

#Spielstart
    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            self.check_for_collision()


        pygame.quit()

    #Tastatur event und andere events
    def watch_for_events(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.alien.down()
                elif event.key == pygame.K_UP:
                    self.alien.up()
                elif event.key == pygame.K_LEFT:
                    self.alien.left()
                elif event.key == pygame.K_RIGHT:
                    self.alien.right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.alien.stop()
                elif event.key == pygame.K_UP:
                    self.alien.stop()
                elif event.key == pygame.K_LEFT:
                    self.alien.stop()
                elif event.key == pygame.K_RIGHT:
                    self.alien.stop()

#Aktualisiert die Sprites und  andere Spielkomponenten.
    def update(self):
        self.check_for_collision()
        self.alien.update()
        self.all_meteor.update()

    
    def start(self):
        self.background= background()

        for a in range(settings.nof_meteors):
           self.all_meteor.add(meteorit ("meteorit.png"))
    

#Kollisions kontrolle
    def check_for_collision(self):
        self.alien.hit = False
        for s in self.all_meteor:
            if pygame.sprite.collide_mask(s,self.alien):
                self.alien.hit = True
                break
        if self.alien.hit:
            self.alien.rect.top =600
            self.alien.rect.left=400
            settings.lifes -= 1
            for self.nof_meteors in self.all_meteor.sprites():
                    self.all_meteor.remove(self.all_meteor)
                    for a in range(settings.nof_meteors):
                        self.all_meteor.add(meteorit("meteorit.png"))
                        if settings.lifes <= 0:
                            settings.lifes = 3
                            settings.points = 0

#Zeichnet alle Bitmaps auf dem Bildschirm.
    def draw(self):
        self.background.draw(self.screen)
        self.all_meteor.draw(self.screen)
        self.alien.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':

    game = Game()
    game.run()

        
