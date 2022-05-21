

# Router
# VUE

- el 绑定html id
- data 数据字典
- computed 计算属性字典，有cache
- methods 方法字典，无cache
- watch 异步访问

# 指令
- v-if bool表达式
- v-model  输入， 双向绑定
- v-bind 绑定attribute, 简写为:
- v-on 事件处理, 简写为@
- v-once 一次数据绑定
- v-html
- v-slot:one 具名插槽，可以简写为 #one
```
父组件中
<template v-slot:one> 插入到one插槽的内容 </template>

<template #one> 插入到one插槽的内容 </template>
```

# 组件
单文件组件(.vue文件) https://www.cnblogs.com/SamWeb/p/6391373.html

# vue 路由

设置路由表项的component时，使用箭头函数导入组件
```
const routes = [
  {
    'path': '/login',
    component: () => import('@/views/login/Login.vue')
  },
]
```

- router-link 站内链接
```html
<router-link to="/home">Go to Home</router-link>
```
- router-view 页面局部刷新


# Hook
- created
- mounted



# ESLint

```
./node_modules/.bin/eslint --fix src/components/test.vue
```

# 

https://wdd.js.org/vue-vue-router-elementui-stupid-simple-dashboard.html

# vue webpack

webpack的作用： 让js和html进行分离， 对js进行模块化，管理js相互之间的依赖，对js进行打包


# Vue django

## 分页功能

首次访问页面
前端请求参数
- pagenum = 1（第一页）
- pagesize = 0 （表示由后端决定页面有多少条数据）

后端返回
- 第一页数据
- pagesize（页大小）由后端根据数据量大小决定， 例如设置为10
- 数据总数
- pagesizes（分页单位）配置列表


前端请求信息
- 第几页
- 每页的大小

django返回数据
