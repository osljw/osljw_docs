
Sampling-Bias-Corrected Neural Modeling for Large CorpusItem Recommendations

- tens of millions of videos
- long-tail content


- batch softmax optimization
    - However, as shown in our experiments,batch softmax is subject to sampling bias and could severely restrictthe model performance without any correction. 



# 推荐算法


- 基于内容的推荐(Content-based Recommendation)
    - 对内容相似性建模（根据物品或内容的元数据）
    - 根据目标用户自身喜欢的历史内容推荐相似内容

- 基于协同过滤的推荐(Collaborative Filtering-based Recommendation)
    - 基于用户的协同过滤推荐(User-based)
        - 对用户相似性建模 (根据用户在物品上的行为数据， 用户-物品共现对)
        - 推荐相似用户喜欢的内容给目标用户
    - 基于物品的协同过滤推荐(Item-based）
        - 对物品相似性建模 (根据用户在物品上的行为数据， 物品-物品共现对)
        - 推荐目标用户自身喜欢的历史内容推荐相似内容
    - 基于模型的协同过滤推荐(Model-based)




- BPR(Bayesian Personalized Ranking)