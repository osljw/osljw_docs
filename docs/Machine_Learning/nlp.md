

# NLP

# 语言模型
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



# 评测
- GLUE


# Transformer
http://jalammar.github.io/illustrated-transformer/

attention
- Q: query-vec
- K: key-vec
- V: value-vec

I为(word_len, embedding_size), Q,K,V的大小为(word_len, v)， WQ, WK, WV的大小为embedding_size * v
Q = I * WQ
K = I * WK
V = I * WV
词的embedding共享Q，K，V的权重矩阵

1. `Q * K^T`: (word_len, word_len) 通过点积得到两个词之间的关联度
2. `Q * K^T / sqrt(d_k)`: 通过sqrt(d_k) 对关联度进行缩放， 数值梯度的稳定
3. `softmax(Q * K^T / sqrt(d_k))`:  (word_len) 用softmax归一化权重
4. `softmax(Q * K^T / sqrt(d_k)) * V`: （word_len, v)

Positional Encoding

# tf.keras.layers.Attention
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