import pandas as pd
from MainStatistics import MainStatistics

class StatisticsMerger:
    @staticmethod
    def sort_dictionary(dic):
        return dict(sorted(dic.items(), key=lambda item: float(item[1]), reverse=True))

    @staticmethod
    def cut_to_ten_len(dic):
        result = {}
        for x in dic.keys():
            result[x] = dic[x]
            if len(result) == 10:
                return result
        return result

    @staticmethod
    def get_statistics_by_area(file_name):
        read_csv = pd.read_csv(f'{file_name}', delimiter=',')
        salary_dataframe = read_csv[['name', 'salary_from', 'salary_to', 'area_name', 'salary_currency']]
        salary_dataframe = salary_dataframe.assign(salary_middle=lambda x: (x.salary_from + x.salary_to) / 2)
        salary_dataframe['salary_middle'] = salary_dataframe['salary_middle'] * salary_dataframe[
            'salary_currency'].apply(lambda y: MainStatistics.currency_to_rub[y])
        areas_list = []
        salaries_dict = {}
        vacancy_number_dict = {}
        groupped_by_towns_df = salary_dataframe.groupby('area_name')
        for a in salary_dataframe.itertuples():
            area_name = a[4]
            if area_name in areas_list:
                continue
            else:
                areas_list.append(area_name)
        for area in areas_list:
            current_group = groupped_by_towns_df.get_group(area)
            if len(current_group) < len(salary_dataframe)/100:
                continue
            else:
                salaries_dict[area] = round(current_group['salary_middle'].mean())
                vacancy_number_dict[area] = len(current_group['salary_middle'])
        salaries_dict = StatisticsMerger.cut_to_ten_len(StatisticsMerger.sort_dictionary(salaries_dict))
        vacancy_number_dict = StatisticsMerger.cut_to_ten_len(StatisticsMerger.sort_dictionary(vacancy_number_dict))
        return vacancy_number_dict, salaries_dict

    @staticmethod
    def merge_statistics(statistics_objects_array, full_file_name: str):
        towns_statistics_amount_dic, towns_statistics_salary_dic = StatisticsMerger.get_statistics_by_area(
            full_file_name)
        number_by_year = {}
        mid_salary_by_year = {}
        vacancy_amount_by_year = {}
        vacancy_mid_salary_by_year = {}
        for year_stat_object in statistics_objects_array:
            number_by_year[year_stat_object.year] = year_stat_object.vacancy_number_by_year
            mid_salary_by_year[year_stat_object.year] = round(year_stat_object.average_salary_by_year)
            vacancy_amount_by_year[year_stat_object.year] = year_stat_object.vacancy_number_by_year_for_vac
            vacancy_mid_salary_by_year[year_stat_object.year] = round(year_stat_object.average_salary_by_year_for_vac)
        print(f'Динамика уровня зарплат по годам: {number_by_year}')
        print(f'Динамика количества вакансий по годам: {mid_salary_by_year}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {vacancy_amount_by_year}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {vacancy_mid_salary_by_year}')
        print(f'Уровень зарплат по городам (в порядке убывания): {towns_statistics_salary_dic}')
        print(f'Доля вакансий по городам (в порядке убывания): {towns_statistics_amount_dic}')


