# -*- coding: utf-8 -*-
import os

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def data_dir() -> str:
    """Абсолютный путь к каталогу с исходными данными проекта."""
    return os.path.join(PROJECT_ROOT, "data")
