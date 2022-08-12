import json
from datetime import datetime


def get_json_data(filename: str):
    """Open json file and store its content in 'data' variable"""

    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def store_data_in_dict(data: dict):
    """Store data from json to one, non nested dictionary"""

    # empty dict to store data later on
    birthdays = {}

    for info in data.values():

        # combine first and last name for simplicity
        full_name = str(info['first_name']) + ' ' + str(info['last_name'])
        full_name = full_name.title()

        # convert str to 'datetime' type
        birthday = datetime.strptime(info['birthday'], '%d.%m.%Y')

        # adding key-value pair to birthday's dictionary
        birthdays[full_name] = birthday

    return birthdays


def show_all_persons(birthdays: dict):
    """Print list of persons we know birthdays"""

    print('\nWe know birthdays of:')

    # full names are keys in 'birthdays' dictionary
    for name in birthdays:
        print(name)


def show_birthday(birthdays: dict):
    """Print choosen person's birthday"""

    # asking user for input
    user_input = input("\nWho's birthday do you want to check?: ").title()

    # formating output to DD.MM.YYYY
    bday = birthdays[user_input].date()
    bday = bday.strftime("%d.%m.%Y")

    print(f"{user_input}'s birthday is {bday}")


def add_bday_to_json(data: dict, filename: str):
    """This function allows user to add someone's birthday to json"""

    # empty dictionary to store info about new person
    new_person_info = {}

    # asking user for new person info
    first_name = input('\nFirst name: ')
    last_name = input('Last name: ')
    birthday = input('Birthday (format: DD.MM.YYYY): ')

    # adding inputs to dictionary
    new_person_info['first_name'] = first_name
    new_person_info['last_name'] = last_name
    new_person_info['birthday'] = birthday

    # determinig name of the new key in json dictionary
    # keys in json dict are named by convention 'person + number of a person'
    new_person = 'person'
    # accessing name of the last key
    for person in data:
        # accessing number of a person
        person_id = int(person[len(new_person):])
    # new key: person + number of the last person + 1
    new_person += str(person_id + 1)

    # adding new key-value pair to data dictionary
    data[new_person] = new_person_info

    # updating json data
    with open(filename, 'w') as file:
        json.dump(data, file)

    # printing fancy message to the user
    full_name = first_name + ' ' + last_name
    print(f"{full_name.title()}'s birthday added succsessfully")


def get_actual_data(filename: str):
    """Update stored data after e.g. adding someone's birthday"""

    data = get_json_data(filename)
    birthdays = store_data_in_dict(data)

    return data, birthdays


def main():
    filename = 'birthdays.json'

    data, birthdays = get_actual_data(filename)

    # program menu in while loop
    while True:

        # program functionalities
        print()
        print("1: Show persons list")
        print("2: Check someone's birthday")
        print("3: Add someone's birthday")

        # asking user for choice, then executing corresponding function
        choice = input('Type corresopnding number: ')
        if choice == '1':
            show_all_persons(birthdays)
        elif choice == '2':
            show_birthday(birthdays)
        elif choice == '3':
            add_bday_to_json(data, filename)
            data, birthdays = get_actual_data(filename)
        else:
            break


if __name__ == '__main__':
    main()
