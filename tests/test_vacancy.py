import pytest
from src.vacancy import Vacancy


class TestVacancy:

    def test_vacancy_creation(self):
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Django",
            requirements="Опыт Python 3+",
            employer="IT Company"
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary == "100000 - 150000 RUR"
        assert vacancy.employer == "IT Company"

    def test_vacancy_without_salary(self):
        vacancy = Vacancy(
            title="Developer",
            url="https://hh.ru/vacancy/456",
            description="Разработка",
            requirements="Опыт"
        )

        assert vacancy.salary == "Зарплата не указана"
        assert vacancy.description == "Разработка"

    def test_vacancy_comparison(self):
        vacancy1 = Vacancy(
            title="Junior",
            url="url1",
            salary={"from": 50000},
            description="",
            requirements=""
        )

        vacancy2 = Vacancy(
            title="Senior",
            url="url2",
            salary={"from": 150000},
            description="",
            requirements=""
        )

        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert not vacancy1 == vacancy2

    def test_vacancy_validation(self):
        vacancy = Vacancy(title="", url="", salary=None)

        assert vacancy.title == "Название не указано"
        assert vacancy.url == "Ссылка не указана"
        assert vacancy.salary == "Зарплата не указана"

    def test_vacancy_string_representation(self):
        vacancy = Vacancy(
            title="Test",
            url="https://test.ru",
            salary={"from": 100000}
        )

        result = str(vacancy)
        assert "Test" in result
        assert "100000" in result


if __name__ == "__main__":
    pytest.main()