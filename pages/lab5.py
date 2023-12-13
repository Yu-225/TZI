import os
from tkinter import filedialog

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from modules.DSS import DSS
import pyperclip


class DrawLab5(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.oppened_file_to_sign = None
        self.oppened_file_to_verify = None
        self.oppened_signature_file = None

        self.keys_folder_path = os.path.join('DSS', 'key_folder')
        self.output_folder_path = os.path.join('DSS', 'output')
        self.public_key_path = None  # os.path.join('DSS', 'key_folder', 'dss_public_key.pem')
        self.private_key_path = None  # os.path.join('DSS', 'key_folder', 'dss_private_key.pem')

        # Create tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.add('Keys')
        self.tab_view.add('Signature')
        self.tab_view.add('Verify')
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

        self.button_open_public_key = ctk.CTkButton(self.key_frame_btns, text="Open Public Key",
                                                    command=self.select_public_key)
        self.button_open_public_key.grid(row=0, column=0, padx=10, pady=10, sticky='nwes')

        self.button_open_private_key = ctk.CTkButton(self.key_frame_btns, text="Open Private Key",
                                                     command=self.select_private_key)
        self.button_open_private_key.grid(row=0, column=1, padx=10, pady=10, sticky='nwes')

        self.button_create_keys = ctk.CTkButton(self.key_frame_btns, text="Create keys", command=self.create_keys)
        self.button_create_keys.grid(row=1, column=0, padx=10, pady=10, sticky='nwes')

        self.button_open_key_folder = ctk.CTkButton(self.key_frame_btns, text="Open key folder",
                                                    command=self.open_key_folder)
        self.button_open_key_folder.grid(row=1, column=1, padx=10, pady=10, sticky='nwes')


        # SIGNATURE
        self.sgn_frame_text = ctk.CTkFrame(self.tab_view.tab('Signature'))
        # self.sgn_frame_text.configure(fg_color="blue")  # transparent
        self.sgn_frame_text.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        self.sgn_textbox_input = ctk.CTkTextbox(self.sgn_frame_text, height=100)
        self.sgn_textbox_input.insert("0.0", "Message")
        self.sgn_textbox_input.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # text output
        self.sgn_textbox_output = ctk.CTkTextbox(self.sgn_frame_text, height=100)
        self.sgn_textbox_output.insert("0.0", "Signature")
        self.sgn_textbox_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)
        self.sgn_textbox_output.configure(state='disabled')

        # frame for buttons
        self.sgn_button_frame_text = ctk.CTkFrame(self.sgn_frame_text)
        self.sgn_button_frame_text.configure(fg_color="transparent")
        self.sgn_button_frame_text.pack(padx=0, pady=0, expand=True)
        self.sgn_button_frame_text.grid_columnconfigure((0, 1, 2), weight=1)
        # button sgnrypt
        self.sgn_button_sgnrypt_text = ctk.CTkButton(self.sgn_button_frame_text, text="Signature text",
                                                     command=self.sgn_signature_text)
        self.sgn_button_sgnrypt_text.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button copy
        self.sgn_button_copy_text = ctk.CTkButton(self.sgn_button_frame_text, text="Copy msg + sgn",
                                                  command=self.sgn_copy_output)
        self.sgn_button_copy_text.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.sgn_button_paste_text = ctk.CTkButton(self.sgn_button_frame_text, text="Paste msg",
                                                   command=self.sgn_paste_input)
        self.sgn_button_paste_text.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')

        # FILE sign
        self.sgn_frame_file = ctk.CTkFrame(self.tab_view.tab('Signature'))
        # self.sgn_frame_file.configure(fg_color="red")  # transparent
        self.sgn_frame_file.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        # self.sgn_frame_file.grid_rowconfigure((0, 1, 2), weight=1)

        self.sgn_file_to_sgn_label1 = ctk.CTkLabel(self.sgn_frame_file, text="Openned File: ")
        self.sgn_file_to_sgn_label1.pack(padx=0, pady=0, expand=True)
        self.sgn_file_to_sgn_label = ctk.CTkLabel(self.sgn_frame_file, text=". . . . .")
        self.sgn_file_to_sgn_label.pack(padx=0, pady=0, expand=True)

        # frame for buttons
        self.sgn_button_frame_file = ctk.CTkFrame(self.sgn_frame_file)
        self.sgn_button_frame_file.configure(fg_color="transparent")
        self.sgn_button_frame_file.pack(padx=0, pady=0, expand=True)
        self.sgn_button_frame_file.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # button sgnrypt
        self.sgn_button_sgnrypt_file = ctk.CTkButton(self.sgn_button_frame_file, text="Sign file",
                                                     command=self.sgn_sign_file)
        self.sgn_button_sgnrypt_file.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button sgnrypt
        self.sgn_button_select_file_to_sgn = ctk.CTkButton(self.sgn_button_frame_file, text="Select File",
                                                           command=self.sgn_select_file)
        self.sgn_button_select_file_to_sgn.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button copy
        self.sgn_button_open_folder = ctk.CTkButton(self.sgn_button_frame_file, text="Open folder",
                                                    command=self.open_output_folder)
        self.sgn_button_open_folder.grid(row=0, column=3, padx=5, pady=0, sticky='nwes')



        # TEXT VER
        self.ver_frame_text = ctk.CTkFrame(self.tab_view.tab('Verify'))
        # self.enc_frame_text.configure(fg_color="blue")  # transparent
        self.ver_frame_text.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # message
        self.ver_textbox_input = ctk.CTkTextbox(self.ver_frame_text, height=100)
        self.ver_textbox_input.insert("0.0", "Message")
        self.ver_textbox_input.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # signature
        self.ver_textbox_output = ctk.CTkTextbox(self.ver_frame_text, height=100)
        self.ver_textbox_output.insert("0.0", "Signsture")
        self.ver_textbox_output.pack(padx=5, pady=(5, 0), expand=True, fill=ctk.BOTH)

        # frame for buttons
        self.ver_button_frame_text = ctk.CTkFrame(self.ver_frame_text)
        self.ver_button_frame_text.configure(fg_color="transparent")
        self.ver_button_frame_text.pack(padx=0, pady=0, expand=True)
        self.ver_button_frame_text.grid_columnconfigure((0, 1, 2), weight=1)
        # button verify
        self.ver_button_encrypt_text = ctk.CTkButton(self.ver_button_frame_text, text="Verify text", command=self.ver_verify_text)
        self.ver_button_encrypt_text.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button copy
        # self.ver_button_copy_text = ctk.CTkButton(self.ver_button_frame_text, text="Copy output", command=self.ver_copy_output)
        # self.ver_button_copy_text.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button paste
        self.ver_button_paste_text = ctk.CTkButton(self.ver_button_frame_text, text="Paste msg + sgn", command=self.ver_paste_input)
        self.ver_button_paste_text.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')

        # FILE VER
        self.ver_frame_file = ctk.CTkFrame(self.tab_view.tab('Verify'))
        # self.enc_frame_file.configure(fg_color="red")  # transparent
        self.ver_frame_file.pack(padx=5, pady=5, expand=True, fill=ctk.BOTH)
        # self.enc_frame_file.grid_rowconfigure((0, 1, 2), weight=1)

        self.ver_file_to_ver_label1 = ctk.CTkLabel(self.ver_frame_file, text="Openned File: ")
        self.ver_file_to_ver_label1.pack(padx=0, pady=0, expand=True)
        self.ver_file_to_ver_label = ctk.CTkLabel(self.ver_frame_file, text=". . . . .")
        self.ver_file_to_ver_label.pack(padx=0, pady=0, expand=True)

        self.ver_signature_label1 = ctk.CTkLabel(self.ver_frame_file, text="Signature File: ")
        self.ver_signature_label1.pack(padx=0, pady=0, expand=True)
        self.ver_signature_label = ctk.CTkLabel(self.ver_frame_file, text=". . . . .")
        self.ver_signature_label.pack(padx=0, pady=0, expand=True)

        # frame for buttons
        self.ver_button_frame_file = ctk.CTkFrame(self.ver_frame_file)
        self.ver_button_frame_file.configure(fg_color="transparent")
        self.ver_button_frame_file.pack(padx=0, pady=0, expand=True)
        self.ver_button_frame_file.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # button encrypt
        self.ver_button_encrypt_file = ctk.CTkButton(self.ver_button_frame_file, text="Verify file", command=self.ver_verify_file)
        self.ver_button_encrypt_file.grid(row=0, column=0, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.ver_button_select_file_to_ver = ctk.CTkButton(self.ver_button_frame_file, text="Select File", command=self.ver_select_file)
        self.ver_button_select_file_to_ver.grid(row=0, column=1, padx=5, pady=0, sticky='nwes')
        # button encrypt
        self.ver_button_select_file_to_ver = ctk.CTkButton(self.ver_button_frame_file, text="Select Signature",
                                                           command=self.ver_select_signature)
        self.ver_button_select_file_to_ver.grid(row=0, column=2, padx=5, pady=0, sticky='nwes')
        # button copy
        self.ver_button_open_folder = ctk.CTkButton(self.ver_button_frame_file, text="Open folder", command=self.open_output_folder)
        self.ver_button_open_folder.grid(row=0, column=3, padx=5, pady=0, sticky='nwes')


    def create_keys(self):
        msg = CTkMessagebox(title="Generate new key pair",
                            message="Make sure you keep the keys in a safe place.\nGenerating new keys will overwrite previous ones.\nContinue?",
                            icon="question", option_1="Cancel", option_2="Continue")
        response = msg.get()
        if response == "Continue":
            dss = DSS()
            dss.generate_key()
            CTkMessagebox(title="Generate new key pair",
                          message="The key pair is created and stored in the files 'private_key.pem' and 'public_key.pem'.",
                          icon="question", option_1="Thx")

    def select_private_key(self):
        self.private_key_path = filedialog.askopenfilename()
        self.k_private_key_label.configure(text=self.private_key_path)

    def select_public_key(self):
        self.public_key_path = filedialog.askopenfilename()
        self.k_public_key_label.configure(text=self.public_key_path)

    def open_key_folder(self):
        if self.keys_folder_path:
            os.startfile(self.keys_folder_path)
        else:
            print('floder not exsts')

    def sgn_signature_text(self):
        if not self.private_key_path:
            return CTkMessagebox(title="Chose key file",
                                 message='To begin, you need to select a private key file on the "Keys" page.',
                                 icon="info", option_1="Okay")

        message = self.sgn_textbox_input.get("0.0", "end")[:-1]

        dss = DSS()
        private_key = dss.load_private_key(self.private_key_path)
        signature = dss.sign_message(message, private_key)

        self.sgn_textbox_output.configure(state='normal')
        self.sgn_textbox_output.delete("0.0", "end")
        self.sgn_textbox_output.insert("0.0", signature)
        self.sgn_textbox_output.configure(state='disabled')

    def sgn_copy_output(self):
        msg = self.sgn_textbox_input.get("0.0", "end")[:-1]
        sgn = self.sgn_textbox_output.get("0.0", "end")[:-1]
        t2c = f'{msg}РОЗДІЛЬНИК))){sgn}'
        pyperclip.copy(t2c)

    def sgn_paste_input(self):
        text_to_paste = pyperclip.paste()
        self.sgn_textbox_input.delete("0.0", "end")
        self.sgn_textbox_input.insert("0.0", text_to_paste)

    def sgn_sign_file(self):
        if not self.private_key_path:
            return CTkMessagebox(title="Chose key file",
                                 message='To begin, you need to select a private key file on the "Keys" page.',
                                 icon="info", option_1="Okay")

        if not self.oppened_file_to_sign:
            return CTkMessagebox(title="Chose file",
                                 message='To begin, you need to select a file to sign.',
                                 icon="info", option_1="Okay")

        dss = DSS()
        private_key = dss.load_private_key(self.private_key_path)
        output_path = os.path.join(self.output_folder_path, 'signatre.bin')

        dss.sign_file(self.oppened_file_to_sign, private_key, output_path)

    def sgn_select_file(self):
        self.oppened_file_to_sign = filedialog.askopenfilename()
        self.sgn_file_to_sgn_label.configure(text=self.oppened_file_to_sign)

    def ver_select_file(self):
        self.oppened_file_to_verify = filedialog.askopenfilename()
        self.ver_file_to_ver_label.configure(text=self.oppened_file_to_verify)

    def ver_select_signature(self):
        self.oppened_signature_file = filedialog.askopenfilename()
        self.ver_signature_label.configure(text=self.oppened_signature_file)

    def open_output_folder(self):
        if self.output_folder_path:
            os.startfile(self.output_folder_path)
        else:
            print('floder not exsts')

    def ver_verify_text(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Choise key file",
                                 message='To begin, you need to select a public key file on the "Keys" page.',
                                 icon="info", option_1="Okay")

        message = self.ver_textbox_input.get("0.0", "end")[:-1]
        signature = self.ver_textbox_output.get("0.0", "end")[:-1]

        dss = DSS()
        public_key = dss.load_public_key(self.public_key_path)
        res = dss.verify_signature(message, signature, public_key)
        if res:
            self.success()
        else:
            self.fail()

    def ver_verify_file(self):
        if not self.public_key_path:
            return CTkMessagebox(title="Choise key file",
                                 message='To begin, you need to select a public key file on the "Keys" page.',
                                 icon="info", option_1="Okay")
        if not self.oppened_file_to_verify:
            return CTkMessagebox(title="Chose file",
                                 message='To begin, you need to select a file to verify.',
                                 icon="info", option_1="Okay")
        if not self.oppened_signature_file:
            return CTkMessagebox(title="Chose file",
                                 message='To begin, you need to select a signature file.',
                                 icon="info", option_1="Okay")

        dss = DSS()
        public_key = dss.load_public_key(self.public_key_path)
        signature_path = os.path.join('DSS', 'output', 'signatre.bin')
        res = dss.verify_file(self.oppened_file_to_verify, public_key, signature_path)
        if res:
            self.success()
        else:
            self.fail()

    def ver_copy_output(self):
        msg = self.ver_textbox_input.get("0.0", "end")[:-1]
        sgn = self.ver_textbox_output.get("0.0", "end")[:-1]
        t2c = f'{msg}РОЗДІЛЬНИК))){sgn}'
        pyperclip.copy(t2c)

    def ver_paste_input(self):
        text_to_paste = pyperclip.paste()

        split_values = text_to_paste.split('РОЗДІЛЬНИК)))')
        msg = split_values[0]
        sgn = split_values[1]

        self.ver_textbox_input.delete("0.0", "end")
        self.ver_textbox_input.insert("0.0", msg)
        self.ver_textbox_output.delete("0.0", "end")
        self.ver_textbox_output.insert("0.0", sgn)

    def success(self):
        return CTkMessagebox(title="Success",
                             message='Signature verified successfully. Everything is fine... I don\'t know what else to write.',
                             icon="check", option_1="Okay")

    def fail(self):
        return CTkMessagebox(title="Fail",
                             message='Oops, looks like the signature doesn\'t match.',
                             icon="warning", option_1="Okay")

    def disableChildren(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
                child.configure(state='disable')
            else:
                self.disableChildren(child)
