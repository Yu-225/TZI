from misc.mytabview import TabView
from pages.home import DrawHome
from pages.lab1 import DrawLab1
from pages.lab2 import DrawLab2
from pages.lab3 import DrawLab3
from pages.lab4 import DrawLab4
from pages.lab5 import DrawLab5

import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ТЗІ")
        self.geometry(f"{560}x{650}")
        self.resizable(False, False)
        self.iconbitmap('img/icon.ico')

        # Create tab view
        self.tab_view = TabView(master=self)
        self.tab_view.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # Home
        self.homepage = DrawHome(self.tab_view.tab("Home"), fg_color='transparent')
        self.homepage.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # LAB 1
        self.lab1page = DrawLab1(self.tab_view.tab('Lab1'), fg_color='transparent')
        self.lab1page.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # LAB 2
        self.lab2page = DrawLab2(self.tab_view.tab('Lab2'), fg_color='transparent')
        self.lab2page.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # LAB 3
        self.lab3page = DrawLab3(self.tab_view.tab('Lab3'), fg_color='transparent')
        self.lab3page.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # LAB 4
        self.lab4page = DrawLab4(self.tab_view.tab('Lab4'), fg_color='transparent')
        self.lab4page.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # LAB 5
        self.lab5page = DrawLab5(self.tab_view.tab('Lab5'), fg_color='transparent')
        self.lab5page.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')


if __name__ == "__main__":
    app = App()
    app.mainloop()
