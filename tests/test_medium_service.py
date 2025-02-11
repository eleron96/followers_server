import pytest
from unittest.mock import patch, MagicMock
from src.services.medium_service import (
    get_medium_followers,
    fetch_and_store_medium_data,
    get_latest_medium,
    get_medium_statistics,
    get_medium_daily_stats
)
from src.database.medium_db import add_medium_data, get_latest_medium_data, \
    get_followers_over_period, get_daily_followers


# Тест для get_medium_followers
@patch('requests.get')
def test_get_medium_followers(mock_get):
    # Мокируем ответ от Medium
    mock_response = MagicMock()
    mock_response.text = '<html><script>window.__APOLLO_STATE__ = {"User:@username": {"followersCount": 1000}}</script></html>'
    mock_get.return_value = mock_response

    followers = get_medium_followers()
    assert followers == 1000
    mock_get.assert_called_once_with('https://medium.com/@username',
                                     headers={'User-Agent': 'Mozilla/5.0'})


@patch('requests.get')
def test_get_medium_followers_direct(mock_get):
    # Мокируем прямой поиск подписчиков
    mock_response = MagicMock()
    mock_response.text = '<html><span class="t-bold">1000 Followers</span></html>'
    mock_get.return_value = mock_response

    followers = get_medium_followers()
    assert followers == 1000
    mock_get.assert_called_once_with('https://medium.com/@username',
                                     headers={'User-Agent': 'Mozilla/5.0'})


# Тест для fetch_and_store_medium_data
@patch('src.services.medium_service.get_medium_followers')
@patch('src.database.medium_db.add_medium_data')
def test_fetch_and_store_medium_data(mock_add_medium_data,
                                     mock_get_medium_followers):
    # Мокируем возвращаемое значение get_medium_followers
    mock_get_medium_followers.return_value = 1000

    fetch_and_store_medium_data()
    mock_add_medium_data.assert_called_once_with('username', 1000)


# Тест для get_latest_medium
@patch('src.database.medium_db.get_latest_medium_data')
def test_get_latest_medium(mock_get_latest_medium_data):
    mock_get_latest_medium_data.return_value = {'followers': 1000}
    result = get_latest_medium('username')
    assert result == {'followers': 1000}
    mock_get_latest_medium_data.assert_called_once_with('username')


# Тест для get_medium_statistics
@patch('src.database.medium_db.get_followers_over_period')
def test_get_medium_statistics(mock_get_followers_over_period):
    # Мокируем возвращаемое значение для разных периодов
    mock_get_followers_over_period.side_effect = [100, 200,
                                                  300]  # Для каждого периода
    result = get_medium_statistics('username')
    assert result == {
        "24h": 100,
        "week": 200,
        "month": 300
    }
    assert mock_get_followers_over_period.call_count == 3


# Тест для get_medium_daily_stats
@patch('src.database.medium_db.get_daily_followers')
def test_get_medium_daily_stats(mock_get_daily_followers):
    mock_get_daily_followers.return_value = {'followers': 1000}
    result = get_medium_daily_stats('username')
    assert result == {'followers': 1000}
    mock_get_daily_followers.assert_called_once_with('username')
