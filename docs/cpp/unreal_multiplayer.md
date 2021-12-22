

# 服务器模式

- Listen Server
- Delicated Server


# 多关卡切换
GameInstance 负责ui界面的创建和变量保存

Open Level 时， 调用GameInstance的方法来初始化UI

Execute console cmd
servertravel /Game/Maps/MapName

class setting -> use seamless travel

通过使用travel level作为缓冲， 可以立即回收内存， 减少内存消耗
```
old big level -> travel level -> new big level
```

# 网络系统
- Replication
  - Replicated
  - RepNotify （会创建一个函数， 当变量改变时调用这个函数）

- 服务端
  - 创建服务 -> Create Session -> Open Level
- 客户端
  - 搜索服务 -> Session Result -> 加入服务 ->  Join Session

Create Session
    - 设置玩家数量
    - 设置PlayerController

Open Level
    - Options 设置为listen （ Listen Server模式下， 以listen方式打开服务器地图）


## 网路错误处理
- Event NetworkError
- Event TravelError

# 数据持久化
- SaveGame 类
  - 保存
    - create SaveGame Object
    - 保存信息到SaveGame对象中
    - save game to slot （对象会被保存到工程目录Saved/SaveGame目录下）
  - 恢复
    - load game from slot

# 角色系统

- 角色基类，继承关系
- 动画重定向
    - 播放动画PlayAnimation

BP Structure 维护玩家信息
- PlayerName Text 玩家名称
- PlayerImage Texture2D 玩家头像
- PlayerCharacter ClassReference 玩家角色

# 聊天系统