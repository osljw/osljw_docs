

# NLP

# 语言模型
- n-gram 概率语言模型
- 上下文相关
  - 单向
    - GPT
  - 双向
    - BERT (Bidirectional Encoder Representations from Transformers)
    - ALBERT (A Lite BERT)
    - ELMo
- 上下文无关(词嵌入)
  - word2vec
  - GloVe

1. 一词多义

# 训练方式
- Feature-based
- Fine-tuning


# 处理技巧

## bpe (Byte Pair Encoding)






# 评测
- GLUE

# attention
https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/


# Transformer
http://jalammar.github.io/illustrated-transformer/

transformer = attention + 全联接， encoder-decoder结构

transformer 网络结构和源码 https://zhuanlan.zhihu.com/p/178610196

attention
- Q: query-vec
- K: key-vec
- V: value-vec

I为(word_len, embedding_size), WQ, WK, WV的大小为embedding_size * v, Q,K,V的大小为(word_len, v)

Q = I * WQ 

K = I * WK

V = I * WV

词的embedding共享Q，K，V的权重矩阵

1. `Q * K^T`: (word_len, word_len) 两个词通过点积得到之间的关联度
2. `Q * K^T / sqrt(d_k)`: 通过sqrt(d_k) 对关联度进行缩放， 数值梯度的稳定
3. `softmax(Q * K^T / sqrt(d_k))`:  (word_len) 用softmax归一化权重
4. `softmax(Q * K^T / sqrt(d_k)) * V`: （word_len, v)


## Self-Attention

I:  (batch_size, word_len, embedding_size)

WQ: (embedding_size, dq)
WK: (embedding_size, dk)
WV: (embedding_size, dv)

dq = dk = dv

Q(query vector):  (batch_size, word_len, dq)
K(key vector): (batch_size, word_len, dk)
V(value vector): (batch_size, word_len, dv)

Q * K (batch_size, word_len, dq, dk)   ((q,k) 表示第q和第k个word间的score)

(Q * K) / sqrt(dq)   ( stable gradients )

softmax((Q * K) / sqrt(dq), axis=-1)   (batch_size, word_len , dq, dk)   每个样本的每个词都有一个长度为dk向量，该向量的分数和为1

softmax((Q * K) / sqrt(dq), axis=-1) * V   (batch_size, word_len, dq, dv)

sum(softmax((Q * K) / sqrt(dq), axis=-1) * V)  (batch_size, word_len, dq)

## Positional Encoding

PE是shape为（position, d_model)的矩阵

$$\Large{PE_{(pos, 2i)} = sin(pos / 10000^{2i / d_{model}})} $$
$$\Large{PE_{(pos, 2i+1)} = cos(pos / 10000^{2i / d_{model}})} $$

- $d_{model}$: embedding size
- $2i, 2i+1$: embedding size的偶数和奇数位置
- $pos$: 第pos个序列位置

实现代码：
```python
def positional_encoding(position, d_model):
  # i: (1, d_model)
  i = np.arange(d_model)[np.newaxis, :]
  # angle_rates: (1, d_model)
  angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
  angle_rads = np.arange(position)[:, np.newaxis] * angle_rates
  
  # 将 sin 应用于数组中的偶数索引（indices）；2i
  angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
  
  # 将 cos 应用于数组中的奇数索引；2i+1
  angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    
  pos_encoding = angle_rads[np.newaxis, ...]
    
  return tf.cast(pos_encoding, dtype=tf.float32)

```

## tf.keras.layers.Attention
input: 
  query: [batch_size, Tq, dim] eg: 文本相似度应用中，query是第一段文字的序列嵌入
  value: [batch_size, Tv, dim] eg: 文本相似度应用中，value是第二段文字的序列嵌入
  key: [batch_size, Tv, dim] eg: 文本相似度应用中，key是第二段文字的序列嵌入, key和value相同
output:
  [batch_size, Tq, dim]

1. Calculate scores with shape `[batch_size, Tq, Tv]` as a `query`-`key` dot
  product: `scores = tf.matmul(query, key, transpose_b=True)`.
2. Use scores to calculate a distribution with shape
  `[batch_size, Tq, Tv]`: `distribution = tf.nn.softmax(scores)`.
3. Use `distribution` to create a linear combination of `value` with
  shape `[batch_size, Tq, dim]`:
  `return tf.matmul(distribution, value)`.


## Encoder（编码器）
- 输入： (batch_size, input_seq_len)
- embedding： (batch_size, input_seq_len, d_model)
- 和位置编码相加: (batch_size, input_seq_len, d_model)
- 经过n层编码层： (batch_size, input_seq_len, d_model)
- 输出： (batch_size, input_seq_len, d_model)

## Decoder（解码器）
- 输入： 编码器的输出(batch_size, input_seq_len, d_model)， 和目标序列(batch_size, target_seq_len)
- 目标序列的embedding和位置编码： (batch_size, target_seq_len, d_model)
- 输出： (batch_size, tar_seq_len, d_model)

解码器训练时输入：
SOS: 序列开始标记
EOS: 序列结束标记

```
tar_inp = "SOS  A     lion  in    the    jungle   is        sleeping" (编码器输入)
tar_real = "A   lion  in    the   jungle is       sleeping  EOS"      (预测目标)
```

transform输出： # (batch_size, tar_seq_len, target_vocab_size)



# BERT

embedding：
token embeddings 和 position embedding： 由embedding_lookup方式进行训练






# seq2seq任务
- Encoder
  - Layer
    - multi-head self-attention mechanism
      - residual connection
      - normalisation
    - fully connected feed-forward network
      - residual connection
      - normalisation

- Decoder
  - 


# faiss

https://waltyou.github.io/Faiss-Introduce/

```python
import numpy as np
import faiss

dimension = 2
index = faiss.IndexIDMap2(faiss.IndexFlatL2(dimension))

# embedding must be type of float32
ids = np.array([1,2,3])
data = np.array([
    [0.9840072 , 0.34055966],
    [0.884534  , 0.14055097],
    [0.19493523, 0.72189105]
]).astype('float32')
index.add_with_ids(data, ids)


topk = 2
search_data = np.array([
    [0.9840072 , 0.34055966],
    [0.19493523, 0.72189105]
]).astype('float32')
result_score, result_ids = index.search(search_data, topk)

```


聚类划分搜索空间
```python
import numpy as np
import faiss

dimension = 2
centroids = 2
quantizer = faiss.IndexFlatL2(dimension)  # quantizer 向量和聚类中心的计算索引
#index = faiss.IndexIVFFlat(quantizer, dimension, centroids, faiss.METRIC_L2)
index = faiss.IndexIVFFlat(quantizer, dimension, centroids, faiss.METRIC_INNER_PRODUCT)

ids = np.array([1,2,3])
data = np.array([
    [0.9840072 , 0.34055966],
    [0.884534  , 0.14055097],
    [0.19493523, 0.72189105]
]).astype('float32')
index.train(data)
index.add_with_ids(data, ids)



```


使用工厂模式构建索引
```python
dimension = 2
index = faiss.index_factory(dimension, "IVF2,Flat", faiss.METRIC_INNER_PRODUCT)


ids = np.array([1,2,3])
data = np.array([
    [0.9840072 , 0.34055966],
    [0.884534  , 0.14055097],
    [0.19493523, 0.72189105]
]).astype('float32')
index.train(data)
index.add_with_ids(data, ids)

#index = faiss.IndexIDMap2(index)
```


# word2vec

- skip-gram ( Continuous Skip-gram Model )
- CBOW ( Continuous Bag-of-Words Model )


skip-gram训练样本格式：

```
# 句子 -> (target, context) pair,  use target predict context

window_size = 2 # skip-gram 窗口大小
num_ns = 4

targets: (batch_size, 1)
contexts: (batch_size, )

```


