

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


# Reference

https://zhuanlan.zhihu.com/p/605973097 学习过程

https://github.com/lucidrains/denoising-diffusion-pytorch  (diffusion model)



CompVis - Computer Vision and Learning research group at Ludwig Maximilian University of Munich (formerly Computer Vision Group at Heidelberg University)

https://github.com/CompVis/latent-diffusion (latent diffusion model)
https://github.com/CompVis/stable-diffusion (latent text-to-image diffusion model)



https://github.com/XavierXiao/Dreambooth-Stable-Diffusion