CORS

浏览器需要保护用户浏览网站， 禁止网站源码跨域请求

# React

## create-react-app

```
npx create-react-app <app name> --template typescript
```

项目加入typescript
```
npm install --save-dev typescript @types/node @types/react @types/react-dom @types/jest

npx tsc --init
```
tsconfig.json中加入配置`"jsx": "react-jsx"`

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

## Link
to没有以`/`开头为相对路由， 会相对当前url进行路由， 反之为绝对路由
```
<Link to="123"> doc1 </Link>

<Link to="/123"> doc1 </Link>
```

## 嵌套路由

- 示例一
```
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Layout />}>
      <Route path="/list" element={<List />}>
        <Route path=":id" element={<DocDetail />}> </Route>
      </Route>
    </Route>
  </Routes>
</BrowserRouter>
```
访问`/list/123`时，Layout，List， DocDetail组件均会进行渲染， Layout组件中需要使用`<Outlet />`显示List组件， List组件中需要使用`<Outlet />`显示DocDetail组件

- 示例二
```
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Layout />}>
      <Route path="/list" element={<List />}> </Route>
      <Route path="/list/:id" element={<DocDetail />}></Route>
    </Route>
  </Routes>
</BrowserRouter>
```
访问`/list/123`时，List组件不会渲染， Layout和DocDetail组件均会进行渲染

## 编程式跳转

```
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate()
navigate('/') # 绝对跳转
```

## 路由懒加载

useRoutes: 让路由写成配置表的形式
react-loadable： 实现组件的动态加载

```
npm i react-loadable
```

```js
import Loadable from "react-loadable";

const Loading = () => <div>loading...</div>;
const LayoutPro = Loadable({
  loader: () => import("../view/LayoutPro"),
  loading: Loading,
});
const Home = Loadable({
  loader: () => import("../view/Home"),
  loading: Loading,
});

const routes = [
  {
    path: "/",
    element: <LayoutPro />,
    children: [
      {
        path: '',
        element: <Home />,
      }
    ]
  },
];

function InnerRouter() {
  let element = useRoutes(routes);
  return element;
}

function AppRouter() {
  return (
    <BrowserRouter>
      <InnerRouter />
    </BrowserRouter>
  );
}
```

不能使用如下写法， 因为Loadable返回的不是React.ReactElement类型,
```js
const routes = [
  {
    path: '/',
    element: Loadable({
      loader: () => import('../view/LayoutPro'),
      loading: Loading,
    }),
  }
]
```

## 相关链接
React-Router V6 使用详解 https://juejin.cn/post/7033313711947251743

# 理解React渲染和生命周期

# React Hook

- State Hook
  - useState (class组件中的this.state, this.setState)
- Effect Hook
  - useEffect 
    - 
    - 接收一个函数， React每次渲染后会执行该函数 
    - 接收的函数内部可以选择返回一个清除函数，清除函数会在组件更新或卸载时调用， 这样可以让逻辑代码放在一起

# react markdown

- 文章目录导航
  - 容器大小 = min(目录长度, 窗口指定大小）

```
const NavItem = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'left',
    color: theme.palette.text.secondary,
    maxHeight: "80vh",
    overflow: "auto",
}));

<NavItem>
  <Toc> </Toc>
</NavItem>
```
文章目录的父容器NavItem设置`maxHeight: "80vh"`,  实现目录容器NavItem的大小随目录自适应， 但不超过`80vh`高度,  `overflow: "auto"`实现目录超过`80vh`高度时，出现滚动条


todo：
- 文章页面滚动时， 是否自动滚动目录？

# antd(Ant Design)

# Ant Design Pro Components

ProLayout 

# Mock

- 随机模拟数据 mock.js

# 网络请求 axios

# material UI 

```
npm install @material-ui/core
npm install @material-ui/icons
```




# 语法

Destructuring


# Material UI


# 滚动

浏览器滚动
1. 当页面内容的高度超过视口高度的时候，会出现纵向滚动条
2. 当页面内容的宽度超过视口宽度的时候，会出现横向滚动条

父元素有固定的高度/宽度， 子元素的高度/宽度大于父元素时，出现滚动条

如何设置页面固定视口， 内容超过视口大小时进行滚动

1. 设置父元素P固定高度， overflow为auto
```
  height: "80vh",
  overflow: "auto",
```
2. 在父元素P之外使用antd的Anchor固定父元素P的位置， 禁止窗体滚动条改变视口位置
```
<Anchor affix={true} offsetTop={120}>
```



# markdown文章显示

https://www.emgoto.com/react-table-of-contents/



# build 部署

```
npm run build
```


```
npm install -g serve
serve -s build
```