# -*- coding: utf-8 -*-
"""Настройка путей импорта для запуска тестов из корня проекта.

Модули пакета обращаются друг к другу по коротким именам
(``from Types import DataType``), а тесты -- по полным
(``from src.Types import DataType``). Чтобы оба варианта работали
без ручной установки PYTHONPATH, каталоги проекта и src
добавляются в sys.path.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(PROJECT_ROOT, "src")

for _path in (PROJECT_ROOT, SOURCE_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)
