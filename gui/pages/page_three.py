from tkinter import *
from .page import Page
from PIL import ImageTk, Image
from ..image_processing.main import readImage
from ..sudoku.sudoku_image import SudokuImage
from ..sudoku.difficulty import Difficulty

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.filename_label = None
        self.puzzle_list_label = None
        self.img_label = None
        self.easy_radio = None
        self.medium_radio = None
        self.hard_radio = None
        self.expert_radio = None
        self.puzzles = []
        self.next_btn = None
        self.prev_btn = None
        self.current_index = 0
        self.ref_variable = []
        self.set_query_func = None

        self.is_post_query_selected = False
        self.post_query_ref = IntVar(self, 0)
        self.post_query_button = Radiobutton(self, text="insert values to heroku db", variable=self.post_query_ref, value=1, command=self.unselect)
        self.post_query_button.grid(row=9, column=0)

        self.continue_btn = Button(self, text="submit", padx=10,
                                 pady=5, command=self.next_page)
        self.continue_btn.grid(row=9, column=1)

    def set_images(self, new_ss_list):
        print(len(self.puzzles))
        for filename in new_ss_list:
            try:
                puzzle_list, image = readImage(filename)
                self.puzzles.append(SudokuImage(filename, puzzle_list, image))
            except ValueError as err:
                print(err.args)
        if len(self.puzzles) > 0:
            return True
        else:
            return False

    # override no decorator
    def show(self):
        print("hello " + str(len(self.puzzles)))
        for i in range(len(self.puzzles)):
            self.ref_variable.append(StringVar(self, Difficulty.EASY.value))
        puzzle = self.puzzles[0]
        if isinstance(puzzle, SudokuImage) is False:
            raise ValueError("list object is not a sudoku puzzle")
        blank_space = Frame(self, width=960, height=20)
        blank_space.grid(row=0, column=0, columnspan=4)
        self.filename_label = Label(self, text=puzzle.filename)
        self.filename_label.grid(row=1, column=1)

        self.puzzle_list_label = Label(self, text=puzzle.puzzle_list,
                            wraplength=360, justify=CENTER)
        self.puzzle_list_label.grid(row=2, column=0)

        my_img = ImageTk.PhotoImage(Image.fromarray(puzzle.image).resize((360, 360)))
        self.img_label = Label(self, image=my_img, padx=10, pady=5)
        self.img_label.img = my_img
        self.img_label.grid(row=2, column=2, rowspan=6, columnspan=2)

        self.easy_radio = Radiobutton(self, text=Difficulty.EASY.value, variable=self.ref_variable[0], value=Difficulty.EASY.value)
        self.medium_radio = Radiobutton(self, text=Difficulty.MEDIUM.value, variable=self.ref_variable[0], value=Difficulty.MEDIUM.value)
        self.hard_radio = Radiobutton(self, text=Difficulty.HARD.value, variable=self.ref_variable[0], value=Difficulty.HARD.value)
        self.expert_radio = Radiobutton(self, text=Difficulty.EXPERT.value, variable=self.ref_variable[0], value=Difficulty.EXPERT.value)
        self.easy_radio.grid(row=4, column=0)
        self.medium_radio.grid(row=5, column=0)
        self.hard_radio.grid(row=6, column=0)
        self.expert_radio.grid(row=7, column=0)

        self.prev_btn = Button(self, text="<<", padx=10,
                               pady=5, command=self.prev_img, state=DISABLED)
        self.prev_btn.grid(row=8, column=2)
        if len(self.puzzles) == 1:
            self.next_btn = Button(self, text=">>", padx=10,
                                   pady=5, command=self.next_img, state=DISABLED)
        else:
            self.next_btn = Button(self, text=">>", padx=10,
                                   pady=5, command=self.next_img)
        self.next_btn.grid(row=8, column=3)

        super().show()

    def set_difficulty(self, difficulty):
        self.puzzles[self.current_index].set_difficulty(difficulty)

    def next_img(self):
        self.set_difficulty(self.ref_variable[self.current_index].get())
        self.current_index = self.current_index + 1
        puzzle = self.puzzles[self.current_index]
        self.filename_label.config(text=puzzle.filename)
        self.puzzle_list_label.config(text=puzzle.puzzle_list)
        my_img = ImageTk.PhotoImage(
            Image.fromarray(puzzle.image).resize((360, 360)))
        self.img_label.config(image=my_img)
        self.img_label.img = my_img
        if len(self.puzzles) == self.current_index + 1:
            self.next_btn.config(state=DISABLED)
        self.prev_btn.config(state=NORMAL)
        self.easy_radio.config(variable=self.ref_variable[self.current_index])
        self.medium_radio.config(variable=self.ref_variable[self.current_index])
        self.hard_radio.config(variable=self.ref_variable[self.current_index])
        self.expert_radio.config(variable=self.ref_variable[self.current_index])

    def prev_img(self):
        self.set_difficulty(self.ref_variable[self.current_index].get())
        self.current_index = self.current_index - 1
        puzzle = self.puzzles[self.current_index]
        self.filename_label.config(text=puzzle.filename)
        self.puzzle_list_label.config(text=puzzle.puzzle_list)
        my_img = ImageTk.PhotoImage(
            Image.fromarray(puzzle.image).resize((360, 360)))
        self.img_label.config(image=my_img)
        self.img_label.img = my_img
        if self.current_index == 0:
            self.prev_btn.config(state=DISABLED)
        self.next_btn.config(state=NORMAL)
        self.easy_radio.config(variable=self.ref_variable[self.current_index])
        self.medium_radio.config(variable=self.ref_variable[self.current_index])
        self.hard_radio.config(variable=self.ref_variable[self.current_index])
        self.expert_radio.config(variable=self.ref_variable[self.current_index])

    # override no decorator
    def next_page(self):
        self.set_difficulty(self.ref_variable[self.current_index].get())
        sql_query = "INSERT INTO sudoku_puzzles(puzzle, difficulty) VALUES \n"
        for puzzle in self.puzzles:
            sql_query = sql_query + "('" + puzzle.puzzle_list + "', '" + puzzle.difficulty + "'),\n"
        sql_query = sql_query[:-2] + ";"
        # print(sql_query)
        self.set_query(sql_query, self.is_post_query_selected)
        super().next_page()
    
    def set_set_query(self, func):
        self.set_query_func = func
        
    def set_query(self, query, send):
        self.set_query_func(query, send)

    def unselect(self):
        self.is_post_query_selected = not self.is_post_query_selected
        if self.is_post_query_selected is False:
            self.post_query_ref.set(0)