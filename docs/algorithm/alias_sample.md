# alias sample

https://blog.csdn.net/haolexiao/article/details/65157026

从n个带权重的类别中， 按权重进行随机采样


构建方法：
1.找出其中面积小于等于1的列，如i列，这些列说明其一定要被别的事件矩形填上，所以在Prab[i]中填上其面积
2.然后从面积大于1的列中，选出一个，比如j列，用它将第i列填满，然后Alias[i] = j，第j列面积减去填充用掉的面积。

以上两个步骤一直循环，直到所有列的面积都为1了为止。

预处理得到：
1. Prob[i] (0 <= i < n,  Prob[i] >= 0  && Prob[i] <= 1)
2. Alias[i] (0 <=i < n,  Alias[i] >=0 && Alias[i] < n)

采样过程：
第一次随机产生[0, n)之间的整数i，决定落在哪一列。
第二次随机产生[0, 1]之间的浮点数，判断其与Prob[i]大小，如果小于Prob[i]，则采样结果为类别i，如果大于Prob[i]，则采样结果为Alias[i]




```python
import numpy as np
from collections import Counter

class AliasSample:
    def __init__(self, cate_id, cate_weight):
        '''
        Args:
            cate_id: int list, name of cate
            cate_weight: float list, weight of cate, no need to normalize
        '''
        assert len(cate_id) == len(cate_weight), "len of cate_id and cate_weight must be equal"
        self.total_cate = len(cate_id)
        self.cate_id = cate_id
        self.norm_cate_weight = self.normalize_weight(cate_weight)
        probs, alias = self.build_alias_table(self.norm_cate_weight)
        self.probs = probs
        self.alias = alias
        
    def sample(self):
        '''
        Returns: 
            return one sample cate id
        '''
        n = np.random.randint(0, self.total_cate)
        prob = np.random.uniform(0, 1)
        index = None
        if prob < self.probs[n]:
            index = n
        else:
            index = self.alias[n]
        return self.cate_id[index]


    def normalize_weight(self, weights):
        weight_sum = sum(weights)
        norm_weights = [w / weight_sum for w in weights]
        return norm_weights

    
    def build_alias_table(self, norm_weights):
        small, large = [], []
        alias = [0] * self.total_cate
        probs = [0] * self.total_cate

        for i in range(self.total_cate):
            probs[i] = self.total_cate * norm_weights[i]
            if probs[i] < 1:
                small.append(i)
            elif probs[i] > 1:
                large.append(i)

        while small and large:
            index_small, index_large = small.pop(), large.pop()
            tmp_large = probs[index_large] - (1 - probs[index_small])
            alias[index_small] = index_large
            probs[index_large] = tmp_large
            if tmp_large > 1:
                large.append(index_large)
            elif tmp_large < 1:
                small.append(index_large)

        return probs, alias


alias_sample = AliasSample([1, 5, 6], [0.2, 0.3, 0.5])
sample_result = [alias_sample.sample() for x in range(100)]
print(Counter(sample_result))
```