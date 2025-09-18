from typing import List, Optional
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам

    Args:
        vacancies: Список вакансий для фильтрации
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        search_text = f"{vacancy.description} {vacancy.requirements} {vacancy.title}".lower()
        if any(word.lower() in search_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: Optional[str]) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат

    Args:
        vacancies: Список вакансий для фильтрации
        salary_range: Диапазон зарплат в формате "min-max"

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        if "-" in salary_range:
            min_salary, max_salary = map(int, salary_range.split("-"))
        else:
            min_salary = int(salary_range)
            max_salary = float("inf")
    except ValueError:
        print("Неверный формат диапазона зарплат")
        return vacancies

    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.get_average_salary()
        if min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортировка вакансий по зарплате (по убыванию)

    Args:
        vacancies: Список вакансий для сортировки

    Returns:
        Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        Список топ N вакансий
    """
    return vacancies[:top_n] if vacancies else []


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывод вакансий в читаемом формате

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"=== Вакансия {i} ===")
        print(vacancy)
        print()
