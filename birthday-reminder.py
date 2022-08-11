import json

filename = 'birthdays.json'

with open(filename, 'r') as file:
    birthdays = json.load(file)

print('Welcome to birthdays reminder!')
print('We know birthdays of:')
for value in birthdays.values():
    print(value['first_name'].title(), value['last_name'].title())