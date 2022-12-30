# -*- coding: utf-8 -*-
# Authors: Joe <xiaotu9639@gmail.com>
# Date: 2022/12/30


from urllib import request, parse
import json

YUQUE_BASE_URL = 'https://yuque.com'

if __name__ == '__main__':
    headers = {'X-Auth-Token': '9AP7jcwAfl6B7Jw0P8LeVkabljzB5YForzjXDoUJ'}
    url = '%s/api/v2/search?type=doc&related=true&q=%s' % (YUQUE_BASE_URL, parse.quote('非结构化'))
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    if resp.getcode() == 200:
        resp_data = json.loads(resp.read().decode())
        total = resp_data['meta']['total']
        data = resp_data['data']
        print(total)
        print(data)
