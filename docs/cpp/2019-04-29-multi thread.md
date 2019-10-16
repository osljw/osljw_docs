
---
layout:     post
title:      "title"
subtitle:   "multi thread"
date:       2019-04-29 11:40:28
author:     "soaringsoul"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - tag
---

#
原子性 (避免中间态的存在，所有线程看到原子操作前的状态或者是操作完成后的状态)
可见性 (由于cpu缓存的存在，一个线程的修改，其他线程不能及时看到修改结果)

# 
http://www.droidsec.cn/%E5%B8%B8%E8%A7%81android-native%E5%B4%A9%E6%BA%83%E5%8F%8A%E9%94%99%E8%AF%AF%E5%8E%9F%E5%9B%A0/

## 写空指针
```
int* p = 0; //空指针
*p = 1; //写空指针指向的内存，产生SIGSEGV信号，造成Crash
```
0x0地址页面无写权限， 触发SIGSEGV段错误

## 写野指针
```
int* p; //野指针，未初始化，其指向的地址通常是随机的
*p = 1; //写野指针指向的内存，有可能不会马上Crash，而是破坏了别处的内存
```
野指针指向的是一个无效的地址，该地址如果是不可读不可写的，那么会马上Crash(内核给进程发送段错误信号SIGSEGV)，这时bug会很快被发现。
如果访问的地址为可写，而且通过野指针修改了该处的内存，那么很有可能会等一段时间(其它的代码使用了该处的内存后)才发生Crash。这时查看Crash时显示的调用栈，和野指针所在的代码部分，有可能基本上没有任何关联。

## 数组越界
## 浮点异常(SIGFPE), 如除零错误

## 缓冲区溢出
```
char szBuffer[10]; // szBuffer 在栈上分配内存
//由于函数栈是从高地址往低地址创建，而sprintf是从低地址往高地址打印字符，
//如果超出了缓冲区的大小，函数的栈帧会被破坏，在函数返回时会跳转到未知的地址上，
//基本上都会造成访问异常，从而产生SIGABRT或SIGSEGV，造成Crash

sprintf(szBuffer, "Stack Buffer Overrun!111111111111111"  "111111111111111111111");
```

如果core文件和可执行文件是匹配的，但是调用栈是错乱的，那么很大的可能性是发生了缓冲区溢出。


# 线程停止
通知线程停止一般通过改变标志位来实现，被停止的线程需要周期性的检测该标志位，主动进行退出
