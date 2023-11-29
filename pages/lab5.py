import customtkinter as ctk
from PIL import Image


class DrawLab5(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tbc_image = ctk.CTkImage(Image.open('img/tbc.png'), size=(400, 200))
        self.tbc_label = ctk.CTkLabel(self, image=self.tbc_image, text='')
        self.tbc_label.pack()
