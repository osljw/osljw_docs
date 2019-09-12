---
layout:     post
title:      "data input"
date:       2018-11-19 19:00:00
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 学习笔记
---

# Data Input


继承结构
- DatasetV2
- DatasetSource
    - TensorDataset
    - TensorSliceDataset
- ConcatenateDataset
- UnaryDataset
    - BatchDataset
    - MapDataset


## structure 

tensorflow.python.data.util.structure

- RaggedTensorStructure
- SparseTensorStructure

## test

tensorflow/python/data/experimental/kernel_tests

功能实现代码

tensorflow/python/data/util/structure.py


# dataset 使用

使用生成器 

注意生成器yield时候的格式， 
- 当yield整数i时， dataset取batch后形成的shape为(batch_size,)
- 当yield列表[i]时，dataset取batch后形成的shape为(batch_size,1)

yield返回tuple类型
```
def test_gen():
    i = 0 
    while True:
        i += 1
        x = [i+1, i+2, i+3]
        y = [i] 
        yield (x, y)

ds = tf.data.Dataset.from_generator(test_gen, (tf.int64, tf.int64)).batch(2)
it = iter(ds)
print(next(it))
```

yield返回dict类型
```
def captcha_gen_one():
    i = 0 
    while True:
        i += 1
        x = [i+1, i+2, i+3]
        y = [i] 
        yield {"X":x, "Y":y}

ds = tf.data.Dataset.from_generator(captcha_gen_one, {"X":tf.int64, "Y":tf.int64}).batch(2)
it = iter(ds)
print(next(it))
```

