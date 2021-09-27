

# platodb nebula graph


https://nebula-graph.com.cn/posts/nebula-graph-data-model-and-system-design/

顶点由vid唯一标识， 一个顶点可以有多个tag， 每个tag可以有多个属性，

边分割存储图


```
SHOW TAGS; 
```

## 创建

### 图空间
```
CREATE SPACE i2i (partition_num=10, replica_factor=1);
```

### 图创建
```
CREATE TAG item(name string, type string);
CREATE EDGE rel(score double);
```
数据类型：vid、double、int、bool、string 和 timestamp



### 图插入
```
INSERT VERTEX item(name, type) VALUES 100:("item_id1", “video");
INSERT EDGE rel(score) VALUES 100 -> 101:(0.56);
```

数字为vid， 


### 图查看  

类型查看
```
DESCRIBE TAG item;
DESCRIBE EDGE rel;
```

属性查看
```
FETCH PROP ON item 100;
FETCH PROP ON item 100 -> 101;
```

邻居查看
```
GO FROM 100 OVER rel;
```


## 集群机器信息
```
show hosts;
```

## 架构

https://github.com/vesoft-inc/nebula-docs-cn/blob/master/docs/manual-CN/1.overview/3.design-and-architecture/1.design-and-architecture.md

- Meta Service： leader/follower架构
- Storage Service：
- Query Service：



## nebula 集群配置

1. graphd 和 storaged 需要知道所有meted的ip和端口， 在etc/nebula-graphd.conf和etc/nebula-storaged.conf配置文件中--meta_server_addrs参数指定
2. 用户启动客户端console时需要知道graphd的ip和端口

http服务的port冲突问题， 在

- 用户
  - 只需知道所有graphd机器的地址和端口
  
- graphd
  - 扩容： 扩容graphd需要知道metad的所有addr， 通知用户

- metad
  - 目前不能进行扩容，缩容
  - 需要通知已经启动的graphd， storaged增加和删除metad

- storaged
  - 扩容： 先部署新增机器， 使用管理命令开始迁移数据， 等待任务结束
  - 缩容： 使用管理命令开始迁移目标机器的数据， 等待任务结束， 删除目标机器

启动

```
sbin/nebula --addr 0.0.0.0 --port 18080 -u root -p nebula
```
port 为graphd服务的port


## 参考链接
Nebula 架构剖析系列（一）图数据库的存储设计

https://www.huaweicloud.com/articles/cbc7c60e3ec524dfe279b4de4c687e49.html



- studio 
  - 网页： 默认7001端口链接

# neo4j

下载安装：https://neo4j.com/download-center/#community


# 

```
show databases;
```

```
:use <database>
```

查看数据
```
match(n) return n
```


导入数据
```
CREATE CONSTRAINT itemIdConstraint ON (item:Item) ASSERT item.id IS UNIQUE;

MATCH (n)
DETACH DELETE n;

USING PERIODIC COMMIT 1000 LOAD CSV WITH HEADERS FROM "file:///id.csv" AS csvLine
CREATE (p:Item {id: csvLine.id});

USING PERIODIC COMMIT 1000 LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
MATCH (from:Item{id:line.src}),(to:Item{id:line.dst})
MERGE (from)-[r:Count{count:line.count}]-> (to);
```


清除数据库
```
//clean item graph
drop constraint itemIdConstraint;

match (n) detach delete n
```

节点总数
```

```

边总数
```
MATCH ()-[r]->() RETURN count(*)
```


## Cypher

node: 图的顶点， 用`(var_name:var_type)`表示node

Relationship： 图的边，用`[var_name:var_type]`表示relationship

- Match 图模式匹配
    - 节点`(p:Person)`, `(m:Movie)`
    - 边`[r:ACTED_IN]`
    - 入边`->`, 出边`->`
- WITH 聚合
- where 过滤条件
- RETURN


match 匹配

- 匹配边的方向
```
MATCH (m:Movie)<-[r:ACTED_IN]-(p:Person) RETURN p,r,m
```

```
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie) RETURN p,r,m
```

- 属性匹配和relatedTo相关匹配
```
MATCH (p:Person)-[relatedTo]-(m:Movie {title: "Cloud Atlas"}) return p.name, type(relatedTo)
```


create 创建节点
```
CREATE (john:Person {name: 'John'})
CREATE (joe:Person {name: 'Joe'})
```
create 创建边
```
CREATE (john)-[:FRIEND]->(joe)-[:FRIEND]->(steve)
```

匹配创建
```
MATCH (p:Person), (m:Movie)
WHERE p.name = "Tom Hanks" and m.title = "Cloud Atlas"
CREATE (p)-[w:WATCHED]->(m)
RETURN type(w)
```

merge match create 匹配存在的节点或者创建新的节点