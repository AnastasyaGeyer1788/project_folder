from typing import List, Optional
from src.abstract_classes import FileWorker
from src.models.vacancy import Vacancy


class TXTSaver(FileWorker):
    """Класс для сохранения вакансий в TXT файл (дополнительный формат)"""

    def __init__(self, filename: str = "data/vacancies.txt") -> None:
        """
        Инициализация TXT Saver

        Args:
            filename: Имя файла для сохранения
        """
        self._filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """Добавление вакансии в файл (заглушка)"""
        # Реализация для TXT формата
        return True

    def get_vacancies(self, criteria: Optional[dict] = None) -> List[Vacancy]:
        """Получение вакансий по критериям (заглушка)"""
        # Реализация для TXT формата
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """Удаление вакансии из файла (заглушка)"""
        # Реализация для TXT формата
        return True

    def clear_all(self) -> None:
        """Очистка всех вакансий из файла (заглушка)"""
        # Реализация для TXT формата
        pass
