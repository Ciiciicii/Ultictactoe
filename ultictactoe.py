from tictactoe import TicTacToe

class GridError(Exception):
    def __init__(self, active_grid, message="No moves possible for active grid"):
        self.active_grid = active_grid
        self.message = message
        super().__init__(self.message)

class UlTicTacToe:
    def __init__(self) -> None:
        self.master_grid = TicTacToe()
        self.all_grids = [TicTacToe() for _ in range(9)]
        self.winner = None
        self.last_index = None

        self.active_grid_id = 4
        self.active_grid = self.all_grids[4]
        self.player = 1

    def __repr__(self) -> str:
        str_grid = ""
        for i in range(3):
            start_grid = i * 3
            end_grid = i * 3 + 3
            for j in range(3):
                row = "|".join(
                    [
                        child_grid.__repr__().split("\n")[j]
                        for child_grid in self.all_grids[start_grid:end_grid]
                    ]
                )
                str_grid += f"{row}\n"
            str_grid += "_" * 11 + "\n\n"
        return str_grid

    def query_moves(self) -> list[tuple]:
        return [
            (self.active_grid_id,) + move for move in self.active_grid.query_moves()
        ]

    def make_move(self, index: list[int], player: int):
        if len(index) != 2:
            raise ValueError("argument index must have a length of 2")
        
        grid = self.active_grid_id
        move_id = (grid,) + tuple(index)

        if move_id not in self.query_moves():
            raise ValueError(f"argument grid, index: {grid, index} is an illegal move.")

        r, c = index
        self.active_grid.make_move(index, player)
        active_grid_winner = self.active_grid.check_for_winner()
        if active_grid_winner is not None:
            self.master_grid.make_move(self.last_index, active_grid_winner)

        self.last_index = index
        self.active_grid_id = r * 3 + c
        self.active_grid = self.all_grids[self.active_grid_id]

    def active_grid_finished(self) -> bool:
        if self.last_index is None:
            return False
        r, c = self.last_index
        if self.master_grid.grid[r][c] == -1:
            return False
        return True
    
    def change_active_grid(self, grid: int) -> None:
        self.active_grid_id = grid
        self.active_grid = self.all_grids[grid]

    def check_for_winner(self) -> int | None:
        return self.master_grid.check_for_winner()

    def visualize_grid(self) -> str:
        print(self)


if __name__ == "__main__":
    uttt = UlTicTacToe()
    player = 1
    for _ in range(25):
        if uttt.active_grid_finished():
            grid_num = int(input(f"Player {player}: Select active grid: "))
            uttt.change_active_grid(grid_num)
        move = input(f"Player {player}: Enter move:  ")
        move = int(move)
        id1, id2 = int(move // 10), int(move % 10)
        try:
            uttt.make_move(index=(id1, id2), player=player)
        except ValueError:
            print("Invalid move")
            continue
        player = 1 - player
        uttt.visualize_grid()
        if uttt.check_for_winner() is not None:
            break
    print("Winner:", uttt.check_for_winner())


