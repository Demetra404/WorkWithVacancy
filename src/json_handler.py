import json
import os
from typing import List, Dict, Any, Optional
from src.base_file_handler import BaseFileHandler


class JSONHandler(BaseFileHandler):
    """
    Класс для работы с JSON-файлами вакансий.
    """

    def __init__(self, filename: Optional[str] = None) -> None:

        super().__init__(filename)
        self._encoding = "utf-8"

    def _get_default_filename(self) -> str:

        return "vacancies.json"

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        vacancies = self.get_vacancies()

        if not any(v.get('url') == vacancy.get('url') for v in vacancies):
            vacancies.append(vacancy)

            with open(self._filename, 'w', encoding=self._encoding) as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
            print(f"Вакансия добавлена")
        else:
            print("Вакансии нет")

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:

        if not os.path.exists(self._filename):
            return []

        try:
            with open(self._filename, 'r', encoding=self._encoding) as f:
                vacancies = json.load(f)

            if not criteria:
                return vacancies

            filtered = []
            for vacancy in vacancies:
                match = True
                for key, value in criteria.items():
                    if key in vacancy:
                        if isinstance(value, str) and value.lower() not in str(vacancy[key]).lower():
                            match = False
                            break
                    else:
                        match = False
                        break
                if match:
                    filtered.append(vacancy)

            return filtered

        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения: {e}")
            return []

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        vacancies = self.get_vacancies()
        if not vacancies:
            print("Файл пуст")
            return

        initial_count = len(vacancies)
        filtered = [vacancy for vacancy in vacancies
                    if not self._good_criteriy(vacancy, criteria)
                    #all(str(v.get(k, '')).lower() == str(v).lower() for k, v in criteria.items()
        ]

        if len(filtered) < initial_count:
            with open(self._filename, 'w', encoding=self._encoding) as f:
                json.dump(filtered, f, ensure_ascii=False, indent=2)
            print(f"Удалено {initial_count - len(filtered)} вакансий")
        else:
            print("Не найдено вакансий для удаления по заданным критериям")

    def _good_criteriy(self, vacancy: Dict[str, Any], criteria: Dict[str, Any]) -> bool:

        for key, expected_value in criteria.items():
            actual_value = vacancy.get(key, '')

            if isinstance(expected_value, str) and isinstance(actual_value, str):
                if expected_value.lower() not in actual_value.lower():
                    return False
            else:
                if actual_value != expected_value:
                    return False

        return True
"""
def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
    vacancies = self.get_vacancies()

    if not any(v.get('url') == vacancy.get('url') for v in vacancies):
        vacancies.append(vacancy)
        with open(self._filename, 'w', encoding=self._encoding) as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)
        print(f" Вакансия добавлена в файл: {self._filename}")
    else:
        print(" Вакансия уже существует")
        """