---
layout:     post
title:      "����"
subtitle:   "build_system"
date:       2019-04-17 16:22:51
author:     "soaringsoul"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - ѧϰ�ʼ�
---





# Makefile


## 隐含规则
%.o:%.cpp
    @echo "[^[[1;32;40mBUILD^[[0m][Target:'^[[1;32;40m$<^[[0m']"
    @$(CXX) $(CXXFLAGS) $(INC_DIR) -c $< -o $@

eg:
$< 表示main.cpp
$@ 表示main.o

## 自动变量
$@ 目标
$< 规则的第一个依赖目标

## 
使用shell命令找到cpp文件
$(shell find . -name "*.cpp")

将*.cpp文件替换成*.o文件
$(patsubst %.cpp,%.o, $(cpp_files))