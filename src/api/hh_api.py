import requests
from typing import List, Dict, Any
from src.abstract_classes import API


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        """Инициализация API HeadHunter"""
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "HH-User-Agent"}

    def _connect_to_api(self) -> bool:
        """
        Приватный метод подключения к API

        Returns:
            True если подключение успешно, False в противном случае
        """
        try:
            response = requests.get(self._base_url, headers=self._headers, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу

        Args:
            search_query: Поисковый запрос

        Returns:
            Список вакансий в формате словарей
        """
        if not self._connect_to_api():
            print("Ошибка подключения к API hh.ru")
            return []

        params = {
            "text": search_query,
            "area": 113,  # Россия
            "per_page": 100,
            "page": 0,
        }

        vacancies = []
        while params["page"] < 5:  # Ограничиваем 5 страницами
            try:
                response = requests.get(self._base_url, headers=self._headers, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                page_vacancies = data.get("items", [])
                vacancies.extend(page_vacancies)

                # Проверяем, есть ли еще страницы
                pages = data.get("pages", 1)
                if params["page"] >= pages - 1:
                    break

                params["page"] += 1

            except requests.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break

        return vacancies
