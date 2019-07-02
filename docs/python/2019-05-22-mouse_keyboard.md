
---
layout:     post
title:      "mouse_keyboard"
subtitle:   "mouse_keyboard"
date:       2019-05-22 09:31:09
author:     "none"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - tag
---


# 监控和模拟鼠标键盘事件
pip install pynput

# 模拟鼠标键盘
pip install PyAutoGUI

# 拷贝
将python数据传输到剪切板
```python
#pip install pywin32
import win32clipboard
from io import StringIO
from io import BytesIO


def send_to_clipboard(img):
    ''' copy PIL Image to clipboard '''
    #output = StringIO()
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

```
从剪切板获取数据到python变量中
```python
#pip install pywin32
#pip install chardet
import win32clipboard
import chardet

def get_from_clipboard():
    win32clipboard.OpenClipboard()
    copy_text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()
    return copy_text

```

# 记录器
记录用户动作序列， 包括键盘和鼠标
