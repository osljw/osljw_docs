- [unreal](#unreal)
- [编辑器](#编辑器)
- [Gameplay Framework](#gameplay-framework)
  - [Actor](#actor)
  - [ActorComponent](#actorcomponent)
  - [Pawn and Character](#pawn-and-character)
  - [PlayerController and PlayerState](#playercontroller-and-playerstate)
  - [GameMode and GameStateBase](#gamemode-and-gamestatebase)
  - [Static Mesh](#static-mesh)
- [武器系统 Weapon](#武器系统-weapon)
  - [拾取武器](#拾取武器)
  - [伤害系统](#伤害系统)
  - [瞄准](#瞄准)
- [碰撞系统](#碰撞系统)
- [碰撞系统 和 物理模拟](#碰撞系统-和-物理模拟)
- [人物系统 Character](#人物系统-character)
  - [移动](#移动)
  - [伤害系统](#伤害系统-1)
  - [ThirdPersonCharacter （Blueprint Class)](#thirdpersoncharacter-blueprint-class)
  - [人物骨架](#人物骨架)
  - [换装系统](#换装系统)
  - [伤害过程](#伤害过程)
  - [死亡模拟](#死亡模拟)
- [调试](#调试)
  - [Debug Console Variable](#debug-console-variable)
- [c++ 创建actor提供给unreal使用](#c-创建actor提供给unreal使用)
- [unreal engine project](#unreal-engine-project)
- [摄像机](#摄像机)
- [UE4 网络游戏](#ue4-网络游戏)
  - [Actor Replication](#actor-replication)
  - [Variable Replication](#variable-replication)
  - [Event Replication](#event-replication)
  - [RPC](#rpc)
- [动画系统](#动画系统)
  - [动画重定向（retarget）](#动画重定向retarget)
  - [动画混合空间 （Blend Space)](#动画混合空间-blend-space)
  - [动画蒙太奇 （Animation Montage）](#动画蒙太奇-animation-montage)
  - [逆向运动学（Inverse Kinematics）  IK vs FK](#逆向运动学inverse-kinematics--ik-vs-fk)
    - [动画坐标空间](#动画坐标空间)
  - [Aim Offset 瞄准偏移](#aim-offset-瞄准偏移)
  - [additive anim 叠加动画](#additive-anim-叠加动画)
  - [IK](#ik)
  - [two bone IK](#two-bone-ik)
- [UI系统](#ui系统)
- [材质(Materials)](#材质materials)
- [光源(Light) 和 视觉效果（Visual Effects）](#光源light-和-视觉效果visual-effects)
- [蓝图 （blueprint）](#蓝图-blueprint)
- [关卡环境设计](#关卡环境设计)
  - [相关课程](#相关课程)
- [unreal c++ doc](#unreal-c-doc)
- [online subsystem steam](#online-subsystem-steam)
- [游戏分类](#游戏分类)
- [游戏逻辑](#游戏逻辑)
  - [结束逻辑](#结束逻辑)
- [Blueprint 和 c++ 协作](#blueprint-和-c-协作)

# unreal

Unreal Engine 5 Beginner Tutorial - UE5 Starter Course!
https://www.youtube.com/watch?v=gQmiqmxJMtA&list=PLKPWwh_viQMGQkQfKKD5lF96efA3_RWt-

跑酷项目
https://www.youtube.com/watch?v=9qHRQF3YXZs&list=PLX2_v3fTeazrzhJcnEMvgpMPCghfy1H8p&index=3


# 编辑器

框选物体：  Ctrl + Alt + 鼠标左键
物体自由下落： End

分组： Ctrl + G， 解组：Shift +G 

# Gameplay Framework

https://www.tomlooman.com/ue4-gameplay-framework/

## Actor

- 骨骼网格物体 Actor
- 静态网格物体 Actor

Actor的Role/RemoteRole属性

服务端：
Role == ROLE_Authority
RemoteRole == ROLE_SimulatedProxy || ROLE_AutonomousProxy

客户端：
Role == ROLE_SimulatedProxy || ROLE_AutonomousProxy
RemoteRole == ROLE_Authority

## ActorComponent

AttachToComponent

UActorComponent

- UActorComponent （无形状）
  - USceneComponent （有位置， 无形状）
    - UPrimitiveComponent

## Pawn and Character

交通工具， 战士，等通常用Pawn进行表示

Character是Pawn的子类， 实现了SkeletalMesh和CharacterMovementComponent

## PlayerController and PlayerState

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

## GameMode and GameStateBase

- AGameModeBase::PreLogin  是否接受客户端的加入地图
- AGameModeBase::Login 为玩家创建PlayerController
- AGameModeBase::PostLogin

GameModeBase 中的SpawnDefaultPawnAtTransform为玩家创建Pawn

GameMode 仅存在于服务器端

GameState 存储服务端和客户端恭喜的全局信息

- 连接游戏的玩家

## Static Mesh

StaicMesh - UStaticMesh
SkeletalMesh - UPhysicsAsset

# 武器系统 Weapon

Weapon

- AAcotr
  - AWeapon （自定义武器类）
    - USkeletalMeshComponent （武器外形组件） 可以在编辑器中选择skeletal mesh进行绑定
    - GetOwner() 获取武器正在被谁持有
    - 

武器基类
  - 开火功能
    - 射击起点：相机位置GetWorldLocation
    - 射击终点：相机方向某一距离GetFowardVector
    - 检测起点和终点之间发生的碰撞：LineTraceByChannel
  - 总弹药量， 弹匣容量， 当前弹匣量


## 拾取武器

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

## 武器开火
- 人物Character扣动武器扳机， 因此在人物蓝图中设置按键输入事件
- Character蓝图通过set timer by event来模拟扣动扳机过程
  - time 参数可以用来模拟武器射速
  - looping 参数可以用来模拟武器是单点还是全自动

## 武器子弹
- 使用Actor创建实体 or 使用射线

使用结构体保存武器信息
- AmmoRounds 弹匣数
- 

## 伤害系统

- TSubclassOf `<UDamageType>` 伤害类型
- UGameplayStatics::ApplyPointDamage 点伤害

## 瞄准

获取瞄准方向，由pitch和yaw表达
GetAimBaseRotation
GetActorRotation

使用瞄准偏移Aim Offset 1D呈现动画


## 相关教程
https://www.bilibili.com/video/av28206952/
https://www.bilibili.com/video/BV1pb41177pn?p=27&vd_source=05b9e112882cf3fe738863375b088e4c

# 碰撞系统

# 碰撞系统 和 物理模拟

- FCollisionQueryParams

  - AddIgnoredActor 碰撞忽略的Actor
  - bTraceComplex = true 碰撞情况捕捉更加精细
- FHitResult 碰撞结果
- GetWorld()->LineTraceSingleByChannel 直线碰撞

# 人物系统 Character

被物理力作用的Static Mesh

- Physics -> Simulate Physics  (true)
- Collision -> Generate Overlay Events (true)

如何施加力

- Add Force
- Add Radial Force

## 移动和坐标系

- 大多数建模软件使用的是right-handed的坐标系统， UE选择的是left-handed坐标系
- unreal的人物模型在local object space一般都是朝向y轴正方向的， 在world space中一般会设置rotation z=270°， 让人物正面面向world space X轴正方向。

鼠标 -> Controller

鼠标移动影响的是Controller的Yaw和Pitch, 在人物Character中进行编程
- mouse turn right/left -> AddControllerYawInput
- mouse look up/down -> AddControllerPitchInput
- Pitch会被限制在[-90, 90], Yaw可以无限转动

Controller -> Camera
- 第三人称的FollowCamera组件通常使用Spring Arm Component
- Use Pawn Control Rotation 可以控制Controller和Camera的旋转变换进行同步

Camera -> Character
Character Class Defaults 中，Pawn是否使用Controller的Roll/Yaw/Pitch
- Use Controller Rotation Yaw 设置后可以让人物和Camera的相机的Yaw进行同步
- 用按键设置Use Controller Rotation Yaw的值可以实现自由转动视角和固定视角的切换


人物移动控制

- 移动方向与controller的roation相关， Get Forward/Right Vector
- Character Movement Component
  - 人物的行走， 跳跃/坠落相关属性设置
- 前后左右移动： AddMovementInput

  - Character->Pawn->Use Controller Rotation


### 8向移动方式

- Character类的Use Controller Rotation Yaw 设置为true
- Character Movement Component的Orient Rotation To Movement设置为false


## 伤害系统

- TSubclassOf `<UDamageType>` 伤害类型
- UGameplayStatics::ApplyPointDamage 点伤害

## ThirdPersonCharacter （Blueprint Class)

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


## 人物骨架

1. mixamo 获取人物（mesh 和 skeleton）
2. mixamo 人物Retarget
   1. select Rig： humanoid
   2. source -> target 骨架映射
3. 已有人物skeleton上 select Rig： humanoid
4. 已有动画蓝图（Animation Blueprint）上 Retarget Anim
5. CharacterBP上绑定迁移好的skeleton 和 动画蓝图
6. 工程设置中， default pawn 使用新的CharacterBP

---
|     |     |
| ------ | ------ |
| pelvis | 骨盆 |
| spine  | 脊柱 |
| thigh  | 大腿 |
| clavicle | 锁骨 |
|   |  |

- pelvis 上有三段spine
- 

## 换装系统

- set master pose component

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

## Debug Console Variable

```c++
int32 debug_switch=0;
FAutoConsoleVariableRef CVARDebug(TEXT("NameCate.NameVar"), debug_switch, TEXT("help info"), ECVF_Cheat)
```

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

## Actor Replication

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

## Variable Replication

应用场景示例： 客户端人物标识是否携带目标的变量， 需要客户端同步该变量到服务器以判断游戏是否结束

1. 头文件中使用UPROPERTY(Replicated)修饰变量
2. 源文件中#include "Net/UnrealNetwork.h"
3. 源文件中GetLifetimeReplicatedProps函数中使用DOREPLIFETIME宏配置变量

控制同步方式， 以节省带宽

- DOREPLIFETIME_CONDITION
  - COND_OwnerOnly

## Event Replication

- Multicast
- Run on Server (replicate event from client to server)
- Run on owning Client （replicate event from server to owning client）

## RPC

UFUNCTION(Client): 函数在客户端执行，在服务端发起调用
UFUNCTION(Server): 函数在服务端执行，在客户端发起调用
UFUNCTION(NetMulticast): 函数在所有端执行， 在服务端发起调用

```
UFUNCTION(Server, Reliable, WithValidation)
```

- Reliable: 可靠调用
- WithValidation： 验证

# 动画系统



skeleton (人体结构)

- skeleton tree
  - retarget （迁移动画）

skeleton mesh （人体皮肤）

pyhsics（人体物理约束）

PoseAsset
  Curve

## 动画蓝图 （Animation Blueprint）
Character类 -> CharacterMesh -> Anim Class 给人物选择动画蓝图

- 动画蓝图（Animation Blueprint）
  - Event Graph (蓝图初始化和更新事件， 用于获取人物状态)
  - Anim Graph （Animation State Machine）用于评估当前帧的骨架网格体最终姿势


UE5 动画蓝图

设计动画蓝图基类， 不直接包含动画资产，而是用来混合动画（e.g. blending upper and lower body poses together）， 
- Linked Animation Layers
- Montages
优点： 可以实现只加载相关的动画， 例如当持有武器时，才加载武器相关的动画

改变：

- 动画蓝图基类不再使用Event Graph， 而是使用BlueprintThreadsafeUpdateAnimation 和 use the Property Access system to access data

- 动画蓝图基类 -> AnimGraph 定义状态机
- AnimLayerInterface定义状态接口


Lyra示例：

接口工具类
- 创建动画蓝图基类ABP_Mannequin_Base(Animation Blueprint)
- 创建ALI_ItemAnimLayers（AnimLayerInterface）
  - 动画蓝图基类ABP_Mannequin_Base的Class Setting中设置Interface
  - ABP_Mannequin_Base状态机中Interface和状态输出进行绑定

接口实现公共类
- 创建动画蓝图基类ABP_ItemAnimLayersBase(Animation Blueprint)
  - 动画蓝图基类ABP_ItemAnimLayersBase的Class Setting中实现ALI_ItemAnimLayers接口
  - 实现ALI_ItemAnimLayers中定义的接口
    - sequence player
    - set sequence with inertial blending
    - sequence参数设置成变量， 以便子类进行配置

接口实现具体类
- 创建ABP_ItemAnimLayersBase的子类ABP_UnarmedAnimLayers 
  - 可视化配置相应的动画

接口应用过程
- 人物蓝图的Mesh中设置动画蓝图ABP_Mannequin_Base
- 通过Mesh的Link Anim Class Layers绑定接口实现具体类ABP_UnarmedAnimLayers 

接口实现公共类（ABP_ItemAnimLayersBase）如何访问接口工具类（ABP_Mannequin_Base）的数据
- 在接口工具类（ABP_Mannequin_Base）中定义函数， 设置为纯函数（Pure）， 和线程安全
- 返回值设置为ReturnValue（这样才能在属性存取中显示）

## Lyra动画迁移
https://www.bilibili.com/video/BV1dT41157pS/?p=1&vd_source=05b9e112882cf3fe738863375b088e4c

https://www.bilibili.com/video/BV1Da411n71c/?spm_id_from=333.999.0.0&vd_source=05b9e112882cf3fe738863375b088e4c

- RootMotion
  - 不开启RootMotion： 人物会叠加actor的移动和动画的移动，导致人物和Camera不是固定距离
  - 开启RootMotion：实现原地奔跑的状态
  - 造成的问题： 奔跑速度和人物步幅不匹配
- Distance Matching （距离匹配）
  - Locomotion Library
  - 动画蓝图基类中计算人物当前帧和上一帧的移动距离，并导出到属性存取系统
  - 动画序列通过Locomotion Library插件的DistanceCurveModifier修饰符生成动画曲线（计算出动画本身的位移数据）
  - 使用序列求值器计算动画帧，通过Advance Time by Distance Matching计算位移到序列显示时间的映射
  - 两种方式实现距离匹配
    - 通过位移速度调整动画播放速率实现， 如奔跑循环动画。
    - 通过位移来调整显示时间实现， 如启动奔跑的加速过程。

## 动画重定向（retarget）

- 一个带动画的skeleton A， 一个无动画的skeleton B， 将A的动画迁移到B
- 原理： 将A和B的skeleton 映射对齐， 就能将A的动画自动迁移到B上
- 在A的Retarget Manager界面中， Select Rig -> Select Humanoid Rig,  相当于将A的skeleton和标准skeleton对齐
- 在B的Retarget Manager界面中， Select Rig -> Select Humanoid Rig,  相当于将B的skeleton和标准skeleton对齐
- 在A的动画蓝图（Animation Blueprint）上执行Retarget Anim Blueprints，  选择Target 为B， 就能为B生成动画蓝图了

## 兼容骨骼（Compatible Skeleton）
skeleton窗口 -> 窗口菜单(window) -> 资产详情（Asset Details） -> 添加兼容骨骼

## 动画混合空间 （Blend Space)

## 动画蒙太奇 （Animation Montage）

- Animation Sequence 右键可以创建Animation Montage
- Play Montage要借助Anim Slot才能播放， 在Anim Graph中添加Anim Slot， 在Montage中选择Slot后， Montage的pose才会在Anim Graph中生效， 通常还要使用Layered Blend Per Bone对Montage的动画进行混合。


- Play Montage (可以设置多个回调， Notify, Blend事件)
- Play Anim Montage


## 逆向运动学（Inverse Kinematics）  IK vs FK

使用IK调整动画

1. 在character中计算得到末端执行器的位置

### 动画坐标空间

1. 角色动画的计算发生在局部（Local)空间， 相对于骨骼的Root进行计算，
2. Final Animation Pose 也只能接收局部（Local)空间的数据
3. IK的计算

## Aim Offset 瞄准偏移
axis setting： pitch [-90, 90]
aim offset 本质上是asset，
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

## IK

## two bone IK

IK bone  要控制的目标关节

Effector Target （参照目标关节？）

Joint Target 关节点

例如：左手臂骨骼结构

- LeftShoulder （左肩膀）
  - LeftArm （左上臂）
    - LeftForeArm （左下臂）
      - LeftHand （左手）
      - 

 选择LeftHand为IK bone
 选择RightHand为Effector Target
 选择LeftForeArm为Joint Target

 ## 相关教程
Animation Essentials - Unreal Engine 4 Course

https://www.youtube.com/playlist?list=PLL0cLF8gjBpqpCGt9ayn4Ip1p6kvgXYi2

动画重定向 retarget
https://www.youtube.com/watch?v=92rag3qStI4

UE5 Lyra动画 https://www.bilibili.com/video/BV1X34y1p76u/?spm_id_from=333.999.0.0&vd_source=05b9e112882cf3fe738863375b088e4c

# UI系统

- create widget
- add to viewport
- set show mouse cursor

Actor添加Widget组件， 可以将ui和Actor进行绑定
Pawn添加Widget Interaction组件， 通过Get Hit Result Under Cursor by Channel获取用户点击位置，  用Find look at Rotation计算出旋转角度， 调整Widget Interaction组件的旋转来指向点击位置

- Overlay 分层布局， 如在背景图片之上添加新的UI

- TileView 列表视图，平铺相同的元素

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
  - 大气太阳光（Atmosphere Sun Light）
    - SkyAtmosphere (天空半球变蓝)
    - ExponentialHeightFog(使用雾填充天空和地图的黑色间隙)
    - project setting -> support sky atmosphere affecting heightfog (太阳降落后，天空变黑)
    - sky light (天光反射)

# 蓝图 （blueprint）

- 关卡蓝图 （level blueprint）
  - BeginPlay
  - Character (actor blueprint)

# 关卡环境设计

Blockout 草图


landscape

scale: 100 表示100cm即1m
Quad：1个quad表示长宽均为scale的方块， 默认即1平方米
section size： 63*63 quads  （一个section由64个quad构成）
sections per component： 1 * 1 sections
number of components： 8 * 8 （landscape可以看作一个Actor， Actor包含了多少个components）

left mouse： 凸起
shift + left mouse： 凹陷


landmass插件

## 相关课程
环境美术进阶技能 https://learn.unrealengine.com/course/3783977 

# unreal c++

## 官方文档doc
1. 编程和脚本编写 > 编程指南 > 编程快速入门 (C++ Actor)
   https://docs.unrealengine.com/4.27/zh-CN/ProgrammingAndScripting/ProgrammingWithCPP/CPPProgrammingQuickStart/
2. 编程和脚本编写 > 编程指南 > C++ 编程教程 > 游戏控制的摄像机 ()

## delegate

- 蓝图中绑定事件回调时 eg: OnSeePawn， 使用的是delegate
- C++中为`FSeePawnDelegate onSeePawn;`, 使用AddDynamic函数设置绑定

# online subsystem steam

1. Edit->plugins: enable online subsystem steam

2. Config/DefaultEngine.ini 中添加如下内容
```
[/Script/Engine.GameEngine]
+NetDriverDefinitions=(DefName="GameNetDriver",DriverClassName="OnlineSubsystemSteam.SteamNetDriver",DriverClassNameFallback="OnlineSubsystemUtils.IpNetDriver")

[OnlineSubsystem]
DefaultPlatformService=Steam

[OnlineSubsystemSteam]
bEnabled=true
SteamDevAppId=480

; If using Sessions
; bInitServerOnClient=true

[/Script/OnlineSubsystemSteam.SteamNetDriver]
NetConnectionClassName="OnlineSubsystemSteam.SteamNetConnection"
```
3. 打开并登录steam客户端
4. 工程文件夹下， 右击工程文件launch game, 或者使用Standalone Game运行游戏(同时Net Mode选择Play As Standalone和一个玩家， 不要使用Play As Client 或者Play As Listen Server， 因为该模式会导致服务端功能和客户端功能都运行，但online subsystem steam 不支持运行在同一台机器上)




打开online subsystem steam的情况下， Number of Players设置为1

使用Play As Listen Server启动时，出现一个窗口和一个日志文件，日志会出现： 
```
LogNet: GameNetDriver SteamNetDriver_0 IpNetDriver listening on port 17777

LogOnlineSession: Warning: STEAM: No game present to join for session (GameSession)
```

使用Play As Clent启动时，出现两个窗口和两个日志文件（Saved/Logs目录） 
控制台窗口服务端日志文件会出现：
```
LogCsvProfiler: Display: Metadata set : commandline="" E:/workspace/unreal/OpenWorld/OpenWorld.uproject /Game/Maps/MainMap -game -PIEVIACONSOLE -Multiprocess -server -log GameUserSettingsINI=PIEGameUserSettings0 -MultiprocessSaveConfig -forcepassthrough -messaging -SessionName="Play in Standalone Game" -port=17777 -windowed""

LogNet: Created socket for bind address: 0.0.0.0 on port 17777

LogOnline: Warning: STEAM: Failed to initialize Steam, this could be due to a Steam server and client running on the same machine. Try running with -NOSTEAM on the cmdline to disable.

LogSteamShared: Warning: Steam Dedicated Server API failed to initialize.

Login request: ?Name= xxx_name: userId: STEAM:xxx_id platform: STEAM
```

客户端日志会出现：
```
LogNet: Game client on port 17777, rate 100000

```


问题： 如何单独对开启online subsystem steam的服务端（Dedicated Server）实现运行和调试呢

## 使用一台电脑对online subsystem steam多人联机进行测试
- 使用hyper-v建立windows虚拟机
  - gpu虚拟化 
  - 网络使用 【外部网路虚拟交换机】，让物理主机和虚拟机处在同一个局域网
  - 网络防火墙关闭
- 使用Use LAN模式， 两个steam账号进行多人联机测试，一台client进行Create Session， 另一台client进行Find Sessions和Join Session是可以测试成功的。
- 非Use LAN模式，可能需要NAT才能完成多人联网


# 游戏分类

- MMO （massively multiplayer online）大型多人在线
- RPG（role-playing game） 角色扮演游戏

# 游戏逻辑

## 结束逻辑

- 通关口与玩家Overlap
  - 判断玩家状态
    - 获取GameMode，调用结束游戏函数（只会在服务器上执行）
      - 通过GameState中的UFUNCTION(NetMulticast)函数让所有客户端执行结束函数功能

## 保存游戏
游戏数据由Save Game类型的对象进行保存和序列化
- 创建游戏存档（Create Save Game）
- 判断游戏存档是否存在（Does Save Game Exist）
- 保存游戏存档（Save Game to Slot）， Run on Server

# Blueprint 和 c++ 协作

- c++ 使用 Blueprint中定义的类型， 在cpp头文件中声明TSubclassOf `<AAtor>`类型变量， 并公开到蓝图进行编辑

# 仓库系统Inventory

- 使用Actor Component实现仓库基类BPC_InventoryBase
  - 创建BPC_InventoryBase(Actor Component)的子类来表达不同类型的仓库系统， 如人物背包系统， 车载系统


# unreal git

.gitignore
```
# unreal
Binaries
DerivedDataCache
Intermediate
Saved
Build
Packaged
```


# Unreal 子系统常用开发

- Enum
- Structure
- DataTable

# Unreal Media

- 创建Media Source，并绑定上视频文件
- 创建Media Player，生成Media Texture， 在Media Texture上创建Material
- 创建Actor蓝图类， 
  - 添加Media Sound Component组件，绑定Media Player
  - 添加Cube组件，绑定Media Texture生成的Material
  - 添加MediaPlayer类型变量，使用Open Source来播放文件 

如何动态根据视频创建Material呢

# Unreal Packaging 打包设置

- 设置要打包的地图 （Project Settings > Packaging > List of maps to include in packaged build), `eg: /Game/Maps/Level1`



# unreal 开发常见问题


网络问题

现象： 不登录steam时，Use LAN可以正常联机； 登录steam后，Use LAN 联机出现UEngine::BroadcastNetworkFailure错误

eg: 服务端Create Session为192.168.0.103:7777
```
LogNet: Warning: UNetConnection::Tick: Connection TIMED OUT. Closing connection.. Elapsed: 20.00, Real: 20.00, Good: 20.00, DriverTime: 20.nection] RemoteAddr: 192.168.0.103:7777, Name: SteamNetConnection_xxxx1, Driver: PendingNetDriver SteamNetDriver_xxxx,  NULL, UniqueId: INVALID
LogNet: Error: UEngine::BroadcastNetworkFailure: FailureType = ConnectionTimeout, ErrorString = UNetConnection::Tick: Connection TIMED sed: 20.00, Real: 20.00, Good: 20.00, DriverTime: 20.02, Threshold: 20.00, [UNetConnection] RemoteAddr: 192.168.0.103:7777, Name:  Driver: PendingNetDriver SteamNetDriver_xxxx, IsServer: NO, PC: NULL, Owner: NULL, UniqueId: INVALID, Driver = PendingNetDriver 
LogNet: Warning: Network Failure: PendingNetDriver[ConnectionTimeout]: UNetConnection::Tick: Connection TIMED OUT. Closing connection.. ood: 20.00, DriverTime: 20.02, Threshold: 20.00, [UNetConnection] RemoteAddr: 192.168.0.103:7777, Name: SteamNetConnection_xxxx1, NetDriver_xxxx, IsServer: NO, PC: NULL, Owner: NULL, UniqueId: INVALID
LogNet: NetworkFailure: ConnectionTimeout, Error: 'UNetConnection::Tick: Connection TIMED OUT. Closing connection.. Elapsed: 20.00, Real: 20.00, Good: 20.00, DriverTime: 20.02, Threshold: 20.00, [UNetConnection] RemoteAddr: 192.168.0.103:7777, Name: SteamNetConnection_xxxx1, Driver: PendingNetDriver SteamNetDriver_xxxx, IsServer: NO, PC: NULL, Owner: NULL, UniqueId: INVALID'
LogNet: UNetConnection::Close: [UNetConnection] RemoteAddr: 192.168.0.103:7777, 
```
原因： 访问steam的网络问题， 如地址解析超时等， Open Level的方式
解决： https://forums.unrealengine.com/t/steam-client-timeout-but-works-with-null/343006/4

create session, open level使用`listen?bIsLanMatch=1`

问题： 局域网联机找不到会话， 多网卡，广播没有在所有网卡上进行探测导致的
解决： 安装WinIPBroadcast服务，https://github.com/dechamps/WinIPBroadcast