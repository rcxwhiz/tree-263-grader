from __future__ import annotations

from typing import Optional


class IOResultsMeta(type):
	_instance: Optional[IOResults] = None

	def __call__(self) -> IOResults:
		if self._instance is None:
			self._instance = super().__call__()
		return self._instance


class IOResults(metaclass=IOResultsMeta):

	def __init__(self, key, students):
		self.key = key
		self.students = students
		self.num_students = len(students.keys())
