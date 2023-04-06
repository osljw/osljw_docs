
# PyTorch


tensor
- requires_grad: bool 标识tensor是否需要计算梯度
- grad_fn: function 标识tensor是哪个函数的输出
- backward: function 计算梯度
- grad: tensor 梯度结果
- is_leaf: 用户创建的tensor为leaf节点， grad_fn为None





https://pytorch.org/blog/computational-graphs-constructed-in-pytorch/

memory-mapped tensor
https://github.com/pytorch/pytorch/issues/24119


## accelerate
> A simple way to train and use PyTorch models with multi-GPU, TPU, mixed-precision


查看模型参数量
```py
sum([param.nelement () for param in model.parameters ()])
```


```py
for name, layer in model.named_modules():
    print(name, layer)
```


unet

time_embed

input: (N, 320)
output: (N, 320*4)





# Engine

- https://www.52coding.com.cn/2019/05/05/PyTorch4/

