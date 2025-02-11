import pytest
from unittest.mock import patch, MagicMock
from src.services.youtube_service import (
    get_youtube_subscribers,
    fetch_and_store_youtube_data,
    get_latest_youtube,
    get_youtube_statistics,
    get_youtube_daily_stats
)
from src.database.youtube_db import add_youtube_data, get_latest_youtube_data, \
    get_subscribers_over_period, get_daily_followers


# Тест для get_youtube_subscribers
@patch('googleapiclient.discovery.build')
def test_get_youtube_subscribers(mock_build):
    # Мокируем ответ от YouTube API
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    mock_youtube.channels().list().execute.return_value = {
        'items': [{
            'statistics': {
                'subscriberCount': '1000'
            }
        }]
    }

    subscribers = get_youtube_subscribers()
    assert subscribers == 1000
    mock_youtube.channels().list().execute.assert_called_once()


@patch('googleapiclient.discovery.build')
def test_get_youtube_subscribers_not_found(mock_build):
    # Мокируем отсутствие канала
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    mock_youtube.channels().list().execute.return_value = {
        'items': []
    }

    subscribers = get_youtube_subscribers()
    assert subscribers is None
    mock_youtube.channels().list().execute.assert_called_once()


# Тест для fetch_and_store_youtube_data
@patch('src.services.youtube_service.get_youtube_subscribers')
@patch('src.database.youtube_db.add_youtube_data')
def test_fetch_and_store_youtube_data(mock_add_youtube_data,
                                      mock_get_youtube_subscribers):
    # Мокируем возвращаемое значение get_youtube_subscribers
    mock_get_youtube_subscribers.return_value = 1000

    fetch_and_store_youtube_data()
    mock_add_youtube_data.assert_called_once_with('your_channel_id', 1000)


# Тест для get_latest_youtube
@patch('src.database.youtube_db.get_latest_youtube_data')
def test_get_latest_youtube(mock_get_latest_youtube_data):
    mock_get_latest_youtube_data.return_value = {'followers': 1000}
    result = get_latest_youtube('your_channel_id')
    assert result == {'followers': 1000}
    mock_get_latest_youtube_data.assert_called_once_with('your_channel_id')


# Тест для get_youtube_statistics
@patch('src.database.youtube_db.get_subscribers_over_period')
def test_get_youtube_statistics(mock_get_subscribers_over_period):
    # Мокируем возвращаемое значение для разных периодов
    mock_get_subscribers_over_period.side_effect = [100, 200,
                                                    300]  # Для каждого периода
    result = get_youtube_statistics('your_channel_id')
    assert result == {
        "24h": 100,
        "week": 200,
        "month": 300
    }
    assert mock_get_subscribers_over_period.call_count == 3


# Тест для get_youtube_daily_stats
@patch('src.database.youtube_db.get_daily_followers')
def test_get_youtube_daily_stats(mock_get_daily_followers):
    mock_get_daily_followers.return_value = {'followers': 1000}
    result = get_youtube_daily_stats('your_channel_id')
    assert result == {'followers': 1000}
    mock_get_daily_followers.assert_called_once_with('your_channel_id')
