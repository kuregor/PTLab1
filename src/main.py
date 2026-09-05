# -*- coding: utf-8 -*-
import argparse
import sys
from typing import Optional

from CalcRating import CalcRating
from ReaderFactory import ReaderFactory
from StudentStats import StudentStats


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def format_result(student: Optional[str]) -> str:
    """Готовит сообщение о результате индивидуального задания."""
    if student is None:
        return ("Студентов, имеющих {} баллов минимум по {} дисциплинам, "
                "в файле нет".format(StudentStats.TARGET_SCORE,
                                     StudentStats.MIN_SUBJECTS))

    return ("Студент, имеющий {} баллов минимум по {} дисциплинам: {}"
            .format(StudentStats.TARGET_SCORE,
                    StudentStats.MIN_SUBJECTS, student))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    path = get_path_from_arguments(sys.argv[1:])

    reader = ReaderFactory.create(path)
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    stats = StudentStats(students)
    print(format_result(stats.find_student_with_score_in_subjects()))


if __name__ == "__main__":
    main()
