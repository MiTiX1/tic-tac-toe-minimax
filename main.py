from typing import Tuple
import pygame as pg
import sys
import numpy as np

from components.figures import Circle, Cross

class Game:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    FPS = 60
    BACKGROUND = (255, 255, 255)
    LINE_COLOR = (227, 227, 227)
    FONT_COLOR = (19, 19, 19)
    GRID_SIZE = (3, 3)
    CROSS = 1
    CIRCLE = -1
    EMPTY = 0
    FONT = "helvetica.ttf"

    def __init__(self) -> None:
        pg.font.init()
        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.clock.tick(Game.FPS)
        self.font = pg.font.Font(Game.FONT, 64)
        self.grid = np.zeros(Game.GRID_SIZE, dtype=int)
        self.clicked = False
        self.cell_width = Game.SCREEN_WIDTH / Game.GRID_SIZE[0]
        self.cell_height = Game.SCREEN_HEIGHT / Game.GRID_SIZE[1]
        self.grid_thickness = 5
        self.figures = []
        self.is_player_turn = True

    def _draw_grid(self) -> None:
        x_start = self.cell_width
        for _ in range(Game.GRID_SIZE[0] - 1):
            pg.draw.line(self.screen, Game.LINE_COLOR, (x_start, 0), (x_start, Game.SCREEN_HEIGHT), self.grid_thickness)
            x_start += self.cell_width + self.grid_thickness

        y_start = self.cell_height
        for _ in range(Game.GRID_SIZE[1] - 1):
            pg.draw.line(self.screen, Game.LINE_COLOR, (0, y_start), (Game.SCREEN_WIDTH, y_start), self.grid_thickness)
            y_start += self.cell_height + self.grid_thickness

    def _draw(self) -> None:
        self._draw_grid()
        for figure in self.figures:
            figure.draw(self.screen)

    def _compute_cirle_pos(self, x: int, y: int) -> Tuple[int]:
        return (
            int(y * (self.cell_width + self.grid_thickness) + self.cell_width / 2),
            int(x * (self.cell_height + self.grid_thickness) + self.cell_height / 2)
        )

    def _compute_cross_pos(self, x: int, y: int) -> Tuple[Tuple[Tuple[int]]]:
        x_start = y * (self.cell_width + self.grid_thickness) + self.cell_width // 5
        x_end = y * (self.cell_width + self.grid_thickness) + 4 * self.cell_width // 5
        y_start = x * (self.cell_height + self.grid_thickness) + self.cell_height // 5
        y_end = x * (self.cell_height + self.grid_thickness) + 4 * self.cell_height // 5

        return (
            ((x_start, y_start), (x_end, y_end)),
            ((x_end, y_start), (x_start, y_end))
        )

    def _handle_click(self) -> None:
        if not self.is_player_turn:
            return
        if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
            pos = pg.mouse.get_pos()
            self.clicked = True
            x = int(pos[1] // self.cell_width)
            y = int(pos[0] // self.cell_height)

            if self.grid[x, y] == 0:
                self.grid[x, y] = Game.CIRCLE
                self.figures.append(Circle(self._compute_cirle_pos(x, y), radius=self.cell_width//3))
                self.is_player_turn = not self.is_player_turn

        if pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
            self.clicked = False

    def _minimax(self, depth: int, is_maximazing: bool) -> int:
        winner = self._check_win()
        if winner in [Game.CROSS, Game.CIRCLE]:
            return winner
        if self._check_full():
            return 0

        if is_maximazing:    
            best_score = -float("inf")
            for i in range(Game.GRID_SIZE[0]):        
                for j in range(Game.GRID_SIZE[1]):
                    if self.grid[i, j] == Game.EMPTY:
                        self.grid[i, j] = Game.CROSS
                        best_score = max(best_score, self._minimax(depth + 1, not is_maximazing))
                        self.grid[i, j] = Game.EMPTY
            return best_score

        best_score = float("inf")
        for i in range(Game.GRID_SIZE[0]):        
            for j in range(Game.GRID_SIZE[1]):
                if self.grid[i, j] == Game.EMPTY:
                    self.grid[i, j] = Game.CIRCLE
                    best_score = min(best_score, self._minimax(depth + 1, not is_maximazing))
                    self.grid[i, j] = Game.EMPTY
        return best_score

    def _play_bot(self) -> None:
        if self.is_player_turn:
            return

        best_score = -float("inf")
        best_move = (-1, -1)

        for i in range(Game.GRID_SIZE[0]):    
            for j in range(Game.GRID_SIZE[1]):
                if self.grid[i, j] == Game.EMPTY:
                    self.grid[i, j] = Game.CROSS
                    move_score = self._minimax(0, False)
                    self.grid[i, j] = Game.EMPTY
                    if move_score > best_score:               
                        best_move = (i, j)
                        best_score = move_score

        self.grid[best_move[0], best_move[1]] = Game.CROSS
        self.figures.append(Cross(self._compute_cross_pos(best_move[0], best_move[1])))
        self.is_player_turn = not self.is_player_turn

    def _check_win(self) -> int:
        for row in self.grid:
            if len(set(row)) == 1:
                return row[0]
        
        for row in self.grid.T:
            if len(set(row)) == 1:
                return row[0]

        if len(set([self.grid[i, i] for i in range(Game.GRID_SIZE[0])])) == 1:
            return self.grid[0, 0]
        if len(set([self.grid[i, Game.GRID_SIZE[0]-i-1] for i in range(Game.GRID_SIZE[0])])) == 1:
            return self.grid[0, Game.GRID_SIZE[0]-1]
        return 0

    def _check_full(self) -> bool:
        return Game.EMPTY not in self.grid

    def _update(self) -> None:
        if self._check_full():
            text = self.font.render("DRAW", True, Game.FONT_COLOR)
            self.screen.blit(text, (Game.SCREEN_WIDTH//2 - text.get_rect()[2]//2, Game.SCREEN_HEIGHT//2 - text.get_rect()[3]//2))
            return False

        winner = self._check_win()
        if winner:
            text = self.font.render(f"{'AI' if winner == Game.CROSS else 'PLAYER'} WON", True, Game.FONT_COLOR)
            self.screen.blit(text, (Game.SCREEN_WIDTH//2 - text.get_rect()[2]//2, Game.SCREEN_HEIGHT//2 - text.get_rect()[3]//2))
            return False
            
        self._handle_click()
        self._play_bot()
        return True

    def run(self) -> None:
        pg.init()
        while 1:
            for event in pg.event.get():
                if event.type ==  pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(Game.BACKGROUND)
            self._draw()
            self._update()
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()