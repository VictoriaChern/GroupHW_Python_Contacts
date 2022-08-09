import phonebook
def edit(phonebook):
    print("Введите имя контакта, который хотите изменить: ")
    name = input(" ")
    for index, contact in enumerate(phonebook):
        if contact['name'] == name:
            print("Введите новое имя контакта: ")
            new_name = input(" ")
            print("Введите новый телефон контакта: ")
            new_phone = input(" ")
            contact_update = {
                'name': new_name,
                'phone': new_phone
            }
            phonebook[index] = contact_update
            index = -1
            break
    if index == -1:
        print("Контакт изменен")
    else:
        print("Контакт не найден")