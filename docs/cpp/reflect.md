
# 反射

# 反射实现方式
非侵入反射（不影响原来的类型定义）


## 使用模板， 手动注册
https://github.com/rttrorg/rttr



## 反射辅助接口

- meta: 存储反射信息， 类型，包含的成员信息， 包含的函数信息
    - property
    - method
    - class： 存储类声明信息
    - object: 对对象实例的统一表达，反射动态创建对象时的返回类型

- builder： 非侵入式反射，编译时辅助接口， 实现从原始类型得到meta信息
- runtime: 运行时辅助接口， 如创建对象， 获取成员，调用方法

# 反射应用场景

1. 通过类名字符串创建实例  （ 工厂模式？）




# 自动注册工厂模式


# unreal 反射


unreal 反射借助了哪些工具？
- UnrealHeaderTool
- UnrealBuildTool

一个类和其成员是否需要反射？

通过宏来控制， 例如UCLASS()、USTRUCT()、UFUNCTION()、UPROPERTY()

新增的反射代码怎么生成？

每个需要反射的类会由UBT和UHT在编译时生成代码，例如filename.generated.h和filename.gen.cpp