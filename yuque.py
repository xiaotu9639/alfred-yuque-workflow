#!/usr/bin/python
# encoding: utf-8
import re
import sys
import urllib

from workflow import Workflow3, web

YUQUE_BASE_URL = 'https://yuque.com'


def query_doc(wf, query):
    token = wf.stored_data('token')
    headers = {
        'X-Auth-Token': token}
    url = '%s/api/v2/search?type=doc&related=true&q=%s' % (YUQUE_BASE_URL, urllib.quote(query.encode('utf-8')))
    wf.logger.debug('==> url: %s', url)
    resp = web.get(url, headers=headers)
    if resp.status_code == 200:
        total = resp.json()['meta']['total']
        # 查询结果为空
        if total == 0:
            wf.add_item(u'没有符合条件的查询结果', autocomplete='')

        data = resp.json()['data']
        wf.logger.debug('==> query = %s, got result: %s', query, total)
        # 构建查询结果选择列表
        for doc in data:
            book_name = doc['target']['book']['name']
            title = clean_hilight(doc['title'])
            title = '%s - %s' % (book_name, title)
            subtitle = clean_hilight(doc['summary'])
            wf.add_item(title,
                        subtitle=subtitle,
                        arg='open %s%s' % (YUQUE_BASE_URL, doc['url']),
                        valid=True)
    # 未授权
    elif resp.status_code == 401:
        wf.add_item('Error: Unauthorized', autocomplete='> login ')

    else:
        wf.add_item('Error: Unknow', subtitle=url, autocomplete='')


def action_list(wf, query):
    args = query.split()
    command = args[1] if len(args[0]) == 1 and len(args) > 1 else args[0][1:]

    if command in 'login':
        valid = bool(re.match(r'^>\s*login\s+\w+$', query))
        wf.add_item('> login <Access token>',
                    subtitle=u'设置语雀 AccessToken',
                    arg='login %s' % args[-1],
                    autocomplete='> login ',
                    valid=valid)

    if command in 'update':
        wf.add_item('> update',
                    subtitle=u'检查更新',
                    arg='update',
                    autocomplete='> update ',
                    valid=True)


def clean_hilight(text):
    text = re.sub(r'<em>', '', text)
    text = re.sub(r'</em>', '', text)
    return text


def main(wf):
    query = wf.args[0]
    if query.startswith('>'):
        action_list(wf, query)
    else:
        query_doc(wf, query)

    wf.send_feedback()


if __name__ == '__main__':
    update_settings = {
        'github_slug': 'xiaotu9639/alfred-yuque-workflow',
        'frequency'  : 1
    }
    wf3 = Workflow3(update_settings=update_settings)
    # 更新
    if wf3.update_available:
        wf3.start_update()
    sys.exit(wf3.run(main))
