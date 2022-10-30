
# Modular Software Design

- the single responsibility
- loose coupling, and high cohesion.


# js 

## ES6 Module

浏览器
- Relative Import URLs
- Importing from Node Modules (NPM or YARN)
    - import from package name require a bundler


html中使用ES6 module
```html
<script type="module">
    import * as THREE from 'js/three.module.js'
<script>
```

副作用： type=“module“的script标签内的变量，是这个script标签的私有变量， 会导致在浏览器DevTools JavaScript console中不可调试 （可以将变量在模块内部赋给window进行导出）


## 