

# 协程

为什么需要协程而不是线程？

1. 线程切换上下文比较耗时
2. 线程阻塞时不能用于执行其他任务
3. 线程数量过多时， 线程之间会频繁抢占发生

场景： 线程池中所有线程均由于系统调用发生阻塞， 新增线程会耗时




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


协程何时挂起返回， 返回的是什么？
- 在协程函数开始，编译器自动插入代码，使用co_await调用promise对象的initial_suspend方法，决定是否挂起协程
- 在协程函数末尾，使用co_await调用promise对象的final_suspend方法，决定是否挂起协程



https://blog.panicsoftware.com/co_awaiting-coroutines/

```
co_await expression;
```
`expression`的需要能够转换为Awaitable
- 定义 `operator co_await`

co_await表达式的值
- expression形成的Awaiter对象的await_resume方法的返回值

co_await语句执行时发生的情况：
- Awaiter对象的await_ready方法返回true
  - 运行Awaiter对象的await_resume方法，并将await_resume方法的返回值作为协程的返回值
- Awaiter对象的await_ready方法返回false
  - co_await语句所在的协程函数被挂起， Coroutine suspension, 协程挂起并不是返回协程调用者，只是将一些局部变量保存到堆中
  - Awaiter对象的await_suspend方法返回void
    - 当前协程处于暂停状态，返回到当前
  - Awaiter对象的await_suspend方法返回bool
    - false：运行Awaiter对象的await_resume方法，并将await_resume方法的返回值作为协程的返回值
    - true：
  - Awaiter对象的await_suspend方法返回coroutine_handle



co_await expression => Awaitable  => Awaiter