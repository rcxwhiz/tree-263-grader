from __future__ import annotations

from typing import Optional


class PythonResultsMeta(type):
    _instance: Optional[PythonResults] = None

    def __call__(self) -> PythonResults:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class PythonResults(metaclass=PythonResultsMeta):

    def __init__(self):
        self.key_files = []
        self.student_files = {}
        self.num_students = 0

    def populate(self, key, students):
        self.key_files = key
        self.student_files = students
        self.num_students = len(students)


class ExcelResultsMeta(type):
    _instance: Optional[ExcelResults] = None

    def __call__(self) -> ExcelResults:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class ExcelResults(metaclass=ExcelResultsMeta):

    def __init__(self):
        self.key = None
        self.students = None
        self.num_students = None

    def populate(self, key, students):
        self.key = key
        self.students = students
        self.num_students = len(students)
