

软件中断和硬件中断

中断：有硬件保存和恢复现场

- 软件中断， int 3 指令触发

# ida


字符串视图 view -> open subviews -> strings
1. 搜索常用的字符串， 如血量health， 弹药armor



## Exception handling
![](media/ida_excepthandle.png)

# ollydbg
- Open
- Attach
- Just-in-time debugging


# x64dbg x32dbg

- 使用F9开始运行，找到程序真正的EntryPoint，脱壳定位
- 使用`符号`窗口，搜索用户模块中的相关符号，定位相关代码
- 使用`调用堆栈`窗口，找到正常运行流程和限制运行流程的代码执行路径，两个路径有分叉的地方就是需要破解的地方

## script command
()为表达式求值， eg: (123 + 456)

[]为获取地址处的值， eg: [0x00007FFE6E0A1008]

- msg 消息弹窗
    - 使用{}获取变量的值
```
msg (123 + 456)表达式的值：{(123 + 456)}
msg 0x00007FFE6E0A1008地址保存的值：{[0x00007FFE6E0A1008]}
```