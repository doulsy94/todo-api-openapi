# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime
from typing import List, Dict

from openapi_server.models.base_model import Model
from openapi_server import util


class TaskInput(Model):
    def __init__(self, title=None, completed=None, due_date=None):
        self.openapi_types = {
            'title': str,
            'completed': bool,
            'due_date': date
        }

        self.attribute_map = {
            'title': 'title',
            'completed': 'completed',
            'due_date': 'due_date'
        }

        self._title = title
        self._completed = completed
        self._due_date = due_date

    @classmethod
    def from_dict(cls, dikt):
        return util.deserialize_model(dikt, cls)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")
        self._title = title

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        self._completed = completed

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        self._due_date = due_date