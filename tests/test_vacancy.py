import pytest
from src.models.vacancy import Vacancy


class TestVacancy:

    @pytest.fixture
    def sample_vacancy(self):
        """Фикстура для создания тестовой вакансии"""
        return Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/1",
            {"from": 100000, "to": 150000, "currency": "RUR"},
            "Разработка на Python",
            "Опыт работы от 3 лет",
            "От 1 года",
            "Полная занятость",
            "Москва",
        )

    @pytest.fixture
    def vacancy_no_salary(self):
        """Фикстура для вакансии без зарплаты"""
        return Vacancy(
            "Frontend Developer",
            "https://hh.ru/vacancy/2",
            None,
            "Разработка интерфейсов",
            "Знание JavaScript",
        )

    @pytest.fixture
    def vacancy_usd_salary(self):
        """Фикстура для вакансии с зарплатой в USD"""
        return Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/3",
            {"from": 2000, "to": 3000, "currency": "USD"},
            "Разработка на Python",
            "Опыт работы от 3 лет",
        )

    def test_vacancy_creation(self, sample_vacancy):
        """Тест создания вакансии"""
        assert sample_vacancy.title == "Python Developer"
        assert sample_vacancy.url == "https://hh.ru/vacancy/1"
        assert sample_vacancy.salary["from"] == 100000
        assert sample_vacancy.salary["to"] == 150000

    def test_vacancy_no_salary(self, vacancy_no_salary):
        """Тест вакансии без зарплаты"""
        assert vacancy_no_salary.salary["from"] == 0
        assert vacancy_no_salary.salary["to"] == 0
        assert vacancy_no_salary.salary["currency"] == "не указана"

    def test_usd_salary_conversion(self, vacancy_usd_salary):
        """Тест конвертации зарплаты из USD"""
        # 2000 USD * 90 = 180000 руб.
        # 3000 USD * 90 = 270000 руб.
        assert vacancy_usd_salary.salary["from"] == 180000
        assert vacancy_usd_salary.salary["to"] == 270000
        assert "USD" in vacancy_usd_salary.salary["currency"]

    def test_average_salary(self, sample_vacancy, vacancy_no_salary):
        """Тест расчета средней зарплаты"""
        assert sample_vacancy.get_average_salary() == 125000
        assert vacancy_no_salary.get_average_salary() == 0

    def test_comparison_operators(self, sample_vacancy, vacancy_no_salary):
        """Тест операторов сравнения"""
        # Создаем вакансию с большей зарплатой
        high_salary_vacancy = Vacancy(
            "Senior Developer",
            "https://hh.ru/vacancy/4",
            {"from": 200000, "to": 300000, "currency": "RUR"},
            "Разработка",
            "Опыт",
        )

        assert high_salary_vacancy > sample_vacancy
        assert sample_vacancy < high_salary_vacancy
        assert sample_vacancy <= high_salary_vacancy
        assert high_salary_vacancy >= sample_vacancy
        assert sample_vacancy != high_salary_vacancy
        assert vacancy_no_salary < sample_vacancy

    def test_string_representation(self, sample_vacancy):
        """Тест строкового представления"""
        representation = str(sample_vacancy)
        assert "Python Developer" in representation
        assert "100,000 - 150,000 руб." in representation
        assert "Москва" in representation

    def test_invalid_url_validation(self):
        """Тест валидации неверного URL"""
        with pytest.raises(ValueError, match="Неверный формат URL"):
            Vacancy("Test", "invalid_url", None, "Test", "Test")

    def test_string_validation(self):
        """Тест валидации строковых значений"""
        vacancy = Vacancy("  ", "https://test.com", None, "   ", "")
        assert vacancy.title == "Не указано"
        assert vacancy.description == "Не указано"

    def test_cast_to_object_list(self):
        """Тест преобразования списка данных в объекты"""
        hh_data = [
            {
                "name": "Test Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"responsibility": "Test", "requirement": "Test"},
                "experience": {"name": "От 1 года"},
                "employment": {"name": "Полная занятость"},
                "area": {"name": "Москва"},
            }
        ]

        vacancies = Vacancy.cast_to_object_list(hh_data)
        assert len(vacancies) == 1
        assert vacancies[0].title == "Test Developer"

    def test_cast_empty_list(self):
        """Тест преобразования пустого списка"""
        vacancies = Vacancy.cast_to_object_list([])
        assert len(vacancies) == 0

    def test_cast_invalid_data(self):
        """Тест преобразования невалидных данных"""
        hh_data = [{"invalid": "data"}]
        vacancies = Vacancy.cast_to_object_list(hh_data)
        assert len(vacancies) == 0
