import csv
import re
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side
# D:/пользователи/OneDrive/Рабочий стол/vacancies_by_year.csv
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pathlib
import pdfkit


requests = ["Введите название файла: ", "Введите название профессии: "]


class Vacancy:
    names = ['number', 'name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary',
             'area_name', 'published_at']

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, vacancy):
        self.name = vacancy['name']
        self.salary_from = int(vacancy['salary_from'].split('.')[0])
        self.salary_to = int(vacancy['salary_to'].split('.')[0])
        self.salary_currency = vacancy['salary_currency']
        self.average_salary = self.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2
        self.area_name = vacancy['area_name']
        self.published_at = int(vacancy['published_at'].rsplit('T', 1)[0].split('-')[0])


class DataSet:
    def __init__(self, fileName, vacancyName):
        self.fileName = fileName
        self.vacancyName = vacancyName

    def csv_reader(self):
        r = open(self.fileName, encoding='utf-8-sig')
        file = csv.reader(r)
        titles = []
        for counter, specialitiy in enumerate(file):
            if counter == 0:
                titles = specialitiy
                l = len(specialitiy)
            else:
                if len([parameter for parameter in specialitiy if parameter]) == l:
                    yield dict(zip(titles, specialitiy))

    @staticmethod
    def check_key(dictionary, key, var):
        if key in dictionary:
            dictionary[key] += var
        else:
            dictionary[key] = var

    def make_statistic_data(self):
        salaryDict = {}
        salaryArea = {}
        vacancySalary = {}
        vacanciesCounter = 0

        for dictionar in self.csv_reader():
            vacancy = Vacancy(dictionar)
            self.check_key(salaryDict, vacancy.published_at, [vacancy.average_salary])
            if vacancy.name.find(self.vacancyName) != -1:
                self.check_key(vacancySalary, vacancy.published_at, [vacancy.average_salary])
            self.check_key(salaryArea, vacancy.area_name, [vacancy.average_salary])
            vacanciesCounter += 1

        arr = []
        for key, value in salaryDict.items():
            arr.append((key, len(value)))
        numberOfVacancies = dict(arr)

        arr1 = []
        for key, value in vacancySalary.items():
            arr1.append((key, len(value)))
        vacancyNameCounter = dict(arr1)

        if not vacancySalary:
            arr2 = []
            for key, value in salaryDict.items():
                arr2.append((key, [0]))
            vacancySalary = dict(arr2)

            arr3 = []
            for key, value in numberOfVacancies.items():
                arr3.append((key, 0))
            vacancyNameCounter = dict(arr3)

        statistics_of_salary = self.count_average_number(salaryDict)
        statistics_of_salary_by_vacancy = self.count_average_number(vacancySalary)
        statistics_of_salary_by_area = self.count_average_number(salaryArea)
        temp_dict_of_statistics = {}
        for publishedData, salariesArr in salaryArea.items():
            temp_dict_of_statistics[publishedData] = round(len(salariesArr) / vacanciesCounter, 4)
        temp_arr = []
        for key, value in temp_dict_of_statistics.items():
            temp_arr.append((key, value))
        filtered_arr = filter(lambda x: x[-1] >= 0.01, temp_arr)
        temp_dict_of_statistics = list(filtered_arr)
        temp_dict_of_statistics.sort(key=lambda x: x[-1], reverse=True)
        result_statistics = temp_dict_of_statistics
        temp_dict_of_statistics = dict(temp_dict_of_statistics)

        temp_arr_2 = []
        for key, value in statistics_of_salary_by_area.items():
            temp_arr_2.append((key, value))
        filtered_arr_2 = filter(lambda x: x[0] in list(temp_dict_of_statistics.keys()), temp_arr_2)
        statistics_of_salary_by_area = list(filtered_arr_2)
        statistics_of_salary_by_area.sort(key=lambda a: a[-1], reverse=True)
        statistics_of_salary_by_area = dict(statistics_of_salary_by_area[:10])
        result_statistics = dict(result_statistics[:10])

        return statistics_of_salary, numberOfVacancies, statistics_of_salary_by_vacancy, vacancyNameCounter, statistics_of_salary_by_area, result_statistics

    @staticmethod
    def count_average_number(dict_to_count):
        result = {}
        for key, value in dict_to_count.items():
            a = sum(value)
            b = len(value)
            result[key] = int(a / b)
        return result


class Report:
    def __init__(self, vacancyName, statistics, statistics_of_salary_by_vacancy, statistics_of_salary_by_area,
                 temp_dict_of_statistics, result_statistics, statistics_of_vacancy_by_year):
        self.wb = Workbook()
        self.vacancyName = vacancyName
        self.statistics = statistics
        self.statistics_of_salary_by_vacancy = statistics_of_salary_by_vacancy
        self.statistics_of_salary_by_area = statistics_of_salary_by_area
        self.temp_dict_of_statistics = temp_dict_of_statistics
        self.result_statistics = result_statistics
        self.statistics_of_vacancy_by_year = statistics_of_vacancy_by_year

    def generate_excel(self):
        list1 = self.wb.active
        list1.title = 'Статистика по годам'
        array_for_titles = ['Год', 'Средняя зарплата', 'Средняя зарплата - ' + self.vacancyName, 'Количество вакансий',
                            'Количество вакансий - ' + self.vacancyName]
        list1.append(array_for_titles)
        for date in self.statistics.keys():
            list1.append([date, self.statistics[date], self.statistics_of_salary_by_area[date],
                          self.statistics_of_salary_by_vacancy[date], self.temp_dict_of_statistics[date]])

        titles = [['Год ', 'Средняя зарплата ', ' Средняя зарплата - ' + self.vacancyName, ' Количество вакансий',
                   ' Количество вакансий - ' + self.vacancyName]]
        widthOfColums = []
        for number in titles:
            for i, element in enumerate(number):
                widthOfColums = self.set_colums_length(element, i, widthOfColums)

        for i, j in enumerate(widthOfColums, 1):
            converted_var = get_column_letter(i)
            list1.column_dimensions[converted_var].width = j + 2

        titles = []
        titles.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий'])
        new_dictionary = zip(self.result_statistics.items(), self.statistics_of_vacancy_by_year.items())
        for (first_area, i), (second_area, j) in new_dictionary:
            titles.append([first_area, i, '', second_area, j])

        list2 = self.wb.create_sheet('Статистика по городам')
        for number in titles:
            list2.append(number)

        widthOfColums = []
        for number in titles:
            for i, element in enumerate(number):
                element = str(element)
                if len(widthOfColums) > i:
                    if len(element) > widthOfColums[i]:
                        widthOfColums[i] = len(element)
                else:
                    widthOfColums += [len(element)]

        for i, j in enumerate(widthOfColums, 1):
            list2.column_dimensions[get_column_letter(i)].width = j + 2

        bold = Font(bold=True)
        for column in 'ABCDE':
            list1[column + '1'].font = bold
            list2[column + '1'].font = bold

        for x, y in enumerate(self.result_statistics):
            string_for_x = str(x + 2)
            list2['E' + string_for_x].number_format = '0.00%'

        thin = Side(border_style='thin', color='00000000')

        for number in range(len(titles)):
            for column in 'ABDE':
                self.make_border(column, number, thin, list2)

        for number, y in enumerate(self.statistics):
            for column in 'ABCDE':
                self.make_border(column, number, thin, list1)

        self.wb.save('report.xlsx')

    def generate_pdf(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("python.html")
        reault_array = []
        for date in self.statistics.keys():
            reault_array.append([date, self.statistics[date], self.statistics_of_salary_by_vacancy[date],
                                 self.statistics_of_salary_by_area[date], self.temp_dict_of_statistics[date]])
        for item in self.statistics_of_vacancy_by_year:
            rounded = round(self.statistics_of_vacancy_by_year[item] * 100, 2)
            self.statistics_of_vacancy_by_year[item] = rounded

        pdf_template = template.render({'name': self.vacancyName, 'path': '{0}/{1}'.format(pathlib.Path(__file__).parent.resolve(), 'graph.png'),
                                        'reault_array': reault_array, 'result_statistics': self.result_statistics,
                                        'statistics_of_vacancy_by_year': self.statistics_of_vacancy_by_year})

        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={"enable-local-file-access": ""})


    def generate_image(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

        ax1.set_title('Уровень зарплат по годам', fontdict={'fontsize': 12})
        ax1.grid(axis='y')

        list_for_stats = list(self.statistics.keys())
        ax1.legend((ax1.bar(np.array(list_for_stats) - 0.4, self.statistics.values(), width=0.4)[0],
                    ax1.bar(np.array(list_for_stats), self.statistics_of_salary_by_area.values(), width=0.4)[0]),
                   ('средняя з/п', 'з/п ' + self.vacancyName.lower()), prop={'size': 8})
        ax1.set_xticks(np.array(list_for_stats) - 0.2, list_for_stats, rotation=90)
        ax1.xaxis.set_tick_params(labelsize=8)
        ax1.yaxis.set_tick_params(labelsize=8)

        list_for_salary_stats = list(self.statistics_of_salary_by_vacancy.keys())
        ax2.set_title('Количество вакансий по годам', fontdict={'fontsize': 12})
        ax2.legend((ax2.bar(np.array(list_for_salary_stats) - 0.4,
                            self.statistics_of_salary_by_vacancy.values(), width=0.4)[0],
                    ax2.bar(np.array(list_for_salary_stats), self.temp_dict_of_statistics.values(), width=0.4)[0]),
                   ('Количество вакансий', 'Количество вакансий\n' + self.vacancyName.lower()), prop={'size': 8})
        ax2.set_xticks(np.array(list_for_salary_stats) - 0.2, list_for_salary_stats, rotation=90)
        ax2.grid(axis='y')
        ax2.xaxis.set_tick_params(labelsize=8)
        ax2.yaxis.set_tick_params(labelsize=8)

        list_for_result_keys = list(self.result_statistics.keys())
        list_for_result_values = list(self.result_statistics.values())
        ax3.set_title('Уровень зарплат по городам', fontdict={'fontsize': 12})

        new_list = []
        for a in reversed(list_for_result_keys):
            new_list.append(str(a).replace(' ', '\n').replace('-', '-\n'))

        ax3.barh(new_list, list(reversed(list_for_result_values)), align='center')
        ax3.yaxis.set_tick_params(labelsize=6)
        ax3.xaxis.set_tick_params(labelsize=8)
        ax3.grid(axis='x')

        list_for_stats_date_values = list(self.statistics_of_vacancy_by_year.values())
        list_for_stats_date_keys = list(self.statistics_of_vacancy_by_year.keys())

        ax4.set_title('Доля вакансий по городам', fontdict={'fontsize': 12})

        counter = []
        for i in self.statistics_of_vacancy_by_year.values():
            counter.append(i)

        others = 1 - sum(counter)
        ax4.pie([others] + list_for_stats_date_values, labels=['Другие'] + list_for_stats_date_keys,
                textprops={'fontsize': 6})

        plt.tight_layout()
        plt.savefig('graph.png')

    def set_colums_length(self, element, i, widthOfColums):
        length = len(element)
        if len(widthOfColums) > i:
            if length > widthOfColums[i]:
                widthOfColums[i] = length
        else:
            widthOfColums += [length]
        return widthOfColums

    def make_border(self, column, number, thin, list2):
        list2[column + str(number + 1)].border = Border(left=thin, bottom=thin, right=thin, top=thin)


class InputConnect:
    def __init__(self):
        self.fileName = input(requests[0])
        self.vacancyName = input(requests[1])
        data_set = DataSet(self.fileName, self.vacancyName)
        statistics, statistics_of_salary_by_vacancy, statistics_of_salary_by_area, temp_dict_of_statistics, result_statistics, statistics_of_vacancy_by_year = data_set.make_statistic_data()

        print('Динамика уровня зарплат по годам: {0}'.format(statistics))
        print('Динамика количества вакансий по годам: {0}'.format(statistics_of_salary_by_vacancy))
        print('Динамика уровня зарплат по годам для выбранной профессии: {0}'.format(statistics_of_salary_by_area))
        print('Динамика количества вакансий по годам для выбранной профессии: {0}'.format(temp_dict_of_statistics))
        print('Уровень зарплат по городам (в порядке убывания): {0}'.format(result_statistics))
        print('Доля вакансий по городам (в порядке убывания): {0}'.format(statistics_of_vacancy_by_year))

        report = Report(self.vacancyName, statistics, statistics_of_salary_by_vacancy, statistics_of_salary_by_area,
                        temp_dict_of_statistics, result_statistics, statistics_of_vacancy_by_year)
        report.generate_excel()
        report.wb.save(filename='report.xlsx')
        report.generate_image()
        report.generate_pdf()


if __name__ == '__main__':
    InputConnect()