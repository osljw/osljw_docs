
# mysqld
## 安装
```
conda install -c conda-forge mysql
```

## 配置文件
新建配置文件： /home/test/mysql/etc/my.cnf
```
[client]
#port=3336
#socket=/home/user/mysql/mysql.sock

[mysqld]
#port=3336
basedir=/home/user/miniconda3/pkgs/mysql-5.7.24-hbb652a2_0
datadir=/home/user/software/mysql/data
pid-file=/home/user/software/mysql/mysql.pid
#socket=/home/user/software/mysql/mysql.sock
log_error=/home/user/software/mysql/log/error.log
#server-id=100
lc-messages-dir=/home/user/miniconda3/pkgs/mysql-5.7.24-hbb652a2_0/share/mysql
#socket=/home/appops/test/mysql/mysql.sock

[mysqld]
#port=3336
basedir=/home/appops/test/miniconda3/pkgs/mysql-5.7.24-hbb652a2_0
datadir=/home/appops/software/mysql/data
pid-file=/home/appops/software/mysql/mysql.pid
#socket=/home/appops/test/mysql/mysql.sock
log_error=/home/appops/software/mysql/log/error.log
#server-id=100
lc-messages-dir=/home/appops/test/miniconda3/pkgs/mysql-5.7.24-hbb652a2_0/share/mysql
lc_messages = en_US
log_timestamps = SYSTEM
```
- basedir: mysql的安装位置，该目录下有bin, lib等目录
- lc-messages-dir： mysql 运行sql产生的错误error信息保存位置

## 初始化数据库
```
mysqld --defaults-file=/home/test/mysql/etc/my.cnf --initialize --user=test --basedir=/home/test/mysql --datadir=/home/test/mysql/data

mysqld --defaults-file=`pwd`/etc/my.cnf --initialize --basedir=`pwd` --datadir=`pwd`/data
```
运行该命令时--user参数只有在root用户下才有效，可以不带该参数。该命令执行完后数据库中就存在root用户了，可以在my.cnf文件中配置的log_error参数对应的路径中找打root用户的密码，记录下来。

启动mysqld服务
```
nohup mysqld_safe --defaults-file=/home/test/mysql/etc/my.cnf &
```

使用mysql
```
mysql -u root -p
# 输入上边记录的root密码(log/error.log: A temporary password is generated for root@localhost: AY-DAM)Zh8_Z)

> SET PASSWORD = PASSWORD('root123')

alter user 'root'@'localhost' identified by "rootpassword"
```


# mysql 插入数据

- insert into (插入新数据， key相同时插入失败)
- insert overwrite(会先删除表或分区，再插入数据)

根据数据自动进行插入和更新
```
INSERT INTO <table> VALUES(id1, v1, v2) ON DUPLICATE KEY UPDATE col1=VALUES(v1), col2=VALUES(v2)
```

```
INSERT INTO mytable (col1, col2, col3) VALUES (?, ?, ?)
ON DUPLICATE KEY UPDATE col1=VALUES(col1), col2=VALUES(col2), col3=VALUES(col3);
```


```
CREATE TABLE IF NOT EXISTS ocpc_cvr (
    dt DATE,
    account_id VARCHAR(255),
    scheduling_id VARCHAR(255),
    `show` INT,
    charge DOUBLE(40,2),
    click INT,
    install INT,
    install_fix INT,
    pcvr DOUBLE(40,6),
    pcoc DOUBLE(40,6),
    PRIMARY KEY (dt, account_id, scheduling_id)
);
```


```
CREATE TABLE IF NOT EXISTS convert_back (
    dt DATE,
    request_id VARCHAR(255),
    idea_id VARCHAR(255),
    location VARCHAR(255),
    account_id VARCHAR(255),
    adplan_id VARCHAR(255),
    scheduling_id VARCHAR(255),
    action_type VARCHAR(255),
    status VARCHAR(255),
    active_time VARCHAR(13),
    request_time VARCHAR(13),
    `convert` VARCHAR(255),
    `os` VARCHAR(255),
    `label` VARCHAR(255),
    PRIMARY KEY (dt, request_id, idea_id, location)
);
```

# sql 删除数据
```
delete from cpi
 where (countryid, year) in (('AD', 2010), ('AF', 2009), ('AG', 1992))
```

# sql 分组统计

- group_concat

```sql
SELECT sell_date AS 'sell_date',
    COUNT(DISTINCT product) AS 'num_sold',
    GROUP_CONCAT(DISTINCT product 
        ORDER BY product ASC    #按照字典序排列，升序
        SEPARATOR ',')          #用','分隔
        AS 'products'    #组内拼接
FROM Activities
GROUP BY sell_date
ORDER BY sell_date;
```

# sql 外键（Foreign Key）
一个表的外键用来指向另一个表的主键（Primary Key）
作用： 
- 用于将两个表连接在一起，让两个表的数据保持同步，
- 外键约束能够防止非法数据进入外键字段，因为它的值必须存在于它指向的主键中
- 删除/更新主表记录时，可以选择同时删除/更新从表中的相关记录，也可以选择不删除/更新，您可以在定义外键时对此进行设置。
- 删除主表记录时，必须先删除从表中的关联记录，否则主表中的记录将无法删除。
- 删除主表时，必须先删除从表，否则主表将无法删除。
