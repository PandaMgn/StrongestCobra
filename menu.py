import pygame

class Menu:
    '''
    class for the screens shown during the game
    '''
    def __init__(self, status, screen, background):
        pygame.font.init()
        w, h  = screen.get_size()
        bg_img = pygame.image.load("background_image.png").convert_alpha
        return screen.blit(bg_image, 0,0)
    
    class start_menu:
        def __init__(self, status, screen, background):
            bg_image = pygame.image.load
        
        def draw(screen, bacbackground):
            pygame.font.init()
            w, h = screen.get_size()
            font = pygame.font.SysFont('arial', 48)
            text = font.render("Strongest Cobra", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = w // 2, h // 5

        def start_button(x, y, w, h):
            x, y = screen.get_size() 
            button_rect = pygame.Rect(x//2, y//2, w, h, "Start")           
            for event in pygame.event.get():  
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousedown_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseup_pos =  pygame.mouse.get_pos()
                    if button_rect.collidepoint(mousedown_pos) and button_rect.collidepoint(mouseup_pos):
                        print("HHHHHH")
                        return "Start"
                else:
                    None

    def show_screen(status):


