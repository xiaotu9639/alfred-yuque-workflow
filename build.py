# -*- coding: utf-8 -*-
# Authors: Joe <xiaotu9639@gmail.com>

import os
import re
import zipfile

__version__ = '2.0.0'

if __name__ == '__main__':
    # 获取新版本号
    old_version = open('version', 'r').read()
    old_version = re.sub(r'\s', '', old_version)
    tail = int(old_version[-1]) + 1
    confirm_version = old_version[:-1] + str(tail)
    confirm = input('推荐新版本号为 %s (回车确认或输入指定版本号):' % confirm_version)
    new_version = confirm if confirm else confirm_version
    print(u'将使用新版本号 %s 构建发布包' % new_version)

    # 新版本号写入 version 文件
    with open('version', 'w') as v:
        v.write(new_version)

    # 构建发布包
    if not os.path.exists('out'):
        os.mkdir('out')
    z = zipfile.ZipFile('out/yuque-%s.alfredworkflow' % new_version, 'w')
    z.write('info.plist')
    z.write('icon.png')
    z.write('action.py')
    z.write('yuque.py')
    z.write('version')
    z.write('readme.md')
    for f in os.listdir('workflow'):
        z.write(os.path.join('workflow', f))

    print('Build completed.')

