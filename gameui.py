from ultictactoe import UlTicTacToe

import pygame


class GameUI:
    def __init__(self) -> None:
        self.width, self.height = 720, 720
        self.fps = 30

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Ultimate TicTacToe")

        self.font = pygame.font.SysFont("Times New Roman", 30)
        self.colors = {"bg": "#092635", "accent": "#1B4242", "light": "#9EC8B9"}

        self.running = True

        self.constant_display()
        self.load_sprites()
        self.load_game()
        self.mainloop()

    def load_sprites(self) -> None:
        self.x_img = pygame.image.load("sprites/x.webp")
        self.o_img = pygame.image.load("sprites/ttt_O.svg")

        padding_percent = 0.2
        self.padding = int(padding_percent * self.box_size[0]), int(
            padding_percent * self.box_size[1]
        )

        image_size = (
            self.box_size[0] - self.padding[0] * 2,
            self.box_size[1] - self.padding[1] * 2,
        )
        self.x_img = pygame.transform.smoothscale(self.x_img, image_size)
        self.o_img = pygame.transform.smoothscale(self.o_img, image_size)

        self.screen.blit(self.x_img, (200, 200))

    def load_game(self):
        self.game = UlTicTacToe()
        self.player = 1

    def constant_display(self) -> None:
        self.screen.fill(self.colors["bg"])
        line_color = self.colors["accent"]

        self.margins = self.width // 4, self.height // 4
        self.box_size = (self.width - self.margins[0]) // 9, (
            self.height - self.margins[1]
        ) // 9

        for i in range(10):
            line_width = 5 if i % 3 == 0 else 2
            pygame.draw.line(
                self.screen,
                line_color,
                (self.margins[0] // 2 + self.box_size[0] * i, self.margins[1] // 2),
                (
                    self.margins[0] // 2 + self.box_size[0] * i,
                    self.height - self.margins[1] // 2,
                ),
                line_width,
            )
            pygame.draw.line(
                self.screen,
                line_color,
                (self.margins[0] // 2, self.margins[1] // 2 + self.box_size[1] * i),
                (
                    self.width - self.margins[0] // 2,
                    self.margins[1] // 2 + self.box_size[1] * i,
                ),
                line_width,
            )

    def mainloop(self) -> None:
        time_delta = 0
        while self.running:
            events = pygame.event.get()
            self.events_check(events)
            self.show_turn()
            pygame.display.update()
        pygame.quit()

    def events_check(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return

    def show_turn(self) -> int:
        token = {1: "X", 0: "O"}
        player = self.player
        winner = self.game.check_for_winner()

        if winner:
            text = f"{token[winner]}'s win"
        else:
            text = f"{token[player]}'s win"

        player_turn = self.font.render(text, True, self.colors["light"])
        player_turn_rect = player_turn.get_rect(
            center=(self.width // 2, self.margins[1] // 4)
        )
        self.screen.blit(player_turn, player_turn_rect)
    
    def get_active_grid_positions(self) -> tuple[int]:
        pass

    def user_click(self) -> bool:
        x, y = pygame.get_pos()

        minX, maxX, minY, maxY = self.get_active_grid_positions()
        if minX <= x <= maxX and minY <= y <= maxY:
            relativeX = x - minX
            relativeY = y - minY

            row = relativeX // self.box_size[0]
            column = relativeY // self.box_size[1]

            try:
                active_grid_winner = self.game.make_move((row, column), self.player)
            except ValueError:
                return False
            
            if active_grid_winner is None:
                self.player = 1 - self.player
            self.drawXO(row, column)

            return self.game.active_grid_finished()
        
        return False

    def drawXO(self, row, column):
        pass


if __name__ == "__main__":
    GameUI()
