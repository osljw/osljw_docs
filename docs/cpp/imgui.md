
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