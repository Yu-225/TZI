import base64
import tempfile

import pyperclip

from modules.RSA import RSA
from modules.RC5 import RC5
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import os
from threading import Thread
import time


class DrawLab4(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # A
        self.speedtest_file = None
        self.file_extension = None
        self.output_folder = './RSA/output'
        self.file_to_enc = None
        self.file_to_dec = None
        self.keys_folder_path = './RSA/key_folder'
        self.public_key_path = None
        self.private_key_path = None


        # Create tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.add('Keys')
        self.tab_view.add('Encrypt')
        self.tab_view.add('Decrypt')
        self.tab_view.add('Speedtest')
        self.tab_view.pack(padx=0, pady=0, expand=True, fill=ctk.BOTH)

        # CREATE KEYS
        # frame path
        self.key_frame_path = ctk.CTkFrame(self.tab_view.tab('Keys'))
        self.key_frame_path.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.k_public_key_label1 = ctk.CTkLabel(self.key_frame_path, text="Public key File: ")
        self.k_public_key_label1.pack(padx=0, pady=(10, 0), expand=True)
        self.k_public_key_label = ctk.CTkLabel(self.key_frame_path, text=".....")
        self.k_public_key_label.pack(padx=0, pady=(0, 5), expand=True)

        self.k_private_key_label1 = ctk.CTkLabel(self.key_frame_path, text="Private key File: ")
        self.k_private_key_label1.pack(padx=0, pady=(5, 0), expand=True)
        self.k_private_key_label = ctk.CTkLabel(self.key_frame_path, text=".....")
        self.k_private_key_label.pack(padx=0, pady=(0, 10), expand=True)


        # frame btns
        self.key_frame_btns = ctk.CTkFrame(self.tab_view.tab('Keys'))
        self.key_frame_btns.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        self.key_frame_btns.grid_columnconfigure((0, 1), weight=1)
        self.key_frame_btns.grid_rowconfigure((0, 1), weight=1)

        self.button_open_public_key = ctk.CTkButton(self.key_frame_btns, text="Open Public Key", command=self.select_public_key)
        self.button_open_public_key.grid(row=0, column=0, padx=10, pady=10, sticky='nwes')

        self.button_open_private_key = ctk.CTkButton(self.key_frame_btns, text="Open Private Key",  command=self.select_private_key)
        self.button_open_private_key.grid(row=0, column=1, padx=10, pady=10, sticky='nwes')

        self.button_create_keys = ctk.CTkButton(self.key_frame_btns, text="Create keys", command=self.create_keys)
        self.button_create_keys.grid(row=1, column=0, padx=10, pady=10, sticky='nwes')

        self.button_open_key_folder = ctk.CTkButton(self.key_frame_btns, text="Open key folder", command=self.open_key_folder)
        self.button_open_key_folder.grid(row=1, column=1, padx=10, pady=10, sticky='nwes')


        # TEXT ENC
        self.enc_frame_text = ctk.CTkFrame(self.tab_view.tab('Encrypt'))
        # self.enc_frame_text.configure(fg_color="blue")  # transparent
        self.enc_frame_text.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.enc_textbox_input = ctk.CTkTextbox(self.enc_frame_text, height=100)
        self.enc_textbox_input.insert("0.0", "Input")
        self.enc_textbox_input.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # text output
        self.enc_textbox_output = ctk.CTkTextbox(self.enc_frame_text, height=100)
        self.enc_textbox_output.insert("0.0", "Output")
        self.enc_textbox_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)
        self.enc_textbox_output.configure(state='disabled')

        # frame for buttons
        self.enc_button_frame_text = ctk.CTkFrame(self.enc_frame_text)
        self.enc_button_frame_text.configure(fg_color="transparent")
        self.enc_button_frame_text.pack(padx=0, pady=0, expand=True)
        self.enc_button_frame_text.grid_columnconfigure((0, 1, 2), weight=1)
        # button encrypt
        self.enc_button_encrypt_text = ctk.CTkButton(self.enc_button_frame_text, text="Encrypt text", command=self.enc_encrypt_text)
        self.enc_button_encrypt_text.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button copy
        self.enc_button_copy_text = ctk.CTkButton(self.enc_button_frame_text, text="Copy output", command=self.enc_copy_output)
        self.enc_button_copy_text.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.enc_button_paste_text = ctk.CTkButton(self.enc_button_frame_text, text="Paste input", command=self.enc_paste_input)
        self.enc_button_paste_text.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')

        # FILE ENC
        self.enc_frame_file = ctk.CTkFrame(self.tab_view.tab('Encrypt'))
        # self.enc_frame_file.configure(fg_color="red")  # transparent
        self.enc_frame_file.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        # self.enc_frame_file.grid_rowconfigure((0, 1, 2), weight=1)

        self.enc_file_to_enc_label1 = ctk.CTkLabel(self.enc_frame_file, text="Openned File: ")
        self.enc_file_to_enc_label1.pack(padx=0, pady=0, expand=True)
        self.enc_file_to_enc_label = ctk.CTkLabel(self.enc_frame_file, text=". . . . .")
        self.enc_file_to_enc_label.pack(padx=0, pady=0, expand=True)


        # frame for buttons
        self.enc_button_frame_file = ctk.CTkFrame(self.enc_frame_file)
        self.enc_button_frame_file.configure(fg_color="transparent")
        self.enc_button_frame_file.pack(padx=0, pady=0, expand=True)
        self.enc_button_frame_file.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # button encrypt
        self.enc_button_encrypt_file = ctk.CTkButton(self.enc_button_frame_file, text="Encrypt file", command=self.enc_encrypt_file)
        self.enc_button_encrypt_file.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.enc_button_select_file_to_enc = ctk.CTkButton(self.enc_button_frame_file, text="Select File", command=self.enc_select_file)
        self.enc_button_select_file_to_enc.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.enc_button_open_folder = ctk.CTkButton(self.enc_button_frame_file, text="Open folder", command=self.enc_open_folder)
        self.enc_button_open_folder.grid(row=0, column=3, padx=5, pady=0, sticky='nwes')


        # TEXT DEC
        self.dec_frame_text = ctk.CTkFrame(self.tab_view.tab('Decrypt'))
        # self.enc_frame_text.configure(fg_color="blue")  # transparent
        self.dec_frame_text.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.dec_textbox_input = ctk.CTkTextbox(self.dec_frame_text, height=100)
        self.dec_textbox_input.insert("0.0", "Input")
        self.dec_textbox_input.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # text output
        self.dec_textbox_output = ctk.CTkTextbox(self.dec_frame_text, height=100)
        self.dec_textbox_output.insert("0.0", "Output")
        self.dec_textbox_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)
        self.dec_textbox_output.configure(state='disabled')

        # frame for buttons
        self.dec_button_frame_text = ctk.CTkFrame(self.dec_frame_text)
        self.dec_button_frame_text.configure(fg_color="transparent")
        self.dec_button_frame_text.pack(padx=0, pady=0, expand=True)
        self.dec_button_frame_text.grid_columnconfigure((0, 1, 2), weight=1)
        # button encrypt
        self.dec_button_encrypt_text = ctk.CTkButton(self.dec_button_frame_text, text="Decrypt text", command=self.dec_decrypt_text)
        self.dec_button_encrypt_text.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button copy
        self.dec_button_copy_text = ctk.CTkButton(self.dec_button_frame_text, text="Copy output", command=self.dec_copy_output)
        self.dec_button_copy_text.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.dec_button_paste_text = ctk.CTkButton(self.dec_button_frame_text, text="Paste input", command=self.dec_paste_input)
        self.dec_button_paste_text.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')

        # FILE DEC
        self.dec_frame_file = ctk.CTkFrame(self.tab_view.tab('Decrypt'))
        # self.enc_frame_file.configure(fg_color="red")  # transparent
        self.dec_frame_file.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        # self.enc_frame_file.grid_rowconfigure((0, 1, 2), weight=1)

        self.dec_file_to_dec_label1 = ctk.CTkLabel(self.dec_frame_file, text="Openned File: ")
        self.dec_file_to_dec_label1.pack(padx=0, pady=0, expand=True)
        self.dec_file_to_dec_label = ctk.CTkLabel(self.dec_frame_file, text=". . . . .")
        self.dec_file_to_dec_label.pack(padx=0, pady=0, expand=True)


        # frame for buttons
        self.dec_button_frame_file = ctk.CTkFrame(self.dec_frame_file)
        self.dec_button_frame_file.configure(fg_color="transparent")
        self.dec_button_frame_file.pack(padx=0, pady=0, expand=True)
        self.dec_button_frame_file.grid_columnconfigure((0, 1, 2), weight=1)

        # button encrypt
        self.dec_button_encrypt_file = ctk.CTkButton(self.dec_button_frame_file, text="Decrypt file", command=self.dec_deccrypt_file)
        self.dec_button_encrypt_file.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.dec_button_select_file_to_dec = ctk.CTkButton(self.dec_button_frame_file, text="Select File", command=self.dec_select_file)
        self.dec_button_select_file_to_dec.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.dec_button_open_folder = ctk.CTkButton(self.dec_button_frame_file, text="Open folder", command=self.dec_open_folder)
        self.dec_button_open_folder.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')

        # SPEEDTEST
        self.spt_frame = ctk.CTkFrame(self.tab_view.tab('Speedtest'))
        self.spt_frame.configure(fg_color="transparent")  # transparent
        self.spt_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        self.spt_frame.grid_columnconfigure((0, 1), weight=1)

        # RSA
        self.spt_frame_rsa = ctk.CTkFrame(self.spt_frame)
        self.spt_frame_rsa.grid(row=0, column=0, padx=0, pady=0, sticky='nwes')

        self.spt_frame_rsa_label = ctk.CTkLabel(self.spt_frame_rsa, text="RSA")
        self.spt_frame_rsa_label.pack(padx=10, pady=10, expand=True, fill=ctk.BOTH)
        self.spt_frame_rsa_time = ctk.CTkTextbox(self.spt_frame_rsa, height=42)
        self.spt_frame_rsa_time.configure(state='disabled')
        self.spt_frame_rsa_time.pack(padx=10, pady=10)

        # RC5
        self.spt_frame_rc5 = ctk.CTkFrame(self.spt_frame)
        self.spt_frame_rc5.grid(row=0, column=1, padx=0, pady=0, sticky='nwes')

        self.spt_frame_rc5_label = ctk.CTkLabel(self.spt_frame_rc5, text="RC5")
        self.spt_frame_rc5_label.pack(padx=10, pady=10, expand=True, fill=ctk.BOTH)
        self.spt_frame_rc5_time = ctk.CTkTextbox(self.spt_frame_rc5, height=42)
        self.spt_frame_rc5_time.configure(state='disabled')
        self.spt_frame_rc5_time.pack(padx=10, pady=10)

        # BTN
        self.spt_frame_btn = ctk.CTkFrame(self.spt_frame)
        self.spt_frame_btn.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nwes')
        self.spt_frame_file_label = ctk.CTkLabel(self.spt_frame_btn, text="File:")
        self.spt_frame_file_label.pack(padx=10, pady=10, expand=True, fill=ctk.BOTH)
        self.spt_frame_file_size = ctk.CTkLabel(self.spt_frame_btn, text="Size:")
        self.spt_frame_file_size.pack(padx=10, pady=10, expand=True, fill=ctk.BOTH)
        # button open file
        self.spt_open_file = ctk.CTkButton(self.spt_frame_btn, text="Open file", command=self.spt_open_file)
        self.spt_open_file.pack(padx=10, pady=10, expand=True)
        # button encrypt
        self.spt_start1 = ctk.CTkButton(self.spt_frame_btn, text="Start RSA test", command=self.spt_start1)
        self.spt_start1.pack(padx=10, pady=10, expand=True)
        self.spt_start2 = ctk.CTkButton(self.spt_frame_btn, text="Start RC5 test", command=self.spt_start2)
        self.spt_start2.pack(padx=10, pady=10, expand=True)

    def spt_open_file(self):
        self.speedtest_file = filedialog.askopenfilename()
        self.spt_frame_file_label.configure(text=f'File:\n{self.speedtest_file}')

        size = os.path.getsize(self.speedtest_file)
        if size < 1048576:
            self.spt_frame_file_size.configure(text=f'Size:\n{round(size / 1024, 2)} KB')
        else:
            self.spt_frame_file_size.configure(text=f'Size:\n{round(size / (1024 ** 2), 2)} MB')

    def spt_start1(self):
        Thread(target=self.spt_start_rsa).start()

    def spt_start2(self):
        Thread(target=self.spt_start_rc5).start()

    def spt_start_rsa(self):
        print('start rsa')
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

            rsa = RSA()

            start_time = time.time()
            rsa.encrypt_file(self.speedtest_file, temp_filename, self.public_key_path)
            end_time = time.time()

            print(f"RSA Done in {end_time - start_time} seconds")

            self.spt_frame_rsa_time.configure(state='normal')
            self.spt_frame_rsa_time.delete("0.0", "end")
            self.spt_frame_rsa_time.insert("0.0", f"{round(end_time - start_time, 3)} seconds")
            self.spt_frame_rsa_time.configure(state='disabled')

    def spt_start_rc5(self):
        print('start rc5')
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

            rc5 = RC5(64, 8, 32, 'MEOW')

            start_time = time.time()
            rc5.encrypt_file(self.speedtest_file, temp_filename)
            end_time = time.time()

            print(f"RC5 Done in {end_time - start_time} seconds")
            self.spt_frame_rc5_time.configure(state='normal')
            self.spt_frame_rc5_time.delete("0.0", "end")
            self.spt_frame_rc5_time.insert("0.0", f"{round(end_time - start_time, 3)} seconds")
            self.spt_frame_rc5_time.configure(state='disabled')

    def select_public_key(self):
        self.public_key_path = filedialog.askopenfilename()
        self.k_public_key_label.configure(text=self.public_key_path)

    def select_private_key(self):
        self.private_key_path = filedialog.askopenfilename()
        self.k_private_key_label.configure(text=self.private_key_path)

    def create_keys(self):
        msg = CTkMessagebox(title="Generate new key pair",
                            message="Make sure you keep the keys in a safe place.\nGenerating new keys will overwrite previous ones.\nContinue?",
                            icon="question", option_1="Cancel", option_2="Continue")

        response = msg.get()
        if response == "Continue":
            rsa = RSA()
            rsa.generate_key_pair()
            CTkMessagebox(title="Generate new key pair",
                          message="The key pair is created and stored in the files 'private_key.pem' and 'public_key.pem'.",
                          icon="question", option_1="Thx")

    def open_key_folder(self):
        if self.keys_folder_path:
            os.startfile(self.keys_folder_path)
        else:
            print('floder not exsts')

    def enc_encrypt_text(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Choise key file",
                                 message='To begin, you need to select a public key file on the "Keys" page.',
                                 icon="info", option_1="Okay")

        plain_text = self.enc_textbox_input.get("0.0", "end")[:-1]

        rsa = RSA()
        cypher_text = rsa.encrypt_message(plain_text, self.public_key_path)
        cypher_text = base64.b64encode(cypher_text)

        self.enc_textbox_output.configure(state='normal')
        self.enc_textbox_output.delete("0.0", "end")
        self.enc_textbox_output.insert("0.0", cypher_text)
        self.enc_textbox_output.configure(state='disabled')

    def enc_copy_output(self):
        text_to_copy = self.enc_textbox_output.get("0.0", "end")[:-1]
        pyperclip.copy(text_to_copy)

        CTkMessagebox(message="Output successfully copied to clipboard.",
                      icon="check", option_1="Thanks")

    def enc_paste_input(self):
        text_to_paste = pyperclip.paste()
        self.enc_textbox_input.delete("0.0", "end")
        self.enc_textbox_input.insert("0.0", text_to_paste)

    def enc_encrypt_file(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Chose key file",
                                 message='To begin, you need to select a public key file on the "Keys" page.',
                                 icon="info", option_1="Okay")
        if not self.file_to_enc:
            return CTkMessagebox(title="Chose file",
                                 message='First, you need to select the file to be encrypted.',
                                 icon="info", option_1="Okay")

        rsa = RSA()
        output_file = self.output_folder + "/encrypted.bin"
        print(output_file)
        rsa.encrypt_file(self.file_to_enc, output_file, self.public_key_path)
        CTkMessagebox(title="Done",
                      message='Encrypted.',
                      icon="info", option_1="Okay")

    def enc_select_file(self):
        self.file_to_enc = filedialog.askopenfilename()
        self.file_extension = os.path.splitext(self.file_to_enc)[1]
        self.enc_file_to_enc_label.configure(text=self.file_to_enc)

    def enc_open_folder(self):
        if self.output_folder:
            os.startfile(self.output_folder)
        else:
            print('floder not exsts')

    def dec_decrypt_text(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Chose key file",
                                 message='To begin, you need to select a private key file on the "Keys" page.',
                                 icon="info", option_1="Okay")

        cypher_text = self.dec_textbox_input.get("0.0", "end")[:-1]
        cypher_text = base64.b64decode(cypher_text)

        rsa = RSA()
        plain_text = rsa.decrypt_message(cypher_text, self.private_key_path)

        self.dec_textbox_output.configure(state='normal')
        self.dec_textbox_output.delete("0.0", "end")
        self.dec_textbox_output.insert("0.0", plain_text)
        self.dec_textbox_output.configure(state='disabled')

    def dec_copy_output(self):
        text_to_copy = self.dec_textbox_output.get("0.0", "end")[:-1]
        pyperclip.copy(text_to_copy)

        CTkMessagebox(message="Output successfully copied to clipboard.",
                      icon="check", option_1="Thanks")

    def dec_paste_input(self):
        text_to_paste = pyperclip.paste()
        self.dec_textbox_input.delete("0.0", "end")
        self.dec_textbox_input.insert("0.0", text_to_paste)

    def dec_deccrypt_file(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Chose key file",
                                 message='To begin, you need to select a private key file on the "Keys" page.',
                                 icon="info", option_1="Okay")
        if not self.file_to_enc:
            return CTkMessagebox(title="Chose file",
                                 message='First, you need to select the file that needs to be decrypted.',
                                 icon="info", option_1="Okay")

        rsa = RSA()
        output_file = self.output_folder + "/decrypted" + self.file_extension
        print(output_file)
        rsa.decrypt_file(self.file_to_dec, output_file, self.private_key_path)

    def dec_select_file(self):
        self.file_to_dec = filedialog.askopenfilename()
        self.dec_file_to_dec_label.configure(text=self.file_to_dec)

    def dec_open_folder(self):
        if self.output_folder:
            os.startfile(self.output_folder)
        else:
            print('floder not exsts')



