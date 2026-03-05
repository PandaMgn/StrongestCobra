import pygame

class Menu:
    '''
    class for the screens shown during the game
    '''
    def __init__(self, font, font_color=WHITE, bg_color = BLACK):
        self.font = font
        self.font_color = font_color

    def draw(self, screen):
        screen.fill(self.bg_color)

    class start_menu:
        def __init__(self, status, screen, ):
            screen.fill((0,0,0))

        def draw(screen, bacbackground):
            pygame.font.init()
            w, h = screen.get_size()
            font = pygame.font.SysFont('arial', 48)
            text = font.render("Strongest Cobra", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = w // 2, h // 5

class Button:
    #Cickable button Class
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = pygame.Rect(pos,size)

    def draw(self, surface):
        #fix do not create 2nd event handler
        '''
        mouse down, save, pos as bool, mouse up, check if on button, shwo sprite while and hover
        '''
        start_down = False
        for event in pygame.event.get():  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousedown_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mousedown_pos):
                    return start_down == True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseup_pos =  pygame.mouse.get_pos()
                if self.rect.collidepoint(mousedown_pos) and self.rect.collidepoint(mouseup_pos):
                    print("HHHHHH")
                    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

        else:
            None

