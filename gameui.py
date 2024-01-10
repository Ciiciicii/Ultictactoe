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

        self.font = pygame.font.SysFont("Source Sans Pro", 40)
        # self.colors = {"bg": "#092635", "accent": "#1B4242", "light": "#9EC8B9"}
        # self.colors = {"bg": "#386641", "accent": "#6A994E", "light": "#A7C957"}
        self.colors = {"bg": "#766153", "accent": "#A08470", "light": "#BCBD8B"}
        # self.colors = {"bg": "#772F1A", "accent": "#F58549", "light": "#F2A65A"}f
        self.running = True

        self.constant_display()
        self.load_sprites()
        self.load_game()
        self.mainloop()

    def load_sprites(self) -> None:
        self.x_img = pygame.image.load("sprites/x.webp")
        self.o_img = pygame.image.load("sprites/egg.webp")

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


    def load_game(self):
        self.game = UlTicTacToe()
        self.player = 1
        self.highlight_active_grid(4)

    def constant_display(self) -> None:
        self.screen.fill(self.colors["bg"])
        self.draw_grid()
        
        self.turn_text = self.font.render("X's turn", True, self.colors["light"])
        turn_text_rect = self.turn_text.get_rect(center=(self.width // 2, self.margins[1] // 4))
        self.screen.blit(self.turn_text, turn_text_rect)
    
    def draw_grid(self) -> None:
        line_color = self.colors["accent"]
        
        self.margins = self.width // 4, self.height // 4
        self.box_size = (self.width - self.margins[0]) // 9, (self.height - self.margins[1]) // 9

        for i in range(10):
            line_width = 5 if i % 3 == 0 else 2
            pygame.draw.line(
                self.screen,
                line_color,
                (self.margins[0] // 2 + self.box_size[0] * i, self.margins[1] // 2),
                (self.margins[0] // 2 + self.box_size[0] * i, self.height - self.margins[1] // 2),
                line_width,
            )
            pygame.draw.line(
                self.screen,
                line_color,
                (self.margins[0] // 2, self.margins[1] // 2 + self.box_size[1] * i),
                (self.width - self.margins[0] // 2, self.margins[1] // 2 + self.box_size[1] * i),
                line_width,
            )
        
    def highlight_active_grid(self, grid: int | list) -> None:
        if isinstance(grid, list):
            for grid_num in grid:
                self.highlight_active_grid(grid_num)
            return

        minX, maxX, minY, maxY = self.get_grid_positions(grid)
        
        hl_color = self.colors["light"]
        for i in range(4):
            line_width = 5 if i % 3 == 0 else 2 
            pygame.draw.line(
                self.screen,
                hl_color,
                (minX + self.box_size[0] * i, minY),
                (minX + self.box_size[0] * i, maxY),
                line_width
            )
            pygame.draw.line(
                self.screen,
                hl_color,
                (minX, minY + self.box_size[1] * i),
                (maxX, minY + self.box_size[1] * i),
                line_width
            )

    def mainloop(self) -> None:
        time_delta = 0
        while self.running:
            events = pygame.event.get()
            self.events_check(events)
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

    def events_check(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.user_click()
                self.update_turn()
                self.draw_grid()
                self.draw_master_grid()
                if not self.game.active_grid_finished():
                    self.highlight_active_grid(self.game.active_grid_id)        
                else:
                    unfinished_grids = self.game.list_unfinished_grids()
                    self.highlight_active_grid(unfinished_grids)     

    def update_turn(self) -> int:
        turn_text_rect = self.turn_text.get_rect(center=(self.width // 2, self.margins[1] // 4))
        self.screen.fill(self.colors["bg"], turn_text_rect)
        
        winner = self.game.check_for_winner()

        token = {1: "X", 0: "O"}
        if winner is not None:
            text = f"{token[winner]}'s win"
        else:
            text = f"{token[self.player]}'s turn"

        self.turn_text = self.font.render(text, True, self.colors["light"])
        turn_text_rect = self.turn_text.get_rect(center=(self.width // 2, self.margins[1] // 4))
        self.screen.blit(self.turn_text, turn_text_rect)
    
    def get_grid_positions(self, grid: int) -> tuple[int]:
        grid_row, grid_column = grid // 3, grid % 3
        minX, maxX = self.margins[0] // 2 + self.box_size[0] * 3 * grid_column, self.margins[0] // 2 + self.box_size[0] * 3 * (grid_column + 1)
        minY, maxY = self.margins[1] // 2 + self.box_size[1] * 3 * grid_row, self.margins[1] // 2 + self.box_size[1] * 3 * (grid_row + 1)
        return minX, maxX, minY, maxY
    
    def grid_from_position(self, x: int, y: int) -> int:
        if x < self.margins[0] // 2 or x > self.width - self.margins[0] // 2:
            return None
        if y < self.margins[1] // 2 or y > self.height - self.margins[1] // 2:
            return None
        
        grid_width = self.box_size[0] * 3
        grid_height = self.box_size[1] * 3

        grid_col = (x - self.margins[0] // 2) // grid_width
        grid_row = (y - self.margins[1] // 2) // grid_height

        return grid_row * 3 + grid_col

    def user_click(self) -> None:
        x, y = pygame.mouse.get_pos()
        grid = self.game.active_grid_id

        if self.game.active_grid_finished():
            grid = self.grid_from_position(x, y)
            if grid is None:
                return
            self.game.change_active_grid(grid)

        minX, maxX, minY, maxY = self.get_grid_positions(grid)
        if minX <= x <= maxX and minY <= y <= maxY:
            relativeX = x - minX
            relativeY = y - minY

            row = relativeY // self.box_size[1]
            column = relativeX // self.box_size[0]
            
            try:
                active_grid_winner = self.game.make_move((row, column), self.player)
            except ValueError:
                return
            
            self.drawXO(grid, row, column)

            if active_grid_winner is None:
                self.player = 1 - self.player

    def drawXO(self, grid, row, column):
        minX, _, minY, _ = self.get_grid_positions(grid)
        box_center = minX + self.box_size[0] * (column + 0.5), minY + self.box_size[1] * (row + 0.5)

        if self.player == 1:
            x_rect = self.x_img.get_rect(center=box_center)
            self.screen.blit(self.x_img, x_rect)
        else:
            o_rect = self.o_img.get_rect(center=box_center)
            self.screen.blit(self.o_img, o_rect)
    
    def draw_master_grid(self) -> None:
        master_grid = self.game.master_grid
        for i in range(3):
            for j in range(3):
                grid_num = i * 3 + j
                minX, _, minY, _ = self.get_grid_positions(grid_num)

                if master_grid.grid[i][j] < 0:
                    continue

                rect = pygame.Rect(minX + 2, minY + 2, self.box_size[0] * 3 - 4, self.box_size[1] * 3 - 4)
                big_image_size = (
                    3 * self.box_size[0] - 5 * self.padding[0] * 2,
                    3 * self.box_size[1] - 5 * self.padding[1] * 2,
                )
                pygame.draw.rect(self.screen, self.colors["bg"], rect)

                if master_grid.grid[i][j] == 1:
                    big_img = pygame.transform.smoothscale(self.x_img, big_image_size)

                if master_grid.grid[i][j] == 0:
                    big_img = pygame.transform.smoothscale(self.o_img, big_image_size)

                o_rect = big_img.get_rect(center=(minX + 1.5 * self.box_size[0], minY + 1.5 * self.box_size[1]))
                self.screen.blit(big_img, o_rect)


if __name__ == "__main__":
    GameUI()
