
# Lyra运行流程分析

## 游戏入口关卡
Project Settings -> Maps & Modes
B_LyraGameMode 
LyraStarterGame/Content/B_LyraGameMode.uasset

编辑器默认关卡：LyraStarterGame/Content/System/DefaultEditorMap/L_DefaultEditorOverview.umap
游戏默认关卡： LyraStarterGame/Content/System/FrontEnd/Maps/L_LyraFrontEnd.umap

## 关卡绑定的Experience
关卡 World Settings -> 设置关卡要使用的Experience

L_LyraFrontEnd的Experience为B_LyraFrontEnd_Experience

LyraStarterGame/Content/System/FrontEnd/B_LyraFrontEnd_Experience.uasset

- Level
    - LyraExperienceDefinition
        - LyraPawnData（人物配置数据eg: HeroData_ShooterGame)
            - LyraAbilitySet(人物技能eg: AbilitySet_ShooterHero)
                - LyraGameplayAbility(近战技能eg：GA_Melee）



## UI加载
B_LyraFrontEnd_Experience 中通过Add Components Action，在LyraGameState中加载B_LyraFrontendStateComponent组件，该组件设置要加载的UI, 

- B_LyraFrontEnd_Experience 
    - B_LyraFrontendStateComponent 
        - W_LyraStartup （Press Start Screen Class） 游戏开始UI
        - W_LyraFrontEnd

B_LyraFrontendStateComponent位置：
Blueprint'/Game/UI/B_LyraFrontendStateComponent.B_LyraFrontendStateComponent'

ULyraFrontendStateComponent继承自UGameStateComponent

W_LyraFrontEnd位置为： WidgetBlueprint'/Game/UI/Menu/W_LyraFrontEnd.W_LyraFrontEnd'

W_LyraFrontEnd 点击Play Lyra后， 会创建显示experiences的界面

WidgetBlueprint'/Game/UI/Menu/Experiences/W_ExperienceSelectionScreen.W_ExperienceSelectionScreen'

- 显示experiences选择界面
    - 单机玩
    - Host -> W_HostSessionScreen
    - Browse -> W_SessionBrowserScreen




UI切换： 使用Push Content to Layer for Player

- W_HostSessionScreen
    - 位置：WidgetBlueprint'/Game/UI/Menu/Experiences/W_HostSessionScreen.W_HostSessionScreen'
    - ExperienceList 容器
        - 位置：WidgetBlueprint'/Game/UI/Menu/Experiences/W_ExperienceList.W_ExperienceList'
        - Get Primary Asset Id List 获取LyraUserFacingExperienceDefinition数组进行展示
        - 每个LyraUserFacingExperienceDefinition的显示由W_ExperienceTile定义
            - 位置WidgetBlueprint'/Game/UI/Menu/Experiences/W_ExperienceTile.W_ExperienceTile'

LyraUserFacingExperienceDefinition是如何被Get Primary Asset Id List进行收集的？

Project Settings -> Asset Manager -> Primary Asset Types to Scan -> LyraUserFacingExperienceDefinition -> Directories 会定义该类型Asset被收集的位置

Lyra预定义的LyraUserFacingExperienceDefinition：

- LyraUserFacingExperienceDefinition'/ShooterMaps/System/Playlists/DA_Expanse_TDM.DA_Expanse_TDM'
- LyraUserFacingExperienceDefinition'/ShooterMaps/System/Playlists/DA_Convolution_ControlPoint.DA_Convolution_ControlPoint'


W_SessionBrowserScreen
- W_SessionBrowserScreen
    - 位置：WidgetBlueprint'/Game/UI/Menu/Experiences/W_SessionBrowserScreen.W_SessionBrowserScreen'


LyraExperienceDefinition and LyraUserFacingExperienceDefinition
- LyraExperienceDefinition 用于定义游戏模式（GameMode）所需要的操作和数据
- LyraUserFacingExperienceDefinition 用于定义Map和LyraExperienceDefinition的关联，即地图需要使用什么游戏模式


用户操作后会确定LyraUserFacingExperienceDefinition， 根据这个信息有common session subsystem创建游戏会话

## 游戏增强输入 EnhancedInput

Plugins: Enhanced Input

Project Setting -> Input -> 
- Default Player Input Class: EnhancedPlayerInput
- Default Input Component Class: LyraInputComponent

InputMappingContext:  配置按键和InputAction的绑定


InputMappingContext'/Game/Input/Mappings/IMC_Default_KBM.IMC_Default_KBM'


LyraPawnData

- LyraPawnData： HeroData_ShooterGame 
    - 位置：LyraPawnData'/ShooterCore/Game/HeroData_ShooterGame.HeroData_ShooterGame'
    - Input Config配置输入： InputData_Hero
        - 位置：LyraInputConfig'/Game/Input/InputData_Hero.InputData_Hero'
        - 可以设置InputAction和Input Tag的绑定
    - Ability Sets配置能力：AbilitySet_ShooterHero
        - 位置：LyraAbilitySet'/ShooterCore/Game/AbilitySet_ShooterHero.AbilitySet_ShooterHero'
        - Ability 可以设置触发的Input Tag
        - 问题：Input Tag是如何触发Ability的，触发流程是怎样的？

InputAction可以被用于映射到硬件输入
IMC_Default_KBM（InputMappingContext类型） 用于控制映射
InputMappingContext'/Game/Input/Mappings/IMC_Default_KBM.IMC_Default_KBM'

Character -> -> ULyraHeroComponent -> LyraInputComponent -> LyraPawnData


ULyraHeroComponent::InitializePlayerInput负责增强输入的初始化
1. 通过ULyraPawnExtensionComponent组件获取到ULyraPawnData中的ULyraInputConfig
2. ULyraInputComponent负责对UEnhancedInputLocalPlayerSubsystem进行AddInputMappings
3. 调用ULyraInputComponent的BindAbilityActions， 将InputTag和InputAction进行绑定
4. 当有按键按下时会调用ULyraHeroComponent::Input_AbilityInputTagPressed， 当有按键释放时会调用ULyraHeroComponent::Input_AbilityInputTagReleased, 并将FGameplayTag作为函数参数
5. ULyraHeroComponent的按键处理函数会通过ULyraPawnExtensionComponent找到ASC组件，交由ULyraAbilitySystemComponent的AbilityInputTagPressed函数和AbilityInputTagReleased对InputTag进行处理， 如果FGameplayAbilitySpec中的DynamicAbilityTags与输入Tag匹配，

ULyraPawnExtensionComponent的ASC和ALyraPlayerState的ASC是同一个ASC。

```c++
void ULyraHeroComponent::OnPawnReadyToInitialize() {
    // ......
    ALyraPlayerState* LyraPS = GetPlayerState<ALyraPlayerState>();

	if (ULyraPawnExtensionComponent* PawnExtComp = ULyraPawnExtensionComponent::FindPawnExtensionComponent(Pawn))
	{
		PawnData = PawnExtComp->GetPawnData<ULyraPawnData>();

		// The player state holds the persistent data for this player (state that persists across deaths and multiple pawns).
		// The ability system component and attribute sets live on the player state.
		PawnExtComp->InitializeAbilitySystem(LyraPS->GetLyraAbilitySystemComponent(), LyraPS);
	}
}
```

## Lyra 人物系统

人物蓝图 （ShooterCore 插件）
/ShooterCore/Game/B_Hero_ShooterMannequin.B_Hero_ShooterMannequin'

### 组件

- UPawnComponent
    - ULyraPawnComponent （An actor component that can be used for adding custom behavior to pawns）
        - ULyraPawnExtensionComponent
        - ULyraHeroComponent



### 能力系统
- 跳跃
- 瞄准ADS
- 扔武器
- 近战 melee

能力描述继承关系
- UPrimaryDataAsset    
    - ULyraAbilitySet（eg：AbilitySet_ShooterHero）

ULyraAbilitySet可以配置人物所具备的GameplayAbility和GameplayEffect，以及AttributeSet

能力赋予过程
- ULyraExperienceDefinition：B_ShooterGame_Elimination
    - Default Pawn Data： HeroData_ShooterGame
        - Ability Sets： AbilitySet_ShooterHero

ULyraExperienceDefinition继承自UPrimaryDataAsset，该资产文件是如何被GameMode加载的呢？

1. ALyraGameState会创建ULyraExperienceManagerComponent组件
2. ULyraExperienceManagerComponent调用StartExperienceLoad，使用ULyraAssetManager来加载ULyraExperienceDefinition
3. ALyraGameMode调用GetPawnDataForController，获取到ULyraExperienceDefinition的Default Pawn Data，进而获得PawnClass
4. ALyraPlayerState的OnExperienceLoaded调用SetPawnData，设置AbilitySets（HeroData_ShooterGame中配置的AbilitySets）
5. 每个配置的AbilitySet使用自身的GiveToAbilitySystem，将能力赋予给了ALyraPlayerState的ASC组件


Source\LyraGame\AbilitySystem\LyraAbilitySet.cpp
```c++
		ULyraGameplayAbility* AbilityCDO = AbilityToGrant.Ability->GetDefaultObject<ULyraGameplayAbility>();

		FGameplayAbilitySpec AbilitySpec(AbilityCDO, AbilityToGrant.AbilityLevel);
		AbilitySpec.SourceObject = SourceObject;
		AbilitySpec.DynamicAbilityTags.AddTag(AbilityToGrant.InputTag);

		const FGameplayAbilitySpecHandle AbilitySpecHandle = LyraASC->GiveAbility(AbilitySpec);
```
GiveAbility会调用OnGiveAbility， 该函数根据FAbilityTriggerData设置能力的触发方式


6. ALyraPlayerState::PostInitializeComponents中设置ASC的OwnerActor(ALyraPlayerState)和AvatarActor(ALyraCharacter)
```
AbilitySystemComponent->InitAbilityActorInfo(this, GetPawn());
```

能力使用过程， 例如近战能力GA_Melee是如何被触发的？
GA_Melee在AbilitySet_ShooterHero中配置为与InputTag.Ability.Melee绑定， 从能力赋予过程分析可知道该技能最终会由ALyraPlayerState的ASC进行管理， 从增强输入过程分析知道Character的组件会接收到输入信息并调用Character的ULyraAbilitySystemComponent的AbilityInputTagPressed函数和AbilityInputTagReleased对InputTag进行处理， 如果FGameplayAbilitySpec中的DynamicAbilityTags与输入Tag匹配，就会将FGameplayAbilitySpecHandle能力Handle存到数组中

```
	// Handles to abilities that had their input pressed this frame.
	TArray<FGameplayAbilitySpecHandle> InputPressedSpecHandles;

	// Handles to abilities that had their input released this frame.
	TArray<FGameplayAbilitySpecHandle> InputReleasedSpecHandles;

	// Handles to abilities that have their input held.
	TArray<FGameplayAbilitySpecHandle> InputHeldSpecHandles;
```

ALyraPlayerController的PostProcessInput函数会每帧调用，
- ALyraPlayerController::PostProcessInput
    - ULyraAbilitySystemComponent::ProcessAbilityInput
        - UAbilitySystemComponent::TryActivateAbility


跳跃能力示例：
AbilitySet_ShooterHero（LyraAbilitySet类型）中将GA_Hero_Jump和InputTag.Jump标签进行绑定
位置： Blueprint'/Game/Characters/Heroes/Abilities/GA_Hero_Jump.GA_Hero_Jump'

TagRelationships_ShooterHero: Tag和能力的对应关系，
LyraAbilityTagRelationshipMapping'/ShooterCore/Game/TagRelationships_ShooterHero.TagRelationships_ShooterHero'


- 继承LyraGameplayAbility
    - Event OnPawnAvatarSet： 可以使用UIExtension Subsystem注册UI组件
    - Event ActivateAbility： 确定能力是否激活


### 回血技能


- B_AbilitySpawner
    - Blueprint'/ShooterCore/Blueprint/B_AbilitySpawner.B_AbilitySpawner'
    - Gameplay Effect to Apply选择GE_InstantHeal_Part
        - Blueprint'/ShooterCore/Items/HealthPickup/GE_InstantHeal_Part.GE_InstantHeal_Part'
    - 继承自B_WeaponSpawner
    - 复用了GiveWeapon函数来实现回血
    - 通过ASC组件调用Apply Gameplay Effect to Self

- GameplayEffect
    - GameplayEffectParent_Heal
        - GE_InstantHeal_Big (治疗50)
        - GE_InstantHeal_Part （治疗25）



- UAttributeSet
    - ULyraAttributeSet
        - ULyraHealthSet
        - ULyraCombatSet
            - BaseDamage （FGameplayAttributeData）
            - BaseHeal （FGameplayAttributeData）

- UGameFrameworkComponent
    - ULyraHealthComponent
        - ULyraHealthSet（引用） 
            - Health
            - MaxHealth
            - FLyraAttributeEvent OnOutOfHealth 当Health为零时，可以触发该事件上绑定的回调函数`ULyraHealthComponent::HandleOutOfHealth`
        - ULyraHealthComponent::HandleOutOfHealth 死亡逻辑，发送"GameplayEvent.Death" Gameplay Event， 激活死亡技能GA_Hero_Death

- UGameplayEffectExecutionCalculation
    - ULyraHealExecution
    - ULyraDamageExecution
        - 从FLyraGameplayEffectContext中获取HitResult



### 近战技能
- GA_Melee
    - Blueprint'/ShooterCore/Game/Melee/GA_Melee.GA_Melee'
    - (TagName="InputTag.Weapon.ADS") 由该输入标签激活能力
    - Event ActivateAbility （激活能力）
        - -> Play Montage and Wait （异步播放攻击动画）
        - -> Has Authority (确保只在服务器执行伤害判断)
        - -> Capsule Trace For Objects （碰撞检测）
        - -> HitActor -> Get Ability System Component （被击中Actor有ASC）
        - -> Lyra Team Subsystem -> CompareTeams (不同队伍玩家)
        - -> Line Trace By Channel (二次检测， 确保无阻挡物)
        - -> ApplyGameplayEffectToTarget（应用GE_Damage_Melee, 计算伤害)
        - -> Execute GameplayCueWithParams On Owner 
        - -> (Multicast)Play Sound at Location （无论是否击中都有播放近战声音）
        - End Ability

- GE_Damage_Melee
    - Blueprint'/ShooterCore/Weapons/GE_Damage_Melee.GE_Damage_Melee'

    - GameplayEffect
        - Duration Policy: Instant （查看什么类型的GE）
        - Executions
            - Calculation Class： LyraDamageExecution （伤害计算）
    - Display 
        - -> Gameplay Cues：GameplayCue.Character.DamageTaken 
        - Tools -> GameplayCue Editor 找到触发了哪个GameplayCue Notify
        - Blueprint'/Game/GameplayCueNotifies/GCNL_Character_DamageTaken.GCNL_Character_DamageTaken'
        
- Gameplaycue Notify： GCNL_Character_DamageTaken
    - 发出攻击的玩家（IsLocallyControlled) 可以看到伤害数值（pop up numbers）
    - 被击中的玩家， 播放击中声音


### 开枪技能

设置开火按键

1. 创建InputAction IA_Weapon_Fire, eg: InputAction'/Game/Input/Actions/IA_Weapon_Fire.IA_Weapon_Fire'
2. 设置输入映射

InputMappingContext'/Game/Input/Mappings/IMC_Default_KBM.IMC_Default_KBM'

将Left Mouse Button绑定到InputAction： IA_Weapon_Fire

3. 配置输入产生的GameplayTag
LyraInputConfig'/Game/Input/InputData_Hero.InputData_Hero'

InputData_Hero 中设置开火输入按键InputAction和触发的GameplayTag
- InputData_Hero
    - Input Action: 
    - Input TAg: 选择InputTag.Weapon.Fire


设置能力触发
- GA_Weapon_Fire
    - ClassDefaults ->
        -   Triggers -> 
            - AbilityTriggers
                - Trigger TAg: InputTag.Weapon.Fire
                - Trigger Source: Gameplay Event

GA_Weapon_Fire技能没有配置到ASC系统中，而是作为武器开火技能的父类，提供技能逻辑框架。 具体的武器开火技能会在武器装备时，才会绑定到Character上。


GA_Weapon_Fire 继承关系
- ULyraGameplayAbility
    - ULyraGameplayAbility_FromEquipment
        - ULyraGameplayAbility_RangedWeapon
            - GA_Weapon_Fire
                - Blueprint'/Game/Weapons/GA_Weapon_Fire.GA_Weapon_Fire'

激活技能： (TagName="InputTag.Weapon.Fire")


- ActivateAbility
    - Is Locally Controlled -> Start Ranged Weapon Targeting -> 
        - Event On Ranged Weapon Target Data Ready
        - GA->AvatarPawn-> Controller -> GetPlayerViewPoint 获取射击起点和射击方向
    - 播放fire montage
    - 

Tag之间的相互影响：

LyraAbilityTagRelationshipMapping'/ShooterCore/Game/TagRelationships_ShooterHero.TagRelationships_ShooterHero'

TagRelationships_ShooterHero中定义了GA_Weapon_Fire技能相关的GameplayTag

当Fire时会阻止和取消带有Emote和Reload的标签的技能

### 死亡能力

能力賦予： AbilitySet_ShooterHero中配置

- ULyraGameplayAbility
    - ULyraGameplayAbility_Death
        - GA_Hero_Death
            - Blueprint'/Game/Characters/Heroes/Abilities/GA_Hero_Death.GA_Hero_Death'
            - ActivateAbilityFromEvent
                - GameplayEventData获取相关参数
                - GameplayCue.Character.Death

激活方式： ActivateAbilityFromEvent (TagName="GameplayEvent.Death")

激活过程：

Source\LyraGame\LyraGameplayTags.h 中建立"GameplayEvent.Death"的GameplayTag
```
FGameplayTag GameplayEvent_Death;

AddTag(GameplayEvent_Death, "GameplayEvent.Death", "Event that fires on death. This event only fires on the server.");
```

伤害技能GA使用扣减血量的GE时，最终会调用到ULyraHealthSetULyraHealthComponent::HandleOutOfHealth， 通过gameplay event的方式激活GA_Hero_Death技能

具体示例：

GA_Melee -> GE_Damage_Melee -> ULyraDamageExecution -> ULyraHealthSet(OnOutOfHealth) -> ULyraHealthSetULyraHealthComponent::HandleOutOfHealth -> "GameplayEvent.Death" gameplay event -> GA_Hero_Death

## Lyra 武器系统



### 武器出生 与 拾取武器
- B_WeaponSpawner
    - Blueprint'/ShooterCore/Blueprint/B_WeaponSpawner.B_WeaponSpawner'
    - 通过配置选择Weapon Definition（LyraWeaponPickupDefinition），定义出现武器类型
    - 通过父类（ALyraWeaponSpawner c++）进行碰撞检测， 
    - 通过GiveWeapon函数将Weapon Definition->LyraInventoryItemDefinition绑定到Pawn身上
        - 确保是非游戏结束阶段
        - 调用execute GameplayCue on Actor
        - 调用Controller的LyraInventoryManagerComponent->AddItemDefinition将武器添加到库存
        - QuickBar添加库存系统创建的ULyraInventoryItemInstance， 调用SetActiveSlotIndex设置刚捡起的武器为激活状态, EquipItemInSlot， ULyraQuickBarComponent通过Controller找到Pawn的ULyraEquipmentManagerComponent组件，然后调用EquipItem， 根据ULyraEquipmentDefinition生成相应的ULyraEquipmentInstance。
        - 触发Gameplay Tag: GameplayCue.ShooterGame.Interact.WeaponPickup
![](media/pickup-weapon.png)

GameplayCue.ShooterGame.Interact.WeaponPickup 会触发创建GCN_InteractPickUp实例
- GCN_InteractPickUp
    - Blueprint'/ShooterCore/GameplayCues/GCN_InteractPickUp.GCN_InteractPickUp'
    - On Burst函数处理捡起特效

LyraWeaponPickupDefinition 定义了拾取声音，冷却时间，武器Mesh
- UDataAsset
    - ULyraPickupDefinition （Equipment）
        - LyraWeaponPickupDefinition
            - WeaponPickupData_Shotgun（猎枪）
                - LyraWeaponPickupDefinition'/ShooterCore/Weapons/Shotgun/WeaponPickupData_Shotgun.WeaponPickupData_Shotgun'
                - DisplayMesh：  SM_Shotgun （显示武器模型）
                    - StaticMesh'/Game/Weapons/Shotgun/Mesh/SM_Shotgun.SM_Shotgun'
                - Inventory Item Definition （库存系统）
                    - Blueprint'/ShooterCore/Weapons/Shotgun/ID_Shotgun.ID_Shotgun'
            - WeaponPickupData_Pistol（手枪）
                - LyraWeaponPickupDefinition'/ShooterCore/Weapons/Pistol/WeaponPickupData_Pistol.WeaponPickupData_Pistol'


Lyra Inventory Item Definition（库存物品定义）
- UObject
    - ULyraInventoryItemDefinition
        - ID_Shotgun （Lyra Inventory Item Definition）
            - Blueprint'/ShooterCore/Weapons/Shotgun/ID_Shotgun.ID_Shotgun'
            - UInventoryFragment_EquippableItem
                - Equipment Definition：WID_Pistol （LyraEquipmentDefinition）
                    - Blueprint'/ShooterCore/Weapons/Pistol/WID_Pistol.WID_Pistol'

Lyra Inventory Item Definition 通过Fragments数组来定义物品

LyraEquipmentDefinition 定义武器捡起后获得的能力/装备位置
- UObject
    - ULyraEquipmentDefinition
        - WID_Pistol
            - Blueprint'/ShooterCore/Weapons/Pistol/WID_Pistol.WID_Pistol'
            - Instance Type （定义要装备的实例类型， 武器相关动画/参数）
                - Blueprint'/ShooterCore/Weapons/Pistol/B_WeaponInstance_Pistol.B_WeaponInstance_Pistol'
            - Actor to Spawn (定义要spawn的Actor)
                - Blueprint'/ShooterCore/Weapons/Pistol/B_Pistol.B_Pistol'
            - AbilitySet_ShooterPistol 配置装备武器后具有的能力
                - LyraAbilitySet'/ShooterCore/Weapons/Pistol/AbilitySet_ShooterPistol.AbilitySet_ShooterPistol'
                - 开火能力 GA_Weapon_Fire_Pistol
                - 手动装弹能力
                - 自动装弹能力

- ULyraEquipmentInstance
    - ULyraWeaponInstance
        - LyraRangedWeaponInstance
            - B_WeaponInstance_Base
                - B_WeaponInstance_Pistol
                    - Blueprint'/ShooterCore/Weapons/Pistol/B_WeaponInstance_Pistol.B_WeaponInstance_Pistol'
                    - 定义武器装备/卸载人物动画， 拿起武器后的动画集，移除武器后的动画集
                    - 定义武器射击距离

B_Pistol（父类B_Weapon)
    - Blueprint'/ShooterCore/Weapons/Pistol/B_Pistol.B_Pistol'
    - 定义了拿在手上的武器模型（SkeletalMesh）
    - 定义了抛弹壳相关



### 实现武器流程

/ShooterCore/Weapons目录下， 每个目录对应一把武器, 创建武器对应的目录，例如Pistol


- 创建B_Weapon的子类, 用于配置武器模型， 例如B_Pistol
    - 设置Skeletal Mesh
    - 设置Anim Class

- 创建B_WeaponInstance_Base的子类， 例如B_WeaponInstance_Pistol
    - 设置Weapon Equip Montage,  捡起武器时的动画
    - 设置Equipped Anim Set
        - Default Layer， 该动画层为持有武器时的人物动画层

- 创建LyraEquipmentDefinition的子类， 例如WID_Pistol， 对可装卸物品进行资产配置
    - 配置Instance Type为B_WeaponInstance_Pistol
    - 在Actors to Spawn中新增条目
        - 配置Actor to Spawn为B_Pistol
        - 配置Attach Socket为weapon_r

- 创建LyraInventoryItemDefinition的子类， 例如ID_Pistol
    - Fragments下添加Inventory Fragment Equippable Item
        - 配置Equipment Definition为WID_Pistol

- 创建DataAsset -> LyraWeaponPickupDifinition的子类，例如WeaponPickupData_Pistol
    - 配置Inventory Item Definition为ID_Pistol

- 地图上创建B_WeaponSpawner实例
    - 配置 Weapon Definition为WeaponPickupData_Pistol

人物预定义武器
- B_Hero_ShooterMannequin人物蓝图
    - WeaponID（LyraEquipmentDefinition）
        - DefaultValue：Blueprint'/ShooterCore/Weapons/Pistol/WID_Pistol.WID_Pistol'
        - 定义了武器蓝图实例
        - attach Socket等信息




### 武器开火

- GA_Weapon_Fire 
    - GA_Weapon_Fire_Pistol （装备武器时，自动获得的技能）
        - Character Fire Montage 可以自定义武器开火动画
        - GE Damage： GE_Damage_Pistol 设置武器伤害GE


武器伤害
- GameplayEffect
    - GameplayEffectParent_Damage_Basic（蓝图）
        - GE_Damage_Basic_Instant
            - GE_Damage_Pistol


### 医疗包捡起功能
B_AbilitySpawner继承自B_WeaponSpawner 
Blueprint'/ShooterCore/Blueprint/B_AbilitySpawner.B_AbilitySpawner'

## 冲刺技能

1. InputAction'/Game/Input/Actions/IA_Ability_Dash.IA_Ability_Dash'

2. InputMappingContext'/Game/Input/Mappings/IMC_Default_KBM.IMC_Default_KBM'

IMC_Default_KBM中将IA_Ability_Dash和Left Shift按键绑定

3. LyraInputConfig'/Game/Input/InputData_Hero.InputData_Hero'

InputData_Hero中将IA_Ability_Dash和InputTag.Ability.Dash进行绑定


4. Blueprint'/ShooterCore/Game/Dash/GA_Hero_Dash.GA_Hero_Dash'

GA_Hero_Dash技能设置Trigger Tag为InputTag.Ability.Dash

GA_Hero_Dash 继承自GA_AbilityWithWidget， 触发技能时可以显示UI效果

Blueprint'/Game/Characters/Heroes/Abilities/GA_AbilityWithWidget.GA_AbilityWithWidget'

    
## GameplayCue

- UGameplayCueNotify_Burst
    - 立即效果， 不支持 delays and time lines


背景加载：
LyraStarterGame/Content/Environments/B_LoadRandomLobbyBackground.uasset






- LyraExperienceDefinition
    - 示例： Blueprint'/ShooterCore/Experiences/B_ShooterGame_Elimination.B_ShooterGame_Elimination'
    - 设置Pawn Data： LyraPawnData'/ShooterCore/Game/HeroData_ShooterGame.HeroData_ShooterGame'
        - 设置Pawn Class: Blueprint'/ShooterCore/Game/B_Hero_ShooterMannequin.B_Hero_ShooterMannequin'
        - 设置Ability Sets： LyraAbilitySet'/ShooterCore/Game/AbilitySet_ShooterHero.AbilitySet_ShooterHero'
        - 设置输入
        - 设置Camera Mode
    - 执行的Actions
        - Abilities
        - Components
        - UI

LyraPawnData'/ShooterCore/Game/HeroData_ShooterGame.HeroData_ShooterGame'

# InventoryManager 库存系统

- UActorComponent
    - ULyraInventoryManagerComponent组件
        - 挂载在Controller Actor （在GameFeatureData'/ShooterCore/ShooterCore.ShooterCore'中Add Components进行配置）
        - 负责库存物品管理
        - Add Item Definition 添加物品
            - 创建ULyraInventoryItemInstance，绑定TSubclassOf<ULyraInventoryItemDefinition>类型的定义

ULyraInventoryManagerComponent通过FLyraInventoryList保存物品
```
	UPROPERTY(Replicated)
	FLyraInventoryList InventoryList;
```

- UControllerComponent
    - ULyraQuickBarComponent组件
        - 挂载在Controller Actor (在LAS_ShooterGame_StandardComponents中配置)

- UPawnComponent
    - ULyraEquipmentManagerComponent组件
        - 挂载在LyraCharacter Actor （在GameFeatureData'/ShooterCore/ShooterCore.ShooterCore'中Add Components进行配置）
        - 负责可装卸物品的管理
        - FLyraEquipmentList
            - FLyraEquipmentList::AddEntry 实现从装备定义数据ULyraEquipmentDefinition到ULyraEquipmentInstance装备实例的生成， ULyraEquipmentInstance实例挂载在Character Actor


ULyraQuickBarComponent -> AController -> Pawn -> ULyraEquipmentManagerComponent
```c++
ULyraEquipmentManagerComponent* ULyraQuickBarComponent::FindEquipmentManager() const
{
	if (AController* OwnerController = Cast<AController>(GetOwner()))
	{
		if (APawn* Pawn = OwnerController->GetPawn())
		{
			return Pawn->FindComponentByClass<ULyraEquipmentManagerComponent>();
		}
	}
	return nullptr;
}
```


人物蓝图中设置QuickBar的输入按键
- B_Hero_ShooterMannequin
    - Blueprint'/ShooterCore/Game/B_Hero_ShooterMannequin.B_Hero_ShooterMannequin'
    - Change Quickbar Slot 函数
        - 判断Quick Slot有效
        - Send Gameplay Event to Actor (TagName="InputTag.Ability.Quickslot.SelectSlot")

- GA_QuickbarSlots （由AbilitySet_ShooterHero赋予人物技能）
    - Blueprint'/ShooterCore/Game/GA_QuickbarSlots.GA_QuickbarSlots'
    - ActivateAbility
        - Wait Gameplay Event (TagName="InputTag.Ability.Quickslot.SelectSlot")
            - 通过响应Event的方式执行QuickBarComponent -> Set Active Slot Index

QuickBar UI
Experience 配置中添加
- LAS_ShooterGame_StandardHUD
    - LyraExperienceActionSet'/ShooterCore/Experiences/LAS_ShooterGame_StandardHUD.LAS_ShooterGame_StandardHUD'
    - 通过Add Widgets Action， 在(TagName="HUD.Slot.Equipment")标记的位置上添加W_QuickBar 

装备过程由FLyraEquipmentList::AddEntry实现
- 获得ULyraEquipmentDefinition类的CDO对象，该对象中保存了要创建的实例类型ULyraEquipmentInstance
- 将ULyraEquipmentInstance创建到Character Actor上
- 将CDO对象中保存的AbilitySetsToGrant能力描述， 通过GiveToAbilitySystem函数赋予到Character的ASC能力系统上


## Fragments
通过Fragments实现库存物品的模块化

继承关系
- ULyraInventoryItemFragment
    - UInventoryFragment_EquippableItem  <-> ULyraEquipmentDefinition
    - UInventoryFragment_SetStats  用GameplayTag维护数值属性，如弹匣大小，备用弹药数量
    - UInventoryFragment_PickupIcon 
    - UInventoryFragment_QuickBarIcon 
    - UInventoryFragment_ReticleConfig 

## 装备后获得技能
- ULyraGameplayAbility
    - ULyraGameplayAbility_FromEquipment
        - ULyraGameplayAbility_RangedWeapon


# Lyra Animation


## State Machine 状态机

状态机节点播放动画的方式

1. Sequence Player
2. Linked Anim Layer （本质上最后还是调用的Sequence Player）
3. Sequence Evaluator（Anim Node Function）

按照Sequence Player的使用方式进行区分
- bind方式设置sequence， 直接选取动画序列资产即可
- dynamic方式， 通过函数动态决定要使用的动画资产



Lyra Idle状态实现
- idle状态
    - FullBody_IdleState 接口（Linked Anim Layer）
        - Idle State Machine 
            - Idle
            - IdleBreak
            - 
    - Ouput Animation Pose
        - Update Idle State

## Control Rig

Anim Graph 中使用 Control Rig节点

- Alpha Input Type 控制是否使用Control Rig

Control Rig Class

## CopyPose and IK Retarget

CopyPose： 骨架相同时的动画复用
IK Retarget： 骨架不同时，通过IK Rig 和 IK Retarget实现动画重定向

- UControllerComponent
    - ULyraControllerComponent_CharacterParts
        - B_PickRandomCharacter （在Experience Definition中通过AddComponents挂载到Controller）
            - Blueprint'/Game/Characters/Cosmetics/B_PickRandomCharacter.B_PickRandomCharacter'
            - B_PickRandomCharacter在BeginPlay时随机选择B_Manny或B_Quinn, 添加到Character身上

- UPawnComponent
    - ULyraPawnComponent_CharacterParts

- LyraTaggedActor
    - B_Manny
        - Blueprint'/Game/Characters/Cosmetics/B_Manny.B_Manny'
        - Mesh使用的动画蓝图：AnimBlueprint'/Game/Characters/Heroes/Mannequin/Animations/ABP_Mannequin_CopyPose.ABP_Mannequin_CopyPose'


- IK Retarget
    - Retarget Pose From Mesh节点 （可以从父SkeletalMeshComponent拷贝pose）
    - 支持离线和在线动画重定位
    - Retarget 时要确保Pose一致， UE5支持Pose的调整

mixamo动画迁移到ue mannequin时，IK Rig不需要IK solver； 使用mixamo角色时需要需要IK solver


使用自定义角色
1. 继承LyraTaggedActor， 创建B_Test
    - 添加SkeletalMesh组件为 default scene root component
    - 配置Skeletal Mesh为自定义角色
    - 配置Anim Class为 CopyPose（角色兼容骨架）或者Retarget（角色IK Retarget骨架）动画蓝图
2. B_PickRandomCharacter中修改AddCharacterPart的New Part Part Class为B_Test

## 相关链接

https://zhuanlan.zhihu.com/p/517368184

dynamic-ik-retargeting-in-ue5
https://stefanperales.com/blog/dynamic-ik-retargeting-in-ue5/

# Lyra Game Feature
https://dev.epicgames.com/community/learning/tutorials/rdW2/unreal-engine-how-to-create-a-new-game-feature-plugin-and-experience-in-lyra

## LyraPawnData 
LyraPawnData'/ShooterCore/Game/HeroData_ShooterGame.HeroData_ShooterGame'

- 定义使用的人物蓝图
    - Blueprint'/ShooterCore/Game/B_Hero_ShooterMannequin.B_Hero_ShooterMannequin'
- 定义能力系统
    - LyraAbilityTagRelationshipMapping'/ShooterCore/Game/TagRelationships_ShooterHero.TagRelationships_ShooterHero'
- 定义输入配置
    - LyraInputConfig'/Game/Input/InputData_Hero.InputData_Hero'
- 定义Camera Mode
    - Blueprint'/Game/Characters/Cameras/CM_ThirdPerson.CM_ThirdPerson'


## LyraExperienceDefinition

Blueprint'/ShooterCore/Experiences/B_LyraShooterGame_ControlPoints.B_LyraShooterGame_ControlPoints'

## LyraUserFacingExperienceDefinition

- Set Map ID
- Set Experience ID
- 

API
- Create Hosting Request 返回UCommonSession_HostSessionRequest， 创建游戏时使用


# Lyra Bot AI系统

AIController

Blueprint'/ShooterCore/Bot/B_AI_Controller_LyraShooter.B_AI_Controller_LyraShooter'

行为树

BehaviorTree'/ShooterCore/Bot/BT/BT_Lyra_Shooter_Bot.BT_Lyra_Shooter_Bot'


# 使用Lyra资源

自定义Character使用ShooterCore的Animation Blueprint时， 需要在Project Setting -> Game -> Asset Referencing Policy -> Project Content -> Can Reference These Domains -> 添加ShooterCore

# Lyra UI系统

通过Experience的Add Widgets添加
    - 继承自LyraTaggedWidget

WidgetBlueprint'/ShooterCore/ControlPoint/UI/W_CPScoreWidget.W_CPScoreWidget'


# Lyra 动画系统

## 自定义Property Access

动画蓝图中创建纯函数， 返回值名称为ReturnValue才能识别




## Lyra动画迁移
https://www.bilibili.com/video/BV1dT41157pS/?p=1&vd_source=05b9e112882cf3fe738863375b088e4c

https://www.bilibili.com/video/BV1Da411n71c/?spm_id_from=333.999.0.0&vd_source=05b9e112882cf3fe738863375b088e4c

- RootMotion
  - 不开启RootMotion： 人物会叠加actor的移动和动画的移动，导致人物和Camera不是固定距离
  - 开启RootMotion：实现原地奔跑的状态
  - 造成的问题： 奔跑速度和人物步幅不匹配
- Distance Matching （距离匹配）
    - 基于距离数据来播放动画， 而非线性时间播放动画。
    - https://docs.unrealengine.com/5.0/zh-CN/distance-matching-in-unreal-engine/
    - 将人物速度调低， 动画是否会播放小碎步姿态
    - Animation Locomotion Library插件
    - 动画蓝图基类中计算人物当前帧和上一帧的移动距离，并导出到属性存取系统
    - 动画序列通过Animation Locomotion Library插件的DistanceCurveModifier修饰符生成动画曲线（计算出动画本身的位移数据）

    - 两种方式实现距离匹配
        - 通过位移速度调整动画播放速率实现， 如奔跑循环动画。
            - set playrate to match speed
        - 通过位移来调整动画显示时间实现
            -启动奔跑的加速过程。
                - 使用序列求值器计算动画帧，通过Advance Time by Distance Matching计算位移到动画序列显示时间的映射
            - 停止运动过程
                - Distance Match to Target


### 姿势扭曲

https://docs.unrealengine.com/5.0/zh-CN/pose-warping-in-unreal-engine/

方向扭曲（Orientation Warping）： 下半身的朝向和运动方向一致

步幅扭曲（Stride Warping）： 动态调整角色的动画步幅来匹配胶囊体移动速度

斜面扭曲（Slope Warping）： 让斜坡和楼梯上的移动动画的更平滑地过渡


- 步幅适配
    - 人物速度和动画的脚步跨距是否匹配
    - 插件： Animation Warping


起跑姿势
    - 是否蹲伏
    - 是否瞄准
    - 与 Local Velocity Direction有关


## 回转运动 （pivot）

突然转向时的过度动画， 例如向左走时， 突然向右走


# GameFeatures

[UOD2021]虚怀若谷-模块化游戏功能框架 | Epic Games 大钊(官方字幕)

https://www.bilibili.com/video/BV1j34y1B7Nf/?spm_id_from=333.337.search-card.all.click&vd_source=05b9e112882cf3fe738863375b088e4c

https://dev.epicgames.com/community/learning/tutorials/rdW2/unreal-engine-how-to-create-a-new-game-feature-plugin-and-experience-in-lyra


1. CoreGame Content 不能引用GameFeatures中的Content，反过来可以引用，方便了GameFeature的模块化开发和移除
2. 当game feature plugin is registered时， CoreGame可以使用Asset Manager来跟踪和找到在引擎Asset Manager和GameFeatureData上指定的Primary Asset Types

插件：
- ModularGameplay 实现AddComponent等功能
- GameFeatures

GameFeature必须放在/Game/Plugins/GameFeatures目录下


开启GameFeature插件
- 时机： 如进入传送门
- 方法： Toggle Game Feature Plugin
- Set Game Feature Active

GameFeature Actions
- Add Components
    - Actor要支持Add Component操作， 需要调用Game Framework Component Manager -> Add Receiver
- 

GameFeature 状态
- Loaded
- Registered
- Active
- 

激活GameFeature的方法
1. GameFeaturesSubsystem c++
2. 控制台命令
    - ListGameFeaturePlugins
    - LoadGameFeaturePlugin <name>
    - DeactiveGameFeaturePlugin <name>

控制台通过ListGameFeaturePlugins查看GameFeature的当前状态

Lyra何时激活ShooterCore， ShooterMaps这两个GameFeature？


框架原理
![](media/gamefeature_subsystem.png)
- UGameFeatureSubsystem 管理插件的加载，激活等
- Policy 哪些GameFeature加载，哪些忽略


ULyraGameFeaturePolicy

Source\LyraGame\GameFeatures\LyraGameFeaturePolicy.h


# CommonUserSubsystem

数据对象
- UCommonSession_HostSessionRequest： MapID/OnlineMode/MaxPlayerCount/ExtraArgs

API
- Login for Online Play 打开地图时需要用户登录
- Host Session ： 创建游戏
    - ECommonSessionOnlineMode::Offline 如果是创建离线模式， 通过ServerTravel方式打开地图
    - online模式，通过CreateSession来打开地图


# Lyra 启动分析


- ULyraExperienceManagerComponent::OnExperienceLoadComplete
    - ULyraExperienceManagerComponent::OnExperienceFullLoadCompleted


- ALyraPlayerState::OnExperienceLoaded
    - ALyraGameMode::GetPawnDataForController


# 游戏模式 LyraUserFacingExperienceDefinition

大厅模式
- LyraUserFacingExperienceDefinition'/Game/System/Playlists/DA_Frontend.DA_Frontend'

占点模式
- LyraUserFacingExperienceDefinition'/ShooterMaps/System/Playlists/DA_Convolution_ControlPoint.DA_Convolution_ControlPoint'
- LyraUserFacingExperienceDefinition'/ShooterMaps/System/Playlists/DA_Expanse_TDM.DA_Expanse_TDM'

## 占点模式

- LyraUserFacingExperienceDefinition
    - 位置：LyraUserFacingExperienceDefinition'/ShooterMaps/System/Playlists/DA_Convolution_ControlPoint.DA_Convolution_ControlPoint'
    - Map ID
        - World'/ShooterMaps/Maps/L_Convolution_Blockout.L_Convolution_Blockout'
    - Experience ID
        - 位置：Blueprint'/ShooterCore/Experiences/B_LyraShooterGame_ControlPoints.B_LyraShooterGame_ControlPoints'
    

Experience分析

人物配置（Default Pawn Data）: LyraPawnData'/ShooterCore/Game/HeroData_ShooterGame.HeroData_ShooterGame'

UI配置：

团队分数UI
- (TagName="HUD.Slot.TeamScore") 
- WidgetBlueprint'/ShooterCore/ControlPoint/UI/W_CPScoreWidget.W_CPScoreWidget'

占点状态UI
- (TagName="HUD.Slot.ModeStatus")
- WidgetBlueprint'/ShooterCore/ControlPoint/UI/W_ControlPointStatusWidget.W_ControlPointStatusWidget'

能力配置（Add Abilities）

向LyraPlayerState添加能力集：AbilitySet_ControlPoint

LyraAbilitySet'/ShooterCore/ControlPoint/AbilitySet_ControlPoint.AbilitySet_ControlPoint'

- GA_ShowLeaderboard_CP 展示分数面板能力
    - Blueprint'/ShooterCore/ControlPoint/GA_ShowLeaderboard_CP.GA_ShowLeaderboard_CP'
    - 绑定(TagName="InputTag.Ability.ShowLeaderboard")
- GA_AutoRespawn 重生能力
    - Blueprint'/ShooterCore/Game/Respawn/GA_AutoRespawn.GA_AutoRespawn'


组件配置（Add Components）

向LyraGameState添加组件，控制游戏模式

- B_TeamSetup_TwoTeams 建立团队组件
    - Blueprint'/ShooterCore/Game/B_TeamSetup_TwoTeams.B_TeamSetup_TwoTeams'
    - 继承自LyraTeamCreationComponent
- B_TeamSpawningRules 团队出生规则组件
    - Blueprint'/ShooterCore/Game/B_TeamSpawningRules.B_TeamSpawningRules'
- B_PickRandomCharacter
    - Blueprint'/Game/Characters/Cosmetics/B_PickRandomCharacter.B_PickRandomCharacter'


# lyra subsystem

## Lyra Team Subsystem

- CompareTeams 比较actor是否为同组玩家， 例如在GA_Melee中进行伤害判定


## LyraGamePhaseSubsystem

ShooterGame.GamePhase.PostGame 游戏结束阶段

- Is Phase Active 例如在B_WeaponSpawner -> Give Weapon 时判断是否为PostGame阶段

- ULyraGamePhaseSubsystem
    - OnBeginPhase
    - OnEndPhase
    - StartPhase
        - GameState_ASC->GiveAbilityAndActivateOnce 通过GameState的ASC组件激活游戏阶段技能
- ULyraGameplayAbility
    - ULyraGamePhaseAbility


# 全局能力 ULyraGlobalAbilitySystem

- GE_PregameLobby
    - Blueprint'/ShooterCore/Experiences/Phases/GE_PregameLobby.GE_PregameLobby'
    - 继承自GE_DamageImmunity_FromGameMode
        - Blueprint'/ShooterCore/Experiences/Phases/GE_DamageImmunity_FromGameMode.GE_DamageImmunity_FromGameMode'
        - GrantedTags 赋予Gameplay.DamageImmunity 伤害免疫效果
    - Gameplay Cue Tags设置GameplayCue.ShooterGame.UserMessage.WaitingForPlayers, 显示等待UI

- GCNL_WaitingForPlayers
    - Blueprint'/ShooterCore/GameplayCues/GCNL_WaitingForPlayers.GCNL_WaitingForPlayers'
    - Gameplay Cue Tag： GameplayCue.ShooterGame.UserMessage.WaitingForPlayers 设置激活该GameplayCue Notify的Tag
    - Widget to Spawn 设置要显示的UI
        - WidgetBlueprint'/ShooterCore/GameplayCues/W_WaitingForPlayers_Message.W_WaitingForPlayers_Message'


# Modular Gameplay

- plugin
    - Modular Gameplay
    - Modular Gameplay Actors

GameFeature插件依赖Modular Gameplay插件

ModularGameplayActors通过UGameFrameworkComponentManager实现组件模块化功能
- UGameFrameworkComponentManager
    - 

- APawn 
    - AModularPawn （ModularGameplayActors插件代码）
        - ALyraPawn

