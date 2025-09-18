import pytest
from src.utils.helpers import (
    filter_vacancies,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)
from src.models.vacancy import Vacancy


class TestHelpers:

    @pytest.fixture
    def sample_vacancies(self):
        """Фикстура для тестовых вакансий"""
        return [
            Vacancy(
                "Python Developer",
                "https://hh.ru/vacancy/1",
                {"from": 100000, "to": 150000, "currency": "RUR"},
                "Разработка на Python Django Flask",
                "Опыт работы от 3 лет",
            ),
            Vacancy(
                "Java Developer",
                "https://hh.ru/vacancy/2",
                {"from": 120000, "to": 180000, "currency": "RUR"},
                "Разработка на Java Spring",
                "Опыт работы от 2 лет",
            ),
            Vacancy(
                "Frontend Developer",
                "https://hh.ru/vacancy/3",
                {"from": 80000, "to": 120000, "currency": "RUR"},
                "Разработка на React JavaScript",
                "Опыт работы от 1 года",
            ),
        ]

    def test_filter_vacancies(self, sample_vacancies):
        """Тест фильтрации по ключевым словам"""
        # Фильтр по Python
        filtered = filter_vacancies(sample_vacancies, ["Python"])
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

        # Фильтр по JavaScript
        filtered = filter_vacancies(sample_vacancies, ["JavaScript"])
        assert len(filtered) == 1
        assert filtered[0].title == "Frontend Developer"

        # Фильтр по нескольким словам
        filtered = filter_vacancies(sample_vacancies, ["Разработка", "Опыт"])
        assert len(filtered) == 3  # Все вакансии содержат эти слова

        # Пустой фильтр
        filtered = filter_vacancies(sample_vacancies, [])
        assert len(filtered) == 3

    def test_sort_vacancies(self, sample_vacancies):
        """Тест сортировки вакансий"""
        sorted_vac = sort_vacancies(sample_vacancies)
        # Должны быть отсортированы по убыванию зарплаты
        assert sorted_vac[0].title == "Java Developer"  # avg: 150000
        assert sorted_vac[1].title == "Python Developer"  # avg: 125000
        assert sorted_vac[2].title == "Frontend Developer"  # avg: 100000

    def test_get_top_vacancies(self, sample_vacancies):
        """Тест получения топ N вакансий"""
        # Сначала отсортируем по зарплате
        sorted_vacancies = sort_vacancies(sample_vacancies)

        # Топ 2 вакансии (самые высокооплачиваемые)
        top_vac = get_top_vacancies(sorted_vacancies, 2)
        assert len(top_vac) == 2
        assert top_vac[0].title == "Java Developer"  # avg: 150000
        assert top_vac[1].title == "Python Developer"  # avg: 125000

        # Топ больше чем есть вакансий
        top_vac = get_top_vacancies(sorted_vacancies, 5)
        assert len(top_vac) == 3

        # Топ 0
        top_vac = get_top_vacancies(sorted_vacancies, 0)
        assert len(top_vac) == 0

        # Пустой список
        top_vac = get_top_vacancies([], 5)
        assert len(top_vac) == 0

    def test_print_vacancies(self, sample_vacancies, capsys):
        """Тест вывода вакансий"""
        print_vacancies(sample_vacancies)
        captured = capsys.readouterr()
        assert "Python Developer" in captured.out
        assert "Java Developer" in captured.out
        assert "Frontend Developer" in captured.out

    def test_print_empty_vacancies(self, capsys):
        """Тест вывода пустого списка вакансий"""
        print_vacancies([])
        captured = capsys.readouterr()
        assert "Вакансии не найдены" in captured.out
