# -*- coding: utf-8 -*-
import os

import pytest

from src.StudentStats import StudentStats
from src.Types import DataType
from src.YamlDataReader import YamlDataReader

ABRAMOV = "Абрамов Петр Сергеевич"
KUZNETSOV = "Кузнецов Дмитрий Олегович"
MOROZOVA = "Морозова Елена Игоревна"
SIDOROVA = "Сидорова Анна Павловна"


@pytest.fixture()
def data() -> DataType:
    return {
        ABRAMOV: [
            ("математика", 80),
            ("русский язык", 76),
            ("программирование", 100),
        ],
        KUZNETSOV: [
            ("математика", 55),
            ("химия", 76),
            ("программирование", 76),
            ("литература", 90),
        ],
        MOROZOVA: [
            ("математика", 76),
            ("химия", 76),
            ("русский язык", 76),
            ("литература", 88),
        ],
        SIDOROVA: [
            ("математика", 76),
            ("химия", 76),
            ("литература", 76),
            ("философия", 76),
        ],
    }


@pytest.fixture()
def stats(data: DataType) -> StudentStats:
    return StudentStats(data)


class TestStudentStats:

    def test_variant_constants(self) -> None:
        assert StudentStats.TARGET_SCORE == 76
        assert StudentStats.MIN_SUBJECTS == 3

    @pytest.mark.parametrize("student, score, expected", [
        (ABRAMOV, 76, 1),
        (KUZNETSOV, 76, 2),
        (MOROZOVA, 76, 3),
        (SIDOROVA, 76, 4),
        (MOROZOVA, 88, 1),
        (MOROZOVA, 61, 0),
    ])
    def test_count_subjects_with_score(
            self, stats: StudentStats, student: str, score: int,
            expected: int) -> None:
        assert stats.count_subjects_with_score(student, score) == expected

    def test_count_subjects_of_unknown_student(
            self, stats: StudentStats) -> None:
        with pytest.raises(KeyError):
            stats.count_subjects_with_score("Неизвестный Студент", 76)

    def test_students_with_score_in_subjects(
            self, stats: StudentStats) -> None:
        assert stats.students_with_score_in_subjects() == [
            MOROZOVA, SIDOROVA]

    @pytest.mark.parametrize("min_count, expected", [
        (1, [ABRAMOV, KUZNETSOV, MOROZOVA, SIDOROVA]),
        (2, [KUZNETSOV, MOROZOVA, SIDOROVA]),
        (3, [MOROZOVA, SIDOROVA]),
        (4, [SIDOROVA]),
        (5, []),
    ])
    def test_students_by_number_of_subjects(
            self, stats: StudentStats, min_count: int,
            expected: list[str]) -> None:
        result = stats.students_with_score_in_subjects(76, min_count)
        assert result == expected

    def test_students_with_other_score(self, stats: StudentStats) -> None:
        assert stats.students_with_score_in_subjects(90, 1) == [KUZNETSOV]

    def test_nonpositive_number_of_subjects(
            self, stats: StudentStats) -> None:
        with pytest.raises(ValueError):
            stats.students_with_score_in_subjects(76, 0)

    def test_find_student(self, stats: StudentStats) -> None:
        assert stats.find_student_with_score_in_subjects() == MOROZOVA

    def test_find_student_when_none_matches(
            self, stats: StudentStats) -> None:
        assert stats.find_student_with_score_in_subjects(61, 1) is None

    def test_empty_data(self) -> None:
        empty = StudentStats({})
        assert empty.students_with_score_in_subjects() == []
        assert empty.find_student_with_score_in_subjects() is None

    def test_student_without_subjects(self) -> None:
        single = StudentStats({ABRAMOV: []})
        assert single.count_subjects_with_score(ABRAMOV, 76) == 0
        assert single.find_student_with_score_in_subjects() is None

    def test_stats_on_project_datafile(self, data_dir: str) -> None:
        path = os.path.join(data_dir, "data.yaml")
        project = StudentStats(YamlDataReader().read(path))
        assert project.find_student_with_score_in_subjects() == MOROZOVA
