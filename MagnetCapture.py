from urllib import request
import io
import re
import gzip
import ssl
from req import bt_hub_req, bt_hub_cap
from time import sleep
from random import uniform

context = ssl._create_unverified_context()  # fix [SSL: CERTIFICATE_VERIFY_FAILED] error
result = []


class Actress:
    def __init__(self, name):
        self.name = name
        self.dvd_id = []
        self.magnet_dic = {}
        self.page = 1

    def capture_magnet(self):
        for kw in self.dvd_id:
            tem_ary = []  # clean up the temporary array for recording magnet in each id searching
            self.process_url(kw, tem_ary)
            sleep(uniform(1.5, 2.5))  # take a break for the next connecting

    def process_url(self, kw, ary):
        req = bt_hub_req(kw, self.page)
        try:
            respond = request.urlopen(req, timeout=5, context=context)
            data = gzip.decompress(respond.read()).decode('utf-8')
            with io.open('captured_html', 'w') as f:
                f.write(data)
            capture = bt_hub_cap(kw)
            for item in capture[0]:
                ary.append(item)
            if capture[1]:  # if there are pages, run them through
                self.page += 1
                self.process_url(kw, ary)
            self.magnet_dic[kw] = ary
        except BaseException as e:  # reconnect if time out error happened
            print('Error:', e)
            print('Reconnecting...')
            self.process_url(kw, ary)


with io.open('input', 'r') as file:
    for line in file.readlines():
        if re.match(r'[\S][\W]', line, re.A):
            actress = Actress(line)
            result.append(actress)
            continue
        if re.match(r'\w', line, re.A):
            group = re.search(r'^([0-9a-zA-Z]+[a-zA-Z])-?(\d+)', line)
            reform = '%s-%s' % (group[1], group[2])
            actress.dvd_id.append(reform)
for actress in result:
    with io.open('output', 'a') as file:
        file.write(actress.name)
    actress.capture_magnet()
    with io.open('output', 'a') as file:
        for dvd_id in actress.dvd_id:
            file.write('\n%s:\n' % dvd_id)
            for magnet in actress.magnet_dic[dvd_id]:
                file.write(' title:%s\n size:%s\n magnet:%s\n' % (magnet['title'], magnet['size'], magnet['magnet']))
        file.write('\n\n')

print('done')
