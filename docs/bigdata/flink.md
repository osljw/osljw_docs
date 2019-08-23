

https://training.ververica.com/lessons/stateless.html

# Flink

```
# local flink cluster
bin/start-cluster.sh
bin/stop-cluster.sh
```

# sbt

```
# windows git-bash 显示存在问题，使用windows cmd
# 新建工程
sbt new tillrohrmann/flink-project.g8

# 编译
sbt clean assembly

# 运行
sbt run
# 带参数的sbt run
sbt "run -f application.conf"
```


## flink任务
```
# 任务提交和恢复， -s指定savepoint路径， -c指定入口主类
flink run 


```


```scala
// get an ExecutionEnvironment
val env = StreamExecutionEnvironment.getExecutionEnvironment
// configure event-time processing
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
```

## kafka
```scala
import java.util.Properties
import org.apache.flink.streaming.api.scala._
import org.apache.flink.api.common.serialization.SimpleStringSchema;
//import org.apache.flink.streaming.connectors.kafka.{FlinkKafkaConsumer08, FlinkKafkaProducer08}
import org.apache.flink.streaming.connectors.kafka.{FlinkKafkaConsumer, FlinkKafkaProducer}


object Job {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment

    val properties = new Properties()
    properties.setProperty("bootstrap.servers", "ip1:9092,ip2:9092")
    // only required for Kafka 0.8
    //properties.setProperty("zookeeper.connect", "ip:2181")
    properties.setProperty("group.id", "test")

    // val input_stream = env
    //     .addSource(new FlinkKafkaConsumer08[String]("topic_name", new SimpleStringSchema(), properties))

    val input_stream = env.addSource(new FlinkKafkaConsumer[String]("topic_name", new SimpleStringSchema(), properties))

    var data_stream = input_stream.map()

    data_stream.print()

    // execute program
    env.execute("Flink Scala API Skeleton")
```


## keyBy

KeyedStreams

https://ci.apache.org/projects/flink/flink-docs-release-1.8/dev/api_concepts.html#specifying-keys
- field postion: (Specifying keys via field positions is only valid for tuple data types)
-  field expression:

## aggregator functions
- maxBy

custom aggregations

reduce()


## savepoint

- 对stateful operators，使用uid(), name() 



# scala

> class
- 类class里无static类型

> object
- 可以拥有属性和方法，且默认都是"static"类型，可以直接用object名直接调用属性和方法，不需要通过new出来的对象（也不支持）
- 必须无参
- object可以extends父类或Trait，但object不可以extends object，即object无法作为父类。

> trait

多重继承， with

> 伴生对象
- 实现同个类既有普通方法又有静态方法， 伴生类和伴生对象可以相互访问彼此的私有成员