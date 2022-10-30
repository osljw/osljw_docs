
# SFM （Structure from Motion）

1. 求解基础矩阵F （归一化八点法）
2. 求解本质矩阵$E = K_2^TFK_1$, 由两个相机的内参矩阵和基础矩阵F计算
3. 分解本质矩阵E = T x R， 得到相机之间的变换矩阵
4. 三角化（ 已知两个相机的内参矩阵$K_1, K_2$， 两幅图像的匹配点p1(u1, v1), p2(u2, v2), 以及相机坐标的变换矩阵R，T， 求解匹配点P所对应的三维坐标。 


- 用SIFT，SURF匹配得到Corresponding points
- Corresponding points -> findEssentialMat() -> 
- 



