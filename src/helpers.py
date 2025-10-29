from typing import List, Dict, Any
from src.vacancy import Vacancy

def convert_to_vacancy_objects(data: List[Dict[str, Any]]) -> List[Vacancy]:
    """Конвертировать данные"""
    vacancies = []
    for item in data:
        vacancy = Vacancy(
            title=item.get('name', ''),
            url=item.get('alternate_url', ''),
            salary=item.get('salary'),
            description=item.get('snippet', {}).get('responsibility', ''),
            requirements=item.get('snippet', {}).get('requirement', ''),
            employer=item.get('employer', {}).get('name', '')
        )
        vacancies.append(vacancy)
    return vacancies

def get_top_n_by_salary(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    sorted_vacancies = sorted(vacancies, reverse=True)
    return sorted_vacancies[:n]

def filter_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    keyword = keyword.lower()
    return [
        v for v in vacancies
        if keyword in v.description.lower() or
           keyword in v.requirements.lower() or
           keyword in v.employer.lower()
    ]