
---
layout:     post
title:      "tensorflow_eager"
subtitle:   "tensorflow_eager"
date:       2019-06-21 14:22:49
author:     "none"
header-img: "img/posts/default_post.jpg"
catalog: true
tags:
    - tag
---


## pywrap_tensorflow

```python
# tensorflow\__init__.py
from tensorflow.python import pywrap_tensorflow

# tensorflow\python\__init__.py
from tensorflow.python import pywrap_tensorflow

# tensorflow\python\pywrap_tensorflow.py
from tensorflow.python.pywrap_tensorflow_internal import *
```

swig 根据*.i文件生成
1. pywrap_tensorflow_internal.cc文件： 包裹c api， 生成动态链接库.so
2. pywrap_tensorflow_internal.py文件： python编程的接口文件, 加载动态链接库

例如使用swig将c源文件中的TFE_Py_Execute函数给python使用
```c
// tensorflow\python\tensorflow.i
%include "tensorflow/python/pywrap_tfe.i"

// tensorflow\python\pywrap_tfe.i
%{
#include "tensorflow/python/eager/pywrap_tfe.h"
%}

// 相应的swig语法，映射python和c的类型
```

TFE_Py_Execute函数的实现如下：
```c
// tensorflow\python\eager\pywrap_tfe.h
void TFE_Py_Execute(TFE_Context* ctx, const char* device_name,
                    const char* op_name, TFE_InputTensorHandles* inputs,
                    PyObject* attrs, TFE_OutputTensorHandles* outputs,
                    TF_Status* out_status);

// tensorflow\python\eager\pywrap_tfe_src.cc
void TFE_Py_Execute(TFE_Context* ctx, const char* device_name,
                    const char* op_name, TFE_InputTensorHandles* inputs,
                    PyObject* attrs, TFE_OutputTensorHandles* outputs,
                    TF_Status* out_status) {
  TFE_Op* op = TFE_NewOp(ctx, op_name, out_status);
  if (TF_GetCode(out_status) != TF_OK) return;
  TFE_OpSetDevice(op, device_name, out_status);
  if (TF_GetCode(out_status) == TF_OK) {
    for (int i = 0; i < inputs->size() && TF_GetCode(out_status) == TF_OK;
         ++i) {
      TFE_OpAddInput(op, inputs->at(i), out_status);
    }
  }
  if (TF_GetCode(out_status) == TF_OK) {
    SetOpAttrs(ctx, op, attrs, 0, out_status);
  }
  Py_BEGIN_ALLOW_THREADS;
  if (TF_GetCode(out_status) == TF_OK) {
    int num_outputs = outputs->size();
    TFE_Execute(op, outputs->data(), &num_outputs, out_status);
    outputs->resize(num_outputs);
  }
  if (TF_GetCode(out_status) != TF_OK) {
    TF_SetStatus(out_status, TF_GetCode(out_status),
                 tensorflow::strings::StrCat(TF_Message(out_status),
                                             " [Op:", op_name, "]")
                     .c_str());
  }
  TFE_DeleteOp(op);
  Py_END_ALLOW_THREADS;
}
```

在python端，可以使用如下代码调用c api中的TFE_Py_Execute函数
```python
# tensorflow\python\eager\execute.py
tensors = pywrap_tensorflow.TFE_Py_Execute(ctx._handle, device_name,
                                            op_name, inputs, attrs,
                                            num_outputs)
```


- TFE_NewOp: c api, 函数
- TFE_Op: c api internal， 结构体
- EagerOperation: c++, 类
```c
// tensorflow\c\eager\c_api.cc
TFE_Op* TFE_NewOp(TFE_Context* ctx, const char* op_or_function_name,
                  TF_Status* status) {
  const char* name = op_or_function_name;  // Shorthand
  const tensorflow::AttrTypeMap* types;
  bool is_function = false;
  status->status = tensorflow::AttrTypeMapForOp(name, &types, &is_function);
  if (!status->status.ok()) {
    return nullptr;
  }
  if (!is_function) {
    const tensorflow::OpDef* op_def;
    status->status = tensorflow::OpDefForOp(op_or_function_name, &op_def);
    if (!status->status.ok()) {
      return nullptr;
    }
    return new TFE_Op(ctx, name, false, types,
                      new TFE_OpInferenceContext(op_def));
  }
  if (!ctx->context->FindFunctionByName(name)) {
    status->status = tensorflow::errors::NotFound(
        "'", name,
        "' is neither a type of a primitive operation nor a name "
        "of a function registered in binary running on ",
        tensorflow::port::Hostname(),
        ". Make sure the operation or function is "
        "registered in the binary running in this process.");
    return nullptr;
  }
  return new TFE_Op(ctx, name, true, types, nullptr);
}
```

```c
// tensorflow\c\eager\c_api_internal.h
struct TFE_Op {
  TFE_Op(TFE_Context* ctx, const char* op, bool is_function,
         const tensorflow::AttrTypeMap* t,
         TFE_OpInferenceContext* inference_ctx)
      : operation(ctx->context, op, is_function, t),
        inference_ctx(inference_ctx) {}

  tensorflow::EagerOperation operation;
  std::unique_ptr<TFE_OpInferenceContext> inference_ctx;
};
```

## EagerOperation

tensorflow\core\common_runtime\eager\eager_operation.h


## EagerTensor

EagerTensor为python类， 在_EagerTensorBase类的基础上经过c api处理生成

```python
# tensorflow\python\framework\ops.py

from tensorflow.python import pywrap_tensorflow as c_api

# TODO(agarwal): consider getting rid of this.
class _EagerTensorBase(Tensor):
    """Base class for EagerTensor."""

# This call creates an EagerTensor class, as a subclass of _EagerTensorBase, and
# registers it with the current module.
EagerTensor = c_api.TFE_Py_InitEagerTensor(_EagerTensorBase)
```

## eager context

tensorflow\python\eager\context.py
```python
def _create_context():
  global _context
  with _context_lock:
    if _context is None:
      _context = Context()


def context():
  """Returns a singleton context object."""
  if _context is None:
    _create_context()
  return _context
```

## enable_eager_execution

tensorflow\python\framework\ops.py
```
@tf_export(v1=["enable_eager_execution"])
def enable_eager_execution(config=None, device_policy=None,
                           execution_mode=None):
  _api_usage_gauge.get_cell().set(True)
  if context.default_execution_mode != context.EAGER_MODE:
    return enable_eager_execution_internal(
        config=config,
        device_policy=device_policy,
        execution_mode=execution_mode,
        server_def=None)
```
