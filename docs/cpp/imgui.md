
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


- ImGuiWindowSettings
  - 保存窗口信息，如位置，大小等

- ImDrawList

绘制三角形 （屏幕坐标， 三角形顶点为顺时针）
```
ImVec2 pos = ImGui::GetCursorScreenPos();
ImDrawList* list = ImGui::GetWindowDrawList();
list->AddTriangleFilled(pos, ImVec2(pos.x + 100, pos.y), ImVec2(pos.x + 100, pos.y + 100), IM_COL32(255, 0, 0, 255));
```

- ImDrawData
ImGui将所有的渲染数据保存在ImDrawData中
```
ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
```