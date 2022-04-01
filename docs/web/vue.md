

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

# 组件
单文件组件(.vue文件) https://www.cnblogs.com/SamWeb/p/6391373.html


# Hook
- created
- mounted



# ESLint

```
./node_modules/.bin/eslint --fix src/components/test.vue
```

# 

https://wdd.js.org/vue-vue-router-elementui-stupid-simple-dashboard.html




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
