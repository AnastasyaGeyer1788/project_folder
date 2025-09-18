import pytest
import os
import tempfile
from src.file_workers.json_saver import JSONSaver
from src.models.vacancy import Vacancy


class TestJSONSaver:

    @pytest.fixture
    def temp_file(self):
        """Фикстура для временного файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            yield f.name
        if os.path.exists(f.name):
            os.unlink(f.name)

    @pytest.fixture
    def sample_vacancy(self):
        """Фикстура для тестовой вакансии"""
        return Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/1",
            {"from": 100000, "to": 150000, "currency": "RUR"},
            "Разработка на Python",
            "Опыт работы от 3 лет",
        )

    @pytest.fixture
    def another_vacancy(self):
        """Фикстура для другой вакансии"""
        return Vacancy(
            "Java Developer",
            "https://hh.ru/vacancy/2",
            {"from": 120000, "to": 180000, "currency": "RUR"},
            "Разработка на Java",
            "Опыт работы от 2 лет",
        )

    def test_initialization(self, temp_file):
        """Тест инициализации JSONSaver"""
        saver = JSONSaver(temp_file)
        assert saver._filename == temp_file
        assert os.path.exists(temp_file)

    def test_add_vacancy(self, temp_file, sample_vacancy):
        """Тест добавления вакансии"""
        saver = JSONSaver(temp_file)
        result = saver.add_vacancy(sample_vacancy)
        assert result is True
        assert saver.get_vacancies_count() == 1

    def test_add_duplicate_vacancy(self, temp_file, sample_vacancy):
        """Тест добавления дубликата вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        result = saver.add_vacancy(sample_vacancy)  # Дубликат
        assert result is False
        assert saver.get_vacancies_count() == 1

    def test_get_vacancies(self, temp_file, sample_vacancy, another_vacancy):
        """Тест получения вакансий"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(another_vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 2
        assert vacancies[0].title == "Python Developer"
        assert vacancies[1].title == "Java Developer"

    def test_get_vacancies_empty(self, temp_file):
        """Тест получения вакансий из пустого файла"""
        saver = JSONSaver(temp_file)
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_filter_vacancies_by_keyword(self, temp_file, sample_vacancy, another_vacancy):
        """Тест фильтрации по ключевому слову"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(another_vacancy)

        filtered = saver.get_vacancies({"keyword": "Python"})
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_filter_vacancies_by_salary(self, temp_file, sample_vacancy, another_vacancy):
        """Тест фильтрации по зарплате"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)  # avg: 125000
        saver.add_vacancy(another_vacancy)  # avg: 150000

        # Фильтр по минимальной зарплате
        filtered = saver.get_vacancies({"salary_min": 130000})
        assert len(filtered) == 1
        assert filtered[0].title == "Java Developer"

        # Фильтр по максимальной зарплате
        filtered = saver.get_vacancies({"salary_max": 130000})
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_delete_vacancy(self, temp_file, sample_vacancy, another_vacancy):
        """Тест удаления вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(another_vacancy)

        result = saver.delete_vacancy(sample_vacancy)
        assert result is True
        assert saver.get_vacancies_count() == 1
        assert saver.get_vacancies()[0].title == "Java Developer"

    def test_delete_nonexistent_vacancy(self, temp_file, sample_vacancy):
        """Тест удаления несуществующей вакансии"""
        saver = JSONSaver(temp_file)
        result = saver.delete_vacancy(sample_vacancy)
        assert result is False

    def test_clear_all(self, temp_file, sample_vacancy, another_vacancy):
        """Тест очистки всех вакансий"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(another_vacancy)

        saver.clear_all()
        assert saver.get_vacancies_count() == 0

    def test_file_not_found(self):
        """Тест работы с несуществующим файлом"""
        # Создаем временную директорию и файл в ней
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test_vacancies.json")
            saver = JSONSaver(test_file)
            # Должен создать файл
            assert os.path.exists(test_file)
            assert saver.get_vacancies_count() == 0
