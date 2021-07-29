from tkinter import *
from .page import Page
import os
from os.path import isfile, join


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        blank_space_1 = Frame(self, width=960, height=100)
        blank_space_1.grid(row=0, column=0, columnspan=3)
        instruction_label = Label(self, text="Instructions")
        instruction_label.grid(row=1, column=1)

        blank_space_2 = Frame(self, width=960, height=50)
        blank_space_2.grid(row=2, column=0, columnspan=3)

        instruction_1 = Label(
            self, text="Use snipping tool by clicking the button below \nto take a screenshot of the puzzle and save it in the directory:")
        instruction_1.grid(row=3, column=1)
        isntruction_2 = Label(
            self, text= os.getcwd() + "\\images")
        isntruction_2.grid(row=4, column=1)
        instruction_3 = Label(
            self, text="Make sure that the image only contains the puzzle")
        instruction_3.grid(row=5, column=1)
        blank_space_3 = Label(self, text="")
        blank_space_3.grid(row=6, column=0, rowspan=2, columnspan=3)

        open_ss_label = Label(self, text="open snipping tool")
        open_ss_label.grid(row=8, column=1)

        open_ss_btn = Button(
            self, text="open", padx=10, pady=5, command=self.scan_images)
        open_ss_btn.grid(row=9, column=1)

        self.next_btn_label = Label(self, text="Proceed to scan image(s)")
        self.next_btn = Button(self, text="next", padx=10,
                               pady=5, command=self.next_page)

    def scan_images(self):
        mypath = "./images"
        onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
        os.system("SnippingTool")
        onlyfiles2 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

        new_ss_list = []
        for new_ss in onlyfiles2:
            if new_ss not in onlyfiles:
                new_ss_list.append(new_ss)

        if (len(new_ss_list) > 0):
            is_valid_sudoku_image = self.set_images(new_ss_list)
            if is_valid_sudoku_image is True:
                blank_space_4 = Label(self, text="")
                blank_space_4.grid(row=10, column=0, rowspan=2, columnspan=3)
                self.next_btn_label.grid(row=12, column=1)
                self.next_btn.grid(row=13, column=1)


    def set_set_images(self, func):
        self.set_images_func = func

    def set_images(self, images):
        return self.set_images_func(images)