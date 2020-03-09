# sqlite

线程安全
https://www.sqlite.org/threadsafe.html


# No module named _sqlite3

找到_sqlite3.so的位置， 例如其他sqlite3工作正常的机器，或者conda
```
find /usr/local -name _sqlite3.so
```
拷贝到python的lib-dynload目录下
```
python -c "import sys; print(sys.path)"
```
