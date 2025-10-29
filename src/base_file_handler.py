from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseFileHandler(ABC):
    """
    Абстрактный класс для работы с файлами вакансий.
    """

    def __init__(self, filename: Optional[str] = None) -> None:
        self._filename = filename or self._get_default_filename()

    @abstractmethod
    def _get_default_filename(self) -> str:
        pass

    @property
    def filename(self) -> str:
        return self._filename

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        pass