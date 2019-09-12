
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

viewer.show(app)
viewer.terminate() # 关闭后台web服务
viewer.show(app) # 重新启动web服务
```