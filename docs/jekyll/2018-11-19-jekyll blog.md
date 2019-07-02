---
layout:     post
title:      "jekyll blog"
date:       2018-11-19 19:00:00
author:     "ljw"
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - jekyll
---

## 目录结构
_includes: html, 可以使用site可访问_config.yml中定义的值
_posts： 存放文章，如markdown文档
_site： Jekyll转换生成后的网站

archive.html - 索引文章列表

_layouts/post.html 渲染文章页面
_posts 目录下的网站通过front-matter引用_layouts/post.html
```
---
layout:     post
---
```
_layouts/post.html 中可以通过page全局变量引用文章的front-matter




## 分页
### 插件
_config.yml
paginate: 10

### paginator  liquid 对象属性

## 数学公式
配置文件
_config.yml
```
page-mathjax: true

markdown: kramdown
kramdown:
  input: GFM 
  syntax_highlighter_opts:
    span:
      line_numbers: false
    block:
      line_numbers: true
      start_line: 1
```

_layouts/post.html
```
{% raw %}
{% if site.page-mathjax %}
  {% include mathjax_support.html %}
{% endif %}
{% endraw %}
```

_includes/mathjax_support.html
```
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: {
      equationNumbers: {
        autoNumber: "AMS"
      }
    },
    SVG: {
      scale: 90
    },
    tex2jax: {
      inlineMath: [ ['$','$'] ],
      displayMath: [ ['$$','$$'] ],
      processEscapes: true,
    }
  });
</script>
<script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG">
</script>
```