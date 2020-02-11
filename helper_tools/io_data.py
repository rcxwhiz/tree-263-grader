from __future__ import annotations

from typing import Optional


class IOResultsMeta(type):
    _instance: Optional[IOResults] = None

    def __call__(self) -> IOResults:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class IOResults(metaclass=IOResultsMeta):

    def __init__(self):
        self.key_files = None
        self.student_files = None
        self.num_students = None

    def populate(self, key, students):
        self.key_files = key
        self.student_files = students
        self.num_students = len(students)

    def set_stdout_ref(self, ref):
        self.stdout_ref = ref


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
