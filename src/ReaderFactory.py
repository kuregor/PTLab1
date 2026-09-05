# -*- coding: utf-8 -*-
import os

from DataReader import DataReader
from TextDataReader import TextDataReader
from YamlDataReader import YamlDataReader

READERS: dict[str, type[DataReader]] = {
    ".txt": TextDataReader,
    ".yaml": YamlDataReader,
    ".yml": YamlDataReader,
}


class ReaderFactory:
    """Создает подходящий обработчик по расширению файла."""

    @staticmethod
    def create(path: str) -> DataReader:
        extension = os.path.splitext(path)[1].lower()
        if extension not in READERS:
            raise ValueError(
                "Неподдерживаемый формат файла: "
                + (extension or "без расширения"))
        return READERS[extension]()
