
游戏入口 
Project Settings -> Maps & Modes
B_LyraGameMode 
LyraStarterGame/Content/B_LyraGameMode.uasset

编辑器默认关卡：LyraStarterGame/Content/System/DefaultEditorMap/L_DefaultEditorOverview.umap
游戏默认关卡： LyraStarterGame/Content/System/FrontEnd/Maps/L_LyraFrontEnd.umap


World Settings -> GameMode中设置关卡要使用的Experience
L_LyraFrontEnd的Experience为B_LyraFrontEnd_Experience
LyraStarterGame/Content/System/FrontEnd/B_LyraFrontEnd_Experience.uasset

UI加载：
B_LyraFrontEnd_Experience -> B_LyraFrontendStateComponent -> W_LyraFrontEnd

ULyraFrontendStateComponent继承自UGameStateComponent


背景加载：
LyraStarterGame/Content/Environments/B_LoadRandomLobbyBackground.uasset