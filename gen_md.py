# -*- utf8 -*-
from datetime import date, datetime

today = date.today()
now = datetime.now()
now = datetime.strftime(now, format('%Y-%m-%d %H:%M:%S'))

result = []
lay_outs = """
---
layout:     post
title:      "{title}"
subtitle:   "{subtitle}"
date:       {format_date}
author:     "none"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - tag
---
"""
input_file_name = input("please input file name:\n")

file_name = "{date}-{name}".format(date=today, name=input_file_name)
result.append(lay_outs.format(title=input_file_name, subtitle=input_file_name, format_date = now))
with open('%s.md' % file_name, 'w') as fw:
    fw.write('%s' % '\n'.join(result))
