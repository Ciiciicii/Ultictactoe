import pygame

pygame.init()
clock = pygame.time.Clock()

screen_size = (500, 500)
screen = pygame.display.set_mode([screen_size[0], screen_size[1]])

class GameUI:
    def __init__(self) -> None:
        self.width, self.height = 720, 720
        self.fps = 30

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Ultimate TicTacToe")

        self.running = True
        
        self.constant_display()
        self.load_sprites()
        self.mainloop()
    
    def load_sprites(self) -> None:
        self.x_img = pygame.image.load('sprites/x.webp')
        self.o_img = pygame.image.load('sprites/ttt_O.svg')

        padding_percent = 0.2
        self.padding = int(padding_percent * self.box_size[0]), int(padding_percent * self.box_size[1])

        image_size = self.box_size[0] - self.padding[0] * 2, self.box_size[1] - self.padding[1] * 2
        self.x_img = pygame.transform.smoothscale(self.x_img, image_size) 
        self.o_img = pygame.transform.smoothscale(self.o_img, image_size) 

        self.screen.blit(self.x_img, (200, 200))

    def constant_display(self) -> None:
        self.screen.fill((40, 40, 50))

        line_color = (190, 190, 190)
        margins = self.width // 4, self.height // 4
        self.box_size = (self.width - margins[0]) // 9, (self.height - margins[1]) // 9

        for i in range(10):
            line_width = 5 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, line_color, 
                             (margins[0] // 2 + self.box_size[0] * i, margins[1] // 2), 
                             (margins[0] // 2 + self.box_size[0] * i, self.height - margins[1] // 2),
                             line_width)
            pygame.draw.line(self.screen, line_color, 
                             (margins[0] // 2, margins[1] // 2 + self.box_size[1] * i), 
                             (self.width - margins[0] // 2, margins[1] // 2 + self.box_size[1] * i),
                             line_width)
            
        

    def mainloop(self) -> None:
        time_delta = 0
        while self.running:
            events = pygame.event.get()
            self.events_check(events)
            pygame.display.update()
        pygame.quit()

    def events_check(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return 


if __name__ == "__main__":
    GameUI()
