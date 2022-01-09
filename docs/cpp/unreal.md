# unreal

Unreal Engine 5 Beginner Tutorial - UE5 Starter Course!
https://www.youtube.com/watch?v=gQmiqmxJMtA&list=PLKPWwh_viQMGQkQfKKD5lF96efA3_RWt-

跑酷项目
https://www.youtube.com/watch?v=9qHRQF3YXZs&list=PLX2_v3fTeazrzhJcnEMvgpMPCghfy1H8p&index=3

# Gameplay Framework
https://www.tomlooman.com/ue4-gameplay-framework/

# Actor 

- 骨骼网格物体 Actor
- 静态网格物体 Actor


Actor的Role/RemoteRole属性

服务端：
Role == ROLE_Authority
RemoteRole == ROLE_SimulatedProxy || ROLE_AutonomousProxy

客户端：
Role == ROLE_SimulatedProxy || ROLE_AutonomousProxy
RemoteRole == ROLE_Authority



# ActorComponent

AttachToComponent

UActorComponent
  - UActorComponent （无形状）
    - USceneComponent （有位置， 无形状）
      - UPrimitiveComponent

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

-  AGameModeBase::PreLogin  是否接受客户端的加入地图
-  AGameModeBase::Login 为玩家创建PlayerController
-  AGameModeBase::PostLogin

GameModeBase 中的SpawnDefaultPawnAtTransform为玩家创建Pawn

GameMode 仅存在于服务器端



GameState 存储服务端和客户端恭喜的全局信息
- 连接游戏的玩家



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

- 人物skeleton mesh添加插槽, 武器在人物插槽上的位置预览和调整位置

- 在人物（pawn）创建后（AGameMode::RestartPlayer)或者BeginPlay时SpawnActor创建武器，并AttachActorToComponent到人物上, 设置socket name

- 武器添加碰撞

- 人物何时可以捡取武器， 射线碰撞，按键
  - Settings -> Project Settings -> Engine -> Collision -> Trace Channels 
  - SphereTraceByChannel 相机发射直线射线， 检测碰撞

- 拾取武器
  - AttachToComponent 武器绑定到人物的skeletal mesh component上

- 扔掉武器
  - DetachFromComponent 


# 碰撞系统 和 物理模拟
- FCollisionQueryParams
  - AddIgnoredActor 碰撞忽略的Actor
  - bTraceComplex = true 碰撞情况捕捉更加精细

- FHitResult 碰撞结果
- GetWorld()->LineTraceSingleByChannel 直线碰撞


被物理力作用的Static Mesh
- Physics -> Simulate Physics  (true)
- Collision -> Generate Overlay Events (true)

如何施加力
- Add Force
- Add Radial Force 


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


CharacterBP
  - CharacterMesh (绑定人物mesh)
  - Animation (绑定人物动画蓝图BP)


1. mixamo 获取人物（mesh 和 skeleton）
2. mixamo 人物Retarget
   1. select Rig： humanoid
   2. source -> target 骨架映射
3. 已有人物skeleton上 select Rig： humanoid
4. 已有动画蓝图（Animation Blueprint）上 Retarget Anim
5. CharacterBP上绑定迁移好的skeleton 和 动画蓝图
6. 工程设置中， default pawn 使用新的CharacterBP



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


## 伤害过程

Actor 自定义事件，接收伤害数值 

通过碰撞事件获取到处于overlay的Actor， 调用Actor的承伤函数


## 死亡模拟
- CharacterMesh
  - Set Simulate Physics
    - Set Collision Profile Name (Ragdoll)


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

将spawn的代码逻辑只需要在服务端执行, 可以将代码放置在UFUNCTION中, 客户端调用UFUNCTION包裹的函数时(会进行RPC请求），
代码会在服务器上执行， 服务器自动将数据同步给客户端进行模拟

replicated actor可以通过Role可以判断是否只在服务器端执行

- Variable Replication

1. 头文件中使用UPROPERTY(Replicated)修饰变量
2. 源文件中#include "Net/UnrealNetwork.h"
3. 源文件中GetLifetimeReplicatedProps函数中使用DOREPLIFETIME宏配置变量


- Event Replication
  - Multicast
  - Run on Server (replicate event from client to server)
  - Run on owning Client （replicate event from server to owning client）


# 动画系统

Animation Essentials - Unreal Engine 4 Course

https://www.youtube.com/playlist?list=PLL0cLF8gjBpqpCGt9ayn4Ip1p6kvgXYi2


动画重定向 retarget
https://www.youtube.com/watch?v=92rag3qStI4


skeleton (人体结构)
  - skeleton tree
    - retarget （迁移动画）

mesh （人体皮肤） 

pyhsics（人体物理约束）


PoseAsset
  Curve

## 动画重定向（retarget）

- 一个带动画的skeleton A， 一个无动画的skeleton B， 将A的动画迁移到B
- 原理： 将A和B的skeleton 映射对齐， 就能将A的动画自动迁移到B上
- 在A的Retarget Manager界面中， Select Rig -> Select Humanoid Rig,  相当于将A的skeleton和标准skeleton对齐
- 在B的Retarget Manager界面中， Select Rig -> Select Humanoid Rig,  相当于将B的skeleton和标准skeleton对齐
- 在A的动画蓝图（Animation Blueprint）上执行Retarget Anim Blueprints，  选择Target 为B， 就能为B生成动画蓝图了


常驻动画（如奔跑， 跳跃） 用状态机进行控制


- play montage （在动画不同时机执行不同程序）
- play anim montage 
- paly Animation


1. 人物蓝图， 按键事件， play montage
2. 拔枪动画，创建动画蒙太奇montage， 
3. 动画蓝图， 新增Anim slot，
4. 拔枪动画选择3中新增的slot
5. 动画蓝图输出， 


6. layered blend per bone 对骨架的不同部分进行动画混合

保存状态机输出pose： default pose -> cached default pose
构建上肢动画： cache default pose -> upper slot -> upper pose
混合： base pose 使用cached default pose， pose 0 使用upper pose, layer setup中对base pose设置过滤条件branch filter（ 设置的bone表示不要修改该bone下对应的动画）


## additive anim 叠加动画
- zero pose 
- additive Anim Type： Mesh space
- 

# UI系统
- create widget
- add to viewport
- set show mouse cursor


Actor添加Widget组件， 可以将ui和Actor进行绑定
Pawn添加Widget Interaction组件， 通过Get Hit Result Under Cursor by Channel获取用户点击位置，  用Find look at Rotation计算出旋转角度， 调整Widget Interaction组件的旋转来指向点击位置


# 材质(Materials)

材质编辑器构建材质， 对应High-Level Shading Language(HLSL)代码


Texture Sample

Material Function
Material Blend


- 材质混合 
- Use good Texture
- Use Macro Variation (对T_MacroVariation纹理使用多种不同的uv， 控制和改变目标纹理）
- Use Distance Blend （以玩家为中心， startoffset(eg. -2000)， Blend Range（边界模糊 eg：10000）distance blend输出为alpha，  近处使用细节纹理， 远处使用粗糙纹理）
- Use BlendMaterialAttributes(使用Perlin noise纹理作为alpha控制多个纹理的混合， 例如草地和泥土的混合)



# 光源(Light) 和 视觉效果（Visual Effects）

- 点光源 (如灯泡)
- 聚光源
- 定向光源(Directional Ligh)
  -  大气太阳光（Atmosphere Sun Light）
     - SkyAtmosphere (天空半球变蓝)
     - ExponentialHeightFog(使用雾填充天空和地图的黑色间隙)
     - project setting -> support sky atmosphere affecting heightfog (太阳降落后，天空变黑)
     - sky light (天光反射)


# 蓝图 （blueprint）
- 关卡蓝图 （level blueprint）
  - BeginPlay
  - Character (actor blueprint)


# landscape

left mouse： 凸起
shift + left mouse： 凹陷


# unreal c++ doc
1. 编程和脚本编写 > 编程指南 > 编程快速入门 (C++ Actor)
https://docs.unrealengine.com/4.27/zh-CN/ProgrammingAndScripting/ProgrammingWithCPP/CPPProgrammingQuickStart/

2. 编程和脚本编写 > 编程指南 > C++ 编程教程 > 游戏控制的摄像机 ()


# online subsystem steam

-  Edit->plugins: enable online subsystem steam
-  工程文件夹下， 右击工程文件launch game



# 游戏分类

- MMO （massively multiplayer online）大型多人在线
- RPG（role-playing game） 角色扮演游戏



# Blueprint 和 c++ 协作

- c++ 使用 Blueprint中定义的类型， 在cpp头文件中声明TSubclassOf<AAtor>类型变量， 并公开到蓝图进行编辑