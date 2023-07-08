import csv
import re


def get_contact_list(file_name):
    with open(file_name, encoding="utf8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def fix_column(contacts_list):
    """
    Функция исправляет количество столбцов в csv файле
    """
    length = len(contacts_list[0])
    for index, contact in enumerate(contacts_list):
        contacts_list[index] = contact[:length]
    return contacts_list


def fix_fio(contacts_list):
    """
    Функция для переноса ФИО по столбцам
    """
    for line in contacts_list[1:]:
        fio = re.search(r'([а-я]+[ин|ов|ев]а?) ([а-я]+) ?([а-я]+[ич|вна])?', ' '.join(line[:3]).strip(), flags=re.I)
        line[0], line[1], line[2] = fio.group(1), fio.group(2), fio.group(3)
    return contacts_list


def fix_phones(contacts_list):
    """
    Функция для перевода номеров к единому формату
    """
    for line in contacts_list[1:]:
        line[5] = re.sub(r'(\+?[7|8])? ?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2}) ?\(?(доб.\)?)? ?(\d{4})?\)?', r'+7(\2)\3-\4-\5 \6\7', line[5])
        line[5] = line[5].strip()
    return contacts_list


def merge_contacts(contacts_list):
    """
    Функция для объединения повторяющихся записей
    """
    surnames = {}
    fixed_list = [contacts_list[0]]

    for num, line in enumerate(contacts_list[1:]):
        if line[0] not in surnames.keys():
            surnames[line[0]] = num + 1
        else:
            fix_line = contacts_list[surnames[line[0]]]
            for i in range(1, 7):
                fix_line[i] = fix_line[i] or line[i]

    for index in surnames.values():
        fixed_list.append(contacts_list[index])

    return fixed_list


def write_csv(contacts_list, file_name):
    """
    Функция для записи файла в формате CSV
    """
    with open(file_name, "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


def main():
    result = get_contact_list('phonebook_raw.csv')
    result = fix_column(result)
    result = fix_fio(result)
    result = fix_phones(result)
    result = merge_contacts(result)
    write_csv(result, 'phonebook.csv')


if __name__ == '__main__':
    main()
    