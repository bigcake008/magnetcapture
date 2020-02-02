from urllib import request
import ssl
import gzip


context = ssl._create_unverified_context()
req = request.Request('https://bthub.xyz/main-search-kw-IPZ-782-1.html')
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Accept-Encoding', 'gzip')
req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2')
req.add_header('Connection', 'keep-alive')
req.add_header('Host', 'bthub.xyz')
req.add_header('Upgrade-Insecure-Requests', '1')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0')
with request.urlopen(req, context=context) as html:
    data = html.read()

    print(gzip.decompress(data).decode('utf-8'))