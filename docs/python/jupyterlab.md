
# jupyter

- jupyter notebook

```
jupyter notebook --ip=127.0.0.1 --port=8889 --no-browser --allow-root 
```

- jupyter-lab
```
jupyter lab --ip 127.0.0.1 --port 8887 --no-browser --debug
```

dash

https://dash.plot.ly/?_ga=2.52625512.1127282372.1566350192-1348580862.1566350192

https://zhuanlan.zhihu.com/p/33801552


# jupyter kernel
python, scala, c++
```
jupyter kernelspec
jupyter kernelspec list # 查看可用kernel
```

# jupyter extension

labextension 和 nbextension 不兼容，不能混用

- jupyter lab extension

lab extension 使用nodejs开发
```
jupyter labextension help
jupyter labextension list # 查看已安装lab extension
```

- jupyter notebook extension
```
jupyter nbextension help
jupyter nbextension list
```
- jupyter server extension

server extension使用python开发
```
jupyter serverextension help
jupyter serverextension list
```
https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html#writing-a-notebook-server-extension


# jupyterlab

## jupyterlab-dash
对plotly dash的封装， 支持在jupyterlab中创建viewer，以tab标签的方式显示页面，以后台线程的方式创建web服务，不会阻塞用户交互
```python
import jupyterlab_dash
import dash
import dash_html_components as html

viewer = jupyterlab_dash.AppViewer()

app = dash.Dash(__name__)

app.layout = html.Div('Hello World')

viewer.show(app) # 后台会以线程方式启动flask web服务， 故不会阻塞交互式环境
viewer.terminate() # 关闭后台web服务
viewer.show(app) # 重新启动web服务
```


# SparkMonitor

https://krishnan-r.github.io/sparkmonitor/how.html

jupyter notebook可用， jupyter lab不可用

1. Notebook Frontend extension written in JavaScript.
2. IPython Kernel extension written in Python.
3. Notebook web server extension written in Python.
4. An implementation of SparkListener interface written in Scala.

> Frontend extension

代码入口：extension/js/module.js


> IPython Kernel Extension

代码入口: extension/sparkmonitor/kernelextension.py

> Scala SparkListener

代码入口: extension/scalalistener/CustomListener.scala