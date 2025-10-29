from typing import Optional


class Vacancy:
    """
    Класс представляет вакансии.
    """
    __slots__ = ('_title', '_url', '_salary', '_description', '_requirements', '_employer')
    def __init__(self, title: str, url: str, salary: Optional[dict] = None,
                 description: str = "", requirements: str = "", employer: str = "") -> None:
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = description or "Описание отсутствует"
        self._requirements = requirements or "Требования не указаны"
        self._employer = employer or "Работодатель не указан"

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> str:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    @property
    def employer(self) -> str:
        return self._employer

    def _validate_title(self, title: str) -> str:
        if not title or not title.strip():
            return "Название не указано"
        return title.strip()

    def _validate_url(self, url: str) -> str:
        if not url:
            return "Ссылка не указана"
        return url

    def _validate_salary(self, salary: Optional[dict]) -> str:
        if not salary:
            return "Зарплата не указана"

        salary_from = salary.get('from')
        salary_to = salary.get('to')
        currency = salary.get('currency', '')

        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return "Зарплата не указана"

    def __lt__(self, other: 'Vacancy') -> bool:
        return self._get_avg_salary() < other._get_avg_salary()

    def __gt__(self, other: 'Vacancy') -> bool:
        return self._get_avg_salary() > other._get_avg_salary()

    def _get_avg_salary(self) -> int:
        if self.salary == "Зарплата не указана":
            return 0

        if " - " in self.salary:
            parts = self.salary.split(" - ")
            return (int(parts[0].replace('от', '').strip()) + int(parts[1].split()[0])) // 2
        elif "от" in self.salary:
            return int(self.salary.replace('от', '').split()[0])
        elif "до" in self.salary:
            return int(self.salary.replace('до', '').split()[0])
        return 0

    def __str__(self) -> str:
        return (f"Вакансия: {self.title}\n"
                f"Зарплата: {self.salary}\n"
                f"Требования: {self.requirements}\n"
                f"Ссылка: {self.url}\n")