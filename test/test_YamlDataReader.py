# -*- coding: utf-8 -*-
import os

import pytest

from src.Types import DataType
from src.YamlDataReader import YamlDataReader

EXPECTED: DataType = {
    "Иванов Иван Иванович": [
        ("математика", 67), ("литература", 100)
    ],
    "Петров Петр Петрович": [
        ("математика", 78), ("химия", 87)
    ]
}

MAPPING_TEXT = (
    "Иванов Иван Иванович:\n"
    "  математика: 67\n"
    "  литература: 100\n"
    "Петров Петр Петрович:\n"
    "  математика: 78\n"
    "  химия: 87\n"
)

SEQUENCE_TEXT = (
    "- Иванов Иван Иванович:\n"
    "    математика: 67\n"
    "    литература: 100\n"
    "- Петров Петр Петрович:\n"
    "    математика: 78\n"
    "    химия: 87\n"
)


class TestYamlDataReader:

    @pytest.fixture()
    def yaml_dir(self, tmpdir):
        return tmpdir.mkdir("yamldir")

    def test_read_mapping(self, yaml_dir) -> None:
        path = yaml_dir.join("mapping.yaml")
        path.write_text(MAPPING_TEXT, encoding='utf-8')
        assert YamlDataReader().read(str(path)) == EXPECTED

    def test_read_sequence(self, yaml_dir) -> None:
        path = yaml_dir.join("sequence.yaml")
        path.write_text(SEQUENCE_TEXT, encoding='utf-8')
        assert YamlDataReader().read(str(path)) == EXPECTED

    def test_read_project_datafile(self, data_dir: str) -> None:
        data = YamlDataReader().read(os.path.join(data_dir, "data.yaml"))
        assert len(data) == 7
        assert ("литература", 97) in data["Петров Игорь Владимирович"]

    def test_read_wrong_root(self, yaml_dir) -> None:
        path = yaml_dir.join("scalar.yaml")
        path.write_text("42\n", encoding='utf-8')
        with pytest.raises(ValueError):
            YamlDataReader().read(str(path))

    def test_read_wrong_student_value(self, yaml_dir) -> None:
        path = yaml_dir.join("bad.yaml")
        path.write_text("Иванов Иван: 5\n", encoding='utf-8')
        with pytest.raises(ValueError):
            YamlDataReader().read(str(path))

    def test_read_wrong_sequence_element(self, yaml_dir) -> None:
        path = yaml_dir.join("badseq.yaml")
        path.write_text("- 42\n", encoding='utf-8')
        with pytest.raises(ValueError):
            YamlDataReader().read(str(path))
