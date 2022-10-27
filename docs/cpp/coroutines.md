

# 协程

为什么需要协程而不是线程？

1. 线程切换上下文比较耗时
2. 线程阻塞时不能用于执行其他任务
3. 线程数量过多时， 线程之间会频繁抢占发生

场景： 线程池中所有线程均由于系统调用发生阻塞， 新增线程会耗时



# coroutines

- 有栈（stackful）协程
  - 在堆上提前分配内存，存储协程上下文
- 无栈协程
  - C++20 为无栈协程


协程帧(coroutine frame)
- 协程参数
- 局部变量
- promise 对象

caller和协程交互
- caller通过 std::coroutine_handle访问呢协程帧相关数据
- 


一个函数成为一个coroutine， 当这个函数有使用`co_`前缀操作符时
- co_await 挂起协程
- co_yield 挂起协程执行并返回值
- co_return 完成协程执行并返回值



- coroutine handle 在协程外部使用，用于恢复或者摧毁协程
- coroutine state
  - promise 协程内部使用的对象，用于协程提交结果和异常
  - parameters 值拷贝的方式保存的协程参数
  - 局部变量和挂起点等相关数据


当协程函数被调用时，会先做很多初始化工作，
1. 分配coroutine state需要的内存
2. 拷贝协程函数参数到coroutine state
3. 构造promise对象
4. 调用`promise.get_return_object()` 


C++20中的Coroutine
https://marvinsblog.net/post/2019-08-20-cpp20-coroutine-02/

https://github.com/CppCon/CppCon2016/blob/master/Presentations/Introduction%20to%20C%2B%2B%20Coroutines/Introduction%20to%20C%2B%2B%20Coroutines%20-%20James%20McNellis%20-%20CppCon%202016.pdf


## 协程何时挂起返回， 返回的是什么？
- 在协程函数开始，编译器自动插入代码，使用co_await调用promise对象的initial_suspend方法，决定是否挂起协程
- 在协程函数末尾，使用co_await调用promise对象的final_suspend方法，决定是否挂起协程
- 当前协程第一次挂起并返回到调用者时，返回给调用者的是promise.get_return_object()的结果

- 协程函数中不能使用return

https://blog.panicsoftware.com/co_awaiting-coroutines/


## awaiter type
awaiter类型： 实现await_ready、await_suspend、await_resume三个方法的类型
例如： std::suspend_never 和 std::suspend_always
```c++
struct suspend_never {
  bool await_ready() const noexcept { return true; }
  void await_suspend(coroutine_handle<>) const noexcept {}
  void await_resume() const noexcept {}
};

struct suspend_always {
  bool await_ready() const noexcept { return false; }
  void await_suspend(coroutine_handle<>) const noexcept {}
  void await_resume() const noexcept {}
}
```


## co_await

```
auto ret = co_await expr;
```
`expr`需要能够转换为Awaitable对象, Awaitable对象会被编译器转换为awaiter对象，如果不能转换会编译失败
编译器会插入代码调用awaiter对象上的await_ready、await_suspend、await_resume方法


伪代码
```
auto awaitable = expr;
auto awaiter = convert(awaitable);
if (awaiter.await_ready() == false) {
  current_coroutine_suspension();
  if (awaiter.await_suspend(handle) return void) {

  } else if (awaiter.await_suspend(handle) return bool) {

  } else if (awaiter.await_suspend(handle) return handle) {
    handle.resume()
  }
}

auto ret = awaiter.await_resume()
```

## `expr` 转换为awaitable对象

- 当前协程的promise_type中定义了await_transform方法，调用promise.await_transform(expr)得到awaitable对象
- 当前协程的promise_type中没有定义await_transform方法，expr本身必须是awaitable对象

## awaitable对象转换为awaiter对象

- Awaitable对象有operator co_await 操作符重载， 调用该方法获得awaiter对象

## co_await语句执行过程
- 调用`awaiter.await_ready()`
  - 返回false
    - co_await语句所在的协程函数被挂起（Coroutine suspension, 局部变量等保存到协程状态中，此时只是保存好协程上下文，还未返回协程调用者）
    - 调用`awaiter.await_suspend(handle)`
      - 返回void：当前协程处于暂停状态，返回到当前协程的调用者
      - 返回bool
        - true：返回到当前协程的调用者
        - false：恢复当前协程
      - 返回coroutine_handle（来自其他协程）： 在该coroutine_handle上执行resume
- 调用`awaiter.await_resume()`, 无论当前线程是否被挂起，都会进行此次调用， 返回值也会作为`co_await expr`的结果





# x86

编译32位
```
g++ main.cpp -m32
```



c++ 和 汇编 
- MSVC inline asm 
- GNU C inline asm


汇编语法
- Intel syntax - target on the left, source on the right
反汇编
```
objdump -M intel -d a.out
objdump -x86-asm-syntax=intel -d a.out  (mac llvm)
```

`objdump -d` only disassembles sections of the executable where there's supposed to be code.
`objdump -D` to disassemble all sections



## 函数调用分析

### 示例一：
源码：
```c++
int func() {
    return 123;
}

int main()
{
    int ret = func();
    return 0;
}
```

反汇编：
```
g++ main.cpp -m32
objdump -M intel -d a.out
```

带调试信息， c源码和汇编代码
```
g++ main.cpp -m32 -ldl -g
objdump -M intel -dS a.out
```

```
0804850d <_Z4funcv>:
 804850d:       55                      push   ebp
 804850e:       89 e5                   mov    ebp,esp
 8048510:       b8 7b 00 00 00          mov    eax,0x7b
 8048515:       5d                      pop    ebp
 8048516:       c3                      ret   

08048517 <main>:
 8048517:       55                      push   ebp
 8048518:       89 e5                   mov    ebp,esp
 804851a:       83 ec 10                sub    esp,0x10
 804851d:       e8 eb ff ff ff          call   804850d <_Z4funcv>
 8048522:       89 45 fc                mov    DWORD PTR [ebp-0x4],eax
 8048525:       b8 00 00 00 00          mov    eax,0x0
 804852a:       c9                      leave  
 804852b:       c3                      ret 
```

子函数func未分配局部变量， esp未改变， ret前不需要leave指令, 仅需要恢复父函数的ebp即可

### 示例二：

```
int func() {
    int a = 1;
    int b = 2;
    
    return 123;
}

int main()
{
    int ret = func();
    return 0;
}
```

```
0804850d <_Z4funcv>:
 804850d:       55                      push   ebp
 804850e:       89 e5                   mov    ebp,esp
 8048510:       83 ec 10                sub    esp,0x10
 8048513:       c7 45 fc 01 00 00 00    mov    DWORD PTR [ebp-0x4],0x1
 804851a:       c7 45 f8 02 00 00 00    mov    DWORD PTR [ebp-0x8],0x2
 8048521:       b8 7b 00 00 00          mov    eax,0x7b
 8048526:       c9                      leave  
 8048527:       c3                      ret    

08048528 <main>:
 8048528:       55                      push   ebp
 8048529:       89 e5                   mov    ebp,esp
 804852b:       83 ec 10                sub    esp,0x10
 804852e:       e8 da ff ff ff          call   804850d <_Z4funcv>
 8048533:       89 45 fc                mov    DWORD PTR [ebp-0x4],eax
 8048536:       b8 00 00 00 00          mov    eax,0x0
 804853b:       c9                      leave  
 804853c:       c3                      ret    
```

### 函数调用过程分析

栈： 从栈顶入元素， 从栈顶出元素; 栈在内存中是从高地址向低地址生长的

刚进入子程序时， 栈内存的布局：
```
esp -> [call 指令的下一条指令地址]
```

函数的开始都有如下代码, 用于保存父函数的栈帧， 父函数的栈顶（esp） 和子函数的栈底（ebp）相同
```
push   ebp
mov    ebp,esp
```

栈内存的布局：
```
              [call 指令的下一条指令地址]
esp，ebp ->   [父函数的ebp]
```

子函数使用局部变量时， 基于ebp进行寻址, 取传入参数使用+地址， 取局部变量使用-地址

子函数返回时，将返回值保存到eax中

函数返回时， leave指令将父函数的esp置为子程序的ebp， 然后将父函数的ebp从栈里弹出恢复， 
```
esp ->   [call 指令的下一条指令地址]
```
ret指令从栈里取出返回地址， 接着执行父函数








```c++
__declspec(naked) void __stdcall func(void* ptr)
{
    __asm
    {
      //...
    }
}
```
__declspec() : MSVC的拓展属性声明
naked: https://docs.microsoft.com/en-us/cpp/cpp/naked-cpp?view=msvc-160， 用户自定义函数进入（prolog）和退出（epilog）逻辑



Function prolog and epilog





函数调用指令

影响参数传递和返回值的方式
__stdcall：被调用者（callee) 负责清理栈内存 （winapi  dll 默认为__stdcall 方式）
__cdecl： 调用者（caller) 负责清理栈内存 
__fastcall: 通过寄存器来传送参数的（实际上，它用ECX和EDX传送前两个双字（DWORD）或更小的参数，剩下的参数仍旧自右向左压栈传送，被调用的函数在返回前清理传送参数的内存栈）

```
/* example of __stdcall */
push arg1 
push arg2 
push arg3 
call function // callee does stack cleanup
```

```
/* example of __cdecl */
push arg1
push arg2
push arg3
call function
add sp,12 // effectively "pop; pop; pop"
```


# 协程使用场景

系统调用IO阻塞， 通过hook系统调用改为非阻塞， 进行协程切换