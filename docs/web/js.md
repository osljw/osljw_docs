
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