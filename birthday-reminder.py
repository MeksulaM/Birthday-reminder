import json
from datetime import datetime


def get_json_data(filename: str):

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


def add_bday_to_json(filename: str):

    data = get_json_data(filename)
    new_person_info = {}

    first_name = input('First name: ')
    last_name = input('Last name: ')
    birthday = input('Birthday: ')

    new_person_info['first_name'] = first_name
    new_person_info['last_name'] = last_name
    new_person_info['birthday'] = birthday

    new_person = 'person'
    for person in data:
        person_id = int(person[len(new_person):])
    new_person += str(person_id + 1)

    data[new_person] = new_person_info

    with open(filename, 'w') as file:
        json.dump(data, file)


def get_actual_data(filename: str):

    data = get_json_data(filename)
    birthdays = store_data_in_dict(data)

    return data, birthdays


def main():
    filename = 'birthdays.json'

    data, birthdays = get_actual_data(filename)

    while True:
        print("1: Show persons list")
        print("2: Check someone's birthday")
        print("3: Add someone's birthday")

        choice = input('Type corresopnding number: ')

        if choice == '1':
            show_all_persons(birthdays)
        elif choice == '2':
            show_birthday(birthdays)
        elif choice == '3':
            add_bday_to_json(filename)
            data, birthdays = get_actual_data(filename)
        else:
            break


if __name__ == '__main__':
    main()
