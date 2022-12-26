import pandas as pd

class MainStatistics:
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
        "UZS": 0.0055
    }

    @staticmethod
    def make_statistics_dictionaries(tuple_vacancy):
        file_name, vacancy_name = tuple_vacancy
        read_csv = pd.read_csv(f'parsed_data/{file_name}', delimiter=',')
        salary_dataframe = read_csv[['name','salary_from','salary_to','salary_currency']]
        salary_dataframe = salary_dataframe.assign(salary_middle=lambda x: (x.salary_from + x.salary_to)/2)
        salary_dataframe['salary_middle'] = salary_dataframe['salary_middle'] * salary_dataframe['salary_currency'].apply(lambda y: MainStatistics.currency_to_rub[y])
        one_vacancy_statistics_dataframe = salary_dataframe.loc[salary_dataframe['name'].str.contains(vacancy_name)]
        average_salary_by_year = salary_dataframe['salary_middle'].mean()
        average_salary_of_vacancy = one_vacancy_statistics_dataframe['salary_middle'].mean()
        vacancy_number_by_year = len(salary_dataframe['salary_middle'])
        vacancy_number_by_vacancy = len(one_vacancy_statistics_dataframe['salary_middle'])

        return MainStatisticsInfo(round(average_salary_by_year, 2), vacancy_number_by_year, round(average_salary_of_vacancy, 2),
                                  vacancy_number_by_vacancy, file_name[len(file_name)-8:len(file_name)-4])
class MainStatisticsInfo:
    def __init__(self, average_salary_by_year, vacancy_number_by_year, average_salary_by_year_for_vac,
             vacancy_number_by_year_for_vac, year):
        self.average_salary_by_year = average_salary_by_year
        self.vacancy_number_by_year = vacancy_number_by_year
        self.average_salary_by_year_for_vac = average_salary_by_year_for_vac
        self.vacancy_number_by_year_for_vac = vacancy_number_by_year_for_vac
        self.year = year

