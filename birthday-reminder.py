import json
from os import system
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
        birthday = birthday.date()

        # adding key-value pair to birthday's dictionary
        birthdays[full_name] = birthday

    return birthdays


def show_all_persons(birthdays: dict):
    """Print list of persons we know birthdays"""

    print('\nWe know birthdays of:')

    # full names are keys in 'birthdays' dictionary
    names_sorted = sorted(birthdays.keys())
    for name in names_sorted:
        print(name)


def show_person_bday(birthdays: dict):
    """Print choosen person's birthday"""

    # asking user for input
    user_input = input("\nWho's birthday do you want to check?: ").title()

    # formating output to DD.MM.YYYY
    # bday = birthdays[user_input].date()
    bday = birthdays[user_input].strftime("%d.%m.%Y")

    print(f"{user_input}'s birthday is {bday}")


def delete_person_bday(data: dict, filename: str):
    """Deleting key-value pair from json dict"""

    # finding dictionary key and creating variables for message at the end
    person_to_del, first_name, last_name = find_dict_key(data)

    # deleting key-value pair from dictionary
    del data[person_to_del]

    # format keys names after removing one key-value pair
    data_formated = format_keys_names(data)

    # updating json data
    write_to_json(filename, data_formated)

    # printing fancy message to the user
    full_name = first_name + ' ' + last_name
    print(f"{full_name.title()}'s birthday removed successfully")


def find_dict_key(data: dict):
    """Return key that matches user inputs"""

    # asking user who to delete
    print('\nWho to delete?:')
    first_name = input('first name: ')
    last_name = input('last name: ')

    # finding key name that matches user inputs
    for person, info in data.items():
        condition1 = first_name == info['first_name']
        condition2 = last_name == info['last_name']
        if condition1 and condition2:
            person_to_del = person

    return person_to_del, first_name, last_name


def format_keys_names(data: dict):
    """formating keys names"""

    # empty dictionary to store values from old 'data'
    data_formated = {}

    # 'id' - variable for keys numeration
    id = 1
    for info in data.values():
        # copying values from 'data' to 'data_formated'
        data_formated['person' + str(id)] = info
        id += 1
    del data

    return data_formated


def add_person_bday(data: dict, filename: str):
    """This function allows user to add someone's birthday to json"""

    # creating dict with new person's info
    new_person_info = create_new_person_dict()

    # updating 'data' with new person's info
    data = add_key_value(data, new_person_info)

    # updating json data
    write_to_json(filename, data)

    # printing fancy message to the user
    full_name = new_person_info['first_name'] + ' ' + new_person_info['last_name']
    print(f"{full_name.title()}'s birthday added succsessfully")


def create_new_person_dict():
    """Asking user to provide info, then storing info in dict"""

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

    return new_person_info


def add_key_value(data: dict, new_person_info: dict):

    # determinig name of the new key in json dictionary
    # keys in json dict are named by convention 'person + number of a person'
    new_person = 'person'

    # accessing name of the last key
    person_id = list(data.keys())[-1][len(new_person):]

    # new key: person + number of the last person + 1
    new_person += str(int(person_id) + 1)

    # adding new key-value pair to data dictionary
    data[new_person] = new_person_info

    return data


def write_to_json(filename: str, data: dict):

    with open(filename, 'w') as file:
        json.dump(data, file)


def show_upcoming_bdays(birthdays: dict):
    """Showing upcoming birthdays within a one month"""

    # sorting 'birthdays' by month, day
    birthdays = dict(sorted(birthdays.items(), key=lambda x: (x[1].month, x[1].day)))

    # today's date
    now = datetime.now()

    print()
    for person, birthday in birthdays.items():

        # condition 1 - when birthday is in upcoming month
        # considering two cases: months from 1 to 11 and december
        if now.month != 12:
            condition1 = birthday.day <= now.day and birthday.month - now.month == 1
        else:
            condition1 = birthday.day <= now.day and birthday.month == 1
        # condition 2 - when birthday is in the same month as now.month
        condition2 = birthday.day >= now.day and birthday.month == now.month

        # one of two conditions must be true
        if condition1 or condition2:
            birthday = birthday.strftime("%d.%m.%Y")
            print(f'{person}: {birthday}')


def refresh_data(filename: str):
    """Update stored data after e.g. adding someone's birthday"""

    data = get_json_data(filename)
    birthdays = store_data_in_dict(data)

    return data, birthdays


def clear_console():
    """Clearing console"""

    system('cls')


def show_banner():
    banner = """

888           888                                                        d8b               888                  
888           888                                                        Y8P               888                  
888           888                                                                          888                  
88888b.   .d88888  8888b.  888  888       888d888  .d88b.  88888b.d88b.  888 88888b.   .d88888  .d88b.  888d888 
888 "88b d88" 888     "88b 888  888       888P"   d8P  Y8b 888 "888 "88b 888 888 "88b d88" 888 d8P  Y8b 888P"   
888  888 888  888 .d888888 888  888       888     88888888 888  888  888 888 888  888 888  888 88888888 888     
888 d88P Y88b 888 888  888 Y88b 888       888     Y8b.     888  888  888 888 888  888 Y88b 888 Y8b.     888     
88888P"   "Y88888 "Y888888  "Y88888       888      "Y8888  888  888  888 888 888  888  "Y88888  "Y8888  888     
                                888                                                                             
                           Y8b d88P                                                                             
                            "Y88P"                                                                              

    """
    print(banner)


def main():
    filename = 'birthdays.json'

    data, birthdays = refresh_data(filename)

    # program menu in while loop
    while True:

        clear_console()
        show_banner()

        # program functionalities
        print()
        print("1: Show persons list")
        print("2: Check someone's birthday")
        print("3: Add someone's birthday")

        # asking user for choice, then executing corresponding function
        choice = input('Type corresopnding number: ')
        if choice == '1':
            show_all_persons(birthdays)
            input('')
        elif choice == '2':
            show_person_bday(birthdays)
            input('')
        elif choice == '3':
            add_person_bday(data, filename)
            data, birthdays = refresh_data(filename)
            input('')
        elif choice == '4':
            show_upcoming_bdays(birthdays)
            input('')
        elif choice == '5':
            delete_person_bday(data, filename)
            data, birthdays = refresh_data(filename)
            input('')
        else:
            break


if __name__ == '__main__':
    main()
