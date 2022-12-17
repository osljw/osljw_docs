

# VS 插件
- visual assist
    - Shift + Alt + O  搜索文件位置，定位头文件


# UCLASS, UPROPERTY, UFUNCTION

UCLASS代码示例
```
UCLASS(Blueprintable)

UCLASS(Abstract, HideCategories = Input, Meta = (ShortTooltip = "The base gameplay ability class used by this project."))
```


```
	UPROPERTY(VisibleAnywhere, Category = "Components")
	UStaticMeshComponent* MeshComp;
```

- EditInstanceOnly:  选中放置在word中的actor， detail面板中可进行编辑 
- meta = (EditCondition = "boolvar")  编辑依赖

定义蓝图可调用函数
```
UFUNCTION(BlueprintCallable, Category = "Lyra|Character")
ULyraAbilitySystemComponent* GetLyraAbilitySystemComponent() const;
```

定义事件
```
UFUNCTION(BlueprintImplementableEvent)
void function_name(params...)
```

定义RPC调用
```
UFUNCTION(Server, Reliable, WithValidation)
void ServerRunFunc();

void XxxxActor::ServerRunFunc_Implementation() {

}

bool XxxxActor::ServerRunFunc_Validate() {
	return true;
}
```

## 创建组件

当头文件引用到其他类型时， 避免直接包含头文件，而是在头文件中使用class <type_name>进行声明， 在源文件中include头文件， 提高编译速度

头文件（.h)
```
class USphereComponent;

UPROPERTY(VisibleAnywhere, Category = "Components")
UStaticMeshComponent* MeshComp;
```

源文件(.cpp)
```
#include "Components/XxxComponent.h" // 头文件的位置

MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
```

# GameplayStatics

SpawnEmitterAtLocation， 在哪个actor上（第一个参数）， 产生哪个粒子特效（第二个参数）， 在什么位置上（第三个参数）

#include "Kismet/GameplayStatics.h"
UGameplayStatics::SpawnEmitterAtLocation(this, PickupFX, GetActorLocation());


# Delegate and Event
1. Single-cast  Delegate
2. Multi-cast  Delegate
3. Dynamic  Delegate



