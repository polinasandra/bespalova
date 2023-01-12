from unittest import TestCase
from task_git import Vacancy, DataSet

class DataSetTests(TestCase):
    def test_dataset(self):
        dataset = DataSet("D:/пользователи/OneDrive/Рабочий стол/vacancies.csv",
                                      "Программист", "RUR", "Название", "Да", "1 9")
        self.assertEqual(type(dataset).__name__, "DataSet")
        self.assertEqual(dataset.vacancies_objects, [])


    def test_dataset(self):
        self.assertEqual(DataSet("D:/пользователи/OneDrive/Рабочий стол/vacancies.csv",
                                      "Программист", "RUR", "Название", "Да", "1 9").inDataNumbers, "1 9")

class VacancyTests(TestCase):
    vacancy = Vacancy(
        {'name': 'Программист', 'salary_from': '10000.0', 'salary_to': '35000.0', 'salary_currency': 'RUR',
         'area_name': 'Москва', 'published_at': '2022-05-31T17:32:31+0300'})
    def test_vacancy_salary_to(self):
        self.assertEqual(VacancyTests.vacancy.salary_to, 35000)

    def test_vacancy_salary_from(self):
        self.assertEqual(VacancyTests.vacancy.salary_from, 10000)

    def test_vacancy_salary_currency(self):
        self.assertEqual(VacancyTests.vacancy.salary_currency, 'RUR')

    def test_vacancy_salary_year(self):
        self.assertEqual(VacancyTests.vacancy.year, 2022)

    def test_vacancy_salary_published_at(self):
        self.assertEqual(VacancyTests.vacancy.published, '2022-05-31T17:32:31+0300')