import csv
import re
import math
#vacancies_with_skills.csv

file = csv.reader(open('vacancies_with_skills.csv', 'r', encoding='utf-8-sig'))


def format_string(x):
    return re.sub(r'\<[^>]*\>', '', x).strip()


def csv_reader(file_name):
    counter = 0
    specialities = []
    for specialitiy in file:
        if counter == 0:
            titles = []
            for a in specialitiy:
                titles.append(a)
            l = len(specialitiy)
        else:
            if len([parameter for parameter in specialitiy if parameter]) == l:
                specialities.append(specialitiy)
        counter += 1

    newSpecialities = []
    for eachList in specialities:
        newList = []
        for x in eachList:
            s = format_string(x)
            newList.append(s)
        newSpecialities.append(newList)

    result = []
    for list1 in newSpecialities:
        newDict = dict(zip(titles, list1))
        result.append(newDict)

    return result


def make_salaries_top(vacancies, if_true):
    counter = 10
    top_arr = []
    for a in vacancies:
        top_arr.append(a)
        if len(top_arr) == counter:
            break
    return top_arr


def make_popular_skills(vacancies):
    skills_list = []
    skills_counter = {}
    for vacancy in vacancies:
        for skill in vacancy['key_skills'].split('\n'):
            if skill not in skills_counter.keys():
                skills_counter[skill] = 1
            else:
                skills_counter[skill] += 1

    for key, value in skills_counter.items():
        skills_list.append((key, value))
    skills_list.sort(key=lambda x: x[1], reverse=True)

    return skills_list


def get_suffix_by_rubles(count):
    if count % 10 == 0 or 5 <= count % 10 <= 9 or 10 <= count % 100 <= 19:
        return 'рублей'
    elif 2 <= count % 10 <= 4:
        return 'рубля'
    else:
        return 'рубль'


def get_suffix_by_count(count):
    if count % 10 == 0 or 5 <= count % 10 <= 9 or 10 <= count % 100 <= 19:
        return 'раз'
    elif 2 <= count % 10 <= 4:
        return 'раза'
    else:
        return 'раз'


def get_suffix_by_vacancy(vacancy_count):
    if vacancy_count % 10 == 0 or 5 <= vacancy_count % 10 <= 9 or 10 <= vacancy_count % 100 <= 19:
        return 'вакансий'
    elif 2 <= vacancy_count % 10 <= 4:
        return 'вакансии'
    else:
        return 'вакансия'


def make_top_of_areas(vacancies):
    salaries_by_areas_counter = {}
    top_arr = []
    for vacancy in vacancies:
        salary = average_amount(vacancy['salary_from'], vacancy['salary_to'])
        if vacancy['area_name'] not in salaries_by_areas_counter.keys():
            salaries_by_areas_counter[vacancy['area_name']] = [salary, 1]
        else:
            salaries_by_areas_counter[vacancy['area_name']][0] += salary
            salaries_by_areas_counter[vacancy['area_name']][1] += 1

    for city, salary in salaries_by_areas_counter.items():
        count_fraction = round(salary[1] / len(vacancies), 3)
        if count_fraction >= 0.01:
            top_arr.append((city, salary[0] // salary[1], salary[1]))
    top_arr.sort(key=lambda x: x[1], reverse=True)

    return top_arr, len(salaries_by_areas_counter)


def print_top_of_salaries(vacancy, condition: int):
    print('Самые высокие зарплаты:') if condition == 1 else print('Самые низкие зарплаты:')
    for i in range(0, len(vacancy)):
        average = average_amount(vacancy[i]['salary_from'], vacancy[i]['salary_to'])
        print(f'    {i + 1}) {vacancy[i]["name"]} в компании "какой то" - {average} '
              f'{get_suffix_by_rubles(average)} (г. {vacancy[i]["area_name"]})')


def print_top_skills(vacancy):
    print(f'Из {(len(vacancy))} скиллов, самыми популярными являются:')
    for i in range(0, min(len(vacancy), 10)):
        print(f'    {i + 1}) {vacancy[i][0]} - упоминается {(vacancy[i][1])} {get_suffix_by_count(vacancy[i][1])}')


def print_top_of_cities(vacancy, count):
    print(f'Из {count} городов, самые высокие средние ЗП:')
    for i in range(0, min(len(vacancy), 10)):
        print(f'    {i + 1}) {vacancy[i][0]} - средняя зарплата {vacancy[i][1]} {get_suffix_by_rubles(vacancy[i][1])}'
              f' ({vacancy[i][2]} {get_suffix_by_vacancy(vacancy[i][2])})')


def average_amount(a, b):
    return math.floor((float(a) + float(b)) / 2)


result = csv_reader(file)
resulted_vacancies = []
for j in result:
    if j['salary_currency'] == 'RUR':
        resulted_vacancies.append(j)

print_top_of_salaries(make_salaries_top(sorted(
    resulted_vacancies, key=lambda x: average_amount(x['salary_from'], x['salary_to']), reverse=True), True), 1)
print()
print_top_of_salaries(make_salaries_top(sorted(
    resulted_vacancies, key=lambda a: average_amount(a['salary_from'], a['salary_to'])), False), 0)
print()
print_top_skills(make_popular_skills(resulted_vacancies))
print()
top_cities, count_city = make_top_of_areas(resulted_vacancies)
print_top_of_cities(top_cities, count_city)
