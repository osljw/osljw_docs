
# 字体

加载中文字体
```
ImGuiIO& io = ImGui::GetIO(); (void)io;
io.Fonts->AddFontFromFileTTF("C:/Windows/fonts/simhei.ttf", 
    15.0f, 
    NULL, 
    io.Fonts->GetGlyphRangesChineseFull());
```

显示中文
```
ImGui::Text(u8"你好");
```

# 窗口
 

- ImGuiContext
  - imgui上下文，`ImGuiContext*   GImGui`全局变量， 非线程安全
- ImGuiWindow
  - `ImGui::Begin`调用CreateNewWindow来创建`ImGuiWindow`, 窗口名称hash得到ImGuiID
  - ImGuiContext维护`ImGuiID`到`ImGuiWindow`的映射

- ImGuiViewport
    - Each viewports hold their copy of ImDrawData
    - ImGui_ImplWin32_Init初始化
      - 绑定HWND到main_viewport
      - 调用ImGui_ImplWin32_InitPlatformInterface
        - 注册窗口类型`wcex.lpszClassName = _T("ImGui Platform");`
        - ImGuiPlatformIO的函数绑定

- ImGuiPlatformIO
  - Backend interface/functions