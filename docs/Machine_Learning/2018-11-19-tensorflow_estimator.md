---
layout:     post
title:      "Tensorflow Estimator"
subtitle:   "Tensorflow Estimator 学习"
date:       2018-11-19 19:00:00
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 学习笔记
---

# Estimator
模型从checkpoint恢复后， 不会运行init_op 或者调用init_fn

Running local_init_op
tensorflow/python/training/session_manager.py
prepare_session
_try_run_local_init_op


# Dataset

# Feature Column

# loss 
https://stackoverflow.com/questions/47034888/how-to-choose-cross-entropy-loss-in-tensorflow


# input
输入方式 
    dataset
    generator
输入类型
    数值列， size
    embedding列

    embedding concat


# learning rate 学习速率
tf.train.exponential_decay
decayed_learning_rate = learning_rate *
                        decay_rate ^ (global_step / decay_steps)

learning_rate = 0.05
decay_rate = 1.0

# initializer 初始化
tf.glorot_uniform_initializer()

# regularizer 正则化
l1 
tf.contrib.layers.l1_regularizer(l1_reg)
l2
tf.contrib.layers.l2_regularizer(l2_reg)

l1=0.1, l2=0.1 too big!!!!!!!

# dropout
tf.layers.dropout

(无)

# batch_normalization

训练阶段设置training=False， batch_normalization的mean and variance don't get updated， gamma and beta still get updated.

https://stackoverflow.com/questions/50047653/set-training-false-of-tf-layers-batch-normalization-when-training-will-get-a


# estimator train_op
dnn代码：
_dnn_model_fn 
提供train_op_fn 给head， train_op_fn中构建多个train_op

head 中调用train_op_fn 返回train_op, 
1 修改canned/head.py  去掉train_op = _append_update_ops(train_op)

model_fn.py 中 _TPUEstimatorSpec会保存train_op
1 修改_check_is_tensor_or_operation， 

estimator
_train_with_estimator_spec 中
      while not mon_sess.should_stop():
        _, loss = mon_sess.run([estimator_spec.train_op, estimator_spec.loss])
