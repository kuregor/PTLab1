# -*- coding: utf-8 -*-
from typing import Optional

from Types import DataType


class StudentStats:
    """Расчет характеристик студентов по индивидуальному варианту 6.

    Определяет студентов, набравших заданный балл минимум по указанному
    числу дисциплин. По условию варианта требуется найти студента,
    имеющего 76 баллов минимум по трем дисциплинам; если таких студентов
    несколько, подходит любой из них, если их нет -- нужно сообщить об
    отсутствии.
    """

    TARGET_SCORE = 76
    MIN_SUBJECTS = 3

    def __init__(self, data: DataType) -> None:
        self.data: DataType = data

    def count_subjects_with_score(self, student: str, score: int) -> int:
        """Число дисциплин студента, по которым получен балл score."""
        if student not in self.data:
            raise KeyError("Студент не найден: {}".format(student))
        return sum(1 for _, value in self.data[student] if value == score)

    def students_with_score_in_subjects(
            self,
            score: int = TARGET_SCORE,
            min_count: int = MIN_SUBJECTS) -> list[str]:
        """Все студенты с баллом score минимум по min_count дисциплинам.

        Порядок студентов совпадает с порядком их следования во входном
        файле.
        """
        if min_count < 1:
            raise ValueError("Число дисциплин должно быть положительным")

        return [
            student for student in self.data
            if self.count_subjects_with_score(student, score) >= min_count
        ]

    def find_student_with_score_in_subjects(
            self,
            score: int = TARGET_SCORE,
            min_count: int = MIN_SUBJECTS) -> Optional[str]:
        """Первый подходящий студент либо None, если таких студентов нет.

        Условие варианта допускает любого из подходящих студентов;
        возвращается первый по порядку следования во входном файле,
        чтобы результат работы программы был воспроизводимым.
        """
        students = self.students_with_score_in_subjects(score, min_count)
        return students[0] if students else None
