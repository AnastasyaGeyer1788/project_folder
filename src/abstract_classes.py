from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.vacancy import Vacancy


class API(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу

        Args:
            search_query: Поисковый запрос

        Returns:
            Список вакансий в формате словарей
        """
        pass


class FileWorker(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> bool:
        """
        Добавление вакансии в файл

        Args:
            vacancy: Объект вакансии

        Returns:
            True если вакансия добавлена, False если уже существует
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List['Vacancy']:
        """
        Получение вакансий по критериям

        Args:
            criteria: Словарь с критериями фильтрации

        Returns:
            Список отфильтрованных вакансий
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> bool:
        """
        Удаление вакансии из файла

        Args:
            vacancy: Объект вакансии для удаления

        Returns:
            True если вакансия удалена, False если не найдена
        """
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистка всех вакансий из файла"""
        pass
