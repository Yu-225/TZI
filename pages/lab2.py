from modules.MD5 import MD5 as my_md5
from hashlib import md5 as hashlib_md5
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from tkinter import filedialog
import pyperclip
import time
import re
import os


class DrawLab2(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.lab = 'Lab 2'
        self.log_file_path = os.path.abspath('logs/lab2_log.txt')

        log_directory = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        self.opened_file = None
        self.grid_columnconfigure((0, 1), weight=1)

        # Text 2 MD5 frame
        self.text_2_md5_frame = ctk.CTkFrame(self)
        self.text_2_md5_frame.configure(fg_color="transparent")
        self.text_2_md5_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nwes')

        # Text to MD5 label
        self.label = ctk.CTkLabel(self.text_2_md5_frame, text="Text to MD5")
        self.label.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        # text input
        self.textbox_input = ctk.CTkTextbox(self.text_2_md5_frame, height=100)
        self.textbox_input.insert("0.0", "Input")
        self.textbox_input.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        # frame for buttons
        self.button_frame = ctk.CTkFrame(self.text_2_md5_frame)
        self.button_frame.configure(fg_color="transparent")
        self.button_frame.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure((0, 1), weight=1)

        # button encrypt
        self.button_encrypt = ctk.CTkButton(master=self.button_frame, text="Encrypt", command=self.encrypt_text)
        self.button_encrypt.grid(row=0, column=0, padx=(0, 5), pady=5)

        # button copy
        self.button_copy = ctk.CTkButton(master=self.button_frame, text="Copy hash", command=self.copy_hash)
        self.button_copy.grid(row=0, column=1, padx=(5, 0), pady=5)

        # button clear
        self.button_clear = ctk.CTkButton(master=self.button_frame, text="Clear", command=self.clear_text)
        self.button_clear.grid(row=1, column=0, padx=(0, 5), pady=5)

        # button AAA
        self.button_AAA = ctk.CTkButton(master=self.button_frame, text="Open logs",
                                        command=self.open_log_file)
        self.button_AAA.grid(row=1, column=1, padx=(5, 0), pady=5)

        # text output
        self.my_output = ctk.CTkLabel(self.text_2_md5_frame, text="My output")
        self.my_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.textbox_my_output = ctk.CTkTextbox(self.text_2_md5_frame, height=33)
        self.textbox_my_output.insert("0.0", "My output")
        self.textbox_my_output.pack(padx=5, pady=(0, 5), expand=True, fill=ctk.BOTH)
        self.textbox_my_output.configure(state='disabled')

        self.hashlib_output = ctk.CTkLabel(self.text_2_md5_frame, text="Hashlib output")
        self.hashlib_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.textbox_hashlib_output = ctk.CTkTextbox(self.text_2_md5_frame, height=33)
        self.textbox_hashlib_output.insert("0.0", "Hashlib output")
        self.textbox_hashlib_output.pack(padx=5, pady=(0, 5), expand=True, fill=ctk.BOTH)
        self.textbox_hashlib_output.configure(state='disabled')

        # File 2 MD5 frame
        self.file_2_md5_frame = ctk.CTkFrame(self)
        self.file_2_md5_frame.configure(fg_color="transparent")
        self.file_2_md5_frame.grid(row=0, column=1, padx=0, pady=0, sticky='nwes')

        # # # File Tab # # #
        self.label = ctk.CTkLabel(self.file_2_md5_frame, text="File to MD5")
        self.label.pack(padx=5, pady=5)

        # frame open file
        self.file_frame = ctk.CTkFrame(self.file_2_md5_frame)
        # self.file_frame.configure(fg_color="red")
        self.file_frame.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.label_chose = ctk.CTkLabel(master=self.file_frame, text="Chose file")
        self.label_chose.grid(row=0, column=0, padx=5, pady=5)

        self.button_open_file = ctk.CTkButton(master=self.file_frame, text="Open", command=self.open_file)
        self.button_open_file.grid(row=0, column=1, padx=5, pady=5)

        self.label_filepath = ctk.CTkLabel(master=self.file_frame, text="")
        self.label_filepath.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 34))

        # frame for buttons
        self.button_file_frame = ctk.CTkFrame(self.file_2_md5_frame)
        self.button_file_frame.configure(fg_color="transparent")
        self.button_file_frame.pack(padx=0, pady=0, expand=True, fill=ctk.BOTH)
        self.button_file_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_file_frame.grid_rowconfigure((0, 1), weight=1)

        # button encrypt
        self.button_encrypt = ctk.CTkButton(master=self.button_file_frame, text="Encrypt", command=self.encrypt_file)
        self.button_encrypt.grid(row=0, column=0, padx=5, pady=5)

        # button copy
        self.button_copy = ctk.CTkButton(master=self.button_file_frame, text="Copy hash", command=self.copy_hash_file)
        self.button_copy.grid(row=0, column=1, padx=5, pady=5)

        # button clear
        self.button_encrypt = ctk.CTkButton(master=self.button_file_frame, text="Clear", command=self.clear_text_file)
        self.button_encrypt.grid(row=1, column=0, padx=5, pady=5)

        # button cat
        self.button_copy = ctk.CTkButton(master=self.button_file_frame, text="Copy hash", command=self.copy_hash)
        self.button_copy.grid(row=1, column=1, padx=5, pady=5)

        # file output
        self.my_output_file = ctk.CTkLabel(self.file_2_md5_frame, text="My output")
        self.my_output_file.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.textbox_my_output_file = ctk.CTkTextbox(self.file_2_md5_frame, height=30)
        self.textbox_my_output_file.insert("0.0", "My output")
        self.textbox_my_output_file.pack(padx=5, pady=(0, 5), expand=True, fill=ctk.BOTH)
        self.textbox_my_output_file.configure(state='disabled')

        self.hashlib_output_file = ctk.CTkLabel(self.file_2_md5_frame, text="Hashlib output")
        self.hashlib_output_file.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.textbox_hashlib_output_file = ctk.CTkTextbox(self.file_2_md5_frame, height=30)
        self.textbox_hashlib_output_file.insert("0.0", "Hashlib output")
        self.textbox_hashlib_output_file.pack(padx=5, pady=(0, 5), expand=True, fill=ctk.BOTH)
        self.textbox_hashlib_output_file.configure(state='disabled')

    def open_file(self):
        file_path = filedialog.askopenfilename()
        print(type(os.path.getsize(file_path)), os.path.getsize(file_path))
        if os.path.getsize(file_path) >= 10000000:
            CTkMessagebox(title='Sorry', message="Max file size 10 megabytes", option_1="Oh, okay")
            return

        self.opened_file = file_path
        self.label_chose.configure(text="File Opened:")
        self.label_filepath.configure(text=file_path)
        self.log('File opened', file_path)

    def encrypt_file(self):
        if not self.opened_file:
            self.textbox_my_output_file.configure(state='normal')
            self.textbox_hashlib_output_file.configure(state='normal')
            self.textbox_my_output_file.delete("0.0", "end")
            self.textbox_hashlib_output_file.delete("0.0", "end")
            self.textbox_my_output_file.insert("0.0", "First choose a file!")
            self.textbox_hashlib_output_file.insert("0.0", "First choose a file!")
            self.textbox_my_output_file.configure(state='disabled')
            self.textbox_hashlib_output_file.configure(state='disabled')
            self.log('Error', 'First choose a file!')

        else:

            # my md5
            my_H = my_md5()
            with open(self.opened_file, 'rb') as file:
                while True:
                    chunk = file.read()
                    if not chunk:
                        break
                    my_H.update(chunk)

            hsh = my_H.hexdigest()

            self.textbox_my_output_file.configure(state='normal')
            self.textbox_my_output_file.delete("0.0", "end")
            self.textbox_my_output_file.insert("0.0", hsh)
            self.textbox_my_output_file.configure(state='disabled')

            # Hashlib
            hl_H = hashlib_md5()
            with open(self.opened_file, 'rb') as file:
                while True:
                    data = file.read(512)
                    if not data:
                        break
                    hl_H.update(data)

            result_hl_hash = hl_H.hexdigest().upper()
            self.textbox_hashlib_output_file.configure(state='normal')
            self.textbox_hashlib_output_file.delete("0.0", "end")
            self.textbox_hashlib_output_file.insert("0.0", result_hl_hash)
            self.textbox_hashlib_output_file.configure(state='disabled')
            self.log('Hash File', f'{hsh} - {result_hl_hash}')

    def encrypt_text(self):
        text_to_encrypt = self.textbox_input.get("0.0", "end").encode('utf-8')
        text_to_my_md5 = self.textbox_input.get("0.0", "end")[:-1]
        text_to_encrypt = text_to_encrypt[:-1]

        def has_cyrillic(text):
            cyrillic_pattern = re.compile('[а-яА-ЯїЇєЄ]')
            return bool(cyrillic_pattern.search(text))

        if has_cyrillic(text_to_my_md5):
            CTkMessagebox(title='Sorry', message="Unfortunately, Cyrillic is not supported (((", option_1="Oh, okay")
            return

        # my md5
        my_H = my_md5()
        encrypted_text_my_md5 = my_H.hash(text_to_my_md5)

        # hashlib
        hl_H = hashlib_md5()
        hl_H.update(text_to_encrypt)
        encrypted_text_hashlib = hl_H.hexdigest().upper()

        if encrypted_text_my_md5 == encrypted_text_hashlib:
            CTkMessagebox(title='Yay :3', message="Successful", icon="check", option_1="Ok")

        self.textbox_my_output.configure(state='normal')
        self.textbox_hashlib_output.configure(state='normal')

        self.textbox_my_output.delete("0.0", "end")
        self.textbox_my_output.insert("0.0", encrypted_text_my_md5)

        self.textbox_hashlib_output.delete("0.0", "end")
        self.textbox_hashlib_output.insert("0.0", encrypted_text_hashlib)

        self.textbox_my_output.configure(state='disabled')
        self.textbox_hashlib_output.configure(state='disabled')

        self.log('Hash Text', f'H({text_to_encrypt.decode("utf-8")}) = {encrypted_text_my_md5}')

    def copy_hash(self):
        text_to_copy = self.textbox_my_output.get("0.0", "end")
        text_to_copy = text_to_copy[:-1]
        pyperclip.copy(text_to_copy)
        CTkMessagebox(message="Hash successfully copied to clipboard.",
                      icon="check", option_1="Thanks")

        self.log('Copy hash', text_to_copy)

    def copy_hash_file(self):
        text_to_copy = self.textbox_my_output_file.get("0.0", "end")
        text_to_copy = text_to_copy[:-1]
        pyperclip.copy(text_to_copy)
        CTkMessagebox(message="Hash successfully copied to clipboard.",
                      icon="check", option_1="Thanks")

        self.log('Copy hash', text_to_copy)

    def clear_text(self):
        self.textbox_my_output.configure(state='normal')
        self.textbox_hashlib_output.configure(state='normal')
        self.textbox_input.delete("0.0", "end")
        self.textbox_my_output.delete("0.0", "end")
        self.textbox_hashlib_output.delete("0.0", "end")
        self.textbox_my_output.configure(state='disabled')
        self.textbox_hashlib_output.configure(state='disabled')
        self.log('Clear', 'Text')

    def clear_text_file(self):
        self.opened_file = None
        self.label_chose.configure(text='Chose file')
        self.label_filepath.configure(text='')

        self.textbox_my_output_file.configure(state='normal')
        self.textbox_hashlib_output_file.configure(state='normal')

        self.textbox_my_output_file.delete("0.0", "end")
        self.textbox_hashlib_output_file.delete("0.0", "end")

        self.textbox_my_output_file.configure(state='disabled')
        self.textbox_hashlib_output_file.configure(state='disabled')
        self.log('Clear', 'File')

    def log(self, action, result) -> None:
        t = time.strftime("%d.%m.%Y - %H:%M:%S", time.localtime())
        text = f'[ {t} ]\t{action}\t{result}'
        with open(self.log_file_path, 'a') as file:
            file.write(text + '\n')

    def open_log_file(self):
        os.startfile(self.log_file_path)
