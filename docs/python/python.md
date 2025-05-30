
# python


# package and module

https://docs.python.org/3/tutorial/modules.html


module: A module is a file containing Python definitions and statements. The file name is the module name with the suffix .py appended
package： 用于组织module， package对应目录名称


sys.path 路径是如何决定的

```
The directory containing the input script (or the current directory when no file is specified).

PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).

The installation-dependent default.
```



# 内存泄漏 memory leak 定位
```
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from memory_profiler import profile

data_array = np.random.random_sample((1, 1024))
tf_array = tf.constant(data_array, dtype=tf.float32)

input = tf.keras.Input((1, 1024))
hidden_layer = tf.keras.layers.Dense(1024)(input)
output = tf.keras.layers.Dense(1)(hidden_layer)
model = tf.keras.Model(inputs=[input], outputs=[output])

pred = model([tf_array])
print(pred)


@profile
def func():
    export_path = "temp_export"
    tf.saved_model.save(model, export_path)
    imported = tf.saved_model.load(export_path)


for i in tqdm(range(1000000), total=1000000):
    func()
```


# python 工程



# 描述符

```py
class Test:
    a = 11

t = Test()
t.a = 22
print("t.a = {}, Test.a = {}".format(t.a, Test.a))
```

```
t.a = 22, Test.a = 11
```
对象属性和类属性不同

对象属性的访问顺序：
1. getattribute()， 无条件调用
2. 数据描述符：由 ① 触发调用 （若人为的重载了该 getattribute() 方法，可能会调职无法调用描述符）
3. 实例对象的字典（若与描述符对象同名，会被覆盖哦）
4. 类的字典
4. 非数据描述符
5. 父类的字典
6. getattr() 方法


# python 打包

Inno Setup 

.iss 文件配置

Nuitka 是一个 ​​Python 编译器​​，可以将 Python 代码转换为高度优化的 ​​C/C++ 扩展模块​​ 或 ​​独立可执行文件​​（.exe、.app、.bin 等）。相比 PyInstaller、Py2exe 等打包工具，Nuitka 提供更好的性能、更小的体积和更强的兼容性。