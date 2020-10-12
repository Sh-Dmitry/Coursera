import os
import tempfile
import random


class File:
    def __init__(self, path):
        if os.path.exists(path):
            self._path = path
        else:
            open(path, "w").close()
            self._path = path

    def read(self):
        with open(self._path, 'r') as f:
            return f.read()

    def write(self, string):
        with open(self._path, 'w') as f:
            return f.write(string)

    def __add__(self, other):
        new_text = self.read() + other.read()
        rand = random.randint(1, 10)
        new_path = os.path.join(tempfile.gettempdir(), "new_file_{}.txt".format(rand))
        new_file = File(new_path)
        new_file.write(new_text)
        # new_file.close()
        return new_file

    def __str__(self):
        return "{}".format(os.path.abspath(self._path))

    def __iter__(self):
        f = open(self._path, 'r')
        return f

    def __next__(self):
        result = f.readline()
        if result == '':
            f.close()
            raise StopIteration
        return result

