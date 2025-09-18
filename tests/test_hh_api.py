import pytest
from unittest.mock import patch, Mock
from src.api.hh_api import HeadHunterAPI


class TestHHAPI:

    @pytest.fixture
    def hh_api(self):
        """Фикстура для создания экземпляра API"""
        return HeadHunterAPI()

    def test_init(self, hh_api):
        """Тест инициализации API"""
        assert hh_api._base_url == "https://api.hh.ru/vacancies"
        assert hh_api._headers["User-Agent"] == "HH-User-Agent"

    @patch("requests.get")
    def test_connect_to_api_success(self, mock_get, hh_api):
        """Тест успешного подключения к API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = hh_api._connect_to_api()
        assert result is True

    @patch("src.api.hh_api.HeadHunterAPI._connect_to_api")
    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get, mock_connect, hh_api):
        """Тест успешного получения вакансий"""
        mock_connect.return_value = True

        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/1",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {
                        "responsibility": "Разработка",
                        "requirement": "Python",
                    },
                    "experience": {"name": "От 1 года"},
                    "employment": {"name": "Полная занятость"},
                    "area": {"name": "Москва"},
                }
            ],
            "pages": 1,
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python")
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"

    @patch("src.api.hh_api.HeadHunterAPI._connect_to_api")
    def test_get_vacancies_connection_failure(self, mock_connect, hh_api):
        """Тест получения вакансий при ошибке подключения"""
        mock_connect.return_value = False

        vacancies = hh_api.get_vacancies("Python")
        assert len(vacancies) == 0

    @patch("src.api.hh_api.HeadHunterAPI._connect_to_api")
    @patch("requests.get")
    def test_get_vacancies_empty_response(self, mock_get, mock_connect, hh_api):
        """Тест получения вакансий при пустом ответе"""
        mock_connect.return_value = True

        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python")
        assert len(vacancies) == 0

    @patch("src.api.hh_api.HeadHunterAPI._connect_to_api")
    @patch("requests.get")
    def test_get_vacancies_multiple_pages(self, mock_get, mock_connect, hh_api):
        """Тест получения вакансий с нескольких страниц"""
        mock_connect.return_value = True

        # Первая страница
        mock_response1 = Mock()
        mock_response1.json.return_value = {"items": [{"name": "Page1"}], "pages": 2}

        # Вторая страница
        mock_response2 = Mock()
        mock_response2.json.return_value = {"items": [{"name": "Page2"}], "pages": 2}

        mock_get.side_effect = [mock_response1, mock_response2]

        vacancies = hh_api.get_vacancies("Python")
        assert len(vacancies) == 2
        assert mock_get.call_count == 2
