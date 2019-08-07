---
layout:     post
title:      "data input"
date:       2018-11-19 19:00:00
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 学习笔记
---

# Data Input


继承结构
- DatasetV2
- DatasetSource
    - TensorDataset
    - TensorSliceDataset
- ConcatenateDataset
- UnaryDataset
    - BatchDataset
    - MapDataset


## structure 

tensorflow.python.data.util.structure

- RaggedTensorStructure
- SparseTensorStructure

## test

tensorflow/python/data/experimental/kernel_tests

功能实现代码

tensorflow/python/data/util/structure.py


