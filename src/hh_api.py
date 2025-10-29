import requests
from typing import List, Dict, Any
from src.base_api import BaseAPI


class HHAPI(BaseAPI):
    """
    Класс для взаимодействия с API HeadHunter.
    """
    def __init__(self) -> None:
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "VacancyParser/1.0"}

    def _connect_to_api(self) -> None:
        try:
            response = requests.get(self._base_url, params={"text": "test"})
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        self._connect_to_api()

        if not keyword or not keyword.strip():
            raise ValueError("Ключевое слово не может быть пустым")

        self._connect_to_api()

        params = {
            "text": keyword,
            "area": 113,
            "per_page": 100,
            "page": 0
        }

        try:
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = [
                vacancy for vacancy in data.get("items", [])
                if vacancy.get("name")
            ]

            return vacancies

        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка получения вакансий: {e}")