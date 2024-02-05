from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        self.birthday = datetime(year=1900, month=1, day=1)


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):

        if self.find_phone(old_phone) is None:
            raise ValueError("phone number does not exist")

        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def set_birthday(self, str_birthday):
        str_birthday = str_birthday.split("-")
        birthday = datetime(year=int(str_birthday[0]), month=int(str_birthday[1]), day=int(str_birthday[2]))
        self.birthday = birthday.date()

    def days_to_birthday(self):
        print("--1")
        print(self.birthday)
        current_date = datetime.today().date()
        birthday_this_year = self.birthday.replace(year=current_date.year)
        difference = birthday_this_year - current_date
        if difference < timedelta(days=0):
            if current_date.year % 4 == 0:
                difference += timedelta(days=366)
            else:
                difference += timedelta(days=365)

        return difference.days

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(str(p) for p in self.phones)}, "
                f"birthday: {self.birthday}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")

# Додавання запису John до адресної книги
jane_record.set_birthday("1990-03-15")
john_record.set_birthday("1990-01-15")

book.add_record(jane_record)

print(jane_record.days_to_birthday())
print(john_record.days_to_birthday())

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print("---")
    print(record)
    print("-+-")

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
