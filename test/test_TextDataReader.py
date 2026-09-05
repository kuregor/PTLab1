# -*- coding: utf-8 -*-
import os

import pytest

from src.TextDataReader import TextDataReader
from src.Types import DataType


class TestTextDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = "Иванов Константин Дмитриевич\n" + \
               " математика:91\n" + " химия:100\n" + \
               "Петров Петр Семенович\n" + \
               " русский язык:87\n" + " литература:78\n"

        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(
            self,
            file_and_data_content: tuple[str, DataType],
            tmpdir) -> tuple[str, DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.txt")
        p.write_text(file_and_data_content[0], encoding='utf-8')
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = TextDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

    def test_read_project_datafile(self, data_dir: str) -> None:
        data = TextDataReader().read(
            os.path.join(data_dir, "data.txt"))
        assert len(data) == 7
        assert ("математика", 80) in data["Абрамов Петр Сергеевич"]

    def test_read_missing_file(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            TextDataReader().read(str(tmpdir.join("absent.txt")))
