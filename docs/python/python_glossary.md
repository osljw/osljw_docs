
https://docs.python.org/3/glossary.html

# iterable
- iterable object: with an __iter__() method or with a __getitem__() method
- iter(iterable object) return iterator
- iterator对象需要__next__()方法， iterable object的__iter__()方法一般返回self，因此iterable object一般也需要实现__next__()方法

# iterator
- 需要实现__next__()方法，当没有元素返回时，StopIteration异常
- 需要实现__iter__()方法，返回self， 将自己变为iterable object

# sequence

# generator

一起来写个简单的解释器（5）
http://www.opython.com/1411.html

# site-packages
查看python使用的site-packages位置
```
python -m site
```

PYTHONPATH 会被追加到`sys.path`中， python从`sys.path`指定的列表搜表模块位置

# Token

token数据定义和多字符token解析函数自动生成
Grammar/Tokens -> Tools/scripts/generate_token.py -> Parser/token.c

Python源码分析3 – 词法分析器PyTokenizer
https://blog.csdn.net/ATField/article/details/1439068

- Parser/tokenizer.c
- Parser/tokenizer.h
从字符流解析得到token


Lib/token.py
Lib/tokenize.py

https://www.omegaxyz.com/2019/01/29/nfa2dfa/

有限自动机（DFA）M可以定义为一个五元组，M＝（K，∑，F，S，Z）
- K是一个有穷非空集，集合中的每个元素称为一个状态；
- ∑是一个有穷字母表，∑中的每个元素称为一个输入符号；
- F是一个从K×∑→K的单值转换函数，即F（R，a）＝Q，（R，Q∈K）表示当前状态为R，如果输入字符a，则转到状态Q，状态Q称为状态R的后继状态, 每个状态对字母表中的任一输入符号，最多只有一个后继状态；
- S∈K，是惟一的初态；
- Z∈K，是一个终态集。

不确定有限自动机（NFA）M可以定义为一个五元组，M＝（K，∑，F，S，Z），其中：

- k是一个有穷非空集，集合中的每个元素称为一个状态；
- ∑是一个有穷字母表，∑中的每个元素称为一个输入符号；
- F是一个从K×∑→K的子集的转换函数；
- SK，是一个非空的初态集；
- ZK，是一个终态集。

不确定有限自动机NFA与确定有限自动机DFA的主要区别是：

（1）NFA的初始状态S为一个状态集，即允许有多个初始状态；
（2）NFA中允许状态在某输出边上有相同的符号，即对同一个输入符号可以有多个后继状态。即DFA中的F是单值函数，而NFA中的F是多值函数。


Design of the CPython Compiler
https://legacy.python.org/dev/peps/pep-0339/

- Parser/Python.asdl <- an abstraction over Abstract Syntax Trees


recursive-descent parser 

python 语法描述

Grammar/python.gram
- extended BNF
- * for repetition
- + for at-least-once repetition
- [] for optional parts
- | for alternatives
- () for grouping

```
MSTART: (NEWLINE | RULE)* ENDMARKER
RULE: NAME ':' RHS NEWLINE
RHS: ALT ('|' ALT)*
ALT: ITEM+
ITEM: '[' RHS ']' | ATOM ['*' | '+']
ATOM: NAME | STRING | '(' RHS ')'
```

Grammar/python.gram -> pgen -> Include/graminit.h, Python/graminit.c
Grammar/python.gram -> pegen -> Parser/parser.c

pgen从Grammar语法生成的graminit c代码文件包含了DFA transition diagram， DFA(Deterministic Finite Automaton)
python3.8 使用最新的pegen，pegen生成的代码Parser/parser.c可以解析符合Grammar/python.gram定义的语法


pgen
  - LL(1) 解析（只使用单一的前向标记符）， 可以产生空字符串的语法

Parser/Python.asdl -> Parser/asdl_c.py && Parser/asdl.py && -> [Include/Python-ast.h | Python/Python-ast.c]
Parser/asdl_c.py 和 Parser/asdl.py脚本从asdl定义语言生成c文件，包含了ast相关的数据结构


https://eli.thegreenplace.net/2014/06/04/using-asdl-to-describe-asts-in-compilers
https://github.com/eliben/code-for-blog/tree/master/2009/py_rd_parser_example
