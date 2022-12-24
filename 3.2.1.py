import pandas as pd
import threading


def write_chunk_to_file(df: pd.DataFrame, file_name):
    df.to_csv(path_or_buf=file_name, index=False, encoding='utf-8-sig')


file_to_parse = input('Введите название файла: ') # vacancies_by_year.csv
arr_of_titles = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']

data = pd.read_csv(file_to_parse)
data['year'] = data['published_at'].apply(lambda x: x[:4])
years = data['year'].unique()
thread_pool = []

for year in years:
    if_data_accepted = data['year'] == year
    year_data = data[if_data_accepted]
    thread = threading.Thread(target=write_chunk_to_file, args=(
        year_data[arr_of_titles], f'parsed_data/data_sorted_by_{year}.csv'))
    thread_pool.append(thread)

for thread in thread_pool:
    thread.start()

for thread in thread_pool:
    thread.join()
