import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.abstract_classes import FileWorker
from src.models.vacancy import Vacancy


class JSONSaver(FileWorker):
    """Класс для сохранения вакансий в JSON файл"""

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """
        Инициализация JSON Saver

        Args:
            filename: Имя файла для сохранения
        """
        self._filename = filename
        # Создаем директорию если не существует
        Path(self._filename).parent.mkdir(parents=True, exist_ok=True)
        self._initialize_file()

    def _initialize_file(self) -> None:
        """Инициализация файла с правильной структурой"""
        try:
            if os.path.exists(self._filename):
                with open(self._filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if not isinstance(data, list):
                        self._write_file([])
            else:
                self._write_file([])
        except (FileNotFoundError, json.JSONDecodeError):
            self._write_file([])

    def _read_file(self) -> List[Dict[str, Any]]:
        """
        Чтение данных из файла

        Returns:
            Список данных вакансий
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """
        Запись данных в файл

        Args:
            data: Данные для записи
        """
        if not isinstance(data, list):
            data = []

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Добавление вакансии в файл

        Args:
            vacancy: Объект вакансии

        Returns:
            True если вакансия добавлена, False если уже существует
        """
        vacancies = self._read_file()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты по URL
        existing_urls = [v.get("url") for v in vacancies if isinstance(v, dict)]
        if vacancy_dict["url"] not in existing_urls:
            vacancies.append(vacancy_dict)
            self._write_file(vacancies)
            return True
        return False

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """
        Получение вакансий по критериям

        Args:
            criteria: Словарь с критериями фильтрации

        Returns:
            Список отфильтрованных вакансий
        """
        vacancies_data = self._read_file()
        valid_vacancies_data = [data for data in vacancies_data if isinstance(data, dict)]

        vacancies = []
        for data in valid_vacancies_data:
            try:
                vacancy = Vacancy.from_dict(data)
                vacancies.append(vacancy)
            except (KeyError, TypeError) as e:
                print(f"Ошибка при создании вакансии из данных: {e}")
                continue

        if not criteria:
            return vacancies

        return self._filter_vacancies(vacancies, criteria)

    def _filter_vacancies(self, vacancies: List[Vacancy], criteria: Dict[str, Any]) -> List[Vacancy]:
        """
        Фильтрация вакансий по критериям

        Args:
            vacancies: Список вакансий для фильтрации
            criteria: Критерии фильтрации

        Returns:
            Отфильтрованный список вакансий
        """
        filtered_vacancies = []

        for vacancy in vacancies:
            match = True

            for key, value in criteria.items():
                if key == "salary_min" and vacancy.get_average_salary() < value:
                    match = False
                elif key == "salary_max" and vacancy.get_average_salary() > value:
                    match = False
                elif key == "keyword":
                    search_text = f"{vacancy.description} {vacancy.requirements} {vacancy.title}".lower()
                    if value.lower() not in search_text:
                        match = False
                elif key == "experience" and value and value.lower() not in vacancy.experience.lower():
                    match = False
                elif key == "employment" and value and value.lower() not in vacancy.employment.lower():
                    match = False
                elif key == "address" and value and value.lower() not in vacancy.address.lower():
                    match = False

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Удаление вакансии из файла

        Args:
            vacancy: Объект вакансии для удаления

        Returns:
            True если вакансия удалена, False если не найдена
        """
        vacancies = self._read_file()
        vacancy_url = vacancy.url

        initial_count = len(vacancies)
        vacancies = [v for v in vacancies if isinstance(v, dict) and v.get("url") != vacancy_url]

        if len(vacancies) < initial_count:
            self._write_file(vacancies)
            return True
        return False

    def clear_all(self) -> None:
        """Очистка всех вакансий из файла"""
        self._write_file([])

    def get_vacancies_count(self) -> int:
        """
        Получение количества вакансий в файле

        Returns:
            Количество вакансий
        """
        vacancies = self._read_file()
        return len([v for v in vacancies if isinstance(v, dict)])
