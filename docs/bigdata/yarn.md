
# Yarn

- Client
- ResourceManager
- NodeManager (管理多个Container)
- ApplicationMaster


A Yarn Container can have only one Spark Executor, but 1 or indeed more Cores can be assigned to the Executor.

spark executor 对应一个jvm进程

一个executor可以并行执行多个task，实际上一个executor是一个进程，task是executor里的一个线程。

一个task至少要独占executor里的一个虚拟核心vcore。

一个executor里的核心数由spark-submit的`--executor-cores`参数指定。

一个task要占用几个核心，可以由`.config("spark.task.cpus", 1)`配置，默认是1即一个task占用一个vcore。

一个partition对应一个task

# tensorflow on spark


1. 通过rdd的foreachPartition在每个executor上启动自定义函数的执行
2. 在自定义函数中开启网络服务