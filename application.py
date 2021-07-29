from tkinter import *
from gui.pages.page_one import Page1
from gui.pages.page_two import Page2
from gui.pages.page_three import Page3
from gui.pages.page_four import Page4


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0)
        self.create_widgets()

    def create_widgets(self):
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        container = Frame(self, width=960, height=500,)
        container.grid(row=1, column=0, columnspan=2)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p1.set_next_page(p2.show)
        p2.set_next_page(p3.show)
        p3.set_next_page(p4.show)

        p2.set_set_images(p3.set_images)
        p3.set_set_query(p4.set_query)

        home = Button(self, text="home", command=p1.show, padx=10, pady=5)
        home.grid(row=3, column=0)

        quit = Button(self, text="QUIT", fg="red", padx=10,
                      pady=5, command=self.master.destroy)
        quit.grid(row=3, column=1)

        p1.show()


def main():
    root = Tk()
    app = Application(master=root)
    app.master.title("My Sudoku Scanner Application")
    app.master.minsize(960, 540)
    app.master.maxsize(960, 540)

    app.mainloop()


if __name__ == "__main__":
    main()