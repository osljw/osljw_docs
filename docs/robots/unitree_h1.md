

# mujoco模拟
https://github.com/unitreerobotics/unitree_mujoco.git

定位：MuJoCo 仿真环境，**对接 unitree_sdk2**，做到 sim2real 同 API，仿真代码几乎可以直接搬到真机 G1

https://github.com/unitreerobotics/unitree_rl_gym.git
- 定位：基于 NVIDIA Isaac Gym，**大规模并行强化学习训练**，支持 G1/H1/Go2，训练步态、全身技能策略
- 适用：端到端 RL 策略、行走 / 跳跃等运动策略训练
- 和 mujoco 区别：
  - `unitree_mujoco`：单实例、轻量、控制验证、C++ 优先
  - `unitree_rl_gym`：GPU 并行、大批量 RL 训练，适合训练 policy


G1 12dof 和 G1 29dof的主要仿真区别
```xml
    <body name="pelvis" pos="0 0 0.793">
      <!-- <inertial pos="0 0 -0.07605" quat="1 0 -0.000399148 0" mass="3.813" diaginertia="0.010549 0.0093089 0.0079184"/> -->
      <inertial pos="0.0144905 0.000151462 0.144068" quat="0.999881 -0.000505543 -0.0154276 0.000328408" mass="17.7349" diaginertia="0.552723 0.454092 0.211762"/>
```

- 29dof: 单独骨盆零件，3.813kg
- 12dof: 骨盆 + 躯干 + 腰 + 双臂合并为一个刚体，17.7349kg