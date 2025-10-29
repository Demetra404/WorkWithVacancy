from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAPI(ABC):
    """
    Абстрактный класс для работы с API вакансий.
    """
    @abstractmethod
    def _connect_to_api(self) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        pass