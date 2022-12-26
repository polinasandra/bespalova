from AsynchStatisticsLoader import AsynchStatisticsLoader
file_name = 'vacancies_by_year.csv'

def main():
    print('start_code')
    AsynchStatisticsLoader.make_statistics(vacancy_name='Аналитик', full_file_name=file_name)


if __name__ == '__main__':
    main()

