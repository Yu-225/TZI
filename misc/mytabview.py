import customtkinter as ctk


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Home")
        self.add("Lab1")
        self.add("Lab2")
        self.add("Lab3")
        self.add("Lab4")
        self.add("Lab5")
