import pygame

class Game_Screen:
    '''
    class for the screens shown during the game
    '''
    def __init__(self, screen, title_font, subtitle_font, font_color):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.font_color = font_color
        
        #buttons
        self.start_button =  Button("Start Game", (self.w/2.5, self.h/1.5), (200, 50), self.subtitle_font, (255,0,255), (255,0,0)) #button in here becaues its an object and not temporary
        #self.ability_button = Button()
        #self.replay_button = Button("Replay Game", (self.w/2, self.h/1.5), (200, 50), self.font, (255,0,255), (255,0,0))
        
    
    def draw_start_screen(self): #draw the start screen, just the start button and title, maybe add more images later
        
        self.screen.fill(0,0,0)
        title = self.title_font.render("My Game", True, (255,255,255))
        titleRect = title.get_rect()
        titleRect.center = (self.w/2, self.h/4)
        self.screen.blit(title, titleRect)
        self.start_button.draw(self.screen)
        
    def draw_character_screen(self):
        None

    def draw_game_screen(self):
        None
        
    def draw_end_screen(self):
        None


class Button:
    '''
    class for the buttons used in the menues
    '''
    def __init__(self, text, pos, size, font, color, text_color):
        self.text = text
        self.rect = pygame.Rect(pos,size)
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = (min(color[0]+25,255), min(color[1]+25,255), min(color[2]+25,255))
        
        self.pressed = False
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos): #change color if hover overed
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text,True,self.text_color) #draw text in button
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, event): #check if clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                return True
            self.pressed = False
        return False
