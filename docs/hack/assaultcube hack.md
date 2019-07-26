
# Inject DLL
- OpenProcess
- VirtualAllocEx
- WriteProcessMemory
- GetProcAddress
- CreateRemoteThread


# Cheat Engine
- scan type 和 value type 需要匹配， 例如扫描decreased value时，double类型的不能选择float类型
- Code finder， Find what accesses this address
- Code Injection

Find what accesses this address
===============================
CE 默认使用硬件断点的方式，断点只能停在指令执行之后

> 1. 通过值扫描， 找到变量的地址为：0x0184F7D0

![](media/1.png)

> 2. 一级指针，寻找指向0x0184F7D0地址的指针

Find what accesses this address，调试器附加到进程上，

找到使用这个地址的汇编指令，即汇编指令中地址计算后为0x0184F7D0的指令，

![](media/2.png)

图片显示的是mov [esi+18],eax 指令刚执行结束时的信息， esi寄存器的值为0x0184F7B8， 加上偏移量18后为地址0x0184F7D0，这说明存储0x0184F7B8这个值的地址处是个指针， 因此需要扫描0x0184F7B8这个值，获得一级指针
```
0042626C - mov [esi+18],eax

Probable base pointer =0184F7B8

ESI=0184F7B8
```
获得一级指针地址为0x017C5B58， 该地址处的value为0x0184F7B8加上偏移量18后，就得到变量0x0184F7D0

![](media/3.png)

> 3. 二级指针， 寻找指向0x017C5B58地址的指针

在地址0x017C5B58上，Find what accesses this address

![](media/4.png)

此时mov esi,[esi]指令执行结束，esi寄存器存储的是0x0184F7B8，可以查看在其之前的cmp dword ptr [esi],00指令，获得mov esi,[esi]指令运行之前esi寄存器的值为0x017C5B58，因此可以通过扫描0x017C5B58获得二级指针

![](media/5.png)

```
ESI=017C5B58

Probable base pointer =017C5B58

0042622A - cmp dword ptr [esi],00
0042622D - je 00426285
0042622F - mov esi,[esi]
```

二级指针为0x0184F6AC，该地址处value为0x017C5B58，加上偏移量0，就得到一级指针地址0x017C5B58
> 3. 三级指针, 寻找指向0x0184F6AC地址的指针

![](media/6.png)

mov esi, [esi+14]该指令中的esi+14为地址0x0184F6AC， 故该指令执行前esi为0x0184F698，扫描这个值可获得三级指针的地址， 这里扫描这个值会得到两个地址都存储这个值， 分别在这两个地址上使用what accesses this address，哪个地址有相应的汇编代码，哪个地址就为真正的三级指针，这里最后确认为0x017A139C

三级指针为0x0183282C， 该地址处value为0x0184F698，加上偏移量14，就得到二级指针地址0x0184F6AC

> 4. 四级指针，寻找指向0x0183282C地址的指针

![](media/8.png)

mov esi,[esi+0C] 指令中的esi+0C计算后为0x0183282C（只有计算后为这个地址才会定位到这个指令)，故esi的值为0x01832820， 扫描这个值可获得四级指针的地址为"Tutorial-i386.exe"+201660 = 00601660

![](media/9.png)

![](media/10.png)


# detour
https://github.com/microsoft/detours

编译工具： 
- visual studio 2017

编译方法：
- File -> New -> Project From existing Code
- 选择extern build
- build cmd： nmake
- clean cmd： nmake clean

编译结果：
- include目录为头文件
- lib.X86目录为dll文件

# 
- Aimbot 自动瞄准
- Voice Spam 
- Quick Grenade 快速手雷
- Mass Kill 大规模杀伤
- Entity Magnet
- Player ESP 人物感知（透视）

# detour
jmp指令的二进制指令位0xe9

nop指令为0x90

- 分配内存VirtualAlloc 
- 拷贝原函数到新分配的内存上memcpy， 制作跳板程序
- 修改原函数所在内存为可写，VirtualProtect

Trampoline 程序

将原来的目标函数， 拷贝到Trampoline 程序,

紧随其后为5字节的jmp指令，跳转到原来的目标函数

目标函数

开头第一条修改为jmp指令， 跳转到detour之后的新函数 （jmp 指令占用5字节）

新函数

实现功能程序后， jmp到Trampoline 程序， 

```
// pLocation - Target函数的地址
// pDetour - Detour函数的地址
// dwLength - Target函数的备份长度（需要大于等于5字节，且构成完整的汇编指令长度)
void *DetourFunction( void *pLocation, void *pDetour, DWORD dwLength ) {
	// 构造Trampoline程序 
	// 构造Trampoline程序，1. 分配内存， 大小为Target函数的备份长度, 加上5字节的jmp指令用于跳转回Target函数
	void *pTrampoline = VirtualAlloc( NULL, dwLength + 5, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE );
	// 构造Trampoline程序，2. 拷贝Target函数的备份长度到Trampoline程序
	memcpy( pTrampoline, pLocation, dwLength );
	// 构造Trampoline程序，3. 设置5字节的jmp跳转指令， 用于跳转回Target函数未备份的指令
	*reinterpret_cast< BYTE* >( reinterpret_cast< DWORD >( pTrampoline ) + dwLength ) = 0xE9;
	*reinterpret_cast< DWORD* >( reinterpret_cast< DWORD >( pTrampoline ) + dwLength + 1 ) = reinterpret_cast< DWORD >( pLocation ) - ( reinterpret_cast< DWORD >( pTrampoline ) + dwLength );

	// 修改Target函数
	// 修改Target函数, 1. 设置修改Target函数的备份长度所在内存为可读写
	DWORD dwOldProtection = NULL;
	VirtualProtect( pLocation, dwLength, PAGE_EXECUTE_READWRITE, &dwOldProtection );
	// 修改Target函数, 2. 设置修改Target函数的前5字节为jmp指令， 跳转到Detour函数
	*reinterpret_cast< BYTE* >( reinterpret_cast< DWORD >( pLocation ) ) = 0xE9;
	*reinterpret_cast< DWORD* >( reinterpret_cast< DWORD >( pLocation ) + 1 ) = reinterpret_cast< DWORD >( pDetour ) - ( reinterpret_cast< DWORD >( pLocation ) + 5 );
	// 修改Target函数, 3. 设置修改Target函数的其余备份长度为Nop指令
	for( size_t i = 5; i < dwLength; i++ )
		*reinterpret_cast< BYTE* >( reinterpret_cast< DWORD >( pLocation ) + i ) = 0x90;
	// 修改Target函数, 3. 设置修改Target函数的其余备份长度为Nop指令
	VirtualProtect( pLocation, dwLength, dwOldProtection, NULL );

	// 返回Trampoline程序的地址，可以记录到全局变量中，给Detour函数进行调用
	return pTrampoline;
}
```

# main

入口函数DllMain

AssaultCube Hack\Main.cpp
```c++
DWORD WINAPI MainThread( LPVOID lpParameter ) {
	//Hook an ingame function so we won't get conflicts with differnt opengl.dll versions, I used to hook wglSwapBuffers before

    // 初始化菜单
	OnInitialize( );

    // 
	dwDrawHudJmpBack = reinterpret_cast< DWORD >( Utils::DetourFunction( reinterpret_cast< void* >( OFFSET_GL_DRAWHUD_MIDFUNC ), gl_DrawHud, 13 ) );

	return EXIT_SUCCESS;
}

//Dll Entry Point
BOOL WINAPI DllMain( HMODULE hModule, DWORD dwReason, LPVOID lpReserved ) {
	if( dwReason == DLL_PROCESS_ATTACH ) {
		CreateThread( 0, 0, MainThread, 0, 0, 0 );
	}

	return TRUE;
}
```

hook函数， 如何获得被hook函数的地址， hook的函数如何编写

AssaultCube Hack\Hooks.cpp
```c++
#include "Hooks.h"
#include "HackMain.h"

#include <GL/GL.h>
#pragma comment( lib, "OPENGL32.lib" )

void PreRenderFrame( )
{
	glPushMatrix( );

	glEnable( GL_BLEND );
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );

	GLint viewport[4];
	glGetIntegerv( GL_VIEWPORT, viewport );

	glLoadIdentity( );
	glOrtho( 0, viewport[2], viewport[3], 0, 0, 1 );

	OnRenderFrame( );

	glPopMatrix( );

}

DWORD dwDrawHudJmpBack = NULL;

__declspec( naked ) void gl_DrawHud( ) //Mid-Function Hook, right at the end of the drawhud function
{
	__asm
	{
		call PreRenderFrame;

		//Original Code
		mov esi, glDisable;
		push GL_BLEND;
		call esi;

		jmp[dwDrawHudJmpBack];
	}
}
```
PreRenderFrame 函数调用GL库的函数进行绘制