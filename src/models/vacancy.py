from __future__ import annotations
from typing import Dict, Any, List, Optional


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = (
        "_title",
        "_url",
        "_salary",
        "_description",
        "_requirements",
        "_experience",
        "_employment",
        "_address",
    )

    def __init__(
        self,
        title: str,
        url: str,
        salary: Optional[Dict[str, Any]],
        description: str,
        requirements: str = "",
        experience: str = "",
        employment: str = "",
        address: str = "",
    ) -> None:
        """
        Инициализация вакансии

        Args:
            title: Название вакансии
            url: Ссылка на вакансию
            salary: Данные о зарплате
            description: Описание вакансии
            requirements: Требования
            experience: Требуемый опыт
            employment: Тип занятости
            address: Местоположение
        """
        self._title = self._validate_string(title, "Название вакансии")
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_string(description, "Описание")
        self._requirements = self._validate_string(requirements, "Требования")
        self._experience = self._validate_string(experience, "Опыт")
        self._employment = self._validate_string(employment, "Занятость")
        self._address = self._validate_string(address, "Адрес")

    def _validate_string(self, value: str, field_name: str) -> str:
        """
        Валидация строковых значений

        Args:
            value: Значение для валидации
            field_name: Название поля для сообщения об ошибке

        Returns:
            Валидированное значение
        """
        if not isinstance(value, str):
            return "Не указано"
        return value.strip() if value.strip() else "Не указано"

    def _validate_url(self, url: str) -> str:
        """
        Валидация URL

        Args:
            url: URL для валидации

        Returns:
            Валидированный URL

        Raises:
            ValueError: Если URL невалидный
        """
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ValueError("Неверный формат URL")
        return url

    def _validate_salary(self, salary_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Валидация данных о зарплате

        Args:
            salary_data: Данные о зарплате

        Returns:
            Валидированные данные о зарплате
        """
        if not salary_data:
            return {"from": 0, "to": 0, "currency": "не указана"}

        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")
        currency = salary_data.get("currency", "RUR")

        # Конвертируем валюту в рубли
        conversion_rates = {"USD": 90, "EUR": 100, "KZT": 0.2}
        rate = conversion_rates.get(currency, 1)

        validated_salary = {
            "from": int(salary_from * rate) if salary_from else 0,
            "to": int(salary_to * rate) if salary_to else 0,
            "currency": ("руб." if currency == "RUR" else f"{currency} (конвертировано в руб.)"),
        }

        return validated_salary

    @property
    def title(self) -> str:
        """Получить название вакансии"""
        return self._title

    @property
    def url(self) -> str:
        """Получить URL вакансии"""
        return self._url

    @property
    def salary(self) -> Dict[str, Any]:
        """Получить данные о зарплате"""
        return self._salary

    @property
    def description(self) -> str:
        """Получить описание вакансии"""
        return self._description

    @property
    def requirements(self) -> str:
        """Получить требования"""
        return self._requirements

    @property
    def experience(self) -> str:
        """Получить требуемый опыт"""
        return self._experience

    @property
    def employment(self) -> str:
        """Получить тип занятости"""
        return self._employment

    @property
    def address(self) -> str:
        """Получить местоположение"""
        return self._address

    def get_average_salary(self) -> float:
        """
        Получение средней зарплаты

        Returns:
            Средняя зарплата
        """
        salary_from = self._salary.get("from", 0)
        salary_to = self._salary.get("to", 0)

        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        elif salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        else:
            return 0.0

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_info = self._format_salary()
        return (
            f"Должность: {self._title}\n"
            f"Зарплата: {salary_info}\n"
            f"Город: {self._address}\n"
            f"Тип занятости: {self._employment}\n"
            f"Опыт: {self._experience}\n"
            f"Ссылка: {self._url}\n"
            f"Описание: {self._description[:100]}...\n"
            f"Требования: {self._requirements[:100]}...\n"
        )

    def _format_salary(self) -> str:
        """
        Форматирование информации о зарплате

        Returns:
            Отформатированная строка с зарплатой
        """
        salary_from = self._salary.get("from", 0)
        salary_to = self._salary.get("to", 0)
        currency = self._salary.get("currency", "")

        if salary_from and salary_to:
            return f"{salary_from:,.0f} - {salary_to:,.0f} {currency}"
        elif salary_from:
            return f"от {salary_from:,.0f} {currency}"
        elif salary_to:
            return f"до {salary_to:,.0f} {currency}"
        else:
            return "Зарплата не указана"

    def __lt__(self, other: Vacancy) -> bool:
        """Сравнение вакансий по зарплате (<)"""
        return self.get_average_salary() < other.get_average_salary()

    def __le__(self, other: Vacancy) -> bool:
        """Сравнение вакансий по зарплате (<=)"""
        return self.get_average_salary() <= other.get_average_salary()

    def __gt__(self, other: Vacancy) -> bool:
        """Сравнение вакансий по зарплате (>)"""
        return self.get_average_salary() > other.get_average_salary()

    def __ge__(self, other: Vacancy) -> bool:
        """Сравнение вакансий по зарплате (>=)"""
        return self.get_average_salary() >= other.get_average_salary()

    def __eq__(self, other: Vacancy) -> bool:
        """Сравнение вакансий по зарплате (==)"""
        return self.get_average_salary() == other.get_average_salary()

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование в словарь для сохранения

        Returns:
            Словарь с данными вакансии
        """
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "requirements": self._requirements,
            "experience": self._experience,
            "employment": self._employment,
            "address": self._address,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """
        Создание объекта из словаря

        Args:
            data: Словарь с данными вакансии

        Returns:
            Объект Vacancy
        """
        return cls(
            title=data["title"],
            url=data["url"],
            salary=data["salary"],
            description=data["description"],
            requirements=data.get("requirements", ""),
            experience=data.get("experience", ""),
            employment=data.get("employment", ""),
            address=data.get("address", ""),
        )

    @classmethod
    def cast_to_object_list(cls, hh_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """
        Преобразование данных из HH API в список объектов Vacancy

        Args:
            hh_data: Список словарей с данными от API

        Returns:
            Список объектов Vacancy
        """
        vacancies = []

        for item in hh_data:
            try:
                vacancy = cls(
                    title=item.get("name", ""),
                    url=item.get("alternate_url", ""),
                    salary=item.get("salary"),
                    description=item.get("snippet", {}).get("responsibility", ""),
                    requirements=item.get("snippet", {}).get("requirement", ""),
                    experience=item.get("experience", {}).get("name", ""),
                    employment=item.get("employment", {}).get("name", ""),
                    address=(item.get("area", {}).get("name", "") if item.get("area") else ""),
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies
