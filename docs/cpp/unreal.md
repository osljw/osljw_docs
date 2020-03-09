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


# ThirdPersonCharacter （Blueprint Class)
- ThirdPersonCharacter （Blueprint Class)
  - CapsuleComponent
    - SkeletalMeshComponent
      - SkeletalMesh
      - Animation
      - Material





# c++ 创建actor提供给unreal使用
https://docs.unrealengine.com/en-US/Programming/QuickStart/index.html
