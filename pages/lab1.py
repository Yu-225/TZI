from modules.LinearComparison import LinearComparison

import customtkinter as ctk
import configparser
from CTkMessagebox import CTkMessagebox
import pyperclip
import os
import time
import asyncio


class DrawLab1(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.lab = 'Lab 1'
        self.log_file_path = os.path.abspath('logs/lab1_log.txt')

        log_directory = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        config = configparser.ConfigParser()

        config['Lab1'] = {
            'module': '(2 ** 18) - 1',
            'multiplier': '5 ** 3',
            'increase': '34',
            'invalue': '512',
            'num': '30'
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        config.read('config.ini')
        self.module = config.get('Lab1', 'module')
        self.multiplier = config.get('Lab1', 'multiplier')
        self.increase = config.get('Lab1', 'increase')
        self.invalue = config.get('Lab1', 'invalue')
        self.num = config.get('Lab1', 'num')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Input Fields
        self.input_fields = ctk.CTkFrame(self)
        self.input_fields.configure(fg_color="transparent")
        self.input_fields.grid(row=0, column=0, padx=0, pady=0, sticky='nwes')

        # Модуль порівняння
        self.label_module = ctk.CTkLabel(self.input_fields, text="Comprasion module")
        self.label_module.pack(padx=5, pady=(5, 0))
        self.textbox_module = ctk.CTkTextbox(self.input_fields, height=30)
        self.textbox_module.insert("0.0", self.module)
        self.textbox_module.pack(padx=5, pady=(0, 5))

        # Множник
        self.label_multiplier = ctk.CTkLabel(self.input_fields, text="Multiplier")
        self.label_multiplier.pack(padx=5, pady=(5, 0))
        self.textbox_multiplier = ctk.CTkTextbox(self.input_fields, height=30)
        self.textbox_multiplier.insert("0.0", self.multiplier)
        self.textbox_multiplier.pack(padx=5, pady=(0, 5))

        # Приріст
        self.label_increase = ctk.CTkLabel(self.input_fields, text="Increase")
        self.label_increase.pack(padx=5, pady=(5, 0))
        self.textbox_increase = ctk.CTkTextbox(self.input_fields, height=30)
        self.textbox_increase.insert("0.0", self.increase)
        self.textbox_increase.pack(padx=5, pady=(0, 5))

        # Початкове значення
        self.label_invalue = ctk.CTkLabel(self.input_fields, text="Initial value")
        self.label_invalue.pack(padx=5, pady=(5, 0))
        self.textbox_invalue = ctk.CTkTextbox(self.input_fields, height=30)
        self.textbox_invalue.insert("0.0", self.invalue)
        self.textbox_invalue.pack(padx=5, pady=(0, 5))

        # Кількість чисел для генерації
        self.label_num = ctk.CTkLabel(self.input_fields, text="Numbers to generate")
        self.label_num.pack(padx=5, pady=(5, 0))
        self.textbox_num = ctk.CTkTextbox(self.input_fields, height=30)
        self.textbox_num.insert("0.0", self.num)
        self.textbox_num.pack(padx=5, pady=(0, 5))

        # Buttons
        self.btn_fields = ctk.CTkFrame(self)
        self.btn_fields.configure(fg_color="transparent")
        self.btn_fields.grid(row=0, column=1, padx=0, pady=0, sticky='nwes')

        # Button Default
        self.btn_default = ctk.CTkButton(self.btn_fields, text="Reset", command=self.reset)
        self.btn_default.pack(padx=5, pady=15)

        # Button Calculate
        self.btn_calc = ctk.CTkButton(self.btn_fields, text="Calculate", command=self.start_calculation)
        self.btn_calc.pack(padx=5, pady=15)

        # Button Copy
        self.btn_copy = ctk.CTkButton(self.btn_fields, text="Copy", command=self.copy)
        self.btn_copy.pack(padx=5, pady=15)

        # Button Log file
        self.btn_log_file = ctk.CTkButton(self.btn_fields, text="Open logs", command=self.open_log_file)
        self.btn_log_file.pack(padx=5, pady=15)

        # Button Clear
        self.btn_clear = ctk.CTkButton(self.btn_fields, text="Clear logs", command=self.clear_log_file)
        self.btn_clear.pack(padx=5, pady=15)

        # Outputs
        self.out_fields = ctk.CTkFrame(self)
        self.out_fields.configure(fg_color="transparent")
        self.out_fields.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nwes')

        # list
        self.label_out_list = ctk.CTkLabel(self.out_fields, text="Generating numbers:")
        self.label_out_list.pack(padx=5, pady=(0, 0))
        self.textbox_out_list = ctk.CTkTextbox(self.out_fields, height=100, width=450)
        self.textbox_out_list.pack(padx=5, pady=(0, 5))
        self.textbox_out_list.configure(state='disabled')

        #
        self.label_out_period = ctk.CTkLabel(self.out_fields, text="Period:")
        self.label_out_period.pack(padx=5, pady=(5, 0))
        self.textbox_out_period = ctk.CTkTextbox(self.out_fields, height=30)
        self.textbox_out_period.pack(padx=5, pady=(0, 5))
        self.textbox_out_period.configure(state='disabled')

    async def calculate(self):
        try:
            m = eval(self.textbox_module.get("0.0", "end")[:-1])
            a = eval(self.textbox_multiplier.get("0.0", "end")[:-1])
            c = eval(self.textbox_increase.get("0.0", "end"))
            x = eval(self.textbox_invalue.get("0.0", "end"))
            n = eval(self.textbox_num.get("0.0", "end"))

        except SyntaxError:
            CTkMessagebox(title='Error', message='It seems you entered the wrong number.',
                          icon='cancel', option_1='Ok')
            self.log('Error', 'Wrong number')

        if type(n) != int:
            CTkMessagebox(title='Error', message='The number of elements must be an integer.',
                          icon='cancel', option_1='Ok')
            self.log('Error', 'Negative dimensions')
            return

        if n < 0:
            CTkMessagebox(title='Error', message='Negative dimensions are not allowed.',
                          icon='cancel', option_1='Ok')
            self.log('Error', 'Negative dimensions')
            return

        if n >= 10000:
            msg = CTkMessagebox(title="Warning Message!",
                                message="It looks like you want to generate too big a list.\nCalculations may take some time.",
                                icon="warning", option_1="Cancel", option_2="I know what I'm doing")

            if msg.get() == "Cancel":
                return

        lc = LinearComparison()
        lc.update(m, a, c, x, n)

        result_list = lc.gen_list()
        result_period = lc.find_period()

        self.textbox_out_list.configure(state='normal')
        self.textbox_out_list.delete("0.0", "end")
        self.textbox_out_list.insert("0.0", result_list)
        self.textbox_out_list.configure(state='disabled')
        self.textbox_out_period.configure(state='normal')
        self.textbox_out_period.delete("0.0", "end")
        self.textbox_out_period.insert("0.0", result_period)
        self.textbox_out_period.configure(state='disabled')

        CTkMessagebox(title='Successful', message='List has been successfully calculated.',
                      icon='check', option_1='Thanks')
        self.log('Calc', result_list)

    def start_calculation(self):
        # Запускаємо асинхронну функцію у циклі подій Tkinter
        self.after(0, self.run_async_calculation)

    def run_async_calculation(self):
        # Створюємо і запускаємо асинхронний цикл
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.calculate())

    def copy(self):
        text_to_copy = self.textbox_out_list.get("0.0", "end")
        pyperclip.copy(text_to_copy)
        CTkMessagebox(title='Copied', message='List successfully copied to clipboard.',
                      icon='check', option_1='Thanks')
        self.log('Copy', 'Result copied')

    def reset(self):
        self.textbox_num.delete("0.0", "end")
        self.textbox_module.delete("0.0", "end")
        self.textbox_invalue.delete("0.0", "end")
        self.textbox_increase.delete("0.0", "end")
        self.textbox_multiplier.delete("0.0", "end")
        self.textbox_module.insert("0.0", self.module)
        self.textbox_multiplier.insert("0.0", self.multiplier)
        self.textbox_increase.insert("0.0", self.increase)
        self.textbox_invalue.insert("0.0", self.invalue)
        self.textbox_num.insert("0.0", self.num)
        self.log('Clear', 'Text fields')

    def log(self, action, result) -> None:
        t = time.strftime("%d.%m.%Y - %H:%M:%S", time.localtime())
        text = f'[ {t} ]\t{action}\t{result}'
        with open(self.log_file_path, 'a') as file:
            file.write(text + '\n')

    def clear_log_file(self):
        open(self.log_file_path, 'w').close()
        self.log('Clear', 'The log file has been cleared')
        CTkMessagebox(title="Warning Message!", message="The log file has been cleared.",
                      icon="warning", option_1="Ok")

    def open_log_file(self):
        os.startfile(self.log_file_path)
