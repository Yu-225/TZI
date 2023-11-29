import customtkinter as ctk
import webbrowser
import subprocess


class DrawHome(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.url = "https://send.monobank.ua/jar/7ECG1LrAcY"

        self.appearense = 'dark'

        self.label_chose = ctk.CTkLabel(self, text="Home pages")
        self.label_chose.pack()

        self.btn = ctk.CTkButton(self, text="Change theme", command=self.change_app_appearence)
        self.btn.pack(padx=5, pady=15)

        # Button Donate
        self.btn_donate = ctk.CTkButton(self, text="Donate (Mono)", command=self.donate)
        self.btn_donate.pack(padx=5, pady=15)

        # Button Donut
        self.btn_donut = ctk.CTkButton(self, text="Donut", command=self.donut)
        self.btn_donut.pack(padx=5, pady=15)

    def change_app_appearence(self):
        if self.appearense == 'dark':
            ctk.set_appearance_mode('Light')
            # self.tab_view.configure(True, bg_color='#dbdbdb')
            self.appearense = 'light'
        else:
            ctk.set_appearance_mode('Dark')
            # self.tab_view.configure(True, bg_color='#2b2b2b')
            self.appearense = 'dark'

    def donate(self):
        webbrowser.open_new(self.url)

    def donut(self):
        subprocess.Popen('python ./misc/donut.py', shell=True)
