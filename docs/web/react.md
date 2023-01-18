CORS

浏览器需要保护用户浏览网站， 禁止网站源码跨域请求

# React

## create-react-app

## css

新建 public/css/index.css

public/index.html中引用css

```
<link rel="stylesheet" type="text/css" href="%PUBLIC_URL%/css/index.css" />
```

# webpack 
js 打包

```
# 安装webpack
npm i webpack webpack-cli --save-dev

# 
webpack --mode development --watch
```

# babel


# Eslint

package.json配置rules
```json
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ],
    "rules": {
      "no-unused-vars": "off"
    }
  },
```

# React Router


```
npm install react-router-dom
```

- BrowserRouter
- HashRouter (url中使用#分割)


嵌套路由


## 相关链接
React-Router V6 使用详解 https://juejin.cn/post/7033313711947251743

# UI 

```
npm install @material-ui/core
npm install @material-ui/icons
```


# 语法

Destructuring


# Material UI