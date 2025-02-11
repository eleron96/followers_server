import pytest
import requests

BASE_URL = "http://localhost:5000"  # Или URL твоего сервера, если ты тестируешь удаленно


def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200


def test_linkedin_statistics():
    response = requests.get(f"{BASE_URL}/statistics?profile_id=gamsakhurdiya")
    assert response.status_code == 200
    assert 'followers' in response.json()


def test_youtube_statistics():
    response = requests.get(
        f"{BASE_URL}/youtube/statistics?profile_id=test_channel")
    assert response.status_code == 200
    assert 'followers' in response.json()


def test_medium_statistics():
    response = requests.get(
        f"{BASE_URL}/medium/statistics?profile_id=test_user")
    assert response.status_code == 200
    assert 'followers' in response.json()
