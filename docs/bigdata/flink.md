

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

## flink特点
- window机制
- checkpoint机制

## flink on yarn
- 启动一个YARN session(Start a long-running Flink cluster on YARN)
- 直接在YARN上提交运行Flink作业(Run a Flink job on YARN)

## flink任务
```
# 任务提交和恢复， -s指定savepoint路径， -c指定入口主类
flink run 


# 手动保存savepoint
flink savepoint <job_id>
```

# flink shell

本地模式启动交互式shell
```
bin/start-scala-shell.sh local
```

```
val dataSet = benv.fromElements((1,2), (2,3), (3,5), (4,6))
dataSet.maxBy(0).print()
```


# flink time
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
> 内置api
  - maxBy

> 继承AggregateFunction

覆盖三个实现, IN表示输入类型， ACC表示聚合类型， OUT表示输出类型
- def createAccumulator() 负责创建初始值
- override def add((value: IN, accumulator: ACC):ACC 负责将输入数据和已聚合数据进行聚合
- override def merge(a: ACC, b: ACC):ACC 负责合并不同分区的数据
- override def getResult(accumulator: ACC): OUT 负责从迭代类型得到聚合后的返回结果
```
import org.apache.flink.api.common.functions.AggregateFunction

class MyAggFunc(k: String) extends AggregateFunction[IN, ACC, OUT] {
  override def createAccumulator() = ACC()
  override def add((value: IN, accumulator: ACC) = {
    // add value and accumulator
    return ACC()
  }
  override def merge(a: ACC, b: ACC) = {
  }

  override def getResult(accumulator: ACC): OUT = {
  }
}


```

- reduce()

## Window
### timeWindow
Batch 是 Streaming 的一个特例, 使用timeWindow可以统一batch和stream任务的处理
- Tumbling Time Window
```
# 翻滚时间窗口, 1分钟
.timeWindow(Time.minutes(1))

# 滑动时间窗口, 窗口1分钟，滑动30秒
.timeWindow(Time.minutes(1), Time.seconds(30))
```
### countWindow
### Session Window


## savepoint

- 对stateful operators，使用uid(), name() 



# scala

> class
- 类class里无static类型

> object
- 可以拥有属性和方法，且默认都是"static"类型，可以直接用object名直接调用属性和方法，不需要通过new出来的对象（也不支持）
- 必须无参
- object可以extends父类或trait，但object不可以extends object，即object无法作为父类。

```scala
import org.apache.spark.{ SparkConf, SparkContext }
import org.apache.spark.sql.SparkSession
 
trait Spark {
    def spark = { 
        val sparkConf = new SparkConf().setAppName("SparkApp")

        val spark = SparkSession.builder()
            .config(sparkConf)
            .enableHiveSupport()
            .getOrCreate()

        spark
    }   
}

object SparkApp extends Spark {
    def main(args: Array[String]) {
        val showSql = "show databases"
        val rdd = spark.sql(showSql)
        rdd.show()
    }   
}
```
object 继承trait后可以使用trait里的函数

> trait
> 
类似java中的接口interface
- 可以定义属性和方法的实现
- 可以被class和object继承(extends)

多重继承， with

> 伴生对象
- 实现同个类既有普通方法又有静态方法， 伴生类和伴生对象可以相互访问彼此的私有成员