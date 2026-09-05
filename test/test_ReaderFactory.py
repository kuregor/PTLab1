# -*- coding: utf-8 -*-
import os

import pytest

from src.ReaderFactory import ReaderFactory


class TestReaderFactory:

    @pytest.mark.parametrize("path, expected", [
        ("data/data.txt", "TextDataReader"),
        ("data/data.yaml", "YamlDataReader"),
        ("data/data.yml", "YamlDataReader"),
        ("data/DATA.YAML", "YamlDataReader"),
    ])
    def test_create(self, path: str, expected: str) -> None:
        reader = ReaderFactory.create(path)
        assert type(reader).__name__ == expected

    @pytest.mark.parametrize("path", [
        "data/data.json", "data/data.xml", "data/data.csv", "data",
    ])
    def test_create_unsupported(self, path: str) -> None:
        with pytest.raises(ValueError):
            ReaderFactory.create(path)

    def test_created_reader_is_usable(self, data_dir: str) -> None:
        path = os.path.join(data_dir, "data.yaml")
        assert len(ReaderFactory.create(path).read(path)) == 7
