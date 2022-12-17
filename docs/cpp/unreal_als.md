

overlay state 描述不同的角色
movement state 描述人物不同的状态
movement action 描述运动指令

movement state
按照位置区分 -> 按照姿态区分

view state 


base pose layer：  站和蹲



# 移动

加速度计算为什么不使用Get Current Acceleration， 而是使用Velocity差值除以Delta Time？

当玩家一直按住W时， 人物在没有达到最大速度限制时，两种方式得到的结果是一样的， 但是当玩家速度超过最大速度限制后， Get Current Acceleration返回的还是加速度数值，使用Velocity差值除以Delta Time获得的加速度是零，更符合真实物理。 


为什么使用ML IS Different(Byte)宏来判断是否不相等？

UE中对象使用引用的方式传递， （引用 ！= 引用）语句阅读时容易产生歧义， 到底是判断值是否相等还是是否是同一个对象。ML IS Different(Byte)宏作用是判断值是否相等。


PlayerInputGraph 用于处理输入， 输入事件，MovementAction和MovementState构成了类似状态机的功能， 方便对WASD和Space键在什么状态下才能生效进行控制。

人物蓝图通过BeginPlay初始化人物运动初始状态， 通过Tick获取人物最新数据， 状态机判断和循环


# gait 步态

- 行走
- 跑步
- 冲刺

movement action行动
- 攀爬
- 翻滚 Rolling
- 起身 GettingUp

# 8向移动

- BaseLayer（函数 Animation Layer）
    - (N) Locomotion Cycles （State Machine）
        - (N) Locomotion Cycles (state)
            - (N) CycleBlending
                - (N) Directional States



# 关于高级运动系统复刻与解耦

第一期~第五期：  摄像机系统
第六期： 人物蓝图运动相关数据， 加速度，速度， Yaw等
第七期 ~ 第九期： 人物蓝图和动画蓝图的数据交互
第十期： 结构体，曲线类型和创建
第十一期： 步态gait 状态
第十二期： 人物蓝图，运动曲线， 跑步，冲刺
第十三期： 动画蓝图相关计算