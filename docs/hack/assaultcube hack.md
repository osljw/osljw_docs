
# Inject DLL
- OpenProcess
- VirtualAllocEx
- WriteProcessMemory
- CreateRemoteThread
- 


# detour
https://github.com/microsoft/detours

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