

# VS 插件
- visual assist
    - Shift + Alt + O  搜索文件位置，定位头文件


# UPROPERTY, UFUNCTION

```
	UPROPERTY(VisibleAnywhere, Category = "Components")
	UStaticMeshComponent* MeshComp;
```

- EditInstanceOnly:  选中放置在word中的actor， detail面板中可进行编辑 
- meta = (EditCondition = "boolvar")  编辑依赖

定义事件
```
UFUNCTION(BlueprintImplementableEvent)
void function_name(params...)
```

## 创建组件

当头文件引用到其他类型时， 避免直接包含头文件，而是在头文件中使用class <type_name>进行声明， 在源文件中include头文件， 提高编译速度

头文件
```
class USphereComponent;


	UPROPERTY(VisibleAnywhere, Category = "Components")
	UStaticMeshComponent* MeshComp;
```

源文件
```
MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
```

# GameplayStatics

SpawnEmitterAtLocation， 在哪个actor上（第一个参数）， 产生哪个粒子特效（第二个参数）， 在什么位置上（第三个参数）

#include "Kismet/GameplayStatics.h"
UGameplayStatics::SpawnEmitterAtLocation(this, PickupFX, GetActorLocation());