from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Invalid value")

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Invalid value")

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Birthday(Field):

    # def __init__(self, value):
    #     super().__init__()

    def is_valid(self, str_birthday):
        try:
            datetime.strptime(str_birthday, '%Y-%m-%d').date()
            return True
        except ValueError:
            raise False  # (f"{self.name} invalid date!")

    # @staticmethod
    # def set_birthday(str_birthday):
    #     try:
    #         valid_date = datetime.strptime(str_birthday, '%d-%m-%Y').date()
    #         print(valid_date)
    #         return True
    #     except ValueError:
    #         return False


class Phone(Field):

    # def __init__(self, value):
    #     super().__init__()
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # # self.phones = [p for p in self.phones if p.value != phone]
        # # Створюємо новий список, виключаючи ті елементи, у яких значення дорівнює вказаному телефону
        # updated_phones = []
        # for p in self.phones:
        #     if p.value != phone:
        #         updated_phones.append(p)
        #
        # self.phones = updated_phones

        # if len(updated_phones) == len(self.phones):
        #     raise ValueError("Phone not found")

        try:
            self.phones.remove(phone)
        except ValueError:
            raise ValueError("Phone not found")

        return phone

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

    # def set_birthday(self, str_birthday):
    #
    #     try:
    #         valid_date = datetime.strptime(str_birthday, '%d-%m-%Y').date()
    #         print(valid_date)
    #     except ValueError:
    #         return print(f"{self.name} invalid date!")
    #
    #     self.birthday = valid_date

    def days_to_birthday(self):
        # if not self.birthday.is_valid(self.birthday):
        #     raise ValueError(f"{self.birthday} does not match format '%Y-%m-%d'")

        if self.birthday is None:
            # return "Birthday not specified!"
            return
        else:
            current_date = datetime.today().date()

            bd = datetime.strptime(self.birthday, '%Y-%m-%d').date()
            # birthday_this_year = self.birthday.replace(year=current_date.year)

            birthday_this_year = datetime(year=current_date.year, month=bd.month, day=bd.day).date()
            difference = birthday_this_year - current_date
            if difference < timedelta(days=0):
                birthday_this_year = datetime(year=current_date.year + 1, month=bd.month, day=bd.day).date()
                difference = birthday_this_year - current_date

            return difference.days

            # if difference < timedelta(days=0):
            #     if current_date.year % 4 == 0:
            #         difference += timedelta(days=366)
            #     else:
            #         difference += timedelta(days=365)

    def __str__(self):
        if self.birthday is None:
            return (f"Contact name: {self.name.value}, "
                    f"phones: {'; '.join(str(p) for p in self.phones)}, ")
        else:
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

# Додавання дня народження для запису Jane та John
jane_record.birthday = "1992-03-0p"

# john_record.birthday = "1990-011-15"

# Додавання запису Jane до адресної книги
book.add_record(jane_record)

# Виведення в консоль днів до дня народження Jane та John
print(jane_record.days_to_birthday())
print(john_record.days_to_birthday())

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print("-++-")
    print(record)

print("---" * 10)

# Знаходження та редагування телефону для John
john = book.find("John")

john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
