import pytest
from src.helpers import convert_to_vacancy_objects, get_top_n_by_salary, filter_by_keyword
from src.vacancy import Vacancy


class TestHelpers:

    def test_convert_to_vacancy_objects(self):
        api_data = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {
                    "responsibility": "Backend development",
                    "requirement": "Python 3+"
                },
                "employer": {"name": "IT Company"}
            }
        ]

        vacancies = convert_to_vacancy_objects(api_data)

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].title == "Python Developer"
        assert vacancies[0].url == "https://hh.ru/vacancy/123"

    def test_convert_empty_data(self):
        vacancies = convert_to_vacancy_objects([])
        assert vacancies == []

    def test_get_top_n_by_salary(self):
        vacancies = [
            Vacancy("Low", "url1", {"from": 50000}, "", ""),
            Vacancy("High", "url2", {"from": 150000}, "", ""),
            Vacancy("Medium", "url3", {"from": 100000}, "", "")
        ]

        top_2 = get_top_n_by_salary(vacancies, 2)

        assert len(top_2) == 2
        assert top_2[0].title == "High"  # Самая высокая зарплата
        assert top_2[1].title == "Medium"

    def test_get_top_more_than_available(self):
        vacancies = [
            Vacancy("Job", "url", {"from": 50000}, "", "")
        ]

        top_5 = get_top_n_by_salary(vacancies, 5)
        assert len(top_5) == 1

    def test_filter_by_keyword(self):
        vacancies = [
            Vacancy("Python Developer", "url1", None, "Python development", "Python experience"),
            Vacancy("Java Developer", "url2", None, "Java development", "Java experience"),
            Vacancy("Manager", "url3", None, "Management", "No programming")
        ]

        python_vacancies = filter_by_keyword(vacancies, "python")

        assert len(python_vacancies) == 1
        assert python_vacancies[0].title == "Python Developer"

    def test_filter_by_nonexistent_keyword(self):
        vacancies = [
            Vacancy("Developer", "url", None, "Development", "Coding")
        ]

        filtered = filter_by_keyword(vacancies, "nonexistent")
        assert len(filtered) == 0


if __name__ == "__main__":
    pytest.main()