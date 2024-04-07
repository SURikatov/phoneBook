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

        self.import_button = tk.Button(master, text="Импорт", command=self.import_contacts)
        self.import_button.grid(row=10, column=0, sticky="we", padx=5)

        self.export_button = tk.Button(master, text="Экспорт", command=self.export_contacts)
        self.export_button.grid(row=10, column=1, sticky="we", padx=5)

        # Нижняя надпись в главном окне
        self.footer_label = tk.Label(master, text="© Created by Alexander Kadochnikov")
        self.footer_label.grid(row=11, column=0, columnspan=2, sticky="s")  

        # Загрузка контактов
        self.load_contacts()

        master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

    def add_contact(self):
        # добавление нового контакта
        pass

    def delete_contact(self):
        # удаление выбранного контакта
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

    def import_contacts(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    imported_contacts = json.load(file)
                    if isinstance(imported_contacts, list):
                        header_mapping.clear()
                        for entry in imported_contacts:
                            contact_id = entry["id"]
                            del entry["id"]
                            entry["uid"] = contact_id
                            self.contacts[contact_id] = entry
                        self.save_contacts()
                        self.load_contacts()
                    else:
                        messagebox.showerror("Ошибка", "Формат файла не соответствует ожидаемому.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при импорте контактов: {e}")

    def export_contacts(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    export_contacts = {}
                    for contact_id, contact in self.contacts.items():
                        english_contact = {}
                        for k, v in contact.items():
                            english_contact[header_mapping[k]["en"]] = v
                        export_contacts[contact_id] = english_contact
                    json.dump(export_contacts, file, ensure_ascii=False, indent=4)
                    messagebox.showinfo("Успех", "Контакты успешно экспортированы.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при экспорте контактов: {e}")

    def save_and_quit(self):
        # Сохранение и выход из программы
        pass

root = tk.Tk()
app = PhonebookApp(root)
root.mainloop()
