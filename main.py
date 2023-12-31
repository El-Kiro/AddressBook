from datetime import datetime, timedelta


class Field:
    def __init__(self, value=None):
        self._value = value

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        pass


class Phone(Field):
    def validate(self, value):
        if value and not all(c.isdigit() or c in ('-', ' ', '(' ,')') for c in value):
            raise ValueError("Invalid phone number")


class Birthday(Field):
    def validate(self, value):
        if value:
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")


class Name(Field):
    pass


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
            days_left = (next_birthday - today).days
            return days_left
        return None


class AddressBook:
    def __init__(self):
        self.data = []

    def add_record(self, record):
        self.data.append(record)

    def find_records(self, field_name, value):
        return [record for record in self.data if getattr(record, field_name) == value]

    def iterator(self, chunk_size=10):
        for i in range(0, len(self.data), chunk_size):
            yield self.data[i:i + chunk_size]


def main():
    address_book = AddressBook()

    record1 = Record("Alice", "123-456-7890", "1990-05-15")
    record2 = Record("Bob", "987-654-3210", "1995-07-20")
    record3 = Record("Charlie", "555-555-5555")

    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)

    while True:
        print("\nOptions:")
        print("1. Find records by name")
        print("2. Find records by phone number")
        print("3. Find records by birthday")
        print("4. List all records (with pagination)")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name to search for: ")
            found_records = address_book.find_records("name", name)
            if found_records:
                for record in found_records:
                    print(f"Name: {record.name}, Phone: {record.phone}, Birthday: {record.birthday}")
            else:
                print("No records found.")

        elif choice == "2":
            phone = input("Enter phone number to search for: ")
            found_records = address_book.find_records("phone", phone)
            if found_records:
                for record in found_records:
                    print(f"Name: {record.name}, Phone: {record.phone}, Birthday: {record.birthday}")
            else:
                print("No records found.")

        elif choice == "3":
            birthday = input("Enter birthday (YYYY-MM-DD) to search for: ")
            found_records = address_book.find_records("birthday", birthday)
            if found_records:
                for record in found_records:
                    print(f"Name: {record.name}, Phone: {record.phone}, Birthday: {record.birthday}")
            else:
                print("No records found.")

        elif choice == "4":
            chunk_size = 2
            page_number = 1
            for chunk in address_book.iterator(chunk_size):
                print(f"\nPage {page_number}:")
                for record in chunk:
                    print(f"Name: {record.name}, Phone: {record.phone}, Birthday: {record.birthday}")
                page_number += 1

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

main()