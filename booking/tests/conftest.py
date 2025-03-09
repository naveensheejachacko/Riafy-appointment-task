# booking/tests/conftest.py
import pytest
from django.test import Client

@pytest.fixture
def client():
    """Django test client fixture"""
    return Client()