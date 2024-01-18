import asyncio
import tkinter as tk
import customtkinter
from tkinter import messagebox

import websockets

from chat_app.color_theme import BUTTON, TEXT, HOVER
from chat_app.settings import PORT, DOMAIN
from client.messages import get_messages, create_new_message


class ChatMessages(tk.Frame):
    def __init__(self, master=None, discussion_list=None):
        super().__init__(master)
        master.grid(row=0, column=1, sticky="nsew")

        self.websocket = None

        self.master = master
        self.chat_text = None
        self.message_entry = None
        self.send_button = None
        self.discussion_list = discussion_list

        self.placeholder = "Type a message..."

        self.discussion_list.listbox_discussions.bind("<<TreeviewSelect>>", self.on_item_select)
        self.messages = []
        self.create_widget()

    async def connect_to_websocket_server_recv(self):
        await asyncio.sleep(2)
        try:
            async with websockets.connect(f"ws://{DOMAIN}:{PORT}/ws/client_id") as websocket:
                while True:
                    self.websocket = websocket
                    response = await websocket.recv()
                    if response:
                        self.on_item_select(response)

        except websockets.ConnectionClosed:
            messagebox.showerror("API error message", "Connection closed.")
        except Exception as e:
            messagebox.showerror("API error message", f"Error: {str(e)}")

    def on_item_select(self, event):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            discussion_id = str(selected_discussion["values"][0])

            messages = get_messages(self.discussion_list.user_id, discussion_id)
            self.display_chat_messages(messages)

    def create_widget(self):
        self.chat_text = tk.Text(self, height=20, width=80, bg="white", fg="black", font=("Helvetica", 12))
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_text.config(cursor="arrow")

        self.message_entry = tk.Text(self, height=4, width=70, bg="white", fg="black", font=("Helvetica", 12))
        self.message_entry.pack(side="left", fill=tk.BOTH, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.insert("1.0", self.placeholder)
        self.message_entry.config(fg="gray")
        self.message_entry.bind("<FocusIn>", self.on_message_focusin)
        self.message_entry.bind("<FocusOut>", self.on_message_focusout)

        self.send_button = customtkinter.CTkButton(self, text="Send",
                                                   height=60,
                                                   width=80,
                                                   fg_color=BUTTON,
                                                   border_color=BUTTON,
                                                   border_width=1,
                                                   hover_color=HOVER,
                                                   text_color=TEXT,
                                                   font=("Roboto", 18 ),
                                                   command=self.send_message)
        self.send_button.pack(side="right", fill=tk.X)

    def send_message(self):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            discussion_id = str(selected_discussion["values"][0])
            message = self.message_entry.get("1.0", tk.END)

            message_obj = {
                "discussion_id": discussion_id,
                "user_id": self.discussion_list.user_id,
                "value": message
            }

            self.messages.append(message_obj)
            self.create_new_chat_messages(message_obj)
            asyncio.get_event_loop().run_until_complete(self.websocket.send("New event"))
            self.message_entry.delete('1.0', tk.END)

    def on_message_focusin(self, event):
        if self.message_entry.get("1.0", "end-1c") == self.placeholder:
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg="black", font=("Helvetica", 12))

    def on_message_focusout(self, event):
        if not self.message_entry.get("1.0", "end-1c"):
            self.message_entry.insert("1.0", self.placeholder)
            self.message_entry.config(fg="gray", font=("Helvetica", 12))

    def send_message_event(self, event):
        self.send_message()

    def display_chat_messages(self, messages):
        self.chat_text.delete('1.0', tk.END)
        for message in messages:
            name = message["name"]
            value = message["value"]
            message_text = f"{name}: {value}\n\n"
            self.chat_text.insert(tk.END, message_text)

    def create_new_chat_messages(self, message):
        create_new_message(message)