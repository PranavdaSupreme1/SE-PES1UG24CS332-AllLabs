"""Simple in-memory address book with CSV and JSON export."""

import csv
import hashlib
import json
import re

CONTACTS = {}


def add_contact(full_name, phone, email="", city="Unknown"):
    """Add a contact if the phone number has exactly ten digits."""
    if not re.fullmatch(r"[0-9]{10}", phone):
        print("Invalid phone number for", full_name)
        return False
    CONTACTS[full_name] = {"phone": phone, "email": email, "city": city}
    return True


def contact_id(full_name):
    """Return a short SHA-256 based identifier for a contact."""
    return hashlib.sha256(full_name.encode()).hexdigest()[:6]


def search_contacts(text):
    """Return names whose name or phone number contains the text."""
    found = []
    for name, info in CONTACTS.items():
        if text.lower() in name.lower() or text in info["phone"]:
            found.append(name)
    return found


def update_city(full_name, city):
    """Update the city of an existing contact."""
    try:
        CONTACTS[full_name]["city"] = city
        return True
    except KeyError:
        print("No contact named", full_name)
        return False


def contacts_by_city():
    """Group contact names by city."""
    grouped = {}
    for name, info in CONTACTS.items():
        grouped.setdefault(info["city"], []).append(name)
    return grouped


def print_directory():
    """Print all contacts sorted by name."""
    names = sorted(CONTACTS)
    for i, name in enumerate(names, 1):
        print(i, name, CONTACTS[name]["phone"])


def export_csv(file_name="contacts.csv"):
    """Export all contacts to a CSV file."""
    with open(file_name, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        for name, info in CONTACTS.items():
            writer.writerow([name, info["phone"], info["email"], info["city"]])


def backup_book(file_name="contacts.json"):
    """Save the address book to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as handle:
        json.dump(CONTACTS, handle)


def restore_book(file_name="contacts.json"):
    """Load an address book from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main():
    """Run a small demonstration of the address book."""
    add_contact("Neha Sharma", "9876543210", "neha@example.com", "Bengaluru")
    add_contact("Rahul Verma", "9123456780", "rahul@example.com", "Mysuru")
    add_contact("Test User", "12345")
    add_contact("Kavya Nair", "9988776655", city="Bengaluru")
    update_city("Rahul Verma", "Chennai")
    update_city("Nobody", "Delhi")
    print_directory()
    print("Search 'ra':", search_contacts("ra"))
    print("By city:", contacts_by_city())
    print("Id for Neha:", contact_id("Neha Sharma"))
    export_csv()
    backup_book()
    restored = restore_book()
    print("Contacts restored:", len(restored), "| first:", sorted(restored)[0])
    matches = restored == CONTACTS
    print("Restored contacts match the in-memory address book:", matches)


if __name__ == "__main__":
    main()
