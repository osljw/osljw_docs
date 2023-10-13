
# javascript

## Promise

异步函数的返回结果为Promise对象

一个 Promise 必然处于以下几种状态之一
- 待定（pending）: 初始状态，既没有被兑现，也没有被拒绝。
- 已兑现（fulfilled）: 意味着操作成功完成。
- 已拒绝（rejected）: 意味着操作失败。


```
const promise = doSomething();
const promise2 = promise.then(successCallback, failureCallback);
```

`catch(failureCallback)` 是 `then(null, failureCallback)` 的缩略形式



# canvas
canvas 获取图片
```
var canvas = document.getElementById("alpha");
var dataURL = canvas.toDataURL("image/png");
var newTab = window.open('about:blank','image from canvas');
newTab.document.write("<img src='" + dataURL + "' alt='from canvas'/>");
```

# 游戏开始
game.start()


# 游戏暂停
game.pause()


# 
game.tetris.move("left")  # 移动
game.tetris.rotate() # 旋转
game.tetris.drop() # 下落

```
game.tetris.curBrickCenterPos # 当前块的位置

game.tetris.grids # 历史grid状态
```


# 脚本
chrome -> dev console -> sources菜单 -> Snippets(用户自定义js脚本)


# javascript debugger

## chrome sources 面板

VM（Virtual Machine）+ 数字：  js运行的独立虚拟环境

debugger的运行

1. settimeout延迟debugger、
2. eval
3. 代码混淆+debugger


debugger在js源码文件中， 使用Never pause here进行绕过


## 混淆 加密

XHR断点



## fiddler web debugger

- 可以快速了解请求了哪些接口和参数

## reres

- reres：替换js的插件， 绕过debugger