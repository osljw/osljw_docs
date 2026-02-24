
# AI


# Gradio 

机器学习模型web可视化

# stable-diffusion-webui

功能

- txt2img
- img2img
    - sketch
    - inpaint
    - outpaint


HyperNetwork: train a small network to influence the weights of a larger one

textual inversion
DreamBooth 
LoRA
customize (or personalize) the contents in the generated results using a small set of images with same topics or objects


Codeformer 人脸修复
https://github.com/sczhou/CodeFormer

# Diffusion Models 论文


- Denoising Diffusion Probabilistic Models 
    - 2020
    - DDPM
    - https://arxiv.org/abs/2006.11239
    - https://github.com/hojonathanho/diffusion （官方 tensorflow）
    - https://github.com/lucidrains/denoising-diffusion-pytorch (pytorch)

- Denoising Diffusion Implicit Mode
    - DDIM

- High-Resolution Image Synthesis with Latent Diffusion Models
    - CVPR 2022
    - LDM （Latent Diffusion Models
    - https://github.com/CompVis/latent-diffusion


- Adding Conditional Control to Text-to-Image Diffusion Models
    - 2023
    - https://github.com/lllyasviel/ControlNet


- LoRA: Low-Rank Adaptation of Large Language Models
    - [Submitted on 17 Jun 2021 (v1), last revised 16 Oct 2021 (this version, v2)]
    
- DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation
    - https://dreambooth.github.io/


# LDM

数据： LAION

perceptual loss
patch-based adversarial objective

CLIP（Contrastive Language-Image Pre-Training）
text encoder (CLIP ViT-L/14) 
PLMS

# DreamBooth

~3-5 images of a subject (low-resolution and high-resolution)

unique identifier

class-specific prior preservation loss

super resolution components


language drift


## run
webui dreambooth： GPU 10GB


# Reference

https://zhuanlan.zhihu.com/p/605973097 学习过程

https://github.com/lucidrains/denoising-diffusion-pytorch  (diffusion model)



CompVis - Computer Vision and Learning research group at Ludwig Maximilian University of Munich (formerly Computer Vision Group at Heidelberg University)

https://github.com/CompVis/latent-diffusion (latent diffusion model)
https://github.com/CompVis/stable-diffusion (latent text-to-image diffusion model)



https://github.com/XavierXiao/Dreambooth-Stable-Diffusion


# streamlit


- st.cache_resource
    - cache global resources,  across all users, sessions, and reruns
    - ML models or database connections

- st.cache_data
    - creates a new copy of the data at each function call


Session State: share variables between reruns, for each user session

# Prompt

prompt prefix


文本摘要： TL;DR




# 

- 语音输入
- 语音转文本
- 语言模型处理
- 文本转语音



# 扩散模型（Diffusion Model）原理与代码对照
扩散模型的核心是**“逐步加噪→逐步去噪”** 的双向过程：先通过固定的噪声过程将真实数据逐步转化为纯噪声，再训练一个模型学习反向去噪过程，最终从随机噪声中生成新数据。本文将结合数学原理与 PyTorch 代码，从“前向扩散”“反向扩散”“模型训练与生成”三个核心模块展开对照讲解。


## 一、核心原理总览
扩散模型分为两个对称过程，均基于马尔可夫链（每一步状态仅依赖上一步）：
1. **前向扩散（Forward Diffusion）**：从真实数据 \( x_0 \) 出发，逐步加入高斯噪声，经过 \( T \) 步（\( T \) 通常取 1000/2000）得到纯噪声 \( x_T \)（近似标准高斯分布）。
2. **反向扩散（Reverse Diffusion）**：从随机噪声 \( x_T \) 出发，训练一个模型 \( \epsilon_\theta(x_t, t) \) 预测每一步的加噪噪声，逐步“去噪”恢复出真实数据 \( x_0 \)。

核心公式约定：
- \( x_0 \)：真实数据（如图片、文本嵌入）
- \( x_t \)：第 \( t \) 步扩散后的样本（\( t \in [0, T] \)）
- \( \beta_t \)：噪声调度器（每步加噪强度，预先设定）
- \( \alpha_t = 1 - \beta_t \)，\( \bar{\alpha}_t = \prod_{s=1}^t \alpha_s \)（累积乘积，简化计算）


## 二、模块1：前向扩散（加噪过程）
### 原理
前向扩散是**固定、无需训练**的过程，每一步遵循高斯分布：
\[ x_t = \sqrt{\alpha_t} \cdot x_{t-1} + \sqrt{1 - \alpha_t} \cdot \epsilon_{t-1} \]
其中 \( \epsilon_{t-1} \sim \mathcal{N}(0, I) \) 是标准高斯噪声。

#### 关键简化：一步到位计算 \( x_t \)
由于马尔可夫性，可直接从 \( x_0 \) 计算任意 \( t \) 步的 \( x_t \)（无需迭代）：
\[ x_t = \sqrt{\bar{\alpha}_t} \cdot x_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \epsilon \]
其中 \( \epsilon \sim \mathcal{N}(0, I) \)，这一简化是训练的核心（直接用 \( x_0 \) 生成 \( x_t \)，避免逐步加噪）。

#### 噪声调度器设计
\( \beta_t \) 需从小学到大（如 \( \beta_1=1e-4 \)，\( \beta_T=2e-2 \)），确保前期加噪温和（数据结构保留），后期加噪剧烈（快速收敛到纯噪声）。

### 代码对照（PyTorch）
```python
import torch
import torch.nn as nn
import numpy as np

# 1. 设定扩散超参数
T = 1000  # 扩散总步数
beta_start = 1e-4
beta_end = 2e-2

# 2. 生成噪声调度器 β_t（线性调度）
beta = torch.linspace(beta_start, beta_end, T, dtype=torch.float32)
alpha = 1. - beta
alpha_bar = torch.cumprod(alpha, dim=0)  # 累积乘积 ᾱ_t = α1*α2*...*αt

# 3. 前向扩散：从 x0 生成任意 t 步的 xt（一步到位）
def forward_diffusion(x0: torch.Tensor, t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Args:
        x0: 真实数据，shape=(batch_size, C, H, W)
        t: 时间步，shape=(batch_size,)
    Returns:
        xt: 加噪后的数据
        eps: 加入的噪声（用于训练标签）
    """
    batch_size = x0.shape[0]
    # 生成标准高斯噪声
    eps = torch.randn_like(x0)
    # 获取每个样本对应的 ᾱ_t（扩展维度匹配 x0）
    alpha_bar_t = alpha_bar[t].view(batch_size, 1, 1, 1)  # shape=(B,1,1,1)
    # 应用核心公式：xt = sqrt(ᾱ_t)*x0 + sqrt(1-ᾱ_t)*eps
    xt = torch.sqrt(alpha_bar_t) * x0 + torch.sqrt(1 - alpha_bar_t) * eps
    return xt, eps
```

### 代码-原理对应说明
| 代码逻辑 | 对应原理 |
|----------|----------|
| `beta = linspace(...)` | 设定噪声调度器 \( \beta_t \)（线性增长） |
| `alpha_bar = cumprod(alpha)` | 计算累积乘积 \( \bar{\alpha}_t \) |
| `eps = randn_like(x0)` | 生成噪声 \( \epsilon \sim \mathcal{N}(0, I) \) |
| `xt = sqrt(alpha_bar_t)*x0 + sqrt(1-alpha_bar_t)*eps` | 一步到位计算 \( x_t \) 的核心公式 |


## 三、模块2：反向扩散（去噪过程）
### 原理
反向扩散是**需要训练**的过程，目标是从 \( x_t \) 恢复 \( x_{t-1} \)。由于前向扩散是高斯分布，反向扩散也近似为高斯分布：
\[ p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \sigma_t^2 I) \]
其中：
- 方差 \( \sigma_t^2 \)：固定为 \( \beta_t \)（简化设计，无需训练）
- 均值 \( \mu_\theta(x_t, t) \)：通过模型预测噪声推导得到：
  \[ \mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right) \]
  核心思想：用模型 \( \epsilon_\theta(x_t, t) \) 预测前向扩散时加入的噪声 \( \epsilon \)，再通过噪声反推去噪后的均值。

### 核心模型：噪声预测器 \( \epsilon_\theta \)
\( \epsilon_\theta \) 是一个带时间步编码的神经网络（如 U-Net），输入为 \( x_t \) 和时间步 \( t \)（需嵌入为向量），输出为预测的噪声 \( \hat{\epsilon} \)。

#### 时间步嵌入（Time Embedding）
时间步 \( t \) 是标量，需转化为高维向量并融入网络，常用**正弦位置编码**（类似 Transformer）：
\[ PE(t, 2k) = \sin\left( \frac{t}{10000^{2k/d}} \right),\quad PE(t, 2k+1) = \cos\left( \frac{t}{10000^{2k/d}} \right) \]
其中 \( d \) 是嵌入维度。

### 代码对照（PyTorch）
#### 1. 时间步嵌入模块
```python
class TimeEmbedding(nn.Module):
    def __init__(self, embed_dim: int):
        super().__init__()
        self.embed_dim = embed_dim
        # 正弦编码的频率参数
        half_dim = embed_dim // 2
        emb = np.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, dtype=torch.float32) * -emb)
        self.register_buffer("emb", emb)  # 不参与训练的缓冲区

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        """
        Args:
            t: 时间步，shape=(batch_size,)
        Returns:
            time_emb: 时间步嵌入，shape=(batch_size, embed_dim)
        """
        t = t.unsqueeze(1)  # (B,1)
        emb = t * self.emb.unsqueeze(0)  # (B, half_dim)
        # 正弦+余弦编码
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1)
        # 若嵌入维度为奇数，补一个维度
        if self.embed_dim % 2 != 0:
            emb = torch.cat([emb, torch.zeros_like(emb[:, :1])], dim=1)
        return emb
```

#### 2. 噪声预测器（简化U-Net）
```python
class SimpleUNet(nn.Module):
    def __init__(self, in_channels: int = 3, out_channels: int = 3, embed_dim: int = 128):
        super().__init__()
        self.time_embed = TimeEmbedding(embed_dim)
        # 时间嵌入的MLP（将嵌入映射到与特征图通道匹配的维度）
        self.time_mlp = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Linear(embed_dim * 4, embed_dim)
        )
        # 下采样模块（提取特征）
        self.down = nn.Sequential(
            nn.Conv2d(in_channels, embed_dim, 3, padding=1),
            nn.GELU(),
            nn.Conv2d(embed_dim, embed_dim * 2, 3, stride=2, padding=1),
            nn.GELU()
        )
        # 中间特征提取
        self.mid = nn.Sequential(
            nn.Conv2d(embed_dim * 2, embed_dim * 4, 3, padding=1),
            nn.GELU(),
            nn.Conv2d(embed_dim * 4, embed_dim * 2, 3, padding=1),
            nn.GELU()
        )
        # 上采样模块（恢复尺寸）
        self.up = nn.Sequential(
            nn.ConvTranspose2d(embed_dim * 2, embed_dim, 3, stride=2, padding=1, output_padding=1),
            nn.GELU(),
            nn.Conv2d(embed_dim, out_channels, 3, padding=1)
        )

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: 加噪数据 xt，shape=(B, C, H, W)
            t: 时间步，shape=(B,)
        Returns:
            eps_pred: 预测的噪声，shape=(B, C, H, W)
        """
        # 时间步嵌入
        time_emb = self.time_embed(t)  # (B, embed_dim)
        time_emb = self.time_mlp(time_emb)  # (B, embed_dim)
        # 下采样
        x = self.down(x)  # (B, embed_dim*2, H/2, W/2)
        # 时间嵌入与特征图相加（广播：time_emb -> (B, embed_dim*2, 1, 1)）
        x = x + time_emb.unsqueeze(-1).unsqueeze(-1).expand(-1, x.shape[1], -1, -1)
        # 中间特征
        x = self.mid(x)  # (B, embed_dim*2, H/2, W/2)
        # 上采样并预测噪声
        eps_pred = self.up(x)  # (B, C, H, W)
        return eps_pred
```

#### 3. 反向扩散采样（从 xt 到 x_{t-1}）
```python
def reverse_diffusion_step(model: nn.Module, xt: torch.Tensor, t: torch.Tensor, beta: torch.Tensor, alpha: torch.Tensor, alpha_bar: torch.Tensor) -> torch.Tensor:
    """
    反向扩散单步：从 xt 生成 x_{t-1}
    Args:
        model: 噪声预测器 ε_θ
        xt: 第 t 步数据，shape=(B, C, H, W)
        t: 时间步，shape=(B,)
        beta, alpha, alpha_bar: 调度器参数
    Returns:
        x_t_minus_1: 第 t-1 步数据
    """
    batch_size = xt.shape[0]
    # 模型预测噪声 ε̂
    eps_pred = model(xt, t)
    # 获取当前步的 α_t, ᾱ_t, β_t（扩展维度）
    alpha_t = alpha[t].view(batch_size, 1, 1, 1)
    alpha_bar_t = alpha_bar[t].view(batch_size, 1, 1, 1)
    beta_t = beta[t].view(batch_size, 1, 1, 1)
    # 计算反向扩散的均值 μ_θ
    mu_theta = (1 / torch.sqrt(alpha_t)) * (
        xt - (1 - alpha_t) / torch.sqrt(1 - alpha_bar_t) * eps_pred
    )
    # 生成噪声（t=0时无需加噪声，直接返回均值）
    if t[0] == 0:
        return mu_theta
    else:
        # 方差 σ_t^2 = β_t（固定）
        sigma_t = torch.sqrt(beta_t)
        z = torch.randn_like(xt)
        # 采样 x_{t-1} ~ N(μ_θ, σ_t^2 I)
        x_t_minus_1 = mu_theta + sigma_t * z
        return x_t_minus_1
```

### 代码-原理对应说明
| 代码逻辑 | 对应原理 |
|----------|----------|
| `TimeEmbedding` | 时间步嵌入 \( PE(t) \)，将标量 \( t \) 转化为高维向量 |
| `SimpleUNet` | 噪声预测器 \( \epsilon_\theta(x_t, t) \)，输入 \( x_t \) 和 \( t \) 预测噪声 |
| `mu_theta = (1/sqrt(alpha_t)) * (xt - (1-alpha_t)/sqrt(1-alpha_bar_t)*eps_pred)` | 反向扩散均值公式 |
| `x_t_minus_1 = mu_theta + sigma_t * z` | 从高斯分布 \( \mathcal{N}(\mu_\theta, \sigma_t^2 I) \) 采样 \( x_{t-1} \) |


## 四、模块3：模型训练与生成
### 训练原理
训练的核心是**最小化预测噪声与真实噪声的MSE损失**：
1. 随机采样真实数据 \( x_0 \) 和时间步 \( t \)（\( t \sim Uniform(0, T) \)）
2. 通过前向扩散生成 \( x_t \) 和真实噪声 \( \epsilon \)
3. 模型预测噪声 \( \hat{\epsilon} = \epsilon_\theta(x_t, t) \)
4. 损失函数：\( \mathcal{L} = \mathbb{E}_{x_0, t, \epsilon} \left[ \|\epsilon - \hat{\epsilon}\|_2^2 \right] \)

### 生成原理
生成是反向扩散的完整迭代过程：
1. 从标准高斯噪声 \( x_T \sim \mathcal{N}(0, I) \) 出发
2. 从 \( t=T \) 逐步迭代到 \( t=1 \)，每步用 `reverse_diffusion_step` 生成 \( x_{t-1} \)
3. 当 \( t=0 \) 时，直接输出均值 \( \mu_\theta \)，即为生成的新数据 \( x_0 \)

### 代码对照（PyTorch）
#### 1. 训练流程
```python
# 超参数设定
batch_size = 32
lr = 1e-4
epochs = 100
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 初始化模型、优化器、损失函数
model = SimpleUNet(in_channels=3, out_channels=3).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr)
criterion = nn.MSELoss()

# 模拟数据集（实际使用时替换为真实数据，如CIFAR-10）
# 这里用随机数据示例，shape=(N, 3, 32, 32)，像素值归一化到[0,1]
dataset = torch.randn(1000, 3, 32, 32).clamp(0, 1)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 训练循环
for epoch in range(epochs):
    model.train()
    total_loss = 0.0
    for x0 in dataloader:
        x0 = x0.to(device)
        batch_size = x0.shape[0]
        
        # 1. 随机采样时间步 t（0~T-1）
        t = torch.randint(0, T, (batch_size,), device=device)
        
        # 2. 前向扩散生成 xt 和真实噪声 eps
        xt, eps = forward_diffusion(x0, t)
        
        # 3. 模型预测噪声 eps_pred
        eps_pred = model(xt, t)
        
        # 4. 计算MSE损失并反向传播
        loss = criterion(eps_pred, eps)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * batch_size
    
    avg_loss = total_loss / len(dataset)
    print(f"Epoch {epoch+1}/{epochs}, Avg Loss: {avg_loss:.4f}")
```

#### 2. 生成流程
```python
def generate_samples(model: nn.Module, num_samples: int = 8, img_size: int = 32) -> torch.Tensor:
    """
    从噪声生成新数据
    Args:
        model: 训练好的噪声预测器
        num_samples: 生成样本数
        img_size: 图像尺寸（H=W=img_size）
    Returns:
        samples: 生成的样本，shape=(num_samples, 3, img_size, img_size)
    """
    model.eval()
    # 1. 初始化 x_T 为标准高斯噪声
    x = torch.randn(num_samples, 3, img_size, img_size).to(device)
    
    # 2. 从 t=T 迭代到 t=0
    with torch.no_grad():
        for t in range(T-1, -1, -1):
            # 生成当前步的时间步张量（批量相同）
            t_tensor = torch.tensor([t] * num_samples, device=device)
            # 反向扩散单步更新
            x = reverse_diffusion_step(model, x, t_tensor, beta, alpha, alpha_bar)
    
    # 3. 归一化到[0,1]（去噪后可能超出范围）
    x = torch.clamp(x, 0, 1)
    return x

# 生成样本
samples = generate_samples(model, num_samples=8)
# 可视化（需用matplotlib）
import matplotlib.pyplot as plt
import torchvision.utils as vutils

plt.figure(figsize=(8, 8))
plt.imshow(vutils.make_grid(samples, nrow=4).permute(1, 2, 0).cpu().numpy())
plt.axis("off")
plt.show()
```

### 代码-原理对应说明
| 代码逻辑 | 对应原理 |
|----------|----------|
| 随机采样 \( t \) 和 \( x_0 \) | 训练时的期望采样（\( x_0 \sim p(x_0) \)，\( t \sim Uniform(0,T) \)） |
| `loss = criterion(eps_pred, eps)` | MSE损失 \( \|\epsilon - \hat{\epsilon}\|_2^2 \) |
| `x = torch.randn(...)` | 初始化 \( x_T \sim \mathcal{N}(0, I) \) |
| 循环 `t from T-1 downto 0` | 反向扩散迭代，逐步去噪 |


## 五、关键总结
1. **核心逻辑**：前向扩散（固定加噪）→ 训练噪声预测器 → 反向扩散（迭代去噪生成）
2. **数学核心**：一步到位的 \( x_t \) 计算、反向扩散的高斯均值推导
3. **代码核心**：噪声调度器设计、时间步嵌入、U-Net噪声预测器、反向迭代采样
4. **扩展方向**：
   - 调度器优化（余弦调度、余弦退火）
   - 模型升级（完整U-Net+注意力机制、DDPM/DDIM改进）
   - 应用扩展（文本到图像、超分辨率、语音生成）

通过以上原理与代码的逐模块对照，可清晰理解扩散模型的“数学公式→代码实现”映射关系，在此基础上可进一步探索更复杂的扩散模型变体（如DDIM、Stable Diffusion）。


