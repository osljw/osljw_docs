

platodb

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