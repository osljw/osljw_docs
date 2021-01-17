
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