from tkinter import *
from .page import Page
import os

class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.query_label = None
        self.sql_query = ""
        self.is_send_query = False

    def set_query(self, query, send):
        self.sql_query = query
        self.is_send_query = send

    # override no decorator
    def show(self):
        blank_space = Frame(self, width=960, height=20)
        blank_space.grid(row=0, column=0, columnspan=3)
        self.query_label = Label(self, text=self.sql_query, wraplength=600, justify=LEFT)
        self.query_label.grid(row=1, column=1)
        Frame(self, width=960, height=20).grid(row=2, column=0, columnspan=3)
        Label(self, text="sql file can be found in " + os.getcwd()).grid(row=3, column=0, columnspan=3)
        super().show()
        f = open("sudoku.sql","a")
        f.write(self.sql_query + "\n")
        f.close()
        if self.is_send_query is True:
            Label(self, text="query has been sent to heroku db").grid(row=4, column=1)
            os.system("heroku pg:psql -- app sudoku-react-application < sudoku.sql")
            # os.remove("sudoku.sql")
        print("done")