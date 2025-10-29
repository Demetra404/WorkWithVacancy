import pytest
import requests
from unittest.mock import Mock, patch
from src.hh_api import HHAPI


class TestHHAPI:
    def test_init(self):

        api = HHAPI()
        assert api._base_url == "https://api.hh.ru/vacancies"
        assert "User-Agent" in api._headers

    @patch('src.hh_api.requests.get')
    def test_connect_to_api_success(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HHAPI()
        api._connect_to_api()

    @patch('src.hh_api.requests.get')
    def test_connect_to_api_failure(self, mock_get):

        mock_get.side_effect = requests.RequestException("Connection error")

        api = HHAPI()
        with pytest.raises(ConnectionError):
            api._connect_to_api()

    @patch('src.hh_api.requests.get')
    def test_get_vacancies_success(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000},
                    "snippet": {
                        "requirement": "Python experience",
                        "responsibility": "Development"
                    },
                    "employer": {"name": "IT Company"}
                }
            ]
        }
        mock_get.return_value = mock_response

        api = HHAPI()
        vacancies = api.get_vacancies("python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"

    @patch('src.hh_api.requests.get')
    def test_get_vacancies_empty_result(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        api = HHAPI()
        vacancies = api.get_vacancies("nonexistent")

        assert len(vacancies) == 0

    def test_get_vacancies_invalid_keyword(self):

        api = HHAPI()
        with pytest.raises(ValueError):
            api.get_vacancies("")


if __name__ == "__main__":
    pytest.main()