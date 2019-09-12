
# session and graph
- TF_Session
    - tensorflow::Session
    - TF_Graph

python层继承关系
- SessionInterface
    - BaseSession
        - Session
        - InteractiveSession

c++层继承关系
- Session
    - DirectSession
    - GrpcSession

# session 创建

> python层

通过tf.Session来创建，通过targe参数确定要创建的session类型，在BaseSession的__init__函数中调用TF_NewSession来创建。 Session对Graph采用引用计数的方式管理，因此同一个Graph可以由多个Session共享

> c++ 层

TF_NewSession最终会调用到c api中的TF_NewSession方法

tensorflow\c\c_api.cc
```c++
TF_Session::TF_Session(tensorflow::Session* s, TF_Graph* g)
    : session(s), graph(g), last_num_graph_nodes(0), extend_before_run(true) {}

TF_Session* TF_NewSession(TF_Graph* graph, const TF_SessionOptions* opt,
                          TF_Status* status) {
  Session* session;
  status->status = NewSession(opt->options, &session);
  if (TF_GetCode(status) == TF_OK) {
    TF_Session* new_session = new TF_Session(session, graph);
    if (graph != nullptr) {
      mutex_lock l(graph->mu);
      graph->sessions[new_session] = "";
    }
    return new_session;
  } else {
    DCHECK_EQ(nullptr, session);
    return nullptr;
  }
}
```

TF_NewSession函数中的NewSession函数根据SessionOptions的设定(如python层target参数)，使用抽象工厂模式找到具体的工厂SessionFactory，来创建相应的Session指针（方便后续多态调用)，然后交由TF_Session进行管理，TF_Session是python和c api沟通的桥梁。

tensorflow\c\c_api_internal.h
```c++
struct TF_Session {
  TF_Session(tensorflow::Session* s, TF_Graph* g);

  tensorflow::Session* session;
  TF_Graph* const graph;

  tensorflow::mutex mu ACQUIRED_AFTER(TF_Graph::mu);
  int last_num_graph_nodes;

  // If true, TF_SessionRun and similar methods will call
  // ExtendSessionGraphHelper before running the graph (this is the default
  // public behavior). Can be set to false if the caller needs to call
  // ExtendSessionGraphHelper manually.
  std::atomic<bool> extend_before_run;
};
```

tensorflow\core\public\session.h
```c++
class Session {
  virtual Status Extend(const RunOptions& run_options, const GraphDef& graph) {
    return errors::Unimplemented(
        "Extend(const RunOptions& run_options, const GraphDef& graph) is not "
        "supported for this session.");
  }

  /// \brief Like `Run`, but allows users to pass in a `RunOptions` proto and
  /// to retrieve non-Tensor metadata output via a `RunMetadata` proto for this
  /// step.  `run_metadata` may be nullptr, in which case any metadata output is
  /// discarded.
  /// NOTE: This API is still experimental and may change.
  virtual Status Run(const RunOptions& run_options,
                     const std::vector<std::pair<string, Tensor> >& inputs,
                     const std::vector<string>& output_tensor_names,
                     const std::vector<string>& target_node_names,
                     std::vector<Tensor>* outputs, RunMetadata* run_metadata);
}
```


tensorflow\core\common_runtime\session.cc
```c++
Status NewSession(const SessionOptions& options, Session** out_session) {
  SessionFactory* factory;
  Status s = SessionFactory::GetFactory(options, &factory);
  if (!s.ok()) {
    *out_session = nullptr;
    LOG(ERROR) << s;
    return s;
  }
  // Starts exporting metrics through a platform-specific monitoring API (if
  // provided). For builds using "tensorflow/core/platform/default", this is
  // currently a no-op.
  monitoring::StartExporter();
  s = factory->NewSession(options, out_session);
  if (!s.ok()) {
    *out_session = nullptr;
  }
  return s;
}
```
如果python层Session创建时target参数为空字符串，则创建DirectSession， 若为grpc://开头则创建GrpcSession。

继承关系
- SessionFactory
  - DirectSessionFactory
  - GrpcSessionFactory -> GrpcSession

GrpcSessionFactory负责创建GrpcSession

tensorflow\core\distributed_runtime\rpc\grpc_session.cc
```c++
/* static */
Status GrpcSession::Create(const SessionOptions& options,
                           std::unique_ptr<GrpcSession>* out_session) {
  std::unique_ptr<GrpcSession> session(new GrpcSession(options));
  std::unique_ptr<MasterInterface> master;
  // For testing, we enable the client to disable the use of the local
  // master registry, so that the RPC stack is exercised.
  if (!options.config.rpc_options().use_rpc_for_inprocess_master()) {
    master = LocalMaster::Lookup(options.target);
  }
  if (!master) {
    SharedGrpcChannelPtr master_channel;
    TF_RETURN_IF_ERROR(
        NewHostPortGrpcChannel(options.target.substr(kSchemePrefixLength),
                               &options.config.rpc_options(), &master_channel));
    master.reset(NewGrpcMaster(master_channel));
  }
  session->SetRemoteMaster(std::move(master));
  *out_session = std::move(session);
  return Status::OK();
}
```
GrpcSession的创建，并使用GrpcRemoteMaster使用master service通信


# session 运行
> python层


tensorflow\python\client\session.py
```python
class SessionInterface(object):

  def run(self, fetches, feed_dict=None, options=None, run_metadata=None):
    """Runs operations in the session. See `BaseSession.run()` for details."""
    raise NotImplementedError('run')

class BaseSession(SessionInterface):
  def run(self, fetches, feed_dict=None, options=None, run_metadata=None):
    options_ptr = tf_session.TF_NewBufferFromString(
        compat.as_bytes(options.SerializeToString())) if options else None
    run_metadata_ptr = tf_session.TF_NewBuffer() if run_metadata else None

    try:
      result = self._run(None, fetches, feed_dict, options_ptr,
                         run_metadata_ptr)
      if run_metadata:
        proto_data = tf_session.TF_GetBuffer(run_metadata_ptr)
        run_metadata.ParseFromString(compat.as_bytes(proto_data))
    finally:
      if run_metadata_ptr:
        tf_session.TF_DeleteBuffer(run_metadata_ptr)
      if options:
        tf_session.TF_DeleteBuffer(options_ptr)
    return result


@tf_export(v1=['Session'])
class Session(BaseSession):
```

调用路径
- _run
    - _do_run
        - _do_call
            - _run_fn (run触发的路径)
                - _extend_graph
                - _call_tf_sessionrun
            - _prun_fn (partial_run触发的路径)

```python
  def _extend_graph(self):
    with self._graph._session_run_lock():  # pylint: disable=protected-access
      tf_session.ExtendSession(self._session)
```

> c++ 层
tf_session.ExtendSession最终会调用到c api中的ExtendSession




tensorflow\c\python_api.cc
```c++
void ExtendSession(TF_Session* session, TF_Status* status) {
  ExtendSessionGraphHelper(session, status);
  session->extend_before_run = false;
}
```

tensorflow\c\c_api.cc
```c++
bool ExtendSessionGraphHelper(TF_Session* session, TF_Status* status) {
  if (session->graph != nullptr) {
    // Take the graph lock before the session lock to avoid deadlock. This is
    // safe since session->graph does not change.
    session->graph->mu.lock();
    mutex_lock session_lock(session->mu);
    const Graph& graph = session->graph->graph;

    const string& mutation_warning = session->graph->sessions[session];
    if (!mutation_warning.empty()) {
      // TODO(b/74949947): turn this back into an error status
      LOG(WARNING) << mutation_warning;
      session->graph->sessions[session].clear();
    }

    const auto num_nodes = graph.num_node_ids();
    if (session->last_num_graph_nodes < num_nodes) {
      // TODO(nolivia): check this on a subset of the graph instead of all of
      // it.
      status->status = graph::ValidateGraphHasNoCycle(session->graph->graph);
      if (TF_GetCode(status) != TF_OK) {
        session->graph->mu.unlock();
        return false;
      }

      GraphDef graph_def;
      *graph_def.mutable_versions() = graph.versions();
      // Fill graph_def with nodes with ids in the range
      // [session->last_num_graph_nodes, num_nodes), that is the nodes
      // added since the last TF_SessionRun() call.
      for (auto id = session->last_num_graph_nodes; id < num_nodes; ++id) {
        Node* const node = graph.FindNodeId(id);
        if (node != nullptr && node->IsOp()) {
          NodeDef* const node_def = graph_def.add_node();
          *node_def = node->def();
        }
      }
      *graph_def.mutable_library() = graph.flib_def().ToProto();
      session->graph->mu.unlock();
      status->status = session->session->Extend(graph_def);
      if (TF_GetCode(status) != TF_OK) {
        // Contract is we always delete input_values[i].
        return false;
      }
      // Note: session->session is not modified if Extend() fails, so
      // we only set last_num_graph_nodes if it succeeds.
      session->last_num_graph_nodes = num_nodes;
    } else {
      session->graph->mu.unlock();
    }
  }
  return true;
}
```
ExtendSessionGraphHelper函数从TF_Session中由TF_Graph获取到GraphDef对象，并使用session->session->Extend(graph_def)反序列化, session->session为Session*类型，会多态调用DirectSession或者GrpcSession

tensorflow\core\common_runtime\direct_session.cc
```c++
Status DirectSession::Extend(const GraphDef& graph) {
  TF_RETURN_IF_ERROR(CheckNotClosed());
  mutex_lock l(graph_state_lock_);
  return ExtendLocked(graph);
}
```
DirectSession::Extend调用ExtendLocked对GraphDef进行拓展（每次run时，graph上可能新增节点）， 第一次调用时会直接使用GraphDef创建GraphExecutionState

tensorflow\core\common_runtime\direct_session.cc
```c++
Status DirectSession::ExtendLocked(const GraphDef& graph) {
  bool already_initialized;
  // If this is the first call, we can initialize the execution state
  // with `graph` and do not need to call `Extend()`.
  TF_RETURN_IF_ERROR(
      MaybeInitializeExecutionState(graph, &already_initialized));
  if (already_initialized) {
    TF_RETURN_IF_ERROR(flib_def_->AddLibrary(graph.library()));
    std::unique_ptr<GraphExecutionState> state;
    TF_RETURN_IF_ERROR(execution_state_->Extend(graph, &state));
    execution_state_.swap(state);
  }
  return Status::OK();
}
```
调用过程
- DirectSession::MaybeInitializeExecutionState
  - GraphExecutionState::MakeForBaseGraph
    - GraphExecutionState::InitBaseGraph

tensorflow\core\common_runtime\graph_execution_state.cc
```c++
/* static */ Status GraphExecutionState::MakeForBaseGraph(
    GraphDef* graph_def, const GraphExecutionStateOptions& options,
    std::unique_ptr<GraphExecutionState>* out_state) {
#ifndef __ANDROID__
  VLOG(4) << "Graph proto is \n" << graph_def->DebugString();
#endif  // __ANDROID__

  std::unique_ptr<GraphExecutionState> ret(
      new GraphExecutionState(graph_def, options));

  TF_RETURN_IF_ERROR(
      AddDefaultAttrsToGraphDef(&ret->original_graph_def_, *ret->flib_def_, 0));
  // TODO(mrry): Refactor InitBaseGraph() so that we don't have to
  // pass an empty BuildGraphOptions (that isn't going to be used when
  // place_pruned_graph is false).
  if (!ret->session_options_->config.graph_options().place_pruned_graph()) {
    TF_RETURN_IF_ERROR(ret->InitBaseGraph(BuildGraphOptions()));
  }
  *out_state = std::move(ret);
  return Status::OK();
}
```
InitBaseGraph函数从GraphDef构建Graph对象， 使用Placer部署Graph对象
