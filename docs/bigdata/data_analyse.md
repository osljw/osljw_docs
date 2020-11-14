

# 等频分箱

```
# q为分箱数量， qcut的输出结果为对应数据所属分组的标签
cvr_data['group'] = pd.qcut(cvr_data['cvr'], q=1000, duplicates='drop')


```