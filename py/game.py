import os
import sys
import pygame
from scripts.UI import Text
from scripts.utils import load_image, load_image_black
import random
from scripts.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Last Stand")
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_size = pygame.display.get_surface().get_size()
        self.display = pygame.Surface((1920, 1080))
        self.clock = pygame.time.Clock()
        self.playmenumus = True

        self.assets = {
            # menu assets
            'W': load_image('UI/W.png'),
            'A': load_image('UI/A.png'),
            'S': load_image('UI/S.png'),
            'D': load_image('UI/D.png'),
            'ESC': load_image('UI/ESC.png'),
            'click': load_image('UI/click.png'),
            'button': load_image('UI/bullet.png'),
            "main_menu_bg": load_image_black("main/LastStand_MainMenu.png"),
            "gun": load_image("UI/gun.png"),
            "select": load_image("UI/select.png"),
            "sound": load_image("UI/sound.png"),
            # game assets
            'background': load_image('backgrounds/background.png'),
        }

        self.audio = 0


    def main_menu(self):
        self.selected = 0 # tracks which menu item is selected

        while True:
            self.display.fill((255, 255, 255))

            bg = self.assets['main_menu_bg']
            bg_width, bg_height = bg.get_width(), bg.get_height()
            disp_width, disp_height = self.display.get_width(), self.display.get_height()
            bg_x = (disp_width - bg_width) // 1
            bg_y = (disp_height - bg_height) // 1
            self.display.blit(bg, (bg_x, bg_y))

            # Title
            self.title = Text('Last Stand', [720, 200])
            self.title.render(self.display, 120, (255, 255, 255))

            # Start button
            self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)), (850, 485))
            start_text = Text('Start', (900, 510))
            start_text.render(self.display, 50, color=(0, 0, 0))
            start_rect = pygame.Rect(850, 485, self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)

            # Audio Control button
            self.display.blit(pygame.transform.scale(self.assets['sound'], (self.assets['sound'].get_width() * 1, self.assets['sound'].get_height() * 1)), (600, 635))
            self.display.blit(pygame.transform.scale(self.assets['gun'], (self.assets['gun'].get_width() * 1.75, self.assets['gun'].get_height() * 1.75)), (650, 635))
            # Audio Level, a Bullet image is used to represent audio levels
            if self.audio == 0:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (870, 660))
            elif self.audio == 1:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (910, 660))
            elif self.audio == 2:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (950, 660))
            elif self.audio == 3:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (990, 660))
            elif self.audio == 4:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (1030, 660))
            

            # Quit button
            self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)), (850, 785))
            quit_text = Text('Quit', (910, 810))
            quit_text.render(self.display, 50, color=(0, 0, 0))

            # display the selector next to the selected option
            if self.selected == 0:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 455))
            elif self.selected == 1:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 605))
            elif self.selected == 2:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 775))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % 3
                    elif event.key == pygame.K_LEFT and self.selected == 1:
                        # Decrease audio level
                        self.audio = max(0, self.audio - 1)
                    elif event.key == pygame.K_RIGHT and self.selected == 1:
                        # Increase audio level
                        self.audio = min(4, self.audio + 1)
                    elif event.key == pygame.K_x:
                        if self.selected == 0:
                            self.run()
                        elif self.selected == 1:
                            pass  # Audio level is adjusted with left/right keys
                        elif self.selected == 2:
                            pygame.quit()
                            sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        self.run()

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
            pygame.display.update()
            self.clock.tick(60)

    def intro(self):
        # run through the intro sequence in the intro folder
        BASE_IMG_PATH = 'data/images/intro/'
        for i in range(0, len(os.listdir(f"{BASE_IMG_PATH}"))):
            img = pygame.image.load(BASE_IMG_PATH + f"frame{str(i).zfill(4)}.png").convert()
            self.display.blit(pygame.transform.scale(img, (1920, 1080)), (0, 0))
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
            pygame.display.update()
            pygame.time.delay(150) 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main_menu()

        return
    
    def load_chamber(self, level):
        # loads a chamber based on the level number
        BASE_IMG_PATH = 'data/images/load/'
        for i in range(0, self.level):
            for i in range(0, len(os.listdir(f"{BASE_IMG_PATH}"))):
                img = pygame.image.load(BASE_IMG_PATH + f"frame{str(i).zfill(4)}.png").convert()
                self.display.blit(pygame.transform.scale(img, (1920, 1080)), (0, 0))
                self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
                pygame.display.update()
                pygame.time.delay(100) 
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()
        return

    def run(self):
        # start of the game
        self.intro_played = False
        self.title_drop = False
        self.chamber_loaded = False

        self.level = 3

        while True:
            self.display.fill((0, 0, 0))
            if self.intro_played == False:
                self.intro()
                self.intro_played = True
            self.display.blit(self.assets['background'], (0, 0))
            if self.title_drop == False and self.intro_played == True:
                pygame.time.delay(1000)
                self.title = Text('Last Stand', [720, 200])
                self.title.render(self.display, 120, (255, 255, 255))
                self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
                pygame.display.update()
                pygame.time.delay(2000)
                self.title_drop = True
            if self.chamber_loaded == False:
                self.load_chamber(self.level)
                self.chamber_loaded = True
                self.level -= 1


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
            pygame.display.update()
            self.clock.tick(60)
# returns the game then runs it
Game().main_menu()