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
        new_contact = self.add_contact_dialog()
        if new_contact and any(new_contact.values()):
            contact_id = str(uuid.uuid4())
            self.contacts[contact_id] = new_contact
            self.save_contacts()
            self.load_contacts()

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Ошибка", "Выберите контакт для удаления.")
            return

        if messagebox.askokcancel("Подтверждение", "Вы уверены, что хотите удалить выбранный контакт?"):
            del self.contacts[list(self.contacts.keys())[selected_index[0]]]
            self.save_contacts()
            self.load_contacts()

    def search_contacts(self, event=None):
        query = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for contact_id, contact in self.contacts.items():
            name = contact.get(header_mapping.get("name", {}).get("en"), "").lower()
            surname = contact.get(header_mapping.get("surname", {}).get("en"), "").lower()
            if query in name or query in surname:
                self.listbox.insert(tk.END, f"{contact.get(header_mapping.get('name', {}).get('en'), '')} {contact.get(header_mapping.get('surname', {}).get('en'), '')}")

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
                    self.contact_id_map[full_name] = contact_id

        except FileNotFoundError:
            self.contacts = {}
        except Exception as e:
            print(f"Ошибка при загрузке контактов из файла: {e}")
            
    def view_contact(self, event=None):
        try:
            index = self.listbox.curselection()[0]
            self.selected_contact_name = self.listbox.get(index)
        except IndexError:
            pass

        if not hasattr(self, 'selected_contact_name'):
            messagebox.showerror("Ошибка", "Выберите контакт для просмотра.")
            return

        contact_id = self.contact_id_map.get(self.selected_contact_name)
        if contact_id:
            contact = self.contacts[contact_id]

            view_window = tk.Toplevel(self.master)
            view_window.title("Просмотр контакта")

            self.edit_entries = []

            for i, key in enumerate(contact.keys()):
                tk.Label(view_window, text=f"{header_mapping[key]['ru']}:").grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(view_window)
                entry.insert(0, contact[key])
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.edit_entries.append(entry)

            save_button = tk.Button(view_window, text="Сохранить", command=lambda: self.save_contact_changes(view_window, contact))
            save_button.grid(row=len(contact), column=0, columnspan=2, pady=10)

            close_button = tk.Button(view_window, text="Закрыть", command=view_window.destroy)
            close_button.grid(row=len(contact) + 1, column=0, columnspan=2)

    def save_contacts(self):
        contacts_list = []
        for contact_id, contact in self.contacts.items():
            contact_entry = {"uid": contact_id}
            for key, value in contact.items():
                contact_entry[key] = value
            contacts_list.append(contact_entry)

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(contacts_list, file, ensure_ascii=False, indent=4)

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
