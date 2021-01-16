
# CPython 


Grammar
- Backus-Naur Form (BNF)
- grammar file: Extended-BNF (EBNF) 
- pgen: EBNF -> Non-deterministic Finite Automaton (NFA) -> Deterministic Finite Automaton (DFA).

Tokens
- Lib/tokenize.py `python -m tokenize`


CPython compiler 
Python Interpreter

# GIL
- python字节码的执行过程支持线程抢占式，每隔1000条字节码或者15ms会调度线程
- 一条字节码执行的过程不会被打断， 是线程安全的， 如list.sort()函数会被编译成一条字节码
https://emptysqua.re/blog/grok-the-gil-fast-thread-safe-python/