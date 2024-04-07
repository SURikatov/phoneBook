import tkinter as tk
from tkinter import filedialog, messagebox
import json
from PIL import Image, ImageTk

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

        # Загрузка изображения Phone_Book-1024.webp
        self.phone_book_image = Image.open("icon.png")
        self.phone_book_image = self.phone_book_image.resize((50, 50), Image.BILINEAR) 
        self.phone_book_image = ImageTk.PhotoImage(self.phone_book_image)
        self.image_label = tk.Label(master, image=self.phone_book_image)
        self.image_label.grid(row=0, column=0, columnspan=2) 

        self.label = tk.Label(master, text="Поиск:")
        self.label.grid(row=1, column=0, sticky="e")

        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=1, column=1, sticky="we", padx=5)

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.grid(row=2, column=0, columnspan=2, rowspan=6, sticky="nsew")

        self.load_contacts()

        master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

    def load_contacts(self):
        try:
            with open("contacts.json", "r", encoding="utf-8") as file:
                contacts_list = json.load(file)

                for entry in contacts_list:
                    name = entry.get("name", "")
                    surname = entry.get("surname", "")
                    full_name = f"{name} {surname}"
                    self.listbox.insert(tk.END, full_name)

        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка при загрузке контактов из файла: {e}")

    def save_and_quit(self):
        self.master.destroy()

root = tk.Tk()
app = PhonebookApp(root)
root.mainloop()

