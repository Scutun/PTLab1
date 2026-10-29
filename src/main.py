# -*- coding: utf-8 -*-
import argparse
import os
import sys

from CalcRating import CalcRating
from DataReader import DataReader
from JsonDataReader import JsonDataReader
from TextDataReader import TextDataReader
from ThirdQuartileStudents import ThirdQuartileStudents


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def get_reader(path: str) -> DataReader:
    extension = os.path.splitext(path)[1].lower()
    if extension == ".json":
        return JsonDataReader()
    if extension == ".txt":
        return TextDataReader()
    raise ValueError(f"Неподдерживаемый формат файла: '{extension}'")


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = get_reader(path)
    students = reader.read(path)
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Rating: ", rating)
    third_quartile = ThirdQuartileStudents(rating)
    result = third_quartile.calc()
    print(f"Q2 (медиана) = {third_quartile.q2:.2f}, "
          f"Q3 = {third_quartile.q3:.2f}")
    print("Студенты, чей рейтинг попадает в третью квартиль:")
    if not result:
        print("  таких студентов нет")
    for name, score in result.items():
        print(f"  {name}: {score:.2f}")


if __name__ == "__main__":
    main()
