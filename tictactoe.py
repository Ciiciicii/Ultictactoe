class TicTacToe:
    def __init__(self) -> None:
        self.grid = [[-1] * 3 for _ in range(3)]
        self.moves = None
        self.winner = None

    def __repr__(self) -> str:
        marks = {-1: "-", 0: "O", 1: "X"}
        return "\n".join("".join(marks[i] for i in row) for row in self.grid)

    def query_moves(self) -> list[tuple]:
        self.moves = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == -1:
                    self.moves.append((i, j))
        return self.moves

    def make_move(self, index: list[int], player: int) -> None:
        if len(index) != 2:
            raise ValueError("argument index must have a length of 2")
        if self.moves is None:
            self.query_moves()
        if index not in self.moves:
            raise ValueError(f"argument index: {index} is an illegal move.")
        r, c = index
        self.grid[r][c] = player
        self.moves.remove((r, c))            

    def visualize_grid(self) -> None:
        print(self)        

    def check_for_winner(self) -> int | None:
        def connected_triplet(triplet: list[int] | tuple[int, int, int]) -> bool:
            if -1 in triplet:
                return False
            if len(set(triplet)) == 1:
                return True
            return False

        for row in self.grid:
            if connected_triplet(row):
                self.winner = row[0]
                return self.winner

        transposed = list(zip(*self.grid))
        for col in transposed:
            if connected_triplet(col):
                self.winner = col[0]
                return self.winner

        diagonal1 = [self.grid[i][i] for i in range(3)]
        center = self.grid[1][1]
        if connected_triplet(diagonal1):
            self.winner = center
            return self.winner
        
        diagonal2 = [self.grid[2 - i][i] for i in range(3)]
        if connected_triplet(diagonal2):
            self.winner = center
            return self.winner

        if not any(-1 in row for row in self.grid):
            self.winner = -2

        return self.winner


if __name__ == "__main__":
    ttt = TicTacToe()
    player = 1
    while ttt.check_for_winner() is None:
        move = input(f"Player {player}: Enter move:  ")
        move = int(move)
        id1, id2 = int(move // 10), int(move % 10)
        try:
            ttt.make_move((id1, id2), player)
        except ValueError:
            print("Invalid move")
            continue
        player = 1 - player
        print(ttt)

    winner = ttt.check_for_winner()
    if winner == -2: 
        print(f"Tie!!")
    else:
        print(f"Winner: {winner}")
