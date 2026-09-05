# -*- coding: utf-8 -*-
import argparse
import sys

from CalcRating import CalcRating
from ReaderFactory import ReaderFactory


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    path = get_path_from_arguments(sys.argv[1:])

    reader = ReaderFactory.create(path)
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)


if __name__ == "__main__":
    main()
