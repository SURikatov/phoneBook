import tkinter as tk
from tkinter import filedialog, messagebox
import json
import uuid
from PIL import Image, ImageTk

# Маппинг заголовков для перевода интерфейса
header_mapping = {
    "name": {"ru": "имя", "en": "name"},
    "surname": {"ru": "фамилия", "en": "surname"},
    "phone1": {"ru": "телефон 1", "en": "phone1"},
    "phone2": {"ru": "телефон 2", "en": "phone2"},
    "phone3": {"ru": "телефон 3", "en": "phone3"},
    "email": {"ru": "email", "en": "email"},
    "job": {"ru": "место работы", "en": "job"},
    "position": {"ru": "должность", "en": "position"},
    "birthdate": {"ru": "дата рождения", "en": "birthdate"},
    "address": {"ru": "адрес", "en": "address"}
}

class PhonebookApp:
    def __init__(self, master):
        self.master = master
        master.title("Телефонный справочник")

        # Загрузка изображения и установка его на метку
        self.phone_book_image = Image.open("icon.png")
        self.phone_book_image = self.phone_book_image.resize((50, 50), Image.BILINEAR) 
        self.phone_book_image = ImageTk.PhotoImage(self.phone_book_image)
        self.image_label = tk.Label(master, image=self.phone_book_image)
        self.image_label.grid(row=0, column=0, columnspan=2) 

        # Поле для поиска контактов
        self.label = tk.Label(master, text="Поиск:")
        self.label.grid(row=1, column=0, sticky="e")

        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=1, column=1, sticky="we", padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_contacts)

        # Список контактов
        self.listbox = tk.Listbox(master, width=50)
        self.listbox.grid(row=2, column=0, columnspan=2, rowspan=6, sticky="nsew")
        self.listbox.bind('<Double-Button-1>', self.view_contact)

        # Кнопки управления контактами
        self.delete_button = tk.Button(master, text="Удалить", command=self.delete_contact)
        self.delete_button.grid(row=9, column=0, sticky="we", padx=5)

        self.add_button = tk.Button(master, text="Добавить", command=self.add_contact)
        self.add_button.grid(row=9, column=1, sticky="we", padx=5)

        # Нижняя надпись в главном окне
        self.footer_label = tk.Label(master, text="© Created by Alexander Kadochnikov")
        self.footer_label.grid(row=10, column=0, columnspan=2, sticky="s")  

        # Загрузка контактов
        self.load_contacts()

        master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

    def add_contact(self):
        # добавлени нового контакта
        pass

    def delete_contact(self):
        # удалени выбранного контакта
        pass

    def search_contacts(self, event=None):
        # поиск контактов
        pass

    def load_contacts(self):
        # Загрузка контактов из файла
        pass

    def view_contact(self):
        # просмотр контакта с возможностью редактирования
        pass

    def save_contacts(self):
        # Сохранение контактов в файл
        pass

    def save_and_quit(self):
        # Сохранение и выход из программы
        pass

root = tk.Tk()
app = PhonebookApp(root)
root.mainloop()
