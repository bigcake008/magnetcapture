from urllib import request
import re
import io


def bt_hub_req(kw, page):  # make up a request
    req = request.Request('https://bthub.xyz/main-search-kw-%s-%d.html' % (kw, page))
    print('processing: https://bthub.xyz/main-search-kw-%s-%d.html' % (kw, page))
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Host', 'bthub.xyz')
    req.add_header('Upgrade-Insecure-Requests', '1')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 '
                                 'Firefox/72.0')
    return req


def bt_hub_cap():  # due with the captured html
    result = []
    tem_dic = {}
    with io.open('captured_html', 'r') as f:
        for line in f.readlines():
            if re.search(r'<h3>', line):  # search for title & hash of the magnet
                try:
                    match = re.search(r'title="(.*)" href="/hash/(\w+).html"', line, re.I)
                    tem_dic['title'] = match[1]
                    tem_dic['magnet'] = match[2]
                except BaseException as e:
                    print('error:', e)
            if re.search(r'-pill', line):  # search for size of magnet
                match = re.search(r'<.*>(.+)</b>', line)
                tem_dic['size'] = match[1]
                print(tem_dic['title'])
                result.append(tem_dic)
                tem_dic = {}  # clean up the temporary dictionary after grouping in the result array
            if re.search(r'下一页</a>', line):  # looking for the next page
                next_page = True
            if re.search(r'<span>下一页', line):
                next_page = False
    return [result, next_page]
