
# chatglm

```
git clone https://github.com/THUDM/ChatGLM-6B
cd ChatGLM-6B
```

```
mkdir THUDM
cd THUDM

# if you want to clone without large files – just their pointers
# prepend your git clone with the following env var:
GIT_LFS_SKIP_SMUDGE=1

git lfs install
git clone https://huggingface.co/THUDM/chatglm-6b
```

模型继承结构
- transformers.modeling_utils.PreTrainedModel
    - ChatGLMPreTrainedModel
        - ChatGLMForConditionalGeneration

```
ChatGLMForConditionalGeneration(
  (transformer): ChatGLMModel(
    (word_embeddings): Embedding(150528, 4096)
    (layers): ModuleList(
      (0-27): 28 x GLMBlock(
        (input_layernorm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
        (attention): SelfAttention(
          (rotary_emb): RotaryEmbedding()
          (query_key_value): Linear(in_features=4096, out_features=12288, bias=True)
          (dense): Linear(in_features=4096, out_features=4096, bias=True)
        )
        (post_attention_layernorm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
        (mlp): GLU(
          (dense_h_to_4h): Linear(in_features=4096, out_features=16384, bias=True)
          (dense_4h_to_h): Linear(in_features=16384, out_features=4096, bias=True)
        )
      )
    )
    (final_layernorm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
  )
  (lm_head): Linear(in_features=4096, out_features=150528, bias=False)
)
```

预测过程
```py
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("./THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("./THUDM/chatglm-6b", trust_remote_code=True).float()
#.half().cuda()
model = model.eval()

prompt = "您好"
input_ids = tokenizer([prompt], return_tensors="pt", padding=True)

input_ids = input_ids.to(model.device)

max_length= 2048
num_beams=1
do_sample=True
top_p=0.7
temperature=0.95
logits_processor=None

gen_kwargs = {"max_length": max_length, "num_beams": num_beams, "do_sample": do_sample, "top_p": top_p,
                      "temperature": temperature, "logits_processor": logits_processor}
outputs = model.generate(**input_ids, **gen_kwargs)

model_inputs = model.prepare_inputs_for_generation(input_ids['input_ids'])

# <!-- outputs = model(
#     **model_inputs,
#     return_dict=True,
#     output_attentions=output_attentions,
#     output_hidden_states=output_hidden_states,
# ) -->

inputs_embeds = model.transformer.word_embeddings(model_inputs['input_ids'])
# [seq_len, batch, hidden_size]
hidden_states = inputs_embeds.transpose(0, 1)

model.transformer.layers[0](hidden_states, model_inputs['position_ids'], model_inputs['attention_mask'], torch.tensor(0))

```

transformers\generation\utils.py

- model.generate()  # GenerationMixin.generate
    - model.sample() # GenerationMixin.sample
        - model.prepare_inputs_for_generation
        - model.forward
            - model.transformer() # ChatGLMModel.forward()

ChatGLMForConditionalGeneration.transformer
GenerationMixin.sample
model()
ChatGLMModel.forward()

## 内存

https://huggingface.co/docs/transformers/main_classes/model?highlight=from_pretrained#large-model-loading

初始化 word_embeddings时使用skip_init，跳过参数初始化


from_pretrained函数的low_cpu_mem_usage参数

设置device_map="auto"时，会自动

sharded checkpoint 分片检查点模型文件

`pytorch_model.bin.index.json` 模型参数在分片模型文件中的分布情况


## FAQ

> RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'

pytorch目前不支持half模式在cpu上运行
`model.half()` 修改为`model.float()`

> PYTORCH_CUDA_ALLOC_CONF

6G显存的GPU， 使用模型`THUDM/chatglm-6b-int4-qe`, windows 设置环境变量PYTORCH_CUDA_ALLOC_CONF, 避免pytorch碎片化的分配显存导致Out of memory

> RuntimeError: mixed dtype (CPU): expect input to have scalar type of BFloat16

```
for name, t in model.named_parameters():
    print(name, t.device, t.shape, t.dtype)
```

```
transformer.word_embeddings.weight cpu torch.Size([150528, 4096]) torch.float16
transformer.layers.0.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.0.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.0.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.0.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.0.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.0.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.0.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.0.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.0.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.0.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.0.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.0.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.1.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.1.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.1.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.1.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.1.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.1.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.1.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.1.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.1.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.1.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.1.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.1.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.2.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.2.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.2.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.2.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.2.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.2.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.2.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.2.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.2.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.2.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.2.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.2.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.3.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.3.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.3.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.3.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.3.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.3.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.3.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.3.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.3.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.3.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.3.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.3.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.4.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.4.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.4.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.4.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.4.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.4.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.4.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.4.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.4.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.4.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.4.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.4.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.5.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.5.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.5.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.5.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.5.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.5.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.5.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.5.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.5.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.5.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.5.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.5.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.6.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.6.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.6.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.6.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.6.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.6.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.6.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.6.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.6.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.6.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.6.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.6.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.7.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.7.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.7.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.7.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.7.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.7.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.7.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.7.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.7.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.7.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.7.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.7.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.8.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.8.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.8.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.8.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.8.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.8.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.8.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.8.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.8.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.8.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.8.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.8.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.9.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.9.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.9.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.9.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.9.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.9.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.9.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.9.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.9.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.9.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.9.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.9.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.10.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.10.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.10.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.10.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.10.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.10.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.10.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.10.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.10.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.10.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.10.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.10.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.11.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.11.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.11.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.11.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.11.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.11.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.11.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.11.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.11.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.11.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.11.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.11.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.12.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.12.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.12.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.12.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.12.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.12.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.12.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.12.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.12.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.12.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.12.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.12.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.13.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.13.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.13.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.13.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.13.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.13.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.13.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.13.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.13.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.13.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.13.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.13.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.14.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.14.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.14.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.14.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.14.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.14.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.14.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.14.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.14.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.14.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.14.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.14.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.15.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.15.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.15.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.15.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.15.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.15.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.15.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.15.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.15.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.15.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.15.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.15.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.16.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.16.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.16.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.16.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.16.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.16.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.16.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.16.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.16.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.16.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.16.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.16.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.17.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.17.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.17.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.17.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.17.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.17.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.17.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.17.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.17.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.17.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.17.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.17.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.18.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.18.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.18.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.18.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.18.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.18.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.18.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.18.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.18.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.18.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.18.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.18.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.19.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.19.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.19.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.19.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.19.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.19.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.19.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.19.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.19.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.19.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.19.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.19.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.20.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.20.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.20.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.20.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.20.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.20.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.20.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.20.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.20.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.20.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.20.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.20.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.21.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.21.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.21.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.21.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.21.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.21.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.21.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.21.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.21.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.21.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.21.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.21.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.22.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.22.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.22.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.22.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.22.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.22.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.22.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.22.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.22.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.22.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.22.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.22.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.23.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.23.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.23.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.23.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.23.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.23.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.23.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.23.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.23.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.23.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.23.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.23.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.24.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.24.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.24.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.24.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.24.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.24.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.24.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.24.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.24.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.24.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.24.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.24.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.25.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.25.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.25.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.25.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.25.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.25.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.25.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.25.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.25.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.25.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.25.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.25.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.26.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.26.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.26.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.26.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.26.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.26.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.26.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.26.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.26.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.26.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.26.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.26.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.layers.27.input_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.27.input_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.27.attention.query_key_value.weight cpu torch.Size([12288, 4096]) torch.float16
transformer.layers.27.attention.query_key_value.bias cpu torch.Size([12288]) torch.float16
transformer.layers.27.attention.dense.weight cpu torch.Size([4096, 4096]) torch.float16
transformer.layers.27.attention.dense.bias cpu torch.Size([4096]) torch.float16
transformer.layers.27.post_attention_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.layers.27.post_attention_layernorm.bias cpu torch.Size([4096]) torch.float32
transformer.layers.27.mlp.dense_h_to_4h.weight cpu torch.Size([16384, 4096]) torch.float16
transformer.layers.27.mlp.dense_h_to_4h.bias cpu torch.Size([16384]) torch.float16
transformer.layers.27.mlp.dense_4h_to_h.weight cpu torch.Size([4096, 16384]) torch.float16
transformer.layers.27.mlp.dense_4h_to_h.bias cpu torch.Size([4096]) torch.float16
transformer.final_layernorm.weight cpu torch.Size([4096]) torch.float32
transformer.final_layernorm.bias cpu torch.Size([4096]) torch.float32
```

> https://stackoverflow.com/questions/69994731/what-is-the-difference-between-cuda-amp-and-model-half



# Huggingface Transformers


## AutoTokenizer
