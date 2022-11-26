
# 寄存器

- ebp 基址寄存器
- esp 栈指针寄存器

栈是从高地址向低地址生长的， 

这里的栈是从栈顶push和pop数据

ebp 和 esp 配合构成函数的栈帧，ebp指向当前函数栈帧的栈底， esp指向当前函数栈帧的栈顶，

ebp 也作为当前函数局部变量寻址的基址寄存器

- edi 目的地址寄存器



# 汇编指令

push 和 pop
```
PUSH <src> 
 ESP := ESP-4  ; for x86; -8 for x64
 MEMORY[ESP]:=<operandvalue>

POP <dst> 
 <operandtarget>:=MEMORY[ESP];
 ESP:=ESP+4    ; for x86; +8 for x64
```
push先减地址，后存储， pop先取值，后加地址


栈帧由ebp和esp确定

call 和 leave 和 ret 
- call: 将下一条指令的地址入栈， 并立即跳转到子程序
- leave： 销毁当前函数的栈帧， 恢复父函数的栈帧
- ret: 从栈中弹出存储作为地址， 并立即跳转到该地址执行

```
# leave 等效指令
mov esp ebp ; 恢复父函数的esp
pop ebp ;  恢复父函数的ebp
```



- lea 取址指令

```
; edi 寄存器中将存储一个地址， 地址为栈基址（栈底)地址减去0xC0字节后得到的地址
0023366C  lea         edi,[ebp-0C0h]  	

00233672  mov         ecx,30h  
00233677  mov         eax,0CCCCCCCCh  
0023367C  rep stos    dword ptr es:[edi]  
```

- jmp 跳转指令

jmp 指令占用5字节(1字节操作码，4字节相对偏移地址), 相对偏移地址计算： (目标函数地址 - (jmp指令所在地址 + 5))


- je： 相等/标志位ZF=1，则跳转
- jne: 不相等/标志位ZF=0，则跳转
- JA（jump above）: 大于/CF∨ZF = 0

## 计算指令

xor： 异或指令，常用于寄存器清零
```
xor r14d,r14d
```

# 编译器指令

__declspec(naked) 

对于没有用naked声明的函数一般编译器都会产生保存现场（进入函数时编译器会产生代码来保存ESI，EDI，EBX，EBP寄存器 ——prolog）和清除现场（退出函数时则产生代码恢复这些寄存器的内容——epilog）代码，而对于用naked声明的函数一般不会产生这些代码


# 反汇编

```c++
void hello_world(int i) {
	std::cout << "Hello World!" << i << std::endl;
}

int main()
{
	std::cout << "hello_world addr: 0x" << (void*)hello_world << std::endl;

	int count = 100;
	std::chrono::seconds timespan(5); 

	while (count--) {
		hello_world(count);
		std::this_thread::sleep_for(timespan);
	}
}
```

- 每次反汇编后，函数的地址是不确定的， 调用函数的代码地址也是不确定的
- 函数参数入栈的代码在call指令之前， 函数代码的开头会将该函数使用到的寄存器现场保存到栈上，在函数代码的返回指令ret之前将寄存器现场恢复

调用函数时的汇编代码
==================

```
		hello_world(count);
0023722C  mov         eax,dword ptr [count]  
0023722F  push        eax  
00237230  call        hello_world (02314A1h)  
00237235  add         esp,4  					; 
```	

参数入栈顺序为从右往左

调用函数负责被调用函数的参数入栈和出栈, 只有调用函数知道被调函数需要几个参数




函数hello_world对应的汇编代码
===========================

```
hello_world:
002314A1  jmp         hello_world (0233660h) 
```

约定： 调用函数（即main函数), 被调用函数(即hello_world函数)

在执行hello_world函数的第一条代码之前，各寄存器的状态如下：
- ebp 外部函数(即main函数)栈帧的栈底
- esp 外部函数(即main函数)栈帧的栈顶

main函数栈帧的栈顶将会成为hello_world函数的栈底，


```
void hello_world(int i) {
00233660  push        ebp  
00233661  mov         ebp,esp  
00233663  sub         esp,0C0h  
00233669  push        ebx  
0023366A  push        esi  
0023366B  push        edi  
0023366C  lea         edi,[ebp-0C0h]  
00233672  mov         ecx,30h  
00233677  mov         eax,0CCCCCCCCh  
0023367C  rep stos    dword ptr es:[edi]  
0023367E  mov         ecx,offset _B5E65A06_hellogame@cpp (023F008h)  
00233683  call        @__CheckForDebuggerJustMyCode@4 (02312CBh)  
	//std::cout << "Hello World!" << i << std::endl;
}
00233688  pop         edi  
00233689  pop         esi  
0023368A  pop         ebx  
0023368B  add         esp,0C0h  
00233691  cmp         ebp,esp  
00233693  call        __RTC_CheckEsp (02312DAh)  
00233698  mov         esp,ebp  
0023369A  pop         ebp  
0023369B  ret  
```

hello_world函数保存外部函数（main函数)的现场
```
void hello_world(int i) {
00233660  push        ebp  		; 保存外部函数栈帧的栈底指针
00233661  mov         ebp,esp  	; 设置当前函数(hello_world函数)栈帧的栈底指针为外部函数(main函数)栈帧的栈顶
00233663  sub         esp,0C0h  ; 
00233669  push        ebx  
0023366A  push        esi  
0023366B  push        edi 
```


c++ 类的反汇编

```c++
#include <iostream>
#include <stdio.h>
 
class AAA{
public:
    AAA(){}
    ~AAA(){}

    int get_a() { return a; }

private:
    int a;
};

AAA aaa;//全局变量
 
int main(int argc,char** argv)
{
    AAA test;
    int a = test.get_a();
    return 0;
}
```


构造函数和析构函数的反汇编
```
080485de <_ZN3AAAC1Ev>:
    AAA(){}
 80485de:       55                      push   ebp
 80485df:       89 e5                   mov    ebp,esp
 80485e1:       5d                      pop    ebp
 80485e2:       c3                      ret    
 80485e3:       90                      nop

080485e4 <_ZN3AAAD1Ev>:
    ~AAA(){}
 80485e4:       55                      push   ebp
 80485e5:       89 e5                   mov    ebp,esp
 80485e7:       5d                      pop    ebp
 80485e8:       c3                      ret    
 80485e9:       90                      nop

080485ea <_ZN3AAA5get_aEv>:
    int get_a() { return a; }
 80485ea:       55                      push   ebp
 80485eb:       89 e5                   mov    ebp,esp
 80485ed:       8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
 80485f0:       8b 00                   mov    eax,DWORD PTR [eax]
 80485f2:       5d                      pop    ebp
 80485f3:       c3                      ret    
 80485f4:       66 90                   xchg   ax,ax
 80485f6:       66 90                   xchg   ax,ax
 80485f8:       66 90                   xchg   ax,ax
 80485fa:       66 90                   xchg   ax,ax
 80485fc:       66 90                   xchg   ax,ax
 80485fe:       66 90                   xchg   ax,ax
```
在调用对象的方法时， 第一个参数默认为this指针， 通过调用


# 编译原理
- lexer: lexical analysis
- parser: AST(abstract syntax tree)