

https://github.com/tensorflow/examples/blob/master/community/en/docs/deploy/distributed.md

# Server 创建
> python 层

tensorflow\python\training\server_lib.py
```python
@tf_export("distribute.Server", v1=["distribute.Server", "train.Server"])
@deprecation.deprecated_endpoints("train.Server")
class Server(object):
  def __init__(self,
               server_or_cluster_def,
               job_name=None,
               task_index=None,
               protocol=None,
               config=None,
               start=True):
    self._server_def = _make_server_def(server_or_cluster_def, job_name,
                                        task_index, protocol, config)
    self._server = c_api.TF_NewServer(self._server_def.SerializeToString())
    if start:
      self.start()
```
> c++ 层

tensorflow\c\c_api.cc
```c++
TF_Server* TF_NewServer(const void* proto, size_t proto_len,
                        TF_Status* status) {
#if defined(IS_MOBILE_PLATFORM) || defined(IS_SLIM_BUILD)
  status->status = tensorflow::errors::Unimplemented(
      "Server functionality is not supported on mobile");
  return nullptr;
#else
  tensorflow::ServerDef server_def;
  if (!server_def.ParseFromArray(proto, static_cast<int>(proto_len))) {
    status->status = InvalidArgument(
        "Could not parse provided bytes into a ServerDef protocol buffer");
    return nullptr;
  }

  std::unique_ptr<tensorflow::ServerInterface> out_server;
  status->status = tensorflow::NewServer(server_def, &out_server);
  if (TF_GetCode(status) != TF_OK) return nullptr;

  return new TF_Server(std::move(out_server));
#endif  // defined(IS_MOBILE_PLATFORM) || defined(IS_SLIM_BUILD)
}
```
python层调用c api TF_NewServer函数，tensorflow::NewServer函数根据ServerDef来创建相应的Server

tensorflow\core\distributed_runtime\rpc\grpc_server_lib.h
```c++
class GrpcServer : public ServerInterface {
```

# tensorflow architecture
https://www.tensorflow.org/guide/extend/architecture#client

# client

client 将GraphDef发送给master， 与master进行通信时使用的是MasterInterface接口调用MasterService的功能

# master

- MasterInterface
    - LocalMaster (client和master service位于同一个进程内，直接高效通信)
    - GrpcRemoteMaster (通过grpc与master service进行通信)

> MasterInterface

MasterInterface 为master service提供了统一的实现接口， master service在单机运行时的实现不依赖rpc通信(LocalMaster)，在分布式运行时基于rpc实现(GrpcRemoteMaster)。

master 将划分好的子图传递给worker，与worker service通信时使用的是WorkerInterface接口

tensorflow\core\distributed_runtime\master_interface.h
```c++
// Abstract interface for communicating with the TensorFlow Master service.
//
// This interface supports both RPC-based master implementations, and
// in-process master implementations that do not require an RPC
// roundtrip.
class MasterInterface {
```

> MasterService 

tensorflow\core\protobuf\master_service.proto

# worker

- WorkerInterface
    - Worker
    - GrpcRemoteWorker

> WorkerInterface

tensorflow\core\distributed_runtime\worker_interface.h

> WorkerService

tensorflow\core\protobuf\worker_service.proto




# SavedModel

https://www.tensorflow.org/guide/saved_model?hl=zh_cn#exporting_custom_models

- keras submodel model export
- keras function api model export
- export multiple signatures


# SavedModel c++ 

- tensorflow::SavedModelBundle
  - MetaGraphDef
    - SignatureDef
      - TensorInfo
    - GraphDef

tensorflow\cc\saved_model\loader.h
```
struct SavedModelBundle {
  std::unique_ptr<Session> session;
  MetaGraphDef meta_graph_def;

  /// A TensorFlow Session does not Close itself on destruction. To avoid
  /// resource leaks, we explicitly call Close on Sessions that we create.
  ~SavedModelBundle() {
    if (session) {
      session->Close().IgnoreError();
    }
  }

  SavedModelBundle() = default;
};
```