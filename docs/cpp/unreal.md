# unreal

跑酷项目
https://www.youtube.com/watch?v=9qHRQF3YXZs&list=PLX2_v3fTeazrzhJcnEMvgpMPCghfy1H8p&index=3

# Gameplay Framework
https://www.tomlooman.com/ue4-gameplay-framework/

# Actor 

- 骨骼网格物体 Actor
- 静态网格物体 Actor
- 
# ActorComponent

AttachToComponent


# Pawn and Character 

交通工具， 战士，等通常用Pawn进行表示 

Character是Pawn的子类， 实现了SkeletalMesh和CharacterMovementComponent 


# PlayerController and PlayerState

人物，交通工具等用Pawn来呈现

PlayerController和Pawn为一对多的关系， PlayerController通过Process来绑定需要操作的Pawn



```c++
GetWorld()->GetPlayerControllerIterator() // GetWorld is available in any Actor instance
PlayerState->GetOwner() // owner of playerstate is of type PlayerController, you will need to cast it to PlayerController yourself.
Pawn->GetController() // Only set when the pawn is currently ‘possessed’ (ie. controlled) by a PlayerController.
```

客户端上仅有玩家自身对应的PlayerController， 没有其他玩家对应的PlayerController，因此PlayerController不适合
存储玩家的数据， 当想要访问其他玩家的数据时，可以使用PlayerState进行存储

关卡蓝图中获取对象
- GetPlayerController
- GetPlayerCharacter
  
关卡蓝图中动态生成对象
Spawn Actor from Class

# GameMode and GameStateBase

GameModeBase 中的Login()为玩家创建PlayerController

GameModeBase 中的SpawnDefaultPawnAtTransform为玩家创建Pawn

GameMode 仅存在于服务器端

# Static Mesh

StaicMesh - UStaticMesh
SkeletalMesh - UPhysicsAsset


# 武器系统 Weapon

Weapon 
- AAcotr
  - AWeapon （自定义武器类）
    - USkeletalMeshComponent （武器外形组件） 可以在编辑器中选择skeletal mesh进行绑定
    - GetOwner() 获取武器正在被谁持有
    - 


人物和武器
https://www.bilibili.com/video/av28206952/

- 构建武器AActor

- 人物添加插槽

- 武器在人物插槽上的位置预览和调整位置

- 在人物（pawn）创建后（AGameMode::RestartPlayer)或者BeginPlay时SpawnActor创建武器，并AttachToComponent到人物上

- 武器添加碰撞

- 人物何时可以捡取武器， 射线碰撞，按键
  - Settings -> Project Settings -> Engine -> Collision -> Trace Channels 
  - SphereTraceByChannel 相机发射直线射线， 检测碰撞

- 拾取武器
  - AttachToComponent 武器绑定到人物的skeletal mesh component上

- 扔掉武器
  - DetachFromComponent 


# 碰撞系统
- FCollisionQueryParams
  - AddIgnoredActor 碰撞忽略的Actor
  - bTraceComplex = true 碰撞情况捕捉更加精细

- FHitResult 碰撞结果
- GetWorld()->LineTraceSingleByChannel 直线碰撞

# 伤害系统
- TSubclassOf<UDamageType> 伤害类型
- UGameplayStatics::ApplyPointDamage 点伤害

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

  - Client: 函数在Server上调用, 在Client上执行
  - Server :  函数在Client上调用, 在Server上执行
  - NetMulticast： 函数在Server上调用， 在Server和所有Client上都会执行

  - Reliable 
  - BlueprintCallable

Connection ownership

Actor 拥有Connection，  connection和PlayerController一一对应，一个Actor最外层对应的PlayerController决定了
该Actor的Connection
https://docs.unrealengine.com/en-US/Gameplay/Networking/Actors/OwningConnections/index.html


# 调试
- DrawDebugLine


# c++ 创建actor提供给unreal使用
https://docs.unrealengine.com/en-US/Programming/QuickStart/index.html


# unreal engine project
> 项目入口

Project Settings -> Maps & Modes -> Default Maps 设置游戏启动时的第一个关卡

关卡蓝图的Event BeginPlay事件中， 使用Create Widget创建UI中的Widget Blueprint

Widget Blueprint的Designer界面负责设计UI, Graph界面负责逻辑代码， Button的Events中关联事件，
使用Open Level打开游戏地图关卡

地图关卡设计界面 Window > World Settings 中可以设置每个关卡自己的Game Mode，未设置时使用的是Project Settings中设置的Game Mode
Game Mode 负责处理玩家的生成， 在Player Start出生成玩家(Character)， 
AGameMode::RestartPlayer(class AController* NewPlayer)负责玩家的出生过程
https://www.bilibili.com/video/BV1pb41177pn?p=84 （085 Replicate Weapon Code Part 1）

Character的BeginPlay被调用， 在Character中创建武器时， 只需要在服务器端执行SpawnActor的代码， 并把武器类设置为Replicate和
把Character中保存的武器生成后变量设置为replicated。
这样多个客户端都能看到武器并通过变量操作武器


Edit > Project Settings > Input 输入



> GameInstance

全局对象，生存周期为整个进程, 进程启动时蓝图系统会自动生成该对象
Project Settings -> Maps & Modes -> Game Instance Class

> GameMode

只存在于服务器端， 
Project Settings -> Maps & Modes -> Default Game Mode

> Package

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

1. 头文件中使用UPROPERTY(Replicated)修饰变量
2. 源文件中#include "Net/UnrealNetwork.h"
3. 源文件中GetLifetimeReplicatedProps函数中使用DOREPLIFETIME宏配置变量


# 动画系统

Animation Essentials - Unreal Engine 4 Course

https://www.youtube.com/playlist?list=PLL0cLF8gjBpqpCGt9ayn4Ip1p6kvgXYi2


