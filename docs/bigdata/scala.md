# scala

- Array
```
var z = Array("1", "2", "3")
z(0) = "111"
```



> class
- 类class里无static类型

> object
- 可以拥有属性和方法，且默认都是"static"类型，可以直接用object名直接调用属性和方法，不需要通过new出来的对象（也不支持）
- 必须无参
- object可以extends父类或trait，但object不可以extends object，即object无法作为父类。
- object在第一次被用到时进行初始化

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

# scala json
build.sbt
```
libraryDependencies += "org.json4s" %% "json4s-jackson" % "3.7.0-M1"
libraryDependencies += "org.json4s" %% "json4s-ext" % "3.7.0-M1"
```

```
import org.json4s.{DefaultFormats, Extraction}
import org.json4s.JsonDSL._
import org.json4s.JsonAST._
import org.json4s.jackson.JsonMethods.{compact, parse, render}
import org.json4s.jackson.Serialization
```

# Try Success Failure
```
import scala.util.{Failure, Success, Try}
import java.net.URL

def parseURL(url: String): Try[URL] = Try(new URL(url))

val url = parseURL(Console.readLine("URL: ")) getOrElse new URL("http://hello")

val url = parseURL("http://hello.com") match {
    case Success(u) => u
    case Failure(e) => None
}
```

# scala test
build.sbt
```
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"
```