from tkinter import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

    def set_next_page(self, func):
        self.next_page_func = func

    def next_page(self):
        self.next_page_func()