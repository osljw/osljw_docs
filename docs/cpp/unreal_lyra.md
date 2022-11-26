
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

## UI加载
Experience 中设置要加载的UI

- B_LyraFrontEnd_Experience 
    - B_LyraFrontendStateComponent 
        - W_LyraStartup 
        - W_LyraFrontEnd

B_LyraFrontendStateComponent位置：
Blueprint'/Game/UI/B_LyraFrontendStateComponent.B_LyraFrontendStateComponent'

ULyraFrontendStateComponent继承自UGameStateComponent

W_LyraFrontEnd位置为： WidgetBlueprint'/Game/UI/Menu/W_LyraFrontEnd.W_LyraFrontEnd'

W_LyraFrontEnd 点击Play Lyra后， 会创建显示experiences的界面

WidgetBlueprint'/Game/UI/Menu/Experiences/W_ExperienceSelectionScreen.W_ExperienceSelectionScreen'

- 显示experiences选择界面
    - 单机玩
    - Host
    - Browse

WidgetBlueprint'/Game/UI/Menu/Experiences/W_HostSessionScreen.W_HostSessionScreen'

用户操作后会确定LyraUserFacingExperienceDefinition， 根据这个信息有common session subsystem创建游戏会话



背景加载：
LyraStarterGame/Content/Environments/B_LoadRandomLobbyBackground.uasset

人物蓝图 （ShooterCore 插件）
/ShooterCore/Game/B_Hero_ShooterMannequin.B_Hero_ShooterMannequin'

武器蓝图
/ShooterCore/Weapons/Pistol/B_WeaponInstance_Pistol.B_WeaponInstance_Pistol


- Experience
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