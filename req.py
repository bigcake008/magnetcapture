from urllib import request
import re

# URL OPTION
url_option = {'bthub': 'https://bthub.xyz/main-search-kw-%s-%d.html',
              'sobt5': 'http://sobt5.in/q/%s.html?sort=rel&page=%d'
              }
# REGEX SET
regex_set = {'bthub': {'title': r'title="(.+)" href', 'size': r'-pill">(.+)</b>',
                       'magnet': r'hash/(\w+).html', 'next_page': r'下一页</a>'},
             'sobt5': {'title': r'target="_blank">(.*)</a>', 'size': r'yellow-pill">(.*B)</b>',
                       'magnet': r'torrent/(\w+).html', 'next_page': r'class="nextpage"'}
             }


def make_req(kw, page, url='bthub'):  # make up a request
    req = request.Request(url_option[url] % (kw, page))
    print(url_option[url] % (kw, page))
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Host', re.search(r'//(\w+.\w+)/', url_option[url])[1])
    req.add_header('Upgrade-Insecure-Requests', '1')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 '
                                 'Firefox/72.0')
    return req


def process_data(data, web='bthub'):  # data processing
    i = 0
    result = []
    tem_dic = {}
    next_page = False
    title = re.findall(regex_set[web]['title'], data)
    size = re.findall(regex_set[web]['size'], data)
    magnet = re.findall(regex_set[web]['magnet'], data)
    while i < len(title):
        tem_dic['title'] = re.sub(r'</?em>', '', title[i])
        tem_dic['size'] = size[i]
        tem_dic['magnet'] = magnet[i]
        result.append(tem_dic)
        tem_dic = {}
        i += 1
    if re.search(regex_set[web]['next_page'], data):
        next_page = True
    return [result, next_page]
