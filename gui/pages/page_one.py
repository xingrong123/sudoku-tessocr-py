from tkinter import *
from .page import Page


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        blank_space = Frame(self, width=960, height=200)
        blank_space.grid(row=0, column=0, rowspan=4, columnspan=5)

        myLabel = Label(self, text="Do you want to screenshot?")
        myLabel.grid(row=5, column=2)

        yes_btn = Button(self, text="yes", padx=10,
                            pady=5, command=self.next_page)
        yes_btn.grid(row=6, column=2)