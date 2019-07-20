
# mkdocs

```
mkdocs gh-deploy
```

# math
```
pip install https://github.com/mitya57/python-markdown-math/archive/master.zip
```

```
# test_math/config.yaml

extra_javascript: 
    - https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML

markdown_extensions:
    - mdx_math
        enable_dollar_delimiter: True
```
