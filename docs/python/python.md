
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