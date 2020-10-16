


# 安装bazel
```
https://github.com/bazelbuild/bazel/releases
```

```
wget https://github.com/bazelbuild/bazel/releases/download/1.0.0/bazel-1.0.0-installer-linux-x86_64.sh
bash bazel-1.0.0-installer-linux-x86_64.sh --prefix=/home/test/software
```
添加到PATH环境变量

bazel 使用
https://blog.bazel.build/2017/02/27/protocol-buffers.html


# tensorflow build

## 配置 
./configure

## 全部编译
```
bazel build --config=opt tensorflow/...
```

编译 c++ 动态链接库
```
bazel build //tensorflow:libtensorflow_cc.so
```

## 头文件

```
cp -r bazel-genfiles/*  include/
cp -r tensorflow  include

查看bazel编译的eigen真实编译地址， 
ls -lrt bazel-tensorflow/external/eigen_archive 
cp -r 【bazel-tensorflow/external/eigen_archive】  include/eigen3 
【把eigen_archive用上边查看的真实地址替换】

cp -r bazel-tensorflow/external/protobuf_archive/src/google include/

cp -r third_party /usr/local/include/tf/
```

头文件 2.0.0
> 直接从源码编译
```
# 输出路径为: bazel-bin/tensorflow/include
bazel build //tensorflow:install_headers

# google protobuf 路径
cp -r bazel-bin/tensorflow/include/src/google bazel-bin/tensorflow/include/google
```

> 通过python pip包获取

`pip show tensorflow`获取tensorflow存放地址
```
# python pip 安装目录, 缺少savedmodel和c api头文件
- python3.7/site-packages/tensorflow/include
- python3.7/site-packages/tensorflow_core/include
```
合并生成完整头文件(这样得到的体积较小~40M)
```
cp -r python3.7/site-packages/tensorflow_core/include include
cp -r bazel-bin/tensorflow/include/tensorflow include/
```


## 库文件
```
cp bazel-bin/libtensorflow_cc.so /usr/local/lib/
```

tensorflow 2.0 
```
bazel-bin/tensorflow/libtensorflow_cc.so.2
bazel-bin/tensorflow/libtensorflow_framework.so.2
```

编译c++ 应用
指定头文件路径 -I../include -I../include/eigen3 -I../include/google

编译pip：
```
bazel build --config=opt -c opt --copt=-O3 --copt=-msse4.1 --copt=-msse4.2 //tensorflow/tools/pip_package:build_pip_package
```
上边命令不会直接生成wheel 包， 而是生成了一个中间脚本
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
在/tmp/tensorflow_pkg目录下生成whl安装包

安装：
```
pip install tensorflow-1.8.0-cp27-cp27mu-linux_x86_64.whl 
```

gdb调试
```
bazel build -c dbg
```
TensorFlow项目是使用bazel编译的，编译时需要加入“-c dbg”并且去掉“-c opt”参数

gdb python
run bazel-bin/tensorflow/python/data/kernel_tests/reader_dataset_ops_test


tensorflow 二次开发
相关头文件手机

```
tensorflow/bazel-genfiles/tensorflow  -> include/tensorflow
tensorflow/tensorflow/core                 -> include/tensorflow/
(解决fatal error: tensorflow/core/framework/tensor.h: No such file or directory)
```

## protobuf
自己工程代码中有使用protobuf时， 容易与tensorflow使用的protobuf版本不一致

确定自己的代码
```
protoc --version
```

确认tensorflow使用的protobuf版本
```
google/protobuf/stubs/common.h 
#define GOOGLE_PROTOBUF_VERSION 3009002
```

选择与tensorflow匹配的protoc版本，更新自己的代码
https://github.com/protocolbuffers/protobuf/releases



# tensorflow serving build
tensorflow serving 编译需要添加优化指令，能明显改善性能

serving 编译和打包
```
find -L bazel-out/k8-opt/ -name '*.o' | grep -v '/main\.o$\|\.grpc\.pb\.o$\|/curl/\|/grpc/\|/cloud/\|/hadoop/' | xargs -i ar qv libtensorflow_serving.a '{}'
（速度太慢）
```

tensorflow_serving 编译完成后相关动态链接库的位置
```
bazel-bin/tensorflow_serving/
```

~/.cache/bazel 中有编译生成的静态库文件

tensorflow serving GPU编译
https://docs.bitnami.com/google/how-to/enable-nvidia-gpu-tensorflow-serving/
```
export TF_NEED_CUDA=1
bazel build -c opt --config=cuda --copt=-O3 tensorflow_serving/model_servers:tensorflow_model_server
```




使用bazel打包成动态链接库

tensorflow serving中tensorflow_serving/example/BUILD 下的目标规则，
```
cc_binary(                                                                                                                 
    name = "inception_client_cc",
    srcs = [
        "inception_client.cc",
    ],
    deps = [
        "//tensorflow_serving/apis:prediction_service_proto",
        "@grpc//:grpc++_unsecure",
        "@org_tensorflow//tensorflow/core:framework",
        "@org_tensorflow//tensorflow/core:lib",
        "@protobuf_archive//:protobuf_lite",
    ],
)
```
为了将inception_client.cc依赖的所有目标打包到一起， 在该文件中增加如下目标规则
```
cc_binary(
    name = "libtensorflow_serving.so",
    linkshared = 1,
    deps = [ 
        "//tensorflow_serving/apis:prediction_service_proto",
        "@grpc//:grpc++_unsecure",
        "@org_tensorflow//tensorflow/core:framework",
        "@org_tensorflow//tensorflow/core:lib",
        "@protobuf_archive//:protobuf_lite",
    ],  
)  
```

优化编译全部：
```
bazel build -c opt --copt=-msse4.1 --copt=-msse4.2 --copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-O3 --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0" tensorflow_serving/...
```
优化编译自定义目标打包：
在 tensorflow_serving/example/BUILD中自定义libtensorflow_serving.so目标，打包成动态链接库
```
bazel build -c opt --copt=-O3  tensorflow_serving/example/libtensorflow_serving.so




#  tensorflow GPU

https://www.tensorflow.org/install/gpu#software_requirements

- NVIDIA GPU 驱动程序版本
```
nvidia-smi
```

- CUDA 工具包
```
nvcc --version
```
cuda 版本对nvidia driver驱动版本有要求
https://docs.nvidia.com/deploy/cuda-compatibility/index.html