from .difficulty import Difficulty

class SudokuImage:
    def __init__(self, filename, puzzle_list, image):
        self.filename = filename
        self.puzzle_list = puzzle_list
        self.image = image
        self.difficulty = Difficulty.EASY.value

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty