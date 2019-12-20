

# multi task
- ctr： 点击率(广告曝光之后点击的概率)

- cvr:  转化率
    - 广告曝光之后转化的概率
    - 广告点击之后转化的概率

cvr模型:
- 对广告曝光之后转化的概率进行建模
    - 优势: 样本空间覆盖较全 
    - 劣势：正样本占比太低

- 对广告点击之后转化的概率进行建模
    - 优势: 正样本占比相对较高 
    - 劣势: 不能够对未点击的样本进行建模




# ESMM

CVR预估的新思路：完整空间多任务模型
https://zhuanlan.zhihu.com/p/37562283

- Estimator实现 https://zhuanlan.zhihu.com/p/42214716 
- Estimator实现 https://github.com/lambdaji/tf_repos/tree/master/DeepMTL
- 阿里xdl https://github.com/alibaba/x-deeplearning/wiki/%E5%85%A8%E7%A9%BA%E9%97%B4%E5%A4%9A%E4%BB%BB%E5%8A%A1%E6%A8%A1%E5%9E%8B(ESMM)


