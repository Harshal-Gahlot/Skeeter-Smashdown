"""  TO DO LIST:        # means done
1. END SCREEN BG
2. HOW TO PLAY BG
3. HOW TO PLAY SCRIPT
4. SETTING MUSIC - a) Music bar pointer image
                   # b) Follow curser
                   # c) Pointer stay in limited area
                   # d) Music bar actually affect volume
                   e) setting music BG
                   f) mute button
                   g) mute button affect music bar and visa verse
5. FIX ANY BUG 

FIxES DONE:

"""

import pygame, sys, random, time
#from debug import Debug   

print("""\nHey, Skeeter Smashdown should start in about 2-5 seconds please wait! 
Starting for first time may take more seconds to lode!\n""")
t = time.perf_counter()

# ---- Mosquitos Class ---- #
class Mosquitos(pygame.sprite.Sprite):
    def __init__(self, img_list):
        super().__init__()
        height = HEIGHT/3 if night <5 else HEIGHT
        self.x_pos = random.randint(30, WIDTH - 30)
        self.y_pos = random.randint(HEIGHT - height, HEIGHT - 20) - HEIGHT
        self.speed = self.y_pos         # so that mos goes from where they are created from and not from
                                        # top of screen or stuck where they are born
        self.img_list = img_list
        self.image = pygame.transform.rotozoom(self.img_list[0], 0, 0.1)
        self.img_index = 0                  # for animating imgs in list
        self.init_speed = 50 + ((night)**2)  # /2 can be added for avg easy 26-27 maybe

        self.init_speed = 3*self.init_speed/5 if self.img_list == mos1_list else self.init_speed if self.img_list == mos2_list else 7*self.init_speed/5
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos) # Give img pos(x, y) which we earlier got randomly
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):        # This fun updates and gives speed & animation to diff Mosquitos
        if (self.rect.centery < HEIGHT - HEIGHT//10):
                self.img_index += dt * (15  + night)     # animation speed
                if self.img_index >= 4: self.img_index = 0

                self.image = self.img_list[int(self.img_index)]    # change img 
                
                self.image = pygame.transform.rotozoom(self.image, 0, 0.1)    # resize
                self.speed += dt * self.init_speed 
                self.rect.centery = round(self.speed)    # Lets mosquito go down/ towards people area

        else:
            self.rect.centery = HEIGHT - HEIGHT/10

# ---- Maintains racket's non killing part Class (Parent Class of below class) ---- #
class Racket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/images/empty_racket.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

# ---- Maintains racket's killing part Class ---- #
class Kill_Part(Racket, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/images/main_racket.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.6)

    def update(self):
        super().update()
        self.mask = pygame.mask.from_surface(self.image)

# ---- Buttons Class ---- #
class ButtonsClass():
    def __init__(self, button_text: str, pos: tuple, size:tuple, color: hex, bg_color: hex = (15,15,15),
border = (0,0,0,0), hover_color:hex = (15,15,15), hover_bg_color: hex = (0,255,200), clicked_color: hex = (255,255,0)):
        # makeing below var available ButtonFun function
        self.button_text = button_text
        self.pos = pos
        self.color = color

        self.hover_bg_color = hover_bg_color
        self.hover_color = hover_color
        self.bg_color = self.bg_color_copy = bg_color
        self.clicked_color = clicked_color
        self.press = False

        if border == 'circle': self.TLB, self.TRB, self.BLB, self.BRB = 200,200,200,200
        elif border is None: self.TLB, self.TRB, self.BLB, self.BRB = 0,0,0,0
        else: self.TLB, self.TRB, self.BLB, self.BRB = border

        # button bg color
        self.button_bg = pygame.Rect(pos, size)
        self.button_bg.center = pos

        # button text
        self.button = gamic_font.render(self.button_text, True, self.color)
        
    def ButtonFun(self):
        # Check if hover and further check if clicked
        if self.button_bg.collidepoint(pygame.mouse.get_pos()):     
            # check if user clicked button or not
            clicked = False
            if pygame.mouse.get_pressed()[0]:
                bg_color = self.clicked_color
                self.press = True
            else:
                bg_color = self.hover_bg_color
                if self.press:
                    self.press = False
                    clicked = True 

            self.button = big_gamic_font.render(self.button_text, True, self.hover_color)
            self.button_rect = pygame.Rect(self.pos, self.button.get_size())
            self.button_rect.center = self.pos

            # display text and back color
            pygame.draw.rect(screen, bg_color, self.button_bg, 0, -1, self.TLB, self.TRB, self.BLB, self.BRB)
            screen.blit(self.button, self.button_rect)
            return True, clicked  

        # if not hover
        else:
            self.press = False
            self.button = gamic_font.render(self.button_text, True, self.color)
            self.button_rect = pygame.Rect(self.pos, self.button.get_size())
            self.button_rect.center = self.pos

            # display text and back color
            pygame.draw.rect(screen, self.bg_color, self.button_bg, 0, -1, self.TLB, self.TRB, self.BLB, self.BRB)
            screen.blit(self.button, self.button_rect)
            return False, False

# ---- Main Game Class ---- #
class Main_Game():
    def __init__(self):
        '''Set menu as stage and play menu song when game started '''
        self.stage = 'menu'
        self.move_over_bg_timer = 0
        self.x,self.y = -5, -5
        self.press = False
        self.changing_vol = False
        self.pre_music_x = WIDTH/2
        self.any_shown = False
        self.show_setting = False
        self.show_how2play = False
        self.show_about = False
        self.show_modes = False
        menu_song.play(-1)

    def Menu(self):
        '''Game menu. Show game name and game modes'''
        self.any_shown = (True if (self.show_modes or self.show_about or 
                                   self.show_how2play or self.show_setting) else False)
        
        if self.any_shown:
            
            if self.show_modes:
                if easy_mode_button.ButtonFun()[1]: init_game_var("easy_mode")
                elif normal_mode_button.ButtonFun()[1]: init_game_var("normal_mode")
                elif hardcore_mode_button.ButtonFun()[1]: init_game_var("hardcore_mode")
            elif self.show_setting: 
                if (music_black_bg_rect.collidepoint(pygame.mouse.get_pos()) and
                    pygame.mouse.get_pressed()[0]): self.changing_vol = True
                else : self.changing_vol = False

                if self.changing_vol and pygame.mouse.get_pressed()[0]:
                    screen.blit(self.bg_surf_of_music_slider, self.bg_rect_of_music_slide)
                    screen.blit(music_bar, music_bar_rect)
                    screen.blit(music_black_bg, music_black_bg_rect)

                    music_black_bg_rect.centerx = (pygame.mouse.get_pos()[0] if pygame.mouse.get_pos()[0] 
                                    in range(WIDTH//4, WIDTH*3//4) else self.pre_music_x)
                    self.pre_music_x = music_black_bg_rect.centerx

                    music_vol = round( ((music_black_bg_rect.centerx - music_bar_rect.left)/(WIDTH//2)), 2)
                    set_music_vol(music_vol)
                    
            if back_button.ButtonFun()[1]:      
                self.show_setting = False
                self.show_about = False
                self.show_how2play = False
                self.show_modes = False
        
        else:
            screen.blit(menu_image1, (0, 0))
            screen.blits(((game_title1, game_title_rect1),(game_title2, game_title_rect2)))

            if show_modes_button.ButtonFun()[1]: self.show_modes = True
            elif about_button.ButtonFun()[1] :
                self.show_about = True
                screen.blit(how2play_image, (-518,0))
                screen.blit(about_title, (WIDTH/2 - about_title.get_width()/2, HEIGHT/6 - H(about_title)/2))
                screen.blits((about_content_surf_rect[i], (WIDTH/2 - about_content_surf_rect[i].get_width()/2,
                                                    HEIGHT/3  + (i * 50))) for i in range(len(about_list)) )
            elif how2play_button.ButtonFun()[1]:
                self.show_how2play = True
                screen.blit(how2play_image, (-518,0))
                how2play_text, how2play_rect = get_surf_and_rect("HOW TO PLAY",cut_font, (WIDTH/2, HEIGHT/6 - H(about_title)/2), (128,0,128))
                screen.blit(how2play_text, how2play_rect)
                screen.blits((about_content_surf_rect[i], (WIDTH/2 - about_content_surf_rect[i].get_width()/2,
                                                    HEIGHT/3  + (i * 50))) for i in range(len(about_list)) )
            elif setting_button.ButtonFun()[1]:
                self.bg_surf_of_music_slider,self.bg_rect_of_music_slide = get_surf_and_rect(False,(WIDTH/2 + music_black_bg.get_width()+10, H(music_black_bg)+10), (WIDTH/2, HEIGHT/2),((128,0,0)))
                self.show_setting = True
                screen.fill((128,0,0))
                screen.blit(music_text, music_text_rect)
                screen.blit(music_bar, music_bar_rect)
                screen.blit(music_black_bg, music_black_bg_rect)

    def Running(self):
        '''When Game is Running, Nothing else'''        
        global night, score, fps

        # check if all Mosquitos dead
        if len(mos_group) == 0:
            night += 1
            next_night_sound.play()
            # add new and diff types of Mosquitos to mos group
            for mos in range(1, 8 + (night)):
                if   mos <= ( (8 + night) // 2) :     img_list = mos1_list   # adding green mos
                elif mos <= ( (8 + night) // 4) * 3 : img_list = mos3_list   # adding red mos
                else :                               img_list = mos2_list   # adding orange mos
                self.mosquito = Mosquitos(img_list)
                mos_group.add(self.mosquito)

        # checkes for collision between mouse and Mosquitos
        for mos in mos_group:
            if pygame.sprite.collide_mask(kill_part, mos):
                mos.kill()
                random.choice([mos_sound1, mos_sound2]).play() # play kill soung
                score  += 1 

        if fps == FPS: fps = 0       # used in mos animation fun
        else: fps += 1

        # updates night, score and health bat message for showing
        self.night_text = text_font.render(f"NIGHT {night}", True, RUN_NIGHT_TEXT_COLOR).convert_alpha()
        self.score_text = text_font.render(f"{score} KILLS", True, "RED").convert_alpha()

        health_bar = pygame.Surface((lives, 5)).convert_alpha()
        health_bar.fill(health_bar_color)

        # running2 = pygame.image.load("assets/images/SELECTED(BG)/running2.webp")
        # blit/show bg_color, prople area, night, score, mos, racket on screen
        if self.running_bg_y >= -100: self.running_bg_direction = -1
        elif self.running_bg_y <= -300: self.running_bg_direction = 1
        self.running_bg_y += dt * 100 * random.randint(2,10)/10 * self.running_bg_direction

        if not fps % 10:
            if self.running_bg_angle <= -5: self.rotation_direction = 1
            elif self.running_bg_angle >= 5: self.rotation_direction = -1
            self.running_bg_angle += dt * 50 * self.rotation_direction

        running_rect = pygame.Rect(round(self.running_bg_y), round(self.running_bg_angle), WIDTH, HEIGHT)

        screen.blit(running, running_rect) 

        racket_group.draw(screen)
        racket_group.update()

        kill_part_group.draw(screen)
        kill_part_group.update()
        
        screen.blits(((people_area, people_rect),
            (self.night_text, (25, HEIGHT - 45)),
            (self.score_text, (WIDTH - 10 - self.score_text.get_width(), HEIGHT - 45))))
        
        mos_group.draw(screen)
        mos_group.update()
        
        screen.blit(health_bar, (WIDTH/2 - health_bar.get_width()/2, HEIGHT - H(health_bar)))

    def Game_over(self):
        '''Game over screen. And try again and menu buttons'''
        self.move_over_bg_timer += dt
        
        if self.move_over_bg_timer >= 1:
            self.x,self.y = self.x*-1, self.y*-1
            self.move_over_bg_timer = 0
        screen.blit(menu_image11, (self.x,-self.y))

        screen.blits(((game_over_text, game_over_rect), (self.score_text, 
        (WIDTH/2 - self.score_text.get_width()/2, HEIGHT * 0.5 - H(self.score_text)/2)),
        (self.night_text, (WIDTH/2 - self.night_text.get_width()/2, HEIGHT * 0.4 - H(self.night_text)/2))))

        if try_again_button.ButtonFun()[1]: init_game_var(cur_mode)
        elif menu_button.ButtonFun()[1]: 
            self.stage = "menu"
            menu_song.play(-1)

    def Check_mos(self):   #Check_event(self):
        '''checks if Mosquitos reached peoples area, if True the reduce health 
        and also checks if game's over, if return True then, init set-up for game over stage'''
        global lives, mos_group
        for mos in mos_group:
            if mos.rect.colliderect(people_rect): # (mos_group.spritedict.values()):
                lives -= 50 * dt
                if lives < 0:
                    music.stop()
                    game_over_sound.play()

                    self.night_text = cut_font.render(f"NIGHT {night}", True, OVER_NIGHT_TEXT_COLOR).convert_alpha()
                    self.score_text = cut_font.render(f"{score} KILLS", True, "RED").convert_alpha()

                    pygame.mouse.set_visible(True)
                    mos_group.empty()

                    self.stage = "game_over"
                    return False
        return True

    def Current_screen(self):
        '''Display the correct state/stage of game'''
        if self.stage.lower() == "running" and self.Check_mos(): 
            self.Running()
            menu_song.stop()
        elif self.stage.lower() == "menu":      self.Menu()
        elif self.stage.lower() == "game_over": self.Game_over()

# I created this function because I am little lazy && little smart:) (or am I)
def H(surface):
    '''Short hand for .get_height -> H'''
    return surface.get_height()

# init and rest game var
def init_game_var(game_mode:str):
    '''This function init and reset game variables'''
    global night, score, fps, lives, health_bar_color, music, cur_mode
    night     = 0
    score     = 0
    fps       = 0
    cur_mode  = game_mode
    main_game.show_modes = False
    pygame.mouse.set_visible(False)
    main_game.running_bg_y, main_game.running_bg_direction = random.randint(-299,-101), random.choice([-1,1])
    main_game.running_bg_angle, main_game.rotation_direction = random.randint(-5,5), random.choice([1,-1])
    main_game.stage = "running"
    match game_mode.lower() :
        case "easy_mode" :
            lives = 550
            health_bar_color = "green"
            music = random.choice(general_music_list).play(-1)
        case "normal_mode" :
            lives = 250
            health_bar_color = "green"
            music = random.choice(general_music_list).play(-1)
        case "hardcore_mode" :
            lives = 1
            health_bar_color = "BLACK"
            music = random.choice(random.choice([hardcore_music_list, general_music_list])).play(-1)

# init music which takes most of loading time
def init_music():
    global hardcore_music_list, general_music_list

    # Music list
    
    hm1 = pygame.mixer.Sound(f"assets/music/hardcore_bg1.mpeg")
    hm2 = pygame.mixer.Sound(f"assets/music/hardcore_bg2.mp3")                    
    hardcore_music_list = [hm1, hm2]
    # hardcore_music_list = [pygame.mixer.Sound(f"assets/music/hardcore_bg{num+1}.{ext}") 
    #                        for num, ext in enumerate(['mpeg', 'mp3'])]
    
    print("70%")
    
    gm1 = pygame.mixer.Sound(f"assets/music/general_song-1.mp3")
    gm2 = pygame.mixer.Sound(f"assets/music/general_song-2.mp3")
    gm3 = pygame.mixer.Sound(f"assets/music/general_song-3.mp3")
    gm4 = pygame.mixer.Sound(f"assets/music/general_song-4.mp3")
    gm5 = pygame.mixer.Sound(f"assets/music/general_song-5.mp3")
    gm6 = pygame.mixer.Sound(f"assets/music/general_song-6.mp3")
    general_music_list = [gm1,gm2,gm3,gm4,gm5,gm6]

     
    # general_music_list = [pygame.mixer.Sound(f"assets/music/general_song-{num}.mp3") 
    # for num in range(1, 7)]    
    
    print("99%")

    #[general_music_list[i].set_volume(game_vol) for i in range(len(general_music_list))]
    #[hardcore_music_list[i].set_volume(game_vol) for i in range(len(hardcore_music_list))]

# set or change game music and sound
def set_music_vol(music_vol: float):
    for hm in hardcore_music_list: hm.set_volume(music_vol) 
    for gm in general_music_list: gm.set_volume(music_vol)

    menu_song.set_volume(music_vol)
    game_over_sound.set_volume(music_vol)
    next_night_sound.set_volume(music_vol)
    mos_sound1.set_volume(music_vol)
    mos_sound2.set_volume(music_vol)

    # gm1.set_volume(music_vol)  # 0.4
    # gm2.set_volume(music_vol)  # 0.2
    # gm3.set_volume(music_vol)
    # gm4.set_volume(music_vol) # 0.2
    # gm5.set_volume(music_vol)
    # gm6.set_volume(music_vol)

# This fun gives surf and rect and save 2 lines per call, it can give both render and normal surf 
def get_surf_and_rect(text, font_or_size, location, color=False):
    '''Takes arg of surf and rect cration and give surf. Note rect location is from center of rect'''
    surf = (font_or_size.render(text,True,color).convert_alpha() if text 
            else pygame.Surface(font_or_size).convert_alpha())
    if color and not text: surf.fill(color) 
    rect = surf.get_rect()
    rect.center = location

    return (surf, rect)

# LITTERALS
WIDTH   = 550
HEIGHT  = 600
FPS     = 60        # for now, doesn't have any use, since game is frame independent ;)

ALMOST_WHITE = (230, 230, 230)
ALMOST_BLACK = (35, 35, 35)   # GAME RUNNING BG

MENU_FILL          = (5, 5, 100)
EASY_COLOR         = (0, 255, 0)
NORMAL_COLOR       = (255, 150, 40)
HARDCORE_COLOR     = (255, 0, 0)
HARSHAL_NAME_COLOR = (0, 150, 255)

ABOUT_FILL        = (192, 255, 64*2)
ABOUT_TITLE_COLOR = (255,128,64)
ABOUT_TEXT_COLOR  = (255,255,255)
BACK_BUTTON_COLOR = (0, 0, 128)
BACK_HOVER        = (255,128,128)

OVER_NIGHT_TEXT_COLOR = (255 , 0, 255)
RUN_NIGHT_TEXT_COLOR  = (200 , 0, 255)

GAME_OVER_FILL   = (200, 235, 255)   # GAEM OVER BG COLOR
GAME_TITLE_COLOR = (250, 250, 155)   # MENU BG COLOR, SAND/CREAM    
#GREEN2          = (0, 192, 0)

print("1%")

# Game Set-up
pygame.init()
pygame.display.set_caption("MOSQUITO ATTACK")
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
clock   = pygame.time.Clock() 

print("4%")

game_mode_image1 = pygame.image.load("assets/images/SELECTED(BG)/game_mode.png").convert_alpha()
menu_image1 = game_mode_image1
how2play_image = pygame.image.load("assets/images/SELECTED(BG)/HOW to.jpeg").convert_alpha()
menu_image11 = pygame.image.load("assets/images/SELECTED(BG)/menu.png").convert_alpha()
running1 = pygame.image.load("assets/images/SELECTED(BG)/running.png").convert_alpha()
running2 = pygame.image.load("assets/images/SELECTED(BG)/running2.webp").convert_alpha()
running3 = pygame.image.load("assets/images/SELECTED(BG)/running3.jpg").convert_alpha()

running = pygame.transform.rotozoom(running2, 0, 1.1)

#running_rect = pygame.Rect(-200,0,WIDTH,HEIGHT)

# Fonts
title_font            = pygame.font.Font("assets/fonts/main_title.otf", 72)
game_mode_font        = pygame.font.Font("assets/fonts/robot.ttf", 50)
game_over_font        = pygame.font.Font("assets/fonts/BearHand.otf", 100)
game_over_button_font = pygame.font.Font("assets/fonts/robot.ttf", 40)
text_font             = pygame.font.Font("assets/fonts/joy_bold.otf", 40)
cut_font              = pygame.font.Font("assets/fonts/cuted_font.ttf", 44)
large_text_font       = pygame.font.Font("assets/fonts/good_text.otf", 35)
back_button_font      = pygame.font.Font("assets/fonts/joy_bold.otf", 40)
gamic_font            = pygame.font.Font("assets/fonts/gamic_fanci.ttf", 35)
big_gamic_font        = pygame.font.Font("assets/fonts/gamic_fanci.ttf", 40)
#monster_font         = pygame.font.Font("assets/fonts/font.otf", 50)

print("20%")

# Music and Sound
next_night_sound = pygame.mixer.Sound("assets/music/level_up.mpeg")
game_over_sound = pygame.mixer.Sound("assets/music/game_over.mpeg")
mos_sound1      = pygame.mixer.Sound("assets/music/kill_mos1.mpeg")
mos_sound2      = pygame.mixer.Sound("assets/music/kill_mos2.mpeg")
menu_song       = pygame.mixer.Sound("assets/music/happy_short.mp3")

music_vol = 0.3
game_vol = 0.1
game_vol2 = 0.5

sound_list = [next_night_sound.set_volume(0.5),
game_over_sound.set_volume(game_vol2),
menu_song.set_volume(game_vol2),
mos_sound1.set_volume(game_vol),
mos_sound2.set_volume(game_vol)]

print("35%")

harshal_name         = text_font.render("- Harshal Gahlot", True, HARSHAL_NAME_COLOR).convert_alpha()
harshal_rect         = harshal_name.get_rect()
harshal_rect.midleft = (WIDTH * .5, HEIGHT * 0.375)

about_title = cut_font.render("ABOUT", True, ABOUT_TITLE_COLOR ).convert_alpha()

about_list = ["Hello, Welcome to Skeeter Smashdown,",
              "an INDIE game that I, Harshal Gahlot",
              "have created from scratch as a solo developer",
              "and programmer. It took me over 160 hours of",
              "hard work to create this game. I hope you",
              "found it as enjoyable to play as I did to",
              "develop it. Thanks for trying it out."
              ]

about_content_surf_rect = [(large_text_font.render(about_list[i], True,
                        ABOUT_TEXT_COLOR).convert_alpha()) for i in range(len(about_list))]

MCR = 20    # stands for Muisc Circle Radius, it's of no use now that there is sq in music bar

music_bar = pygame.Surface((WIDTH/2,5))
music_bar_rect = pygame.draw.line(music_bar, (222,222,222), (WIDTH/4, HEIGHT/2), (WIDTH*3/4, HEIGHT/2))
music_bar_rect.center = (WIDTH/4, HEIGHT/2)

people_area, people_rect = get_surf_and_rect(False, (WIDTH, HEIGHT//10), (WIDTH/2, HEIGHT - HEIGHT/20))
music_black_bg, music_black_bg_rect = get_surf_and_rect(False, (MCR*2, MCR*2), (WIDTH/2, HEIGHT/2))

music_text, music_text_rect = get_surf_and_rect("Music Volume", text_font, (WIDTH/3, HEIGHT/3) , (222,222,222))
game_title1, game_title_rect1 = get_surf_and_rect("SKEETER", title_font, (WIDTH/2 , 70), GAME_TITLE_COLOR)
game_title2, game_title_rect2 = get_surf_and_rect("SMASHDOWN", title_font, (WIDTH/2, H(game_title1)+35), GAME_TITLE_COLOR)
game_over_text, game_over_rect = get_surf_and_rect("G A ME   OV E R", game_over_font, (0,0), (200,200,200))

game_over_rect.center = (WIDTH/2 , H(game_over_text))

print("40%")

# mosquito 1,2,3 img list load
mos1_list =[pygame.image.load(f"assets/images/mos1.{img_num}.png").convert_alpha()for img_num in range(1,5)]
mos2_list =[pygame.image.load(f"assets/images/mos2.{img_num}.png").convert_alpha()for img_num in range(1,5)]
mos3_list =[pygame.image.load(f"assets/images/mos3.{img_num}.png").convert_alpha()for img_num in range(1,5)]

print("50%")
init_music()

move_modesY, gap_btw_modes = -25, 60

show_modes_button = ButtonsClass("START", (WIDTH/2, HEIGHT/2 - gap_btw_modes - move_modesY),
                                 (350,50), (00,200,00), border = (20,20,0,0) )
about_button = ButtonsClass("About", (WIDTH/2, HEIGHT/2 - move_modesY), (350,50), (00,200,200))
how2play_button = ButtonsClass("How To Play", (WIDTH/2, HEIGHT/2 + gap_btw_modes - move_modesY),
                                (350,50), (255,0,255), border = (0,0,20,20) )

setting_button = ButtonsClass("SETTING", (WIDTH - 100, 50), (200,50), (200,200,200))
back_button = ButtonsClass("Back", (100,35 - move_modesY), (150, 50), BACK_BUTTON_COLOR, 
                           border = (50,50,50,50), hover_color = BACK_HOVER)

easy_mode_button = ButtonsClass("EASY MODE", (WIDTH/2, HEIGHT/2 - gap_btw_modes - move_modesY),
                                 (350,50), (EASY_COLOR), border = (20,20,0,0) )
normal_mode_button = ButtonsClass("NORMAL MODE", (WIDTH/2, HEIGHT/2 - move_modesY), (350,50),
                                 (NORMAL_COLOR) )
hardcore_mode_button = ButtonsClass("HARDCORE MODE", 
(WIDTH/2, HEIGHT/2 + gap_btw_modes - move_modesY),(350,50), (HARDCORE_COLOR), border = (0,0,20,20) )

try_again_button = ButtonsClass("Try Again!", (WIDTH/2, HEIGHT*.775), (350, 50),(0,128,255))
menu_button  = ButtonsClass("MENU", (WIDTH/2, HEIGHT*0.66), (250, 50),(0,128,255))
last_sec_fps = 0

# making groups for both classes
mos_group = pygame.sprite.Group()
racket_group = pygame.sprite.GroupSingle()
kill_part_group = pygame.sprite.GroupSingle(Kill_Part())

racket = Racket()                   # racket obj
racket_group.add(racket)            # racket obj added to it's group
kill_part = Kill_Part()             # racket kill part obj
kill_part_group.add(kill_part)      # racket kill part obj added to it's group

game_running = False
menu = True

print("100%")
main_game = Main_Game()
print("total",time.perf_counter() - t)

to_calc_fps = 0
to_know_1sec = that_time = old_time = time.monotonic()

# if __name__ == "__main__":
# Main Game loop
while True:
    for event in pygame.event.get():                 
        if event.type == pygame.QUIT :   
            pygame.quit()
            sys.exit()

    dt = time.monotonic() - old_time
    old_time = time.monotonic()

    # to calc fps
    to_know_1sec = time.monotonic()
    if to_know_1sec >= that_time + 1:
        last_sec_fps = to_calc_fps+1    # this x is fps of last sec 
        to_calc_fps = 0
        that_time = to_know_1sec
    else:
        to_calc_fps += 1

    # call Game class current screen
    main_game.Current_screen()
    # Debug(last_sec_fps)

    pygame.display.update()

    '''Since game is frame independent below code is not needed. If uncommented, game will run at given 
    FPS, which would be slower fps then current set-up. If given too high FPS, game will flucituate 
    too much but that is okey because of frame independent set-up.'''
    # clock.tick(FPS)   
