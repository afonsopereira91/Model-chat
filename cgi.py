"""Minimal cgi compatibility shim for Python 3.14+.

Remi imports the legacy cgi.FieldStorage class for handling POST uploads.
This stub provides the minimal API needed to avoid import failures when
running the app in environments where the stdlib cgi module is removed.
"""

class FieldStorage:
    def __init__(self, fp=None, headers=None, environ=None):
        self._fields = {}

    def keys(self):
        return list(self._fields.keys())

    def __getitem__(self, key):
        return self._fields[key]

    def getvalue(self, key, default=None):
        return self._fields.get(key, default)

    def __iter__(self):
        return iter(self._fields)

    def __len__(self):
        return len(self._fields)

    def __bool__(self):
        return bool(self._fields)


class MiniField:
    def __init__(self, value=None, filename=None, file=None):
        self.value = value
        self.filename = filename
        self.file = file

    def __bool__(self):
        return True
