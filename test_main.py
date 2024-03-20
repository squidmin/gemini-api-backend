from unittest.mock import Mock, patch
import requests

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


