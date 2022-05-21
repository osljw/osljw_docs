
# mkdocs

github page 部署
```
pip install mkdocs mkdocs-material
mkdocs gh-deploy
```


# math
```
pip install mkdocs mkdocs-material

# mkdocs.yml
theme:
  name: material

extra_javascript: 
    - https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML

# Extensions
markdown_extensions:
  - pymdownx.arithmatex
```
