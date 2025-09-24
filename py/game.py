import os
import sys
import pygame
from scripts.UI import Text
from scripts.utils import load_image, load_image_black
import random
from scripts.menu import Menu
from enum import Enum
from mac import mac_decides_your_fate, generate_mac_performance

class Moves(Enum):
    SHOOT = 1
    DUCK = 2
    STAND = 3

def randomize_bullets(round, game=None):
    # the round dictates the number of 1's in the player_bullets and enemy_bullets lists
    player_bullets = [1 if i < round else 0 for i in range(6)]
    enemy_bullets = [1 if i < round else 0 for i in range(6)]
    random.shuffle(player_bullets)
    random.shuffle(enemy_bullets)
    game.mac_live_rounds = round
    game.player_live_rounds = round
    return player_bullets, enemy_bullets

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Last Stand")
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_size = pygame.display.get_surface().get_size()
        self.display = pygame.Surface((1920, 1080))
        self.clock = pygame.time.Clock()
        self.playmenumus = True

        self.level = 3
        self.round = 0

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
            'blue': load_image("UI/blue.png"),
            'red': load_image("UI/red.png"),
            'yellow': load_image("UI/yellow.png"),
            # game assets
            'background': load_image('backgrounds/background.png'),
            'round_background': load_image('backgrounds/round_background.png'),
        }

        self.sfx = {
            'title': pygame.mixer.Sound('data/sfx/title_drop.wav'),
            'intro': pygame.mixer.Sound('data/sfx/GBU.wav'),
            'load': pygame.mixer.Sound('data/sfx/load5.wav'),
        }
        
        self.audio = 3

        # bullets
        self.player_bullets = [] # max 6 bullets
        self.enemy_bullets = [] # max 6 bullets

        self.chamber_loaded = False

        self.mac_correct_predictions = 0


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
    
    def load_chamber(self):
        # loads a chamber based on the level number
        BASE_IMG_PATH = 'data/images/load/'
        for i in range(0, self.level):
            self.sfx['load'].play()
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

        self.player_bullets, self.enemy_bullets = randomize_bullets(self.level, game=self)
        return
    
    def recap(self, result):
        # result is a string, either "win" or "lose"
        self.display.blit(self.assets['background'], (0, 0))

        # get the graph to display from the folder on the left side of the screen
        graph = load_image(f'mac_performance.png')
        self.display.blit(pygame.transform.scale(graph, (800, 600)), (560, 200))

        # display win or lose text in center of screen
        if result == "win":
            result_text = Text('You Win!', (850, 100))
            result_text.render(self.display, 100, (0, 255, 0))
        else:
            result_text = Text('You Lose!', (850, 100))
            result_text.render(self.display, 100, (255, 0, 0))

        # display the number of times Mac predicted correctly
        prediction_text = Text(f'Mac Predicted Correctly: {self.mac_correct_predictions} out of {self.round} rounds', (600, 850))
        prediction_text.render(self.display, 40, (255, 255, 255))
        self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])

        # tell them to press escape to return to main menu
        info_text = Text('Press ESC to return to Main Menu', (650, 950))
        info_text.render(self.display, 40, (255, 255, 255))
        self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main_menu()
        return
    
    def run_game_loop(self):
        self.round += 1
        self.show_round = True

        # mac logic and tie breaker
        self.player_shoots = 0
        self.mac_shoots = 0
        self.player_live_rounds = 0
        self.mac_live_rounds = 0
        self.player_move_history = []

        self.player_should_make_move = True
        self.mac_should_make_move = True

        self.mac_move = None
        self.mac_prediction = None

        self.mac_can_kill =  False
        self.player_can_kill = False

        self.player_STOOD = False
        self.mac_STOOD = False

        while True:
            # load the chamber only once per round
            if self.chamber_loaded == False:
                self.load_chamber()
                self.chamber_loaded = True
                # self.level -= 1 @TODO: DO THIS WHEN ROUND ENDS IN VICTORY

            self.display.fill((0, 0, 0))
            # Scale the round background to fit the display surface
            self.display.blit(pygame.transform.scale(self.assets['round_background'], (self.display.get_width(), self.display.get_height())), (0, 0))

            if self.show_round == True:
                round_text = Text(f'Live Rounds {self.level}', [690, 100])
                round_text.render(self.display, 100, (255, 255, 255))


            if len(self.player_bullets) > 0:
                # player shot all his bullets
                # Player Wins
                self.recap("win")
                return
            if len(self.enemy_bullets) > 0:
                # mac shot all his bullets
                # Player Loses
                self.recap("lose")
                return

            if self.mac_STOOD == True:
                # player loses their turn and mac shoots automatically
                self.mac_shoots += 1
                if self.enemy_bullets[0] == 0:
                    self.enemy_bullets.pop(0)
                if self.enemy_bullets[0] == 1:
                    self.enemy_bullets.pop(0)
                    self.mac_live_rounds -= 1
                    self.mac_can_kill = True

                    # player dies
                    # TODO show animation
                    self.recap("lose")

            if self.player_STOOD == True:
                # mac loses their turn and player shoots automatically
                self.player_shoots += 1
                if self.player_bullets[0] == 0:
                    self.player_bullets.pop(0)
                if self.player_bullets[0] == 1:
                    self.player_bullets.pop(0)
                    self.player_live_rounds -= 1
                    self.player_can_kill = True

                    # mac dies
                    # TODO show animation
                    self.recap("win")



            if self.mac_should_make_move == True:
                self.mac_move, self.mac_prediction = mac_decides_your_fate(self.round, self.level, self.player_shoots, self.mac_shoots, self.player_live_rounds, self.mac_live_rounds, self.player_move_history)
                self.mac_should_make_move = False

            # signal for player to make a move
            if self.player_should_make_move == True:
                info_text = Text('Make Your Move', (800, 200))
                info_text.render(self.display, 60, (255, 255, 255))
                self.display.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])


            # TODO depending on move show animation and also calculate outcome
            if self.player_should_make_move == False and self.mac_should_make_move == False:
                # both players have made their moves, calculate outcome
                self.player_should_make_move = True
                self.mac_should_make_move = True

                if self.mac_prediction == self.player_move_history[-1]:
                    self.mac_correct_predictions += 1

                if self.mac_move == Moves.SHOOT:
                    self.mac_shoots += 1
                    if self.enemy_bullets[0] == 0:
                        self.enemy_bullets.pop(0)
                    if self.enemy_bullets[0] == 1:
                        self.enemy_bullets.pop(0)
                        self.mac_live_rounds -= 1
                        self.mac_can_kill = True

                if self.player_move_history[-1] == Moves.SHOOT:
                    self.player_shoots += 1
                    if self.player_bullets[0] == 0:
                        self.player_bullets.pop(0)
                    if self.player_bullets[0] == 1:
                        self.player_bullets.pop(0)
                        self.player_live_rounds -= 1
                        self.player_can_kill = True

                if self.mac_move == Moves.SHOOT and self.player_move_history[-1] == Moves.SHOOT:
                    # both players shoot, both lose
                    self.recap("lose")
                    return
                elif self.mac_move == Moves.SHOOT and self.player_move_history[-1] == Moves.DUCK:
                    # mac shoots, player ducks, mac loses
                    # show animation
                    return
                elif self.mac_move == Moves.SHOOT and self.player_move_history[-1] == Moves.STAND:
                    self.player_STOOD = True
                    # mac shoots, player stands, player loses
                    if self.mac_can_kill == True:
                        # mac stands, player shoots, mac loses
                        self.recap("lose")
                    else:
                        # mac shoots, player stands, nothing happens
                        pass
                    return
                elif self.mac_move == Moves.DUCK and self.player_move_history[-1] == Moves.SHOOT:
                    # mac ducks, player shoots, player loses
                    # show animation
                    return
                elif self.mac_move == Moves.DUCK and self.player_move_history[-1] == Moves.DUCK:
                    # both duck, nothing happens
                    pass
                elif self.mac_move == Moves.DUCK and self.player_move_history[-1] == Moves.STAND:
                    # mac ducks, player stands, nothing happens
                    self.player_STOOD = True
                    pass
                elif self.mac_move == Moves.STAND and self.player_move_history[-1] == Moves.SHOOT:
                    self.mac_STOOD = True
                    if self.player_can_kill == True:
                        # mac stands, player shoots, mac loses
                        self.recap("win")
                        return
                    else:
                        # mac stands, player shoots, nothing happens
                        pass
                elif self.mac_move == Moves.STAND and self.player_move_history[-1] == Moves.DUCK:
                    # mac stands, player ducks, nothing happens
                    self.mac_STOOD = True
                    pass
                elif self.mac_move == Moves.STAND and self.player_move_history[-1] == Moves.STAND:
                    # both stand, nothing happens
                    pass 
                self.mac_can_kill = False
                self.player_can_kill = False

                
                

            # display shoot, duck, stand buttons, on the right side of the screen
            shoot_button = self.assets['blue']
            duck_button = self.assets['red']
            stand_button = self.assets['yellow']
            self.display.blit(pygame.transform.scale(shoot_button, (shoot_button.get_width() * 1.5, shoot_button.get_height() * 1.5)), (1500, 300))
            self.display.blit(pygame.transform.scale(duck_button, (duck_button.get_width() * 1.5, duck_button.get_height() * 1.5)), (1500, 500))
            self.display.blit(pygame.transform.scale(stand_button, (stand_button.get_width() * 1.5, stand_button.get_height() * 1.5)), (1500, 700))
            shoot_text = Text('Shoot (C)', (1600, 330))
            duck_text = Text('Duck (V)', (1600, 530))
            stand_text = Text('Stand (B)', (1600, 730))
            shoot_text.render(self.display, 40, color=(0, 0, 0))
            duck_text.render(self.display, 40, color=(0, 0, 0))
            stand_text.render(self.display, 40, color=(0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()
                    if self.player_should_make_move == True:
                        if event.key == pygame.K_c:
                            self.player_move_history.append(Moves.SHOOT)
                            self.player_shoots += 1
                            self.player_should_make_move = False
                        if event.key == pygame.K_v:
                            self.player_move_history.append(Moves.DUCK)
                            self.player_should_make_move = False
                        if event.key == pygame.K_b:
                            self.player_move_history.append(Moves.STAND)
                            self.player_should_make_move = False


            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
            pygame.display.update()
            pygame.time.delay(2000)
            return

    def run(self):
        # start of the game
        self.intro_played = False
        self.title_drop = False

        for i in self.sfx.values():
            i.set_volume(self.audio * 0.2)  # Set volume based on audio level (0 to 1 scale)

        while True:
            self.display.fill((0, 0, 0))
            if self.intro_played == False:
                self.sfx['intro'].play()
                self.intro()
                self.intro_played = True
                self.sfx['title'].stop()
            self.display.blit(self.assets['background'], (0, 0))
            if self.title_drop == False and self.intro_played == True:
                pygame.time.delay(1000)
                self.sfx['title'].play()
                self.title = Text('Last Stand', [720, 200])
                self.title.render(self.display, 120, (255, 255, 255))
                self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
                pygame.display.update()
                pygame.time.delay(2000)
                self.title_drop = True

            # bullets are shuffled in load_chamber
            # i guess all TODO: implement visual buttons on screen for controls
            # C to shoot, V to reload, B to Duck, N to remain standing

            # first ask Mac what he (the gighachad) wants to do

            self.run_game_loop()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()
                    if event.key == pygame.K_c:
                        print("shoot")
                    if event.key == pygame.K_v:
                        print("reload")
                    if event.key == pygame.K_b:
                        print("duck")
                    if event.key == pygame.K_n:
                        print("stand")

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), [0,0])
            pygame.display.update()
            self.clock.tick(60)
# returns the game then runs it
Game().main_menu()