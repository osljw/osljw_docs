---
layout:     post
title:      "Tensorflow Keras"
subtitle:   "Tensorflow Keras"
date:       2019-02-27 19:00:00
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 学习笔记
---

# keras session
当设置log_device_placement=True时
```
import tensorflow as tf
import tensorflow.keras.backend as K

config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)config.allow_soft_placement = True  # to log device placement (on which device the operation ran)
sess = tf.Session(config=config)
K.set_session(sess)  # set this TensorFlow session as the default session for Keras
```

# keras compile
class Model(Netword)
https://github.com/keras-team/keras/blob/master/keras/engine/training.py
model compile 被调用时，主要完成loss function， optimizer， metrics部分的定义
仅仅使用model进行predict时， 不需要进行compile
当改变变量trainable状态后再次进行训练之前， 也需要进行compile

# keras fit_generator, train_on_batch
https://github.com/keras-team/keras/blob/master/keras/engine/training_generator.py
fit_generator 内部调用的是train_on_batch完成batch数据的训练

fit_generator, train_on_batch的时候， 当self.train_function为None时（即第一次train_on_batch时）， 会在_make_train_function中调用optimizer的get_updates， 定义变量的梯度更新参数
train_on_batch
  _make_train_function # 从optimizer中获得梯度更新op， 构建Keras function， train_function
  outputs = self.train_function(ins) #使用train_function, 把输入变成输出


# keras 变量共享
keras是通过面向对象来共享变量的， 在对象的build方法中定义变量(使用tf.Variable而不是tf.get_variable), 在对象的call方法中使用变量

# keras batch 训练

# keras Input
```
x = Input(shape=(2,), dtype='string')
y = x
model = tf.keras.models.Model(x, y)
sess = tf.Session()
with sess.as_default():
  sess.run(tf.global_variables_initializer())
  print(sess.run(y, feed_dict={x:[[1,-5]]}))

ret = model.predict(data)

https://stackoverflow.com/questions/38972380/keras-how-to-use-fit-generator-with-multiple-outputs-of-different-type
x = Convolution2D(8, 5, 5, subsample=(1, 1))(image_input)
x = Activation('relu')(x)
x = Flatten()(x)
x = Dense(50, W_regularizer=l2(0.0001))(x)
x = Activation('relu')(x)

output1 = Dense(1, activation='linear', name='output1')(x)
output2 = Dense(1, activation='linear', name='output2')(x)

model = Model(input=image_input, output=[output1, output2])
model.compile(optimizer='adam', loss={'output1': 'mean_squared_error', 'output2': 'mean_squared_error'})

batch_generator(x, y, batch_size):
        ....transform images
        ....generate batch batch of size: batch_size 
        yield(X_batch, {'output1': y1, 'output2': y2} ))

model.fit_generator(batch_generator(X_train, y_train, batch_size))
```

# keras embedding
输入到Embedding层的id索引需要在[0, input_dim) 区间内

# keras GPU

## keras gpu 内存使用大小限制
```python
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras
```

## keras multi GPU
https://keras.io/utils/#multi_gpu_model
模型能够在GPU上放下， 使用数据并行
使用multi_gpu_model构建


# keras layers
keras layers 的call方法必须含有inputs参数， inputs参数为keras tensor或者keras tensor list，
keras tensor包含_keras_history属性， Layer类的__call__方法调用子类的call方法后， 会根据inputs里的_keras_history为子类返回的tensor添加_keras_history.


# model weights
keras/engine/base_layer.py
add_weight方法使用K.variable定义变量，
regularizer参数控制是否使用正则化


```
for layer in model.layers:
    print("weights:", layer.get_weights())
```

