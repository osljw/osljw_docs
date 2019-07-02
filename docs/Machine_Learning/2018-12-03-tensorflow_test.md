---
layout:     post
title:      "tensorflow test"
date:       2018-11-19 19:00:00
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 学习笔记
---

```
import tensorflow as tf
x = tf.Variable(0.0)
y = tf.constant(1.0)
loss = y-x
opt_op = tf.train.GradientDescentOptimizer(learning_rate=0.1)
train_op = opt_op.minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10):
        _, loss, x = sess.run([train_op, loss, x])
        print("step:{}, loss:{}, x:{}".format(i, loss, x))
```