
---
layout:     post
title:      "reflection"
subtitle:   "reflection"
date:       2019-05-13 17:39:58
author:     "none"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - tag
---

# 动态加载类文件和构建对象
Class<?> class1 = null
class1 = Class.forName("com.b510.hongten.test.reflex.Person");
Person person = (Person) class1.newInstance();

Method getMethod
public Method getDeclaredMethod(String name, Class<?>... parameterTypes)
        throws NoSuchMethodException, SecurityException
name: 方法的名称
parameterTypes：方法的参数类型
Field getDeclaredField

invoke
