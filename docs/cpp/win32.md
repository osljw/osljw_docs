
# win32 cpp

https://docs.microsoft.com/en-us/windows/win32/learnwin32/learn-to-program-for-windows

## 消息队列

- UI线程消息队列(Thread message queue)
    - 一个UI线程拥有一个消息队列
    - 一个UI线程可以创建多个窗口， 所有窗口共用UI线程的消息队列，每个窗口有相应的窗口过程函数（Window Procedure）
    - 从线程消息队列取消息并送到窗口过程函数，需要用户调用相应的API实现（消息循环）
    - 一个进程只能有一个UI线程
- 系统消息队列（system message queue）： 用户输入等事件会被操作系统内核存储到系统消息队列中， 操作系统有专门线程负责从系统消息队列中取出消息分发到创建UI的线程的消息队列中。


消息循环 
```c++
    MSG msg;
    while (::PeekMessage(&msg, NULL, 0U, 0U, PM_REMOVE))
    {
        ::TranslateMessage(&msg);
        ::DispatchMessage(&msg);
        if (msg.message == WM_QUIT)
            done = true;
    }
```
- TranslateMessage会翻译 WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, or WM_SYSKEYUP为virtual-key messages，不会影响其他类型的消息
- DispatchMessage会根据msg调用相应的Window Procedure窗口过程函数


## 基础概念

窗口类型 https://docs.microsoft.com/en-us/windows/win32/winmsg/window-features

# 集成imgui

1. 拷贝相应的头文件和源文件到imgui目录下
2. 解决方案中将imgui目录包含在项目中
3. 头文件引用路径如下
```
#include "imgui/imgui.h"
#include "imgui/imgui_impl_win32.h"
#include "imgui/imgui_impl_dx12.h"
#include <d3d12.h>
#include <dxgi1_4.h>

#pragma comment(lib, "dxgi.lib")
#pragma comment(lib, "d3d12.lib")
```

## win32 封装imgui
- imgui初始化需要一个窗口HWND， 应用程序先初始化一个透明窗口，在这个窗口上对imgui进行初始化
- imgui在初始化win32时， `ImGui_ImplWin32_Init`函数调用`ImGui_ImplWin32_InitPlatformInterface`会注册窗口类，设置窗口过程函数为`ImGui_ImplWin32_WndProcHandler_PlatformWindow`


# win32 console debug

通过控制台显示调试信息
```c++
DebugConsole::DebugConsole(bool open): open(open) {
	if (!open) return;

	AllocConsole();
	freopen_s(&pCout, "conout$", "w+t", stdout); 
	freopen_s(&pIn, "conin$", "r+t", stdin);
}

DebugConsole::~DebugConsole() {
	if (!open) return;
	fclose(pIn);
	fclose(pCout);
	FreeConsole();
}
```

WndProc中cout无法输出， 可以在WndProc中调用`static DebugConsole dc(true);`初始化console


# win32 无边框 

创建窗口, 使用WS_POPUP创建pop-up window，并设置窗口位置和大小
```
hWnd = CreateWindowW(
	szWindowClass, 
	szTitle, 
	WS_POPUP,
	//CW_USEDEFAULT, 0, 
	200, 200,
	//CW_USEDEFAULT, 0, 
	600, 400,
	nullptr, nullptr, hInstance, nullptr);
```

注册窗口类时，不要设置菜单
```
WNDCLASSEXW wcex;
wcex.lpszMenuName = NULL;
```

# win32 置顶窗口
使用CreateWindowEx创建窗口， 设置WS_EX_TOPMOST风格
```
hWnd = CreateWindowEx(
	WS_EX_TOPMOST,
	szWindowClass,
	szTitle,
	WS_POPUP,
	200, 200,
	20, 20,
	nullptr, nullptr, hInstance, nullptr
);
```

#  win32 透明窗口（client area） 点击穿透（click through）

透明窗口（client area）实现： 注册窗口类时， 设置hbrBackground为NULL
```
WNDCLASSEXW wcex;
wcex.hbrBackground = 0;
```
本质： 没有使用背景颜色填充窗口的client area， client area矩形还是存在的

点击穿透（click through）实现： `WS_EX_LAYERED | WS_EX_TRANSPARENT`实现
```
hWnd = CreateWindowEx(
    WS_EX_TOPMOST | WS_EX_LAYERED | WS_EX_TRANSPARENT,
    szWindowClass,
    szTitle,
    WS_POPUP,
    200, 200,600, 400,
    //0, 0, GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN),
    nullptr, nullptr, hInstance, nullptr
);
```
WS_EX_TRANSPARENT
    - hit-test transparent, 需要配合WS_EX_LAYERED使用
    - 同进程的窗口绘制时，优先绘制没有WS_EX_TRANSPARENT属性的窗口

WS_EX_LAYERED
    - 会导致窗口接收不到WM_PAINT消息, 需要使用UpdateLayeredWindow来更新窗口


```c++
RECT wndRect;
::GetWindowRect(hWnd, &wndRect);
SIZE wndSize = {
    wndRect.right - wndRect.left,
    wndRect.bottom - wndRect.top
};
HBITMAP memBitmap = ::CreateCompatibleBitmap(hdc, wndSize.cx, wndSize.cy);

HDC memDC = ::CreateCompatibleDC(NULL);
HGDIOBJ original = SelectObject(memDC, memBitmap);

Gdiplus::Graphics graphics(memDC);
graphics.DrawImage(image, 0, 0, wndSize.cx, wndSize.cy);

// WM_PAINT 可以使用BitBlt拷贝
//BitBlt(hdc, 0, 0, wndSize.cx, wndSize.cy, memDC, 0, 0, SRCCOPY);

BLENDFUNCTION blend = { 0 };
blend.BlendOp = AC_SRC_OVER;
blend.SourceConstantAlpha = 255;
blend.AlphaFormat = AC_SRC_ALPHA;
//POINT ptPos = { wndRect.left, wndRect.top };
//POINT ptPos = { , 0 };
SIZE sizeWnd = { wndSize.cx, wndSize.cy };
POINT ptSrc = { 0, 0 };
UpdateLayeredWindow(hWnd, hdc, NULL, &sizeWnd, memDC, &ptSrc, 0, &blend, ULW_ALPHA);

ShowWindow(hWnd, nCmdShow);
UpdateWindow(hWnd);
```


# win32 Tray 托盘图标

1. NOTIFYICONDATA.hWnd设置TRAY所要绑定的窗口
2. NOTIFYICONDATA.uFlags中设置NIF_MESSAGE后， 系统才会向Tray所在的窗口消息队列发送MESSAGE
3. NOTIFYICONDATA.uCallbackMessage 设置自定义消息， 当用户在Tray图标上交互时，系统会将该消息投递到Tray所在的窗口消息队列
4. NOTIFYICONDATA.hWnd窗口的WndProc负责处理消息

```c++
#define WM_TRAY (WM_USER + 0x100)

class Tray
{
public:
	Tray(HINSTANCE hInst, HWND hWnd);
	~Tray();

private:
	NOTIFYICONDATA nid;
};

Tray::Tray(HINSTANCE hInst, HWND hWnd) {

	nid.uVersion = NOTIFYICON_VERSION_4;

	nid.cbSize = sizeof(nid);
	nid.hWnd = hWnd;
	nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;

	// This text will be shown as the icon's tooltip.
	StringCchCopy(nid.szTip, ARRAYSIZE(nid.szTip), L"Test application");

	// Load the icon for high DPI.
	nid.hIcon = LoadIcon(hInst, MAKEINTRESOURCE(IDI_TRAY));
	nid.uCallbackMessage = WM_TRAY;
	std::cout << "WM_TRAY =========== " << WM_TRAY << std::endl;

	// Add the icon
	Shell_NotifyIcon(NIM_ADD, &nid);
	// Set the version
	Shell_NotifyIcon(NIM_SETVERSION, &nid);
}

Tray::~Tray() {
	Shell_NotifyIcon(NIM_DELETE, &nid);
}
```

窗口消息处理函数中，建立Tray的菜单，和
```c++
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    {
        case WM_TRAY:
        {
            int wmId = LOWORD(lParam);
            switch (wmId) {
                case WM_RBUTTONDOWN:
                {
                    POINT pt;
                    GetCursorPos(&pt);
                    HMENU hMenu;
                    hMenu = CreatePopupMenu();
                    AppendMenu(hMenu, MF_STRING, 1234, TEXT("显示"));
                    AppendMenu(hMenu, MF_STRING, 2, TEXT("退出"));
                    TrackPopupMenu(hMenu, TPM_LEFTBUTTON, pt.x, pt.y, NULL, hWnd, NULL);
                    break;
                }
                default:
                    break;
             }
        }
        break;
        case WM_COMMAND:
        {
            int wmId = LOWORD(wParam);
            // 分析菜单选择:
            switch (wmId)
            {
            case 1234:
            {
                std::cout << std::endl;
                std::cout << "msg123456: =======" << std::endl;
            }
            break;
            default:
                return DefWindowProc(hWnd, message, wParam, lParam);
            }
        }
        break;
        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            // TODO: 在此处添加使用 hdc 的任何绘图代码...
            //FillRect(hdc, &ps.rcPaint, (HBRUSH)(COLOR_GRAYTEXT + 1));
            EndPaint(hWnd, &ps);
        }
        break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
    }

}
```

# win32 打包

在 Visual Studio 中将应用打包为 MSIX https://docs.microsoft.com/zh-cn/windows/msix/desktop/vs-package-overview

- 创建项目： Windows应用程序打包项目
- 应用程序引用源码工程


打包为安装包
- vs安装扩展插件：Microsoft Visual Studio Installer Projects 
- 新建项目：


# imgui multiple-viewports

multiple-viewports实现 https://greich.com/2019/03/02/imgui-multiple-viewports/


# D3D

DXGI： DirectX Graphics Infrastructure （图像基础设施，与硬件交互的抽象）

backbuffer-> RTV(render target view) -> pipeline



Present之前的数据 RGB ？  RGBA？， dxgi的swapchain


## viewport

D3D12_VIEWPORT 视口的形状描述


## shader（着色）

- vertex-shader （per-vertex operations）
  - transformations
  - skinning
  - morphing


## texture 

- D3D texture
    - SRV 只读
    - RTV 可写

mipmaps： 贴图

LOD (level-of-detail) 

# 渲染

application stage -> geometry stage -> 

## 几何阶段

- 顶点计算： 坐标转换， 模型坐标系->世界坐标系->摄影坐标系
- 投影： 正交投影（Orthographic）， 透视投影（Perspective ）
  - Perspective投影： 近大远小，齐次坐标（带深度）
- 裁剪：只有裁剪出来的部分才能进行光栅化处理
- 屏幕映射： 3D坐标 -> 屏幕2D坐标 

## 光栅化阶段



## 录屏
https://gist.github.com/mmozeiko/80989aa8f46901b2d7a323f3f3165790



# win32 序列号

serial number
- 获取序列号
    - 序列号如何生成
- 通过序列号获取license.dat文件



# windows 虚拟内存

虚拟内存也称为分页文件，也就是C:\pagefile.sys文件(隐藏文件)

查看虚拟内存情况
```
systeminfo
```

任务管理器中显示的`已提交 7.0/28.0 GB`, 前者表示虚拟内存使用中，后者表示虚拟内存最大值

虚拟内存最大值 = 物理内存容量 + 分页文件（C:\pagefile.sys）大小

设置虚拟内存, 系统属性 -> 高级 -> 性能 -> 设置 -> 高级