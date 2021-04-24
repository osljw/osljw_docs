
# docker

# docker build 创建镜像

- docker build 命令用于使用 Dockerfile 创建镜像。


# docker run 运行镜像
- docker run 创建一个新的容器并运行一个命令

# 镜像管理
查看本机已安装镜像
```
docker image ls
```



```
sudo service docker start
```


```shell
# Create the docker group.
sudo groupadd docker

# Add your user to the docker group.
sudo usermod -aG docker ${USER}

# You would need to loog out and log back in so that your group membership is re-evaluated or type the following command:
su -s ${USER}
```


```

--user $(id -u):$(id -g)
```