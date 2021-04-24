
# pyecharts

- ChartMixin
    - Base
        - Chart
            - RectChart
                - Bar


pyecharts/datasets/map_filename.json js和css文件索引列表
Chart对象通过js_dependencies保存依赖的js文件


- ChartMixin.load_javascript
    - engine.load_javascript
load_javascript 根据chart对象的js_dependencies找到依赖的js和css文件，转换成地址， 返回

- Base.render_notebook    
    - engine.render_notebook
render_notebook返回HTML对象， html内容由RenderEngine().render_chart_to_notebook负责生成， 模板渲染引擎为jinja2


https://zhuanlan.zhihu.com/p/127760528

title_opts——标题
legend_opts——图例
tooltip_opts——​提示框
toolbox_opts——工具箱
brush_opts——区域选择组件
xaxis_opts——​X轴
yaxis_opts——Y轴
visualmap_opts——视觉映射
datazoom_opts——​区域缩放
graphic_opts——原生图形元素组件
axispointer_opts——坐标轴指示器


# Bar
```
from pyecharts import options as opts
from pyecharts.charts import Bar

c = (
    Bar()
    .add_xaxis(t1['click'].tolist())
    .add_yaxis("freq", t1['freq'].tolist())
    .set_series_opts(
        label_opts=opts.LabelOpts(
            rotate=45, 
            horizontal_align="left",
            #vertical_align="middle"
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="用户视频点击分布"),
        xaxis_opts=opts.AxisOpts(name="点击次数"),
        yaxis_opts=opts.AxisOpts(name="频次"),
    )
    .render("bar_base.html")
)
```


# 多个Y轴 multi yaxis 

默认的y轴为yaxis_index=0， 属性在set_global_opts中配置， 其他yaxis在extend_axis中配置

```python
from pyecharts import options as opts
from pyecharts.charts import Line

colors = ["#5793f3", "#d14a61", "#675bba"]
c = (
    Line()
    .add_xaxis(df['ds'].astype('str').tolist())
    .add_yaxis("uv", df['uv'].tolist(), yaxis_index=0, color=colors[0])
    .add_yaxis("iv", df['iv'].tolist(), yaxis_index=1, color=colors[1])
    .extend_axis(
       yaxis=opts.AxisOpts(
           name="iv", 
           type_="value",
           position="right",
           interval=10000,
           axisline_opts=opts.AxisLineOpts(
               linestyle_opts=opts.LineStyleOpts(color=colors[1])
           ),
           #axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
      )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="uv",
            type_="value",
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color=colors[0])
            ),
            #axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
)

c.render("video_uv.html")

```