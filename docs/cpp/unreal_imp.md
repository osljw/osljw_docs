

# 开关门实现

https://www.bilibili.com/video/BV164411Y732?p=27


1. SM_door 静态网格体
2. SM_door编辑器，添加碰撞（防止穿模）
3. 添加box trigger
4. 关卡蓝图添加box trigger的overlay事件
5. 开关门对应SetActorRotation， TimeLine控制动画


门的actor BP类



# 上下车

上车
1. box collision begin overlap 和 上车按键（事件）
2. begin overlap获取到character， 关闭character的碰撞（set actor enable collision）
3. 绑定character到车的座位上（attach actor to component）
4. player controller 切换pawn（possess）， 从控制人变成控制车


下车
1. 下车按键触发
2. detach from actor （将人物从车上detach）
3. 设置人物位置（set actor transform）
4. 开启人物碰撞（set actor enable collision）
5. 视角平滑切换 set view target with blend 
6. player controller 切换到character


# 背包系统

https://www.youtube.com/watch?v=OCsfoT4x3Bk&list=PLSm3WOQFq3ILjDNy58KuDHD3odzl0K7rR&index=6

1. inventory UI （widget BP）
2. 人物蓝图按键触发create widget， add to viewport， show mouse cursor


- MasterItem（BP_Actor）
- ItemData(BP Structure)
- ItemEnum(BP Enumeration)

1. Actor创建ItemData类型的变量来对物体进行描述（name， desc， category， weight等等）， Actor父类修改为继承MasterItem
2. 人物创建Inventory变量（ItemData Array类型） 存储各种物资
3. 人物通过SphereTraceByChannel获得物品actor引用， 保存到人物的Inventory变量中



## 获取周边物品
1. 人物通过MultiSphereTraceByChannel获得周边物品的引用


tab按键
    - 更新周边物品
      - 点击item
        - 更新人物物品 （ 传递需要新增的item信息）
    - 更新人物物品
      - 存储物品列表 （Array）
      - 更新过程
        - 销毁item  （需要item的引用）
        - 展示item ui （ 需要item的
      - 点击item
        - 生成item （生成位置信息， 获取人物位置）
