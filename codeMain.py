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
        self.search_entry.bind('<KeyRelease>', self.search_contacts)

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.grid(row=2, column=0, columnspan=2, rowspan=6, sticky="nsew")
        self.listbox.bind('<Double-Button-1>', self.view_contact)

        self.delete_button = tk.Button(master, text="Удалить", command=self.delete_contact)
        self.delete_button.grid(row=9, column=0, sticky="we", padx=5)

        self.load_contacts()

        master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

    def search_contacts(self, event=None):
        query = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)

        for contact_id, contact in self.contacts.items():
            name = contact.get(header_mapping.get("name", {}).get("en"), "").lower()
            surname = contact.get(header_mapping.get("surname", {}).get("en"), "").lower()
            if query in name or query in surname:
                self.listbox.insert(tk.END, f"{contact.get(header_mapping.get('name', {}).get('en'), '')} {contact.get(header_mapping.get('surname', {}).get('en'), '')}")

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Ошибка", "Выберите контакт для удаления.")
            return

        if messagebox.askokcancel("Подтверждение", "Вы уверены, что хотите удалить выбранный контакт?"):
            del_index = selected_index[0]
            self.listbox.delete(del_index)
            del self.contacts[list(self.contacts.keys())[del_index]]
            self.save_contacts()

    def load_contacts(self):
        try:
            with open("contacts.json", "r", encoding="utf-8") as file:
                contacts_list = json.load(file)
                self.contacts = {}

                for entry in contacts_list:
                    contact_id = entry["uid"]
                    del entry["uid"]
                    name = entry.get("name", "")
                    surname = entry.get("surname", "")
                    full_name = f"{name} {surname}"

                    self.contacts[contact_id] = entry
                    self.listbox.insert(tk.END, full_name)

        except FileNotFoundError:
            self.contacts = {}
        except Exception as e:
            print(f"Ошибка при загрузке контактов из файла: {e}")

    def save_contacts(self):
        contacts_list = []
        for contact_id, contact in self.contacts.items():
            contact_entry = {"uid": contact_id}
            for key, value in contact.items():
                contact_entry[key] = value
            contacts_list.append(contact_entry)

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(contacts_list, file, ensure_ascii=False, indent=4)

    def save_and_quit(self):
        self.save_contacts()
        self.master.destroy()

root = tk.Tk()
app = PhonebookApp(root)
root.mainloop()
