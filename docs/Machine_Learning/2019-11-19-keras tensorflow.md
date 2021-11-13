
# keras data

minist numpy data
```python
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
iterator = iter(train_dataset)
x, y = next(iterator)
```

# keras session
当设置log_device_placement=True时
```python
import tensorflow as tf
import tensorflow.keras.backend as K

config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)config.allow_soft_placement = True  # to log device placement (on which device the operation ran)
sess = tf.Session(config=config)
K.set_session(sess)  # set this TensorFlow session as the default session for Keras
```

# keras functional model

In the functional API, models are created by specifying their inputs and outputs in a graph of layers. That means that a single graph of layers can be used to generate multiple models.


Model
- _is_graph_network 是否为图网络
- save_weights： 调用self._trackable_saver.save函数保存checkpoint
- load_weights: 支持延迟恢复Delayed restorations


## tf.keras.Input
```
x = tf.keras.Input(shape=(224, 224, 3), name="input_image")

x = tf.keras.Input(shape=(None, None, 3), name="input_image")
```
- 使用name方便后续训练时feed data
- 

## 中间层
### tf.keras.layers.Conv2D

### tf.keras.layers.GRU
- return_sequences
- go_backwards

### tf.keras.layers.TimeDistributed
在某个axis上，应用同一个层， axis=0为batch_size, axis=1为timesteps

### tf.keras.layers.Bidirectional

# keras model layer

获取所有层的名称name
```
[x.name for x in base_model.layers]
```

将模型的层按照名称变为python中的变量
```python
for x in yolo.layers:
    globals()[x.name] = yolo.get_layer(x.name)
```


# keras compile
```python
# keras/engine/training.py
class Model(Netword)
```
model compile 被调用时，主要完成loss function， optimizer， metrics部分的定义
仅仅使用model进行predict时， 不需要进行compile

当改变变量trainable状态后再次进行训练之前， 也需要进行compile

# keras loss

keras loss函数需要两个参数y_true 和 y_pred, y_pred对应的是model的outputs参数， model进行compile时并不知道label的信息， y_true的rank会被认为和y_pred一样
- 在自定义loss函数中使用tf.reshape将y_true变换为需要的shape
- 将loss函数包裹形成层直接放到model中，定义一个无用的loss函数
- 多目标输出时， 每个输出节点会使用相同的损失函数，或者通过dict配置的损失函数，想要在所用目标上使用一个损失函数，可以把多目标`Concatenate`为一个目标
  

CTC (Connectionist Temporal Classification)

# keras metrics

tf.keras.metrics.Metric
- `__init__` 定义metric计算是需要的变量
- `update_state` 接受y_true和y_pred输入，来计算metric
- `result` 返回metric

在每个train或者valid epoch开始时，keras会使用model.reset_metrics()

在compile中设定metrics参数， 每个metrics

tensorflow/python/keras/engine/training_utils.py


- Metric
  - Reduce
    - MeanMetricWrapper
      - Mean
    - Sum

# keras callbacks

tf.keras.callbacks.Callback

metrics的计算结果如何传递给callback，

tensorflow/python/keras/engine/training_v2.py
```python
      with training_context.on_start(
          model, callbacks, use_sample, verbose, mode):
        # TODO(scottzhu): Handle TPUStrategy training loop
        with training_context.on_epoch(0, mode) as epoch_logs:
          model.reset_metrics()
          result = run_one_epoch(
              model,
              data_iterator,
              execution_function,
              dataset_size=adapter.get_size(),
              batch_size=adapter.batch_size(),
              strategy=strategy,
              steps_per_epoch=steps,
              num_samples=total_samples,
              mode=mode,
              training_context=training_context,
              total_epochs=1)
          cbks.make_logs(model, epoch_logs, result, mode)
```
`training_context.on_epoch`负责构建一个epoch的上下文环境，调用callback函数
`run_one_epoch` 返回的是The loss and metric value from the model.

tensorflow/python/keras/callbacks.py
```python
def make_logs(model, logs, outputs, mode, prefix=''):
  """Computes logs for sending to `on_batch_end` methods."""
  metric_names = model.metrics_names
  if mode in {ModeKeys.TRAIN, ModeKeys.TEST} and metric_names:
    for label, output in zip(metric_names, outputs):
      logs[prefix + label] = output
  else:
    logs['outputs'] = outputs
  return logs
```

# keras fit
支持的数据格式

根据输入数据的不同，选择不同的train loop

- context.executing_eagerly() -> training_v2.Loop()
- self._distribution_strategy -> training_distributed.DistributionSingleWorkerTrainingLoop()


tensorflow/python/keras/engine/training_v2.py
```
class Loop(training_utils.TrainingLoop):
  def fit(
      self, model, x=None, y=None, batch_size=None, epochs=1, verbose=1,
      callbacks=None, validation_split=0., validation_data=None, shuffle=True,
      class_weight=None, sample_weight=None, initial_epoch=0,
      steps_per_epoch=None, validation_steps=None, validation_freq=1, **kwargs):
```



处理一个epoch的数据
```
def run_one_epoch(model,
                  iterator,
                  execution_function,
                  dataset_size=None,
                  batch_size=None,
                  strategy=None,
                  steps_per_epoch=None,
                  num_samples=None,
                  mode=ModeKeys.TRAIN,
                  training_context=None,
                  total_epochs=None):
```



- make_train_function
  - def train_function(iterator)
    - train_step(data)

fit或train_on_batch调用make_train_function获得训练函数， make_train_function返回train_function训练函数， train_function函数调用train_step实现训练

# keras fit trace twice
- train_function

run_eagerly = False的情况下， keras生成的train_function会被tf.function进行装饰， train_function第一次被调用时, 会导致trace两次

1. tensorflow/python/eager/def_function.py,  Function的_call方法中会调用_initialize方法, 会发生一次trace
2. Function的_initialize方法调用时， 导致_created_variables不为None， 则_call方法会继续调用Function的_stateless_fn， 再次发生一次trace


发生一次trace
```python
def f(a, b):
    print("test trace")
    return a + b

tf.function(f)(1, 2)
```


发生两次trace
```python
v = None
def f(a, b):
    print("test trace")
    global v
    if v is None:
        v = tf.Variable(0)
    return a + b

tf.function(f)(1, 2)
```



# keras fit_generator, train_on_batch
https://github.com/keras-team/keras/blob/master/keras/engine/training_generator.py
fit_generator 内部调用的是train_on_batch完成batch数据的训练

fit_generator, train_on_batch的时候， 当self.train_function为None时（即第一次train_on_batch时）， 会在_make_train_function中调用optimizer的get_updates， 定义变量的梯度更新参数
train_on_batch
```
  _make_train_function # 从optimizer中获得梯度更新op， 构建Keras function， train_function
  outputs = self.train_function(ins) #使用train_function, 把输入变成输出
```


# keras 变量共享
keras是通过面向对象来共享变量的， 在对象的build方法中定义变量(使用tf.Variable而不是tf.get_variable), 在对象的call方法中使用变量

# keras batch 训练

# keras Input
```python
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

## keras 禁止使用gpu

```python
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
import tensorflow as tf
```

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

```
Each time a layer is connected to some new input,
a node is added to `layer._inbound_nodes`.
Each time the output of a layer is used by another layer,
a node is added to `layer._outbound_nodes`. 

# 在执行Layer的__call__调用时， 会创建一个Node对象表示这次调用的输入， 
# 把这个Node对象新增到这个Layer的_inbound_nodes列表中表示这层发现了新的输入
# 对这层的所有输入keras tensor， 由其携带的_keras_history信息定位到是哪些层输出的
# 更新这些层的_outbound_nodes
# Wire up Node to Layers.
self.layer._inbound_nodes.append(self)
for kt in self.keras_inputs:
  inbound_layer = kt._keras_history.layer
  if inbound_layer is not None:  # `None` for `Input` tensors.
    inbound_layer._outbound_nodes.append(self)

# Set metadata on outputs.
node_index = len(self.layer._inbound_nodes) - 1
for i, tensor in enumerate(nest.flatten(outputs)):
  tensor._keras_history = KerasHistory(
      layer=layer, node_index=node_index, tensor_index=i)
```

# model weights
keras/engine/base_layer.py
add_weight方法使用K.variable定义变量，
regularizer参数控制是否使用正则化


```
for layer in model.layers:
    print("weights:", layer.get_weights())
```

> load_weights
- TensorFlow format
  - by_name=False (topological loading)
  - by_name=True (不支持)
- HDF5 format
  - by_name=False (topological loading)
  - by_name=True ()

使用Model的_trackable_saver从checkpoint中restore
  
# keras SavedModel

1. Sequential models or Functional models

```python
# Export the model to a SavedModel
keras.experimental.export_saved_model(model, 'path_to_saved_model')

# Recreate the exact same model
new_model = keras.experimental.load_from_saved_model('path_to_saved_model')
```



2. Subclassed models
- need call() method
- subclassed model that has never been used cannot be saved. (可以使用build(input_shape=)方法来确定模型的shape)
- the code of the model subclass to load model

使用model.save_weights 和model.load_weights , 由于自定义层的序列化问题避免使用model.save()


# loss 损失函数

- tf.keras.losses.BinaryCrossentropy


loss的实际计算过程(Loss.__call__函数)
1. `tf.keras.losses.binary_crossentropy(y_true, y_pred)` 由y_true和y_pred得到loss, 会对最后一维平均聚合
2. `compute_weighted_loss(losses, sample_weight, reduction=self._get_reduction())`


示例：
y_true: (num_target, batch_size, 1)
y_pred: (num_target, batch_size, 1)
sample_weight: (num_target, batch_size, 1)

1. `loss = binary_crossentropy(y_true, y_pred)` loss 为(num_target, batch_size)
2. `loss = compute_weighted_loss(losses, sample_weight, reduction.NONE)`  loss 为(num_target, batch_size), 这步进行了weighted_losses = tf.math.multiply(losses, sample_weight)
2. `loss = compute_weighted_loss(losses, sample_weight, reduction.SUM)`  loss 为(num_target, batch_size), 这步进行了weighted_losses = tf.math.multiply(losses, sample_weight) 和 tf.reduce_sum(weighted_losses)

总结： 当`reduction`为`NONE`时， 只对最后一维进行均值聚合， 其余reduction返回的都为标量损失



优化器使用求和损失 vs 平均损失


> tf.keras.losses.CategoricalCrossentropy

batch softmax

```
# 对角线上score为样本分数
scores = tf.linalg.matmul(
    query_embeddings, candidate_embeddings, transpose_b=True)


num_queries = tf.shape(scores)[0]
num_candidates = tf.shape(scores)[1]

labels = tf.eye(num_queries, num_candidates)

loss = self._loss(y_true=labels, y_pred=scores, sample_weight=sample_weight)
```


> tf.keras.backend.ctc_batch_cost

```
tf.keras.backend.ctc_batch_cost(
    y_true,
    y_pred,
    input_length,
    label_length
)
```
- y_true: (samples, max_string_length)
- y_pred: (samples, time_steps, num_categories)
- input_length: (samples, 1)
- label_length: (samples, 1)

y_pred 为模型输出， 其他三个参数一般为模型输入



# tf.distribute.MirroredStrategy
strategy 负责变量的replica和reduce同步

reduce过程：
1. strategy.reduce()
2. StrategyBase.reduce()
3. StrategyExtended._reduce()
4. `StrategyExtended.reduce_to()` destinations 为"/device:CPU:0"
5. `MirroredExtended._reduce_to()` 


# keras export

模型导出h5失败， 变量名重复， 使用如下代码打印变量名称
```
for i, w in enumerate(model.weights): 
    print("model_debug:", i, w.name)
```