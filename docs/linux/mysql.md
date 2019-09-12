
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
#socket=/home/test/mysql/mysql.sock  

[mysqld]
#port=3336
basedir=/home/test/mysql
datadir=/home/test/mysql/data
pid-file=/home/test/mysql/mysql.pid
#socket=/home/test/mysql/mysql.sock
log_error=/home/test/mysql/log/error.log
#server-id=100
```

## 初始化数据库
```
mysqld --defaults-file=/home/test/mysql/etc/my.cnf --initialize -user=test --basedir=/home/test/mysql --datadir=/home/test/mysql/data
```
运行该命令时--user参数只有在root用户下才有效，可以不带该参数。该命令执行完后数据库中就存在root用户了，可以在my.cnf文件中配置的log_error参数对应的路径中找打root用户的密码，记录下来。

启动mysqld服务
```
nohup mysqld_safe --defaults-file=/home/test/mysql/etc/my.cnf &
```

使用mysql
```
mysql -u root -p
# 输入上边记录的root密码
> SET PASSWORD = PASSWORD('root123')
```
