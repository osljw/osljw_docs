


# Makefile


## 隐含规则
%.o:%.cpp
    @echo "[^[[1;32;40mBUILD^[[0m][Target:'^[[1;32;40m$<^[[0m']"
    @$(CXX) $(CXXFLAGS) $(INC_DIR) -c $< -o $@

eg:
$< 表示main.cpp
$@ 表示main.o

## 自动变量
$@ 目标
$< 规则的第一个依赖目标

## 
使用shell命令找到cpp文件
$(shell find . -name "*.cpp")

将*.cpp文件替换成*.o文件
$(patsubst %.cpp,%.o, $(cpp_files))


# 宏
宏展开
```
gcc -E -P input.cpp -o output.cpp
```

代码格式化
```
clang-format -i output.cpp -style=google
```


npm clang-format install
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
```
nvm 装好后需要退出再重新登录服务器，重新加载环境变量。

```
nvm install --lts
npm install -g clang-format
```

项目根目录生成格式配置文件
```
clang-format -style=google -dump-config > .clang-format
```


`shift + option + F` 格式化文件


```
初始化列表格式控制
ConstructorInitializerIndentWidth: 4
ConstructorInitializerAllOnOneLineOrOnePerLine: true

BreakConstructorInitializersBeforeComma: false
BreakConstructorInitializers: AfterColon
```


```
Language: Cpp
BasedOnStyle: LLVM

AccessModifierOffset: -4
# 参数换行如何对齐：Align/DontAlign/AlwaysBreak
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
# 换行连接符\位置，只能是true和false
# AlignEscapedNewlines: DontAlign (6.0使用该项)
AlignEscapedNewlinesLeft: true
AlignOperands: true
AlignTrailingComments: false
AllowAllParametersOfDeclarationOnNextLine: true
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
# 短函数是否换行：None/Inline/Empty/All/InlineOnly(6.0支持该类型)
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
AlwaysBreakAfterDefinitionReturnType: None
AlwaysBreakAfterReturnType: None
AlwaysBreakBeforeMultilineStrings: false
AlwaysBreakTemplateDeclarations: true
BinPackArguments: true
BinPackParameters: true
# 大括号换行，只有当BreakBeforeBraces设置为Custom时才有效
BraceWrapping:   
    AfterClass:            true
    AfterControlStatement: false
    AfterEnum:             true
    AfterFunction:         true
    AfterNamespace:        false
    AfterObjCDeclaration:  true
    AfterStruct:           true
    AfterUnion:            true
    BeforeCatch:           false
    BeforeElse:            true
    IndentBraces:          false
BreakBeforeBinaryOperators: All
BreakBeforeBraces: Custom
BreakBeforeTernaryOperators: true
BreakConstructorInitializersBeforeComma: false
BreakStringLiterals: false
# 一行列数限制，0不限制
ColumnLimit: 120
CommentPragmas: '^ IWYU pragma:'
ConstructorInitializerAllOnOneLineOrOnePerLine: false
ConstructorInitializerIndentWidth: 4
ContinuationIndentWidth: 8
Cpp11BracedListStyle: true
DerivePointerAlignment: false
DisableFormat: false
ExperimentalAutoDetectBinPacking: false
ForEachMacros:   [ foreach, Q_FOREACH, BOOST_FOREACH ]
IncludeCategories: 
    - Regex:           '^"(llvm|llvm-c|clang|clang-c)/'
      Priority:        2
    - Regex:           '^(<|"(gtest|isl|json)/)'
      Priority:        3
    - Regex:           '.*'
      Priority:        1
IncludeIsMainRegex: '$'
IndentCaseLabels: true
IndentWidth: 4
IndentWrappedFunctionNames: false
KeepEmptyLinesAtTheStartOfBlocks: true
MacroBlockBegin: ''
MacroBlockEnd:   ''
# 最大保留连续空行数
MaxEmptyLinesToKeep: 2
NamespaceIndentation: None
PenaltyBreakBeforeFirstCallParameter: 19
PenaltyBreakComment: 300
PenaltyBreakFirstLessLess: 120
PenaltyBreakString: 1000
PenaltyExcessCharacter: 1000000
PenaltyReturnTypeOnItsOwnLine: 60
# 指针*位置：Left/Right/Middle
PointerAlignment: Left
ReflowComments: false
# 是否排序include
SortIncludes: false
SpaceAfterCStyleCast: false
SpaceAfterTemplateKeyword: false
SpaceBeforeAssignmentOperators: true
SpaceBeforeParens: ControlStatements
SpaceInEmptyParentheses: false
SpacesBeforeTrailingComments: 1
SpacesInAngles: false
SpacesInContainerLiterals: false
SpacesInCStyleCastParentheses: false
SpacesInParentheses: false
SpacesInSquareBrackets: false
# C++标准：Cpp03/Cpp11/Auto
Standard: Cpp11
TabWidth: 4
UseTab: Never
```