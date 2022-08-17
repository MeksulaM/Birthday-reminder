import json
from os import system, path
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
        birthday = datetime.strptime(info['birthday'], '%Y-%m-%d')
        birthday = birthday.date()
        # birthday = info['birthday']

        # adding key-value pair to birthday's dictionary
        birthdays[full_name] = birthday

    return birthdays


def show_all_bdays(birthdays: dict):
    """Print list of persons we know birthdays"""

    # for calculating persosn's age
    now = datetime.now()
    # sorting 'birthdays' dict by keys, that is, full names
    birthdays = dict(sorted(birthdays.items(), key=lambda x: x[0]))

    # if dict is not empty
    if birthdays:
        print()
        for person, birthday in birthdays.items():
            age = now.year - birthday.year
            birthday = birthday.strftime("%d.%m.%Y")
            print(f'\t-{person}: {birthday}, currently {age} years old')

    # if dict is empty
    else:
        print('\nThere is no one to show')
        print("Please add someone's birthday")


def show_person_bday(birthdays: dict):
    """Print choosen person's birthday"""

    # if dict is not empty
    if birthdays:
        # asking user for input
        user_input = input("\nWho's birthday do you want to check?: ").title()

        # checking if input is valid
        if user_input in birthdays.keys():

            # formating output to DD.MM.YYYY
            # bday = birthdays[user_input].date()
            bday = birthdays[user_input].strftime("%d.%m.%Y")
            print(f"{user_input}'s birthday is {bday}")

        # for invalid input
        else:
            print('Incorrect input')

    # if dict is empty
    else:
        print('\nThere is no one to show')
        print("Please add someone's birthday")


def delete_person_bday(data: dict, filename: str):
    """Deleting key-value pair from json dict"""

    if data:
        # finding dictionary key and creating variables for message at the end
        person_to_del, first_name, last_name = find_dict_key(data)
        full_name = first_name + ' ' + last_name

        # if inputs does not match any existing values in data
        if not person_to_del:
            print(f"There is no {full_name.title()}'s birthday in memory already")

        else:

            # deleting key-value pair from dictionary
            del data[person_to_del]

            # format keys names after removing one key-value pair
            data_formated = format_keys_names(data)

            # updating json data
            write_to_json(filename, data_formated)

            # printing fancy message to the user
            print(f"{full_name.title()}'s birthday removed successfully")
    else:
        print("\nThere is no one to delete")


def find_dict_key(data: dict):
    """Return key that matches user inputs"""

    # asking user who to delete
    full_name = input('\nWho to delete?: ')

    # checking if input is valid
    try:
        first_name, last_name = full_name.split()
    except ValueError:
        print('Incorrect input')
        return find_dict_key(data)

    # if input is valid
    else:

        # finding key name that matches user inputs
        for person, info in data.items():
            condition1 = first_name == info['first_name']
            condition2 = last_name == info['last_name']
            if condition1 and condition2:
                person_to_del = person
                return person_to_del, first_name, last_name

        # if inputs does not match
        return False, first_name, last_name


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

    if data:
        # creating dict with new person's info
        new_person_info = create_new_person_dict()

        # updating 'data' with new person's info
        data = add_key_value(data, new_person_info)

        # updating json data
        write_to_json(filename, data)

        # printing fancy message to the user
        full_name = new_person_info['first_name'] + ' ' + new_person_info['last_name']
        print(f"{full_name.title()}'s birthday added succsessfully")

    else:
        create_json(filename)


def create_new_person_dict():
    """Asking user to provide info, then storing info in dict"""

    # empty dictionary to store info about new person
    new_person_info = {}

    # asking user for new person info
    first_name = input('\nFirst name: ')
    last_name = input('Last name: ')
    birthday = bday_from_user()

    # adding inputs to dictionary
    new_person_info['first_name'] = first_name
    new_person_info['last_name'] = last_name
    new_person_info['birthday'] = birthday

    return new_person_info


def bday_from_user():
    """Validation of date input"""

    birthday = input('Birthday (format: DD.MM.YYYY): ')
    try:
        birthday = datetime.strptime(birthday, '%d.%m.%Y').date()
    except ValueError:
        print('Incorrect input')
        return bday_from_user()
    else:
        return birthday


def add_key_value(data: dict, new_person_info: dict):
    """determinig name of the new key in json dictionary"""

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
        json.dump(data, file, default=str, indent=4)


def show_upcoming_bdays(birthdays: dict):
    """Showing upcoming birthdays within a one month"""

    # flag checking if someone have birthday in a month
    zero_upcoming_bdays = True

    # sorting 'birthdays' by month, day
    birthdays = dict(sorted(birthdays.items(), key=lambda x: (x[1].month, x[1].day)))

    # today's date
    now = datetime.now().date()

    print('\nUpcoming birthdays:')
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

            # changing value of the flag, so last if statement will not execute
            zero_upcoming_bdays = False

            # formating, calculating age
            bday_num = now.year - birthday.year
            birthday_str = birthday.strftime("%d.%m.%Y")

            # if someone has a birthday today, letting user know about this
            if now.day == birthday.day and now.month == birthday.month:
                print(f'\t-{person} has a {bday_num}th birthday today')
            else:
                print(f'\t-{person}: {birthday_str} - {bday_num}th birthday')


    # if the above loop did not change the value of a flag
    if zero_upcoming_bdays:
        print('\t-No one has a birthday in a month')


def refresh_data(filename: str):
    """Update stored data after e.g. adding someone's birthday"""

    data = get_json_data(filename)
    birthdays = store_data_in_dict(data)

    return data, birthdays


def create_json(filename: str):
    """Function that creates json file and adds first data"""

    data = {}

    first_person_info = create_new_person_dict()

    data['person1'] = first_person_info

    write_to_json(filename, data)

    # printing fancy message to the user
    full_name = first_person_info['first_name'] + ' ' + first_person_info['last_name']
    print(f"{full_name.title()}'s birthday added succsessfully")


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
                            "Y88P"        by Mati                                                                          

    """
    print(banner)


def main():
    clear_console()
    show_banner()
    # filename = 'test.json'
    filename = 'birthdays.json'

    # checking if json file exist
    if not path.isfile(filename):
        # if not, create
        print("Welcome to the bday reminder")
        print("To continue, enter information about first person:")
        create_json(filename)
        input('')

    data, birthdays = refresh_data(filename)

    # program menu in while loop
    while True:

        clear_console()
        show_banner()
        print("Welcome to the bday reminder")
        show_upcoming_bdays(birthdays)

        # program functionalities
        print('\nWhat do you want to do?:')
        print("\t1: Show all birthdays")
        print("\t2: Check someone's birthday")
        print("\t3: Add someone's birthday")
        print("\t4: Delete someone's birthday")
        print("\tany key: exit")

        # asking user for choice, then executing corresponding function
        choice = input('Type corresopnding number: ')
        if choice == '1':
            clear_console()
            show_banner()
            show_all_bdays(birthdays)
            input('')
        elif choice == '2':
            clear_console()
            show_banner()
            show_person_bday(birthdays)
            input('')
        elif choice == '3':
            clear_console()
            show_banner()
            add_person_bday(data, filename)
            data, birthdays = refresh_data(filename)
            input('')
        elif choice == '4':
            clear_console()
            show_banner()
            delete_person_bday(data, filename)
            data, birthdays = refresh_data(filename)
            input('')
        else:
            break


if __name__ == '__main__':
    main()
