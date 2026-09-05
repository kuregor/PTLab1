# -*- coding: utf-8 -*-
import yaml

from DataReader import DataReader
from Types import DataType


class YamlDataReader(DataReader):
    """Читает список студентов и оценок из файла формата YAML.

    Поддерживаются две равнозначные записи -- отображение:

        Иванов Иван Иванович:
          математика: 67
          химия: 100

    и последовательность из одноключевых отображений:

        - Иванов Иван Иванович:
            математика: 67
            химия: 100
    """

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            raw = yaml.safe_load(file)

        self.students = {}
        for name, subjects in self._as_items(raw):
            if not isinstance(subjects, dict):
                raise ValueError(
                    "Оценки студента должны быть заданы отображением")
            self.students[name] = [
                (str(subject), int(score))
                for subject, score in subjects.items()
            ]

        return self.students

    @staticmethod
    def _as_items(raw) -> list[tuple[str, dict]]:
        if isinstance(raw, dict):
            return list(raw.items())

        if isinstance(raw, list):
            items: list[tuple[str, dict]] = []
            for element in raw:
                if not isinstance(element, dict):
                    raise ValueError(
                        "Элемент списка должен быть отображением")
                items.extend(element.items())
            return items

        raise ValueError("Неподдерживаемая структура YAML-файла")
