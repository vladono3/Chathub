from client.client import Client
from client.urls import CONTACTS_ENDPOINT


def get_contacts():
    contacts = Client().get(CONTACTS_ENDPOINT)
    if not contacts:
        return []

    return contacts


def get_contact(user_id):

    contact = Client().get(f"{CONTACTS_ENDPOINT}/{user_id}")

    if not contact:
        return []

    return contact
