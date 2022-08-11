import json
from datetime import datetime


def get_data_from_json(filename: str):

    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def store_data_in_dict(data: dict):

    birthdays = {}

    for info in data.values():
        full_name = str(info['first_name']) + ' ' + str(info['last_name'])
        full_name = full_name.title()
        birthday = datetime.strptime(info['birthday'], '%d.%m.%Y')
        birthdays[full_name] = birthday

    return birthdays


def show_all_persons(birthdays: dict):

    print('We know birthdays of:')
    for name in birthdays:
        print(name)


def show_birthday(birthdays: dict):

    user_input = input("Who's birthday do you want to check?: ")
    print(f'{user_input} birthday is {birthdays[user_input]}')


def main():
    filename = 'birthdays.json'
    data = get_data_from_json(filename)
    birthdays = store_data_in_dict(data)
    show_all_persons(birthdays)
    show_birthday(birthdays)


if __name__ == '__main__':
    main()
