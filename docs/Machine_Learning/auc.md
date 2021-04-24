
# AUC

sklearn
```
import numpy as np
from sklearn import metrics

y_true = np.array([0, 0, 1, 1])
y_pred = np.array([0.1, 0.4, 0.35, 0.8])


metrics.roc_auc_score(y_true, y_pred) # auc = 0.75

fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred, pos_label=1)
metrics.auc(fpr, tpr) # auc = 0.75
```

pyspark



tensorflow metrics

- recall_at_thresholds 

第i个threshold对应的召回率： true_positives[i] / (true_positives[i] + false_negatives[i]， 所有预测正确的样本（正和负）中正样本的比例


- precision

true_positives[i] / (true_positives[i] + false_positives[i]) , 所有预测为正样本中确实是正样本的比例


top K categorical accuracy: how often the true candidate is in the top K candidates for a given query.


```python
# class FactorizedTopK(tf.keras.layers.Layer)

# positive_scores: [num_queries, 1]
positive_scores = tf.reduce_sum(
    query_embeddings * true_candidate_embeddings, axis=1, keepdims=True)

# self._candidates: Layer
# top_k_predictions: [num_queries, k]  top k score
top_k_predictions, _ = self._candidates(query_embeddings, k=self._k)

# y_true: [num_queries, 1 + k]
y_true = tf.concat(
    [tf.ones(tf.shape(positive_scores)),
        tf.zeros_like(top_k_predictions)],
    axis=1)
# y_pred: [num_queries, 1 + k]
y_pred = tf.concat([positive_scores, top_k_predictions], axis=1)

# 只需判断positive_scores分数是不是大于top_k_predictions分数，由TopKCategoricalAccuracy完成
```

tf.keras.metrics.TopKCategoricalAccuracy


# 指标

浏览类指标
PV & UV
播放类指标
VV(Video View，播放数): 是指在一个统计周期内，视频被打开的次数之和。
CV(Content Views，内容播放数): 是指在一个统计周期内，视频被打开，且视频正片内容（除广告）被成功播放的次数之和。