import pytest
import json
import os
import tempfile
from src.json_handler import JSONHandler


class TestJSONHandler:

    def setup_method(self):

        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_vacancies.json")
        self.handler = JSONHandler(self.test_file)

    def teardown_method(self):

        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_default_filename(self):

        handler = JSONHandler()
        assert handler.filename == "vacancies.json"

    def test_custom_filename(self):

        handler = JSONHandler("custom.json")
        assert handler.filename == "custom.json"

    def test_add_vacancy(self):

        vacancy_data = {
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "100000 - 150000 RUR",
            "description": "Development",
            "requirements": "Python",
            "employer": "IT Company"
        }

        self.handler.add_vacancy(vacancy_data)

        assert os.path.exists(self.test_file)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["title"] == "Python Developer"

    def test_add_duplicate_vacancy(self):

        vacancy_data = {
            "title": "Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "100000 RUR"
        }

        self.handler.add_vacancy(vacancy_data)
        self.handler.add_vacancy(vacancy_data)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1

    def test_get_vacancies_empty_file(self):
        vacancies = self.handler.get_vacancies()
        assert vacancies == []

    def test_get_vacancies_with_criteria(self):
        vacancies_data = [
            {
                "title": "Python Developer",
                "url": "https://hh.ru/vacancy/1",
                "salary": "100000 RUR",
                "employer": "Company A"
            },
            {
                "title": "Java Developer",
                "url": "https://hh.ru/vacancy/2",
                "salary": "120000 RUR",
                "employer": "Company B"
            }
        ]

        for vacancy in vacancies_data:
            self.handler.add_vacancy(vacancy)

        python_vacancies = self.handler.get_vacancies({"title": "Python"})
        assert len(python_vacancies) == 1
        assert python_vacancies[0]["title"] == "Python Developer"

    def test_delete_vacancy(self):
        vacancy_data = {
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "100000 RUR",
            "employer": "IT Company"
        }

        self.handler.add_vacancy(vacancy_data)
        self.handler.delete_vacancy({"title": "Python Developer"})
        vacancies = self.handler.get_vacancies()
        assert len(vacancies) == 0

    def test_delete_nonexistent_vacancy(self):
        self.handler.delete_vacancy({"title": "Nonexistent"})
        assert True


if __name__ == "__main__":
    pytest.main()