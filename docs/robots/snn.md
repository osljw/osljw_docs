
# Leaky Integrate-and-Fire (LIF) 模型

Leaky Integrate-and-Fire (LIF) 模型

重置电位（-80mV）

静息电位（-70mV）

阈值电位（-55mV）


电位增量（15mv）： 从静息电位到阈值电位需要达到增量15mv才能激活神经元

电位增量要和输入个数相关

```py

class SpikingNeuron:
    def __init__(self, num_synapses=5, rest_potential=-70, threshold=-55, reset_potential=-80):
        # 神经元基本参数（单位：mV，模拟生物真实电位）
        self.rest_potential = rest_potential  # 静息电位
        self.threshold = threshold            # 放电阈值
        self.reset_potential = reset_potential# 放电后重置电位
        self.membrane_potential = rest_potential  # 当前膜电位
        
        # 突触可塑性核心参数
        self.synapse_weights = np.random.uniform(0.1, 0.5, num_synapses)  # 初始突触权重
        self.learning_rate = 0.01  # 学习率（权重更新步长）
        self.decay_factor = 0.95   # 权重衰减（模拟突触连接自然弱化）

    def integrate_input(self, input_spikes):
        """
        积分阶段：输入脉冲（0/1）通过突触权重转化为膜电位变化
        input_spikes: 一维数组，长度=突触数，元素0（无放电）或1（放电）
        """
        # 输入脉冲 × 突触权重 = 膜电位增量（兴奋性输入）
        potential_increment = np.sum(input_spikes * self.synapse_weights)
        self.membrane_potential += potential_increment
        
        # 膜电位自然衰减（模拟离子泄漏）
        self.membrane_potential = 0.9 * self.membrane_potential + 0.1 * self.rest_potential
        
    def fire(self):
        """
        放电判断：膜电位超过阈值则放电，返回1；否则返回0
        """
        if self.membrane_potential >= self.threshold:
            self.membrane_potential = self.reset_potential  # 放电后重置
            return 1
        return 0


    def update_synapses(self, img, fired):
        """
        突触可塑性核心：根据图像输入和放电结果更新权重
        fired: 神经元是否放电（1/0）
        """
        spikes = self.img_to_spikes(img)
        for i in range(self.input_dim):
            if spikes[i] == 1 and fired == 1:
                # 同步放电（像素激活+神经元放电）→ 权重增强
                self.syn_weights[i] += self.lr * self.syn_weights[i]
            elif spikes[i] != fired:
                # 不同步 → 权重减弱
                self.syn_weights[i] -= self.lr * self.syn_weights[i]
            
            # 权重约束：0.001~0.1（避免过强/过弱）
            self.syn_weights[i] = np.clip(self.syn_weights[i], 0.001, 0.1)
            # 权重自然衰减
            self.syn_weights[i] *= self.decay
```


# STDP（Spike-Timing-Dependent Plasticity）