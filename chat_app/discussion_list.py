import tkinter as tk
from tkinter import ttk
import customtkinter

from chat_app.color_theme import CANVAS, TEXT, BUTTON, HOVER
from chat_app.settings import USER_NAME
from client.contacts import get_contact, get_contacts
from client.discussions import create_new_discussion, get_discussions


def calculate_name(user_id, discussion):
    contacts = discussion.get("contacts", [])

    yourself = contacts[0] == contacts[1] and len(contacts) == 2
    if user_id in contacts:
        if not yourself:
            text = ""
            for contact in contacts:
                if user_id != contact:
                    text = text + get_contact(contact)["name"] + ", "
            return text[:-2]
        else:
            contact = contacts[0]
            if user_id == contact:
                return "You"

    return "error"


class DiscussionList(tk.Frame):
    def __init__(self, master=None, user_id=None):
        super().__init__(master)
        self.listbox_discussions = None
        self.button_discussions = None
        master.grid(row=0, column=0, sticky="ns")

        self.user_id = user_id
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        label = customtkinter.CTkLabel(self, text=f"Hello {USER_NAME}",
                                       text_color=TEXT,
                                       fg_color=CANVAS,
                                       font=("Helvetica", 14))
        label.pack(pady=5)

        discussions = get_discussions(self.user_id)
        self.button_discussions = customtkinter.CTkButton(self, text="New Chat",
                                                          width=100,
                                                          height=55,
                                                          fg_color=BUTTON,
                                                          border_color=BUTTON,
                                                          border_width=1,
                                                          hover_color=HOVER,
                                                          text_color=TEXT,
                                                          font=("Roboto", 18),
                                                          command=self.contact_window)
        self.button_discussions.pack(fill=tk.X)

        self.listbox_discussions = ttk.Treeview(self, style="Treeview", selectmode="browse")
        self.listbox_discussions.pack(fill=tk.BOTH, expand=True, pady=10, ipadx=20)
        self.listbox_discussions.heading("#0", text="Chats")

        for discussion in discussions:
            self.listbox_discussions.insert('', 'end', text=calculate_name(self.user_id, discussion), value=discussion["id"])

    def contact_window(self):
        contact_popup = tk.Toplevel(self)
        contact_popup.title("Contacts")
        contact_popup.configure(height=300, width=500, bg=CANVAS)
        contact_popup.geometry("280x400")
        contact_popup.transient(self)

        contacts_listbox = ttk.Treeview(contact_popup, selectmode="extended")
        contacts_listbox.heading("#0", text="Contacts:")
        contacts_listbox.pack(fill=tk.BOTH, expan=True, padx=30, pady=30)

        contacts = get_contacts()
        for contact in contacts:
            contacts_listbox.insert('', 'end', text=contact["name"], value=contact["id"])

        def add_selected_contact():
            selected_index = contacts_listbox.selection()
            if selected_index:
                selected_discussion = []
                n = len(selected_index)
                for i in range(0, n):
                    selected_discussion.append(contacts_listbox.item(selected_index[i]))

                selected_contacts_id = [self.user_id]
                for i in range(0, n):
                    selected_contacts_id.append(selected_discussion[i]["values"][0])


                discussion = create_new_discussion(selected_contacts_id)
                if discussion:
                    self.listbox_discussions.insert('', 'end', text=calculate_name(self.user_id, discussion), value=discussion["id"])

                contact_popup.destroy()

        def add_contact_event(event):
            add_selected_contact()

        button_select = customtkinter.CTkButton(contact_popup, text="Submit",
                                                width=100,
                                                height=35,
                                                corner_radius=8,
                                                fg_color=BUTTON,
                                                border_color=BUTTON,
                                                border_width=1,
                                                hover_color=HOVER,
                                                text_color=TEXT,
                                                font=("Helvetica", 18, "bold"),
                                                command=add_selected_contact)
        button_select.pack(fill=tk.X, padx=10, pady=10)
        contact_popup.bind("<Return>", add_contact_event)
