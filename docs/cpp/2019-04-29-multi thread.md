
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



# 系统调用

系统调用通过软中断实现， 进入内核空间， 但不会改变线程上下文， current宏是有效的，准备退出中断上下文时，如果没有高优先级的线程抢占， 还是会回到原来的线程上下文

线程状态

https://smartkeyerror.com/Linux-Blocking

运行：
等待：由于缺少 CPU 资源而被迫停止运行， 只要调度器下次选中该进程即可立即执行，进入运行状态，  线程放到就绪队列中（红黑树实现）
睡眠：进程不会被调度器进行选择并执行， 等待外部事件的发生而变为等待状态（例如硬件中断等）， 线程放到等待队列中（双链表实现）

# 系统调用hook

### LD_PRELOAD 方式

https://blog.csdn.net/tianxuhong/article/details/50974400

替换加载的动态连接库


```c++
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
  if( strcmp(argv[1], "test") )
  {
    printf("Incorrect password\n");
  }
  else
  {
    printf("Correct password\n");
  }
  return 0;
}
```


```c++
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
/*
hook的目标是strcmp，所以typedef了一个STRCMP函数指针
hook的目的是要控制函数行为，从原库libc.so.6中拿到strcmp指针，保存成old_strcmp以备调用
*/
typedef int(*STRCMP)(const char*, const char*);
 
int strcmp(const char *s1, const char *s2)
{
  static void *handle = NULL;
  static STRCMP old_strcmp = NULL;
 
  if( !handle )
  {
    handle = dlopen("libc.so.6", RTLD_LAZY);
    old_strcmp = (STRCMP)dlsym(handle, "strcmp");
  }
  printf("oops!!! hack function invoked. s1=<%s> s2=<%s>\n", s1, s2);
  return !old_strcmp(s1, s2);
}
```


运行
```
g++ main.cpp -o main
g++ -fPIC -shared hook.cpp -o hook.so

./main 123
LD_PRELOAD=./hook.so ./a.out 123
```
