
# lex 词法分析器
flex - the fast lexical analyser generator

使用有限状态机（DFA）将源码翻译为token 序列

# 语法分析器
- N - 有限个非终结符的集合
- $\sigma$ - 有限个终结符的集合
- P - 有限个生成规则的集合
- S - 开始符号

自顶向下：LL 文法
自底向上：LR(0)、SLR、LR(1) 和 LALR(1) 
