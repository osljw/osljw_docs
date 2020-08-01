# unreal

跑酷项目
https://www.youtube.com/watch?v=9qHRQF3YXZs&list=PLX2_v3fTeazrzhJcnEMvgpMPCghfy1H8p&index=3


# Actor 

- 骨骼网格物体 Actor
- 静态网格物体 Actor
- 
# Component

AttachToComponent



# PlayerController


关卡蓝图中获取对象
- GetPlayerController
- GetPlayerCharacter
  
关卡蓝图中动态生成对象
Spawn Actor from Class

# Static Mesh

StaicMesh - UStaticMesh
SkeletalMesh - UPhysicsAsset


人物和武器
https://www.bilibili.com/video/av28206952/

- 人物添加插槽

- 武器在人物插槽上的位置预览

- 武器添加碰撞

- 人物何时可以捡取武器， 射线碰撞，按键
  - Settings -> Project Settings -> Engine -> Collision -> Trace Channels 
  - SphereTraceByChannel 相机发射直线射线， 检测碰撞

- 拾取武器
  - AttachToComponent 武器绑定到人物的skeletal mesh component上

- 扔掉武器
  - DetachFromComponent 


# Character
# ThirdPersonCharacter （Blueprint Class)
- ThirdPersonCharacter （Blueprint Class)
  - CapsuleComponent
    - SkeletalMeshComponent
      - SkeletalMesh
      - Animation
      - Material

Input -> Bindings -> Action Mappings
PlayerInputCompo


宏（UHT, Unreal Header Tool进行解析）
UPROPERTY

UFUNCTION
  - BlueprintCallable


# 调试
- DrawDebugLine


# c++ 创建actor提供给unreal使用
https://docs.unrealengine.com/en-US/Programming/QuickStart/index.html


# unreal engine project
> 项目入口

Project Settings -> Maps & Modes

> GameInstance

全局对象，生存周期为整个进程, 进程启动时蓝图系统会自动生成该对象
Project Settings -> Maps & Modes -> Game Instance Class

> GameMode

只存在于服务器端， 
Project Settings -> Maps & Modes -> Default Game Mode


# 摄像机
set_active

# UE4 网络游戏

https://docs.unrealengine.com/en-US/Gameplay/Networking/Overview/index.html

- Actor Replication

1. 在c++ actor类的构造函数中调用
```
SetReplicates(true);
```
2. 在蓝图 actor类的属性设置中勾选Replicates
  
3. actor 设置为Replicates后， 只需要在服务器上进行spawn(服务器会通过网络的方式告知客户端也spawn相应的actor， 这是由UE4引擎自动完成的)， 可以通过ROLE_Authority来保证代码只运行在服务端
```
if (Role == ROLE_Authority) {
  GetWorld()->SpawnActor<AActor>(AActorClass, ...)
}
```
不设置replication时, spawn生成的actor只有本机可见，其他机器不可见  

将spawn的代码逻辑只需要在服务端执行, 可以将代码放置在UFUNCTION中, 客户端调用UFUNCTION包裹的函数时，
代码会在服务器上执行， 服务器自动将数据同步给客户端进行模拟

replicated actor可以通过Role可以判断是否只在服务器端执行

- Variable Replication

1. 使用UPROPERTY(Replicated)修饰变量
2. GetLifetimeReplicatedProps函数中使用DOREPLIFETIME宏配置变量

