
# opengGL

将本次需要执行的缩放、平移等操作放在glPushMatrix和glPopMatrix之间。glPushMatrix()和glPopMatrix()的配对使用可以消除上一次的变换对本次变换的影响。使本次变换是以世界坐标系的原点为参考点进行
```
glPushMatrix()
glPopMatrix()
```

启用和禁止功能
```
glEnable
glDisable
```
GL_BLEND
将源色和目标色以某种方式混合生成特效的技术。混合常用来绘制透明或半透明的物体

glBlendFunc 设置混合系数

glLoadIdentity 恢复初始坐标系
```
glLoadIdentity
```
