from urllib import request
import io
import re


class Actress:
    def __init__(self, name):
        self.name = name
        self.dvd_id = []

    def capture_magnet(self):
        for kw in self.dvd_id:
            # with request.urlopen()
            pass

result = []
with io.open('input', 'r') as file:
    count = 0
    for line in file.readlines():
        if re.match(r'[\S][\W]', line, re.A):
            actress = Actress(line)
            result.append(actress)
            continue
        if re.match(r'\w', line, re.A):
            reform = '%s-%s' % (re.search(r'([\w]+[a-zA-Z])', line)[1], re.search(r'(\d+)', line)[1])
            actress.dvd_id.append(reform)

print('done')
