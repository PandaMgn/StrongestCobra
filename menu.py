import pygame

class Game_Screen:
    '''class for the screens shown during the game'''
    def __init__(self, screen, title_font, subtitle_font):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        
        #buttons
        self.start_button =  Button("Start Game", (self.w/2, self.h/1.5), (200, 50), self.subtitle_font, (255,255,255), (0,0,0)) #button in here becaues its an object and not temporary
        self.ability_button = Button("Ability", (50+15, self.h-25-15), (100, 50), self.subtitle_font, (255,255,255), (0,0,0)) #bottom left corner for now
        self.replay_button = Button("Replay Game", (self.w/2, self.h-25-50), (200, 50), self.subtitle_font, (255,255,255), (0,0,0))

        #input box
        self.name_select = InputBox(self.w/2 - 100, self.h/ 2 - 25, 200, 50, "")
        
        self.cobrabutton = Button("", (self.w/1.4, self.h/4), (200, 200), self.subtitle_font, (0,0,0), (0,0,0), "assets/CoolCobra.png")
        self.foxbutton = Button("", (self.w/3.1, self.h/4), (200, 200), self.subtitle_font, (0,0,0), (0,0,0), "assets/CoolFox.png")
    
    def draw_start_screen(self): #add char select feature
        self.screen.fill((0,0,0))
        title = self.title_font.render("Strongest Cobra", True, (255,255,255))
        titleRect = title.get_rect()
        titleRect.center = (self.w/2, self.h/15)
        self.screen.blit(title, titleRect)
        self.start_button.draw(self.screen)


        self.name_select.update()
        self.name_select.draw(self.screen)

        self.cobrabutton.draw(self.screen)
        self.foxbutton.draw(self.screen)

        
    def draw_game_screen(self): #if not here then overlays over everyting
        self.screen.fill((0,0,0))
        
    def draw_game_menu(self, score, health, player_name):
        #draws the ui while the game is running like health, name and  ability as well as score
        self.ability_button.draw(self.screen)
        score_title = self.title_font.render(f"Score: {score}", True, (255, 255, 255))
        titleRect = score_title.get_rect()
        titleRect.topleft = (12, 12)
        self.screen.blit(score_title, titleRect)
        
        health_title = self.title_font.render(f"Health: {health}", True, (255, 255, 255))
        titleRect = health_title.get_rect()
        titleRect.topleft = (12, 60)
        self.screen.blit(health_title, titleRect)
        
        player_name_title = self.title_font.render(f"{player_name}", True, (255, 255, 255))
        titleRect = player_name_title.get_rect()
        titleRect.topright = (self.w - 12, 12)
        self.screen.blit(player_name_title, titleRect)


    def draw_end_screen(self, score):
        #draws end screen
        self.screen.fill((0,0,0))
        title = self.title_font.render("Game Over", True, (255,255,255))
        titleRect = title.get_rect()
        titleRect.midtop = (self.w/2, 24)
        self.screen.blit(title, titleRect)
        subtitle = self.subtitle_font.render(f"Your Score: {score}", True, (255,255,255))
        subtitleRect = subtitle.get_rect()
        subtitleRect.midtop = (self.w/2, 24+50)
        self.screen.blit(subtitle, subtitleRect)
        self.replay_button.draw(self.screen)
        

class Button:
    '''
    class for the buttons used in the menues
    '''
    def __init__(self, text, pos, size, font, color, text_color, image=None):
        self.text = text
        self.rect = pygame.Rect(pos,size)
        self.rect.center = pos
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = (min(color[0]+25,255), min(color[1]+25,255), min(color[2]+25,255))
        if image != None:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (200,200))
            self.image_rect = self.image.get_rect(center = pos)
        else:
            self.image = None
            self.image_rect = None

        
        self.pressed = False
        
    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos): #change color if hover overed
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        if self.image != None:
            screen.blit(self.image, self.image_rect)

        else:
            text_surface = self.font.render(self.text,True,self.text_color) #draw text in button
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        
    def is_clicked(self, event): #check if clicked

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if self.image != None:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos) or self.image_rect.collidepoint(event.pos):
                        self.pressed = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.pressed = True


            if self.image != None:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.pressed and (self.rect.collidepoint(event.pos) or self.image_rect.collidepoint(event.pos)):
                        self.pressed = False
                        return True
                    self.pressed = False
            else:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.pressed and self.rect.collidepoint(event.pos):
                        self.pressed = False
                        return True
                    self.pressed = False
            return False

pygame.font.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        self.color = COLOR_ACTIVE
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
            else:
                    self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)