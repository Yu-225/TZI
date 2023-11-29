import os
import re
import customtkinter as ctk
from modules.RC5 import RC5
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import pyperclip
import base64


class DrawLab3(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.null_bits = None
        self.file_extension = None
        self.opened_file = None
        self.selected_folder = None
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Inputs field
        self.input_field_frame = ctk.CTkFrame(self)
        self.input_field_frame.configure(fg_color="transparent")  # transparent
        self.input_field_frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nwes')

        self.input_field_frame.grid_columnconfigure((0, 1), weight=1)
        self.input_field_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Word size
        self.w_label = ctk.CTkLabel(self.input_field_frame, text="World size ( 16 | 32 | 64 )")
        self.w_label.grid(row=0, column=0, padx=5, pady=0, sticky='e')
        # input
        self.w_input = ctk.CTkTextbox(self.input_field_frame, height=30)
        self.w_input.insert("0.0", "64")
        self.w_input.grid(row=0, column=1, padx=5, pady=0, sticky='w')

        # Rounds
        self.r_label = ctk.CTkLabel(self.input_field_frame, text="Rounds ( 0 - 255 )")
        self.r_label.grid(row=1, column=0, padx=5, pady=0, sticky='e')
        # input
        self.r_input = ctk.CTkTextbox(self.input_field_frame, height=30)
        self.r_input.insert("0.0", "8")
        self.r_input.grid(row=1, column=1, padx=5, pady=0, sticky='w')

        # Key bytes
        self.b_label = ctk.CTkLabel(self.input_field_frame, text="Key bytes ( 8 | 16 | 32 )")
        self.b_label.grid(row=2, column=0, padx=5, pady=0, sticky='e')
        # input
        self.b_input = ctk.CTkTextbox(self.input_field_frame, height=30)
        self.b_input.insert("0.0", "32")
        self.b_input.grid(row=2, column=1, padx=5, pady=0, sticky='w')

        # Key phrase
        self.key_phrase_label = ctk.CTkLabel(self.input_field_frame, text="Key phrase")
        self.key_phrase_label.grid(row=3, column=0, padx=5, pady=0, sticky='e')
        # input
        self.key_phrase_input = ctk.CTkTextbox(self.input_field_frame, height=30)
        self.key_phrase_input.insert("0.0", "q w e r t y")
        self.key_phrase_input.grid(row=3, column=1, padx=5, pady=0, sticky='w')



        # Create tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nwes')
        self.tab_view.add("Text")
        self.tab_view.add("File")

        # TEXT
        # text input
        self.textbox_input = ctk.CTkTextbox(self.tab_view.tab("Text"), height=100)
        self.textbox_input.insert("0.0", "Input")
        self.textbox_input.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        # frame for buttons
        self.button_frame_text = ctk.CTkFrame(self.tab_view.tab("Text"))
        self.button_frame_text.configure(fg_color="transparent")
        self.button_frame_text.pack(padx=5, pady=5, expand=True)
        self.button_frame_text.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # button encrypt
        self.button_encrypt = ctk.CTkButton(self.button_frame_text, text="Encrypt", command=self.text_encrypt)
        self.button_encrypt.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.button_decrypt = ctk.CTkButton(self.button_frame_text, text="Decrypt", command=self.text_decrypt)
        self.button_decrypt.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.button_copy = ctk.CTkButton(self.button_frame_text, text="Copy", command=self.text_copy)
        self.button_copy.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')
        # button copy
        self.button_paste = ctk.CTkButton(self.button_frame_text, text="Paste", command=self.text_paste)
        self.button_paste.grid(row=0, column=3, padx=5, pady=0, sticky='nwes')

        # text output
        self.textbox_output = ctk.CTkTextbox(self.tab_view.tab("Text"), height=100)
        self.textbox_output.insert("0.0", "Output")
        self.textbox_output.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        self.textbox_output.configure(state='disabled')


        # FILE
        # frame open file
        # self.file_frame = ctk.CTkFrame(self.tab_view.tab("File"))
        # # self.file_frame.configure(fg_color="red")
        # self.file_frame.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        # self.file_frame.grid_columnconfigure(0, weight=1)
        #
        # self.label_chose = ctk.CTkLabel(master=self.file_frame, text="Chose file")
        # self.label_chose.grid(row=0, column=0, padx=5, pady=5)
        #
        # self.button_open_file = ctk.CTkButton(master=self.file_frame, text="Open", command=self.choose_file)
        # self.button_open_file.grid(row=0, column=1, padx=5, pady=5)
        #
        # self.label_filepath = ctk.CTkLabel(master=self.file_frame, text="")
        # self.label_filepath.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 34))

        # frame for buttons
        self.button_frame_file = ctk.CTkFrame(self.tab_view.tab("File"))
        self.button_frame_file.configure(fg_color="transparent")
        self.button_frame_file.pack(padx=5, pady=5, expand=True)
        self.button_frame_file.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        # button encrypt
        self.button_open_file = ctk.CTkButton(self.button_frame_file, text="Open File", command=self.choose_file)
        self.button_open_file.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.button_open_file = ctk.CTkButton(self.button_frame_file, text="Select Folder", command=self.choose_folder)
        self.button_open_file.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.button_encrypt_file = ctk.CTkButton(self.button_frame_file, text="Encrypt", command=self.file_encrypt)
        self.button_encrypt_file.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')
        # button copy
        self.button_decrypt_file = ctk.CTkButton(self.button_frame_file, text="Decrypt", command=self.file_decrypt)
        self.button_decrypt_file.grid(row=0, column=3, padx=5, pady=0, sticky='nwes')
        # button copy
        self.button_paste_file = ctk.CTkButton(self.button_frame_file, text="Open Output", command=self.open_output_folder)
        self.button_paste_file.grid(row=0, column=4, padx=5, pady=0, sticky='nwes')

        # frame
        self.frame_file = ctk.CTkFrame(self.tab_view.tab("File"))
        # self.frame_file.configure(fg_color="transparent")
        self.frame_file.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        self.label_chose = ctk.CTkLabel(self.frame_file, text="Choose file")
        self.label_chose.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        self.chose_path = ctk.CTkLabel(self.frame_file, text="File path")
        self.chose_path.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        self.output_folder = ctk.CTkLabel(self.frame_file, text="Choose folder")
        self.output_folder.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

        self.folder_path = ctk.CTkLabel(self.frame_file, text="Folder path")
        self.folder_path.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)

    def load_preferences(self):
        try:
            text_to_encrypt = self.textbox_input.get("0.0", "end").encode('utf-8')[:-1]
            w = int(self.w_input.get("0.0", "end")[:-1])
            r = int(self.r_input.get("0.0", "end")[:-1])
            b = int(self.b_input.get("0.0", "end")[:-1])
            key_phrase = self.key_phrase_input.get("0.0", "end").encode('utf-8')[:-1]

        except ValueError as err:
            CTkMessagebox(title='Sorry', message="Something went wrong, check the parameters are correct.", option_1="Oh, okay")
            return

        if bool(re.compile('[а-яА-ЯїЇєЄ]').search(text_to_encrypt.decode())):
            CTkMessagebox(title='Sorry', message="Unfortunately, Cyrillic is not supported (((", option_1="Oh, okay")
            return

        if w not in [16, 32, 64]:
            CTkMessagebox(title='Sorry', message="World size only support 16, 32 or 64.", option_1="Oh, okay")
            return

        if r < 0 or r > 255:
            CTkMessagebox(title='Sorry', message="The number of rounds must be within 0 - 255.", option_1="Oh, okay")
            return

        if b not in [8, 16, 32]:
            CTkMessagebox(title='Sorry', message="Key size only support 8, 13 or 32.", option_1="Oh, okay")
            return

        return text_to_encrypt, w, r, b, key_phrase

    def text_encrypt(self):
        text_to_encrypt, w, r, b, key_phrase = self.load_preferences()

        rc5 = RC5(w, r, b, key_phrase)

        result = rc5.encrypt_bytes(text_to_encrypt)

        b64_result = base64.b64encode(result)

        self.textbox_output.configure(state='normal')
        self.textbox_output.delete("0.0", "end")
        self.textbox_output.insert("0.0", b64_result)
        self.textbox_output.configure(state='disabled')

    def text_decrypt(self):
        text_to_encrypt = base64.b64decode(self.textbox_input.get("0.0", "end").encode('utf-8')[:-1])
        w = int(self.w_input.get("0.0", "end")[:-1])
        r = int(self.r_input.get("0.0", "end")[:-1])
        b = int(self.b_input.get("0.0", "end")[:-1])
        key_phrase = self.key_phrase_input.get("0.0", "end").encode('utf-8')[:-1]
        print(text_to_encrypt, w, r, b, key_phrase)

        rc5 = RC5(w, r, b, key_phrase)

        result = rc5.decrypt_bytes(text_to_encrypt)

        print(result)

        self.textbox_output.configure(state='normal')
        self.textbox_output.delete("0.0", "end")
        self.textbox_output.insert("0.0", result)
        self.textbox_output.configure(state='disabled')


    def text_copy(self):
        text_to_copy = self.textbox_output.get("0.0", "end")[:-1]
        pyperclip.copy(text_to_copy)

        CTkMessagebox(message="Output successfully copied to clipboard.",
                      icon="check", option_1="Thanks")

    def text_paste(self):
        text_to_paste = pyperclip.paste()
        self.textbox_input.delete("0.0", "end")
        self.textbox_input.insert("0.0", text_to_paste)

    def choose_file(self):
        file_path = filedialog.askopenfilename()

        self.file_extension = os.path.splitext(file_path)[1]

        self.opened_file = file_path
        self.label_chose.configure(text="File Opened:")
        self.chose_path.configure(text=file_path)

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        self.selected_folder = folder_path
        self.output_folder.configure(text="Folder Selected:")
        self.folder_path.configure(text=folder_path)

    def open_output_folder(self):
        if self.selected_folder:
            os.startfile(self.selected_folder)
        else:
            print('floder not exsts')

    def file_encrypt(self):
        w = int(self.w_input.get("0.0", "end")[:-1])
        r = int(self.r_input.get("0.0", "end")[:-1])
        b = int(self.b_input.get("0.0", "end")[:-1])
        key_phrase = self.key_phrase_input.get("0.0", "end").encode('utf-8')[:-1]
        rc5 = RC5(w, r, b, key_phrase)

        file_to_encrypt = self.opened_file
        output_file = self.selected_folder + "/output_encrypted" + self.file_extension

        rc5.encrypt_file(file_to_encrypt, output_file)
        self.null_bits = rc5.nulbits

    def file_decrypt(self):
        w = int(self.w_input.get("0.0", "end")[:-1])
        r = int(self.r_input.get("0.0", "end")[:-1])
        b = int(self.b_input.get("0.0", "end")[:-1])
        key_phrase = self.key_phrase_input.get("0.0", "end").encode('utf-8')[:-1]
        rc5 = RC5(w, r, b, key_phrase)

        file_to_encrypt = self.opened_file
        output_file = self.selected_folder + "/output_decrypted" + self.file_extension

        rc5.decrypt_file(file_to_encrypt, output_file)

        self.cut_off_this_fucking_null_bits(output_file)

    def cut_off_this_fucking_null_bits(self, file):

        with open(file, 'rb') as f:
            data = f.read()
            for i in range(self.null_bits):
                data = data[:-1]

        with open(file, 'wb') as f:
            f.write(data)
