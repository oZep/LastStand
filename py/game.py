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
            self.display.blit(pygame.transform.scale(self.assets['gun'], (self.assets['gun'].get_width() * 1.75, self.assets['gun'].get_height() * 1.75)), (650, 635))
            # Audio Level, a Bullet image is used to represent audio levels
            if self.audio == 0:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (860, 660))
            elif self.audio == 1:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (900, 660))
            elif self.audio == 2:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (940, 660))
            elif self.audio == 3:
                self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 0.3, self.assets['button'].get_height() * 0.3)), (980, 660))

            # Quit button
            self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)), (850, 785))
            quit_text = Text('Quit', (910, 810))
            quit_text.render(self.display, 50, color=(0, 0, 0))
            quit_rect = pygame.Rect(850, 785, self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)

            # display the selector next to the selected option
            if self.selected == 0:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 485))
            elif self.selected == 1:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 635))
            elif self.selected == 2:
                self.display.blit(pygame.transform.scale(self.assets['select'], (self.assets['select'].get_width() * 0.05, self.assets['select'].get_height() * 0.05)), (1200, 785))


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
                        self.audio = min(3, self.audio + 1)
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

    def controls(self):
        while True:
            self.display.fill((255, 255, 255))

            self.display.blit(pygame.transform.scale(self.assets['button'], (self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)), (850, 785))
            back_text = Text('Back', (920, 809))
            back_text.render(self.display, 50, color=(0, 0, 0))
            back_rect = pygame.Rect(850, 785, self.assets['button'].get_width() * 1.75, self.assets['button'].get_height() * 1.75)

            mpos = pygame.mouse.get_pos() # gets mouse positon
            mpos = (mpos[0] / (self.screen_size[0]/self.display.get_width()), mpos[1] / (self.screen_size[1]/self.display.get_height())) # since screen sometimes scales
            self.display.blit(pygame.transform.scale(self.assets['target'], (32, 32)), (mpos[0], mpos[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # have to code the window closing
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_rect.collidepoint(mpos):
                            self.sfx['select'].play(0)
                            self.main_menu()
                if event.type == pygame.KEYDOWN:
                    def run(self):
                        # Blank window game loop
                        while True:
                            self.display.fill((255, 255, 255))
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
                    if self.dead and event.key == pygame.K_RETURN:
                        self.sfx['select'].play(0)
                        self.sfx['select'].play(0)
                        self.run()
                    if event.key == pygame.K_a: # referencing right and left arrow keys
                        self.movement[0] = True
                    elif event.key == pygame.K_d: 
                        self.movement[1] = True
                    elif event.key == pygame.K_w:
                        self.movement[2] = True
                    elif event.key == pygame.K_s:
                        self.movement[3] = True
                    self.has_moved = True
                if event.type == pygame.KEYUP: # when key is released
                    if event.key == pygame.K_a: 
                        self.movement[0] = False
                    elif event.key == pygame.K_d: 
                        self.movement[1] = False
                    elif event.key == pygame.K_w:
                        self.movement[2] = False
                    elif event.key == pygame.K_s:
                        self.movement[3] = False
                
            if self.movement[1] - self.movement[0] == 0 and self.movement[3] - self.movement[2] == 0 or self.dead:
                self.slowdown = True
            else:
                self.slowdown = False
            

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), screenshake_offset)
            pygame.display.update()
            self.deltatime = self.clock.tick(60) # run at 60 fps, like a sleep

# returns the game then runs it
Game().main_menu()