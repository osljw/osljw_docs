
# Graph

# Graph 创建
tensorflow\python\framework\ops.py
```python
@tf_export("Graph")
class Graph(object):

    def as_default(self):
```
Graph的as_default方法会创建context， 在该context中定义的tensor和op都会交由该Graph进行管理

