import pytest
from unittest.mock import patch, MagicMock
from src.services.linkedin_service import (
    get_linkedin_followers,
    fetch_and_store_linkedin_data,
    get_latest_linkedin,
    get_linkedin_statistics,
    get_linkedin_daily_stats
)
from src.database.linkedin_db import add_linkedin_data, \
    get_latest_linkedin_data, get_followers_over_period, get_daily_followers


# Тест для get_linkedin_followers
@patch('selenium.webdriver.Chrome')
def test_get_linkedin_followers(mock_chrome):
    # Мокируем Selenium WebDriver
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    mock_driver.page_source = '<html><span class="t-bold">1000 followers</span></html>'

    followers = get_linkedin_followers()
    assert followers == "1000"
    mock_chrome.assert_called_once()


# Тест для fetch_and_store_linkedin_data
@patch('src.services.linkedin_service.get_linkedin_followers')
@patch('src.database.linkedin_db.add_linkedin_data')
def test_fetch_and_store_linkedin_data(mock_add_linkedin_data,
                                       mock_get_linkedin_followers):
    # Мокируем возвращаемое значение get_linkedin_followers
    mock_get_linkedin_followers.return_value = "1000"

    fetch_and_store_linkedin_data()
    mock_add_linkedin_data.assert_called_once_with('profile_id', "1000")


# Тест для get_latest_linkedin
@patch('src.database.linkedin_db.get_latest_linkedin_data')
def test_get_latest_linkedin(mock_get_latest_linkedin_data):
    mock_get_latest_linkedin_data.return_value = {'followers': 1000}
    result = get_latest_linkedin('profile_id')
    assert result == {'followers': 1000}
    mock_get_latest_linkedin_data.assert_called_once_with('profile_id')


# Тест для get_linkedin_statistics
@patch('src.database.linkedin_db.get_followers_over_period')
def test_get_linkedin_statistics(mock_get_followers_over_period):
    # Мокируем возвращаемое значение для разных периодов
    mock_get_followers_over_period.side_effect = [100, 200,
                                                  300]  # Для каждого периода
    result = get_linkedin_statistics('profile_id')
    assert result == {
        "24h": 100,
        "week": 200,
        "month": 300
    }
    assert mock_get_followers_over_period.call_count == 3


# Тест для get_linkedin_daily_stats
@patch('src.database.linkedin_db.get_daily_followers')
def test_get_linkedin_daily_stats(mock_get_daily_followers):
    mock_get_daily_followers.return_value = {'followers': 1000}
    result = get_linkedin_daily_stats('profile_id')
    assert result == {'followers': 1000}
    mock_get_daily_followers.assert_called_once_with('profile_id')
