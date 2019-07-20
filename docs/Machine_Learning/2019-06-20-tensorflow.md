

# OP

## REGISTER_OP



REGISTER_OP 本质定义了一个::tensorflow::register_op::OpDefBuilderReceiver类的对象， 这个对象是一个全局变量，该对象的构造参数为一个模板类::tensorflow::register_op::OpDefBuilderWrapper<SHOULD_REGISTER_OP(name)>生成的对象， 

1. REGISTER_OP 最终生成了两个对象，分别为OpDefBuilderReceiver类和OpDefBuilderWrapper模板类的对象，OpDefBuilderReceiver类在赋值符号(=)的右边，OpDefBuilderWrapper模板类对象在赋值符号(=)的左边，
2. REGISTER_OP宏后可以继续调用OpDefBuilderWrapper模板类的方法，如Input，Attr等



tensorflow\core\framework\op.h
```c++
#define REGISTER_OP(name) REGISTER_OP_UNIQ_HELPER(__COUNTER__, name)

#define REGISTER_OP_UNIQ_HELPER(ctr, name) REGISTER_OP_UNIQ(ctr, name)

#define REGISTER_OP_UNIQ(ctr, name)                                          \
  static ::tensorflow::register_op::OpDefBuilderReceiver register_op##ctr    \
      TF_ATTRIBUTE_UNUSED =                                                  \
          ::tensorflow::register_op::OpDefBuilderWrapper<SHOULD_REGISTER_OP( \
              name)>(name)
```

TF_ATTRIBUTE_UNUSED 修饰变量，当变量未被使用时，编译器不需要给出警告信息

tensorflow\core\platform\macros.h
```c++
#if (defined(__GNUC__) || defined(__APPLE__)) && !defined(SWIG)
#define TF_ATTRIBUTE_UNUSED __attribute__((unused))
#elif defined(_MSC_VER)
#define TF_ATTRIBUTE_UNUSED
```

## OpDefBuilderReceiver
::tensorflow::register_op::OpDefBuilderReceiver 类对象在构造时，会调用OpRegistry::Global() 获取到一个OpRegistry类对象的指针, 然后调用其Register方法。OpRegistry类对象负责收集所有注册的op

tensorflow\core\framework\op.h
```c++
struct OpDefBuilderReceiver {
  // To call OpRegistry::Global()->Register(...), used by the
  // REGISTER_OP macro below.
  // Note: These are implicitly converting constructors.
  OpDefBuilderReceiver(
      const OpDefBuilderWrapper<true>& wrapper);  // NOLINT(runtime/explicit)
  constexpr OpDefBuilderReceiver(const OpDefBuilderWrapper<false>&) {
  }  // NOLINT(runtime/explicit)
};
```

tensorflow\core\framework\op.cc
```c++
namespace register_op {
OpDefBuilderReceiver::OpDefBuilderReceiver(
    const OpDefBuilderWrapper<true>& wrapper) {
  OpRegistry::Global()->Register(
      [wrapper](OpRegistrationData* op_reg_data) -> Status {
        return wrapper.builder().Finalize(op_reg_data);
      });
}
}  // namespace register_op
```

## OpDefBuilderWrapper

OpDefBuilderWrapper是一个模板类，其模板参数为true或false， 通过模板参数来控制op是否进行注册

tensorflow\core\framework\op.h
```c++
// Template specialization that forwards all calls to the contained builder.
template <>
class OpDefBuilderWrapper<true> {
 public:
  explicit OpDefBuilderWrapper(const char name[]) : builder_(name) {}
  OpDefBuilderWrapper<true>& Attr(string spec) {
    builder_.Attr(std::move(spec));
    return *this;
  }
  OpDefBuilderWrapper<true>& Input(string spec) {
    builder_.Input(std::move(spec));
    return *this;
  }
  OpDefBuilderWrapper<true>& Output(string spec) {
    builder_.Output(std::move(spec));
    return *this;
  }
  OpDefBuilderWrapper<true>& SetIsCommutative() {
    builder_.SetIsCommutative();
    return *this;
  }
  OpDefBuilderWrapper<true>& SetIsAggregate() {
    builder_.SetIsAggregate();
    return *this;
  }
  OpDefBuilderWrapper<true>& SetIsStateful() {
    builder_.SetIsStateful();
    return *this;
  }
  OpDefBuilderWrapper<true>& SetAllowsUninitializedInput() {
    builder_.SetAllowsUninitializedInput();
    return *this;
  }
  OpDefBuilderWrapper<true>& Deprecated(int version, string explanation) {
    builder_.Deprecated(version, std::move(explanation));
    return *this;
  }
  OpDefBuilderWrapper<true>& Doc(string text) {
    builder_.Doc(std::move(text));
    return *this;
  }
  OpDefBuilderWrapper<true>& SetShapeFn(
      Status (*fn)(shape_inference::InferenceContext*)) {
    builder_.SetShapeFn(fn);
    return *this;
  }
  const ::tensorflow::OpDefBuilder& builder() const { return builder_; }

 private:
  mutable ::tensorflow::OpDefBuilder builder_;
};
```

## OpDefBuilder

REGISTER_OP().Input().Attr() 调用过程中Input，Attr等函数的参数由OpDefBuilder类对象负责存储，

每个OpDefBuilder类对象包含一个OpRegistrationData对象，调用REGISTER_OP().SetShapeFn()时会更新OpShapeInferenceFn到OpRegistrationData对象中， 这个数据会在随后

OpDefBuilder类的Finalize方法调用时会通过参数指针的方式拷贝OpRegistrationData中的数据到外部

tensorflow\core\framework\op_def_builder.h
```c++
// Builder class passed to the REGISTER_OP() macro.
class OpDefBuilder {
 public:
  // Constructs an OpDef with just the name field set.
  explicit OpDefBuilder(string op_name);

  // Adds an attr to this OpDefBuilder (and returns *this). The spec has
  // format "<name>:<type>" or "<name>:<type>=<default>"
  // where <name> matches regexp [a-zA-Z][a-zA-Z0-9_]*
  // (by convention only using capital letters for attrs that can be inferred)
  // <type> can be:
  //   "string", "int", "float", "bool", "type", "shape", or "tensor"
  //   "numbertype", "realnumbertype", "quantizedtype"
  //       (meaning "type" with a restriction on valid values)
  //   "{int32,int64}" or {realnumbertype,quantizedtype,string}"
  //       (meaning "type" with a restriction containing unions of value types)
  //   "{\"foo\", \"bar\n baz\"}", or "{'foo', 'bar\n baz'}"
  //       (meaning "string" with a restriction on valid values)
  //   "list(string)", ..., "list(tensor)", "list(numbertype)", ...
  //       (meaning lists of the above types)
  //   "int >= 2" (meaning "int" with a restriction on valid values)
  //   "list(string) >= 2", "list(int) >= 2"
  //       (meaning "list(string)" / "list(int)" with length at least 2)
  // <default>, if included, should use the Proto text format
  // of <type>.  For lists use [a, b, c] format.
  //
  // Note that any attr specifying the length of an input or output will
  // get a default minimum of 1 unless the >= # syntax is used.
  //
  // TODO(josh11b): Perhaps support restrictions and defaults as optional
  // extra arguments to Attr() instead of encoding them in the spec string.
  // TODO(josh11b): Would like to have better dtype handling for tensor attrs:
  // * Ability to say the type of an input/output matches the type of
  //   the tensor.
  // * Ability to restrict the type of the tensor like the existing
  //   restrictions for type attrs.
  // Perhaps by linking the type of the tensor to a type attr?
  OpDefBuilder& Attr(string spec);

  // Adds an input or output to this OpDefBuilder (and returns *this).
  // The spec has form "<name>:<type-expr>" or "<name>:Ref(<type-expr>)"
  // where <name> matches regexp [a-z][a-z0-9_]* and <type-expr> can be:
  // * For a single tensor: <type>
  // * For a sequence of tensors with the same type: <number>*<type>
  // * For a sequence of tensors with different types: <type-list>
  // Where:
  //   <type> is either one of "float", "int32", "string", ...
  //                 or the name of an attr (see above) with type "type".
  //   <number> is the name of an attr with type "int".
  //   <type-list> is the name of an attr with type "list(type)".
  // TODO(josh11b): Indicate Ref() via an optional argument instead of
  // in the spec?
  // TODO(josh11b): SparseInput() and SparseOutput() matching the Python
  // handling?
  OpDefBuilder& Input(string spec);
  OpDefBuilder& Output(string spec);

  // Turns on the indicated boolean flag in this OpDefBuilder (and
  // returns *this).
  OpDefBuilder& SetIsCommutative();
  OpDefBuilder& SetIsAggregate();
  OpDefBuilder& SetIsStateful();
  OpDefBuilder& SetAllowsUninitializedInput();

  // Deprecate the op at a certain GraphDef version.
  OpDefBuilder& Deprecated(int version, string explanation);

  // Adds docs to this OpDefBuilder (and returns *this).
  // Docs have the format:
  //   <1-line summary>
  //   <rest of the description>
  //   <name>: <description of name>
  //   <name>: <description of name>
  //     <if long, indent the description on subsequent lines>
  // Where <name> is the name of an attr, input, or output.  Please
  // wrap docs at 72 columns so that it may be indented in the
  // generated output.  For tensor inputs or outputs (not attrs), you
  // may start the description with an "=" (like name:= <description>)
  // to suppress the automatically-generated type documentation in
  // generated output.
#ifndef TF_LEAN_BINARY
  OpDefBuilder& Doc(string text);
#else
  OpDefBuilder& Doc(string text) { return *this; }
#endif

  // Sets the shape function to be used for shape inference.
  //
  // Note that currently (October 2016), python code still requires a
  // RegisterShape call to invoke this; see call_cpp_shape_fn in
  // python/framework/common_shapes.py
  OpDefBuilder& SetShapeFn(OpShapeInferenceFn fn);

  // Sets op_reg_data->op_def to the requested OpDef and
  // op_reg_data->shape_inference_fn to the requested shape inference function,
  // or returns an error.
  // Must be called after all of the above methods.
  //
  // Note that OpDefBuilder only reports parsing errors.  You should also
  // call ValidateOpDef() to detect other problems.
  Status Finalize(OpRegistrationData* op_reg_data) const;

 private:
  friend class FunctionDefHelper;

  // Adds control output to this OpDefBuilder (and returns *this).
  // The <name> must be a valid node name (matches regexp
  // [a-zA-Z][a-zA-Z0-9_]*). Named control output can only exist for functions.
  OpDefBuilder& ControlOutput(string name);

  OpDef* op_def() { return &op_reg_data_.op_def; }

  OpRegistrationData op_reg_data_;
  std::vector<string> attrs_;
  std::vector<string> inputs_;
  std::vector<string> outputs_;
  std::vector<string> control_outputs_;
  string doc_;
  std::vector<string> errors_;
};
```

## OpRegistry

OpRegistry类的Global方法，使用singleton单例模式创建了一个OpRegistry类对象

```c++
void OpRegistry::Register(const OpRegistrationDataFactory& op_data_factory) {
  mutex_lock lock(mu_);
  if (initialized_) {
    TF_QCHECK_OK(RegisterAlreadyLocked(op_data_factory));
  } else {
    deferred_.push_back(op_data_factory);
  }
}
```
OpRegistry类的Register方法，其参数为std::function<Status(OpRegistrationData*)>类型，注册OP时会使用lambda函数包裹OpDefBuilder的Finalize方法作为Register方法的参数

```c++
Status OpRegistry::RegisterAlreadyLocked(
    const OpRegistrationDataFactory& op_data_factory) const {
  std::unique_ptr<OpRegistrationData> op_reg_data(new OpRegistrationData);
  Status s = op_data_factory(op_reg_data.get());
  if (s.ok()) {
    s = ValidateOpDef(op_reg_data->op_def);
    if (s.ok() &&
        !gtl::InsertIfNotPresent(&registry_, op_reg_data->op_def.name(),
                                 op_reg_data.get())) {
      s = errors::AlreadyExists("Op with name ", op_reg_data->op_def.name());
    }
  }
  Status watcher_status = s;
  if (watcher_) {
    watcher_status = watcher_(s, op_reg_data->op_def);
  }
  if (s.ok()) {
    op_reg_data.release();
  } else {
    op_reg_data.reset();
  }
  return watcher_status;
}
```
OpRegistry::Register的方法调用时或者调用后，最终都会调用到RegisterAlreadyLocked方法，该会先构造一个OpRegistrationData， 然后将其作为参数调用OpRegistry::Register接收的lambda函数

调用lambda函数，即调用OpDefBuilder的Finalize方法，在该方法中，
1) 会将OpDefBuilder类对象的OpRegistrationData成员拷贝给OpRegistry::Register方法中的OpRegistrationData对象（更新的是
OpShapeInferenceFn), 
2) 然后调用FinalizeAttr，FinalizeInputOrOutput等方法更新OpDef给OpRegistry::Register方法中的OpRegistrationData对象

```c++
// registry_ 存储注册的OP
mutable std::unordered_map<string, const OpRegistrationData*> registry_
    GUARDED_BY(mu_);

// OpRegistry::RegisterAlreadyLocked方法向registry_中插入OP数据
if (s.ok() &&
    !gtl::InsertIfNotPresent(&registry_, op_reg_data->op_def.name(),
                                op_reg_data.get())) {
    s = errors::AlreadyExists("Op with name ", op_reg_data->op_def.name());
}
```
gtl::InsertIfNotPresent方法会完成最终的注册

```
typedef std::function<Status(const Status&, const OpDef&)> Watcher;
```
在检查OpDef有效，且该op没有注册后，会以OpDef为参数调用watcher_函数


```c++
class OpRegistry : public OpRegistryInterface {
 public:
  typedef std::function<Status(OpRegistrationData*)> OpRegistrationDataFactory;
  void Register(const OpRegistrationDataFactory& op_data_factory);
}
```

tensorflow\core\framework\op.h
```c++
// Users that want to look up an OpDef by type name should take an
// OpRegistryInterface.  Functions accepting a
// (const) OpRegistryInterface* may call LookUp() from multiple threads.
class OpRegistryInterface {
 public:
  virtual ~OpRegistryInterface();

  // Returns an error status and sets *op_reg_data to nullptr if no OpDef is
  // registered under that name, otherwise returns the registered OpDef.
  // Caller must not delete the returned pointer.
  virtual Status LookUp(const string& op_type_name,
                        const OpRegistrationData** op_reg_data) const = 0;

  // Shorthand for calling LookUp to get the OpDef.
  Status LookUpOpDef(const string& op_type_name, const OpDef** op_def) const;
};

// The standard implementation of OpRegistryInterface, along with a
// global singleton used for registering ops via the REGISTER
// macros below.  Thread-safe.
//
// Example registration:
//   OpRegistry::Global()->Register(
//     [](OpRegistrationData* op_reg_data)->Status {
//       // Populate *op_reg_data here.
//       return Status::OK();
//   });
class OpRegistry : public OpRegistryInterface {
 public:
  typedef std::function<Status(OpRegistrationData*)> OpRegistrationDataFactory;

  OpRegistry();
  ~OpRegistry() override;

  void Register(const OpRegistrationDataFactory& op_data_factory);

  Status LookUp(const string& op_type_name,
                const OpRegistrationData** op_reg_data) const override;

  // Fills *ops with all registered OpDefs (except those with names
  // starting with '_' if include_internal == false) sorted in
  // ascending alphabetical order.
  void Export(bool include_internal, OpList* ops) const;

  // Returns ASCII-format OpList for all registered OpDefs (except
  // those with names starting with '_' if include_internal == false).
  string DebugString(bool include_internal) const;

  // A singleton available at startup.
  static OpRegistry* Global();

  // Get all registered ops.
  void GetRegisteredOps(std::vector<OpDef>* op_defs);

  // Get all `OpRegistrationData`s.
  void GetOpRegistrationData(std::vector<OpRegistrationData>* op_data);

  // Watcher, a function object.
  // The watcher, if set by SetWatcher(), is called every time an op is
  // registered via the Register function. The watcher is passed the Status
  // obtained from building and adding the OpDef to the registry, and the OpDef
  // itself if it was successfully built. A watcher returns a Status which is in
  // turn returned as the final registration status.
  typedef std::function<Status(const Status&, const OpDef&)> Watcher;

  // An OpRegistry object has only one watcher. This interface is not thread
  // safe, as different clients are free to set the watcher any time.
  // Clients are expected to atomically perform the following sequence of
  // operations :
  // SetWatcher(a_watcher);
  // Register some ops;
  // op_registry->ProcessRegistrations();
  // SetWatcher(nullptr);
  // Returns a non-OK status if a non-null watcher is over-written by another
  // non-null watcher.
  Status SetWatcher(const Watcher& watcher);

  // Process the current list of deferred registrations. Note that calls to
  // Export, LookUp and DebugString would also implicitly process the deferred
  // registrations. Returns the status of the first failed op registration or
  // Status::OK() otherwise.
  Status ProcessRegistrations() const;

  // Defer the registrations until a later call to a function that processes
  // deferred registrations are made. Normally, registrations that happen after
  // calls to Export, LookUp, ProcessRegistrations and DebugString are processed
  // immediately. Call this to defer future registrations.
  void DeferRegistrations();

  // Clear the registrations that have been deferred.
  void ClearDeferredRegistrations();

 private:
  // Ensures that all the functions in deferred_ get called, their OpDef's
  // registered, and returns with deferred_ empty.  Returns true the first
  // time it is called. Prints a fatal log if any op registration fails.
  bool MustCallDeferred() const EXCLUSIVE_LOCKS_REQUIRED(mu_);

  // Calls the functions in deferred_ and registers their OpDef's
  // It returns the Status of the first failed op registration or Status::OK()
  // otherwise.
  Status CallDeferred() const EXCLUSIVE_LOCKS_REQUIRED(mu_);

  // Add 'def' to the registry with additional data 'data'. On failure, or if
  // there is already an OpDef with that name registered, returns a non-okay
  // status.
  Status RegisterAlreadyLocked(const OpRegistrationDataFactory& op_data_factory)
      const EXCLUSIVE_LOCKS_REQUIRED(mu_);

  Status LookUpSlow(const string& op_type_name,
                    const OpRegistrationData** op_reg_data) const;

  mutable mutex mu_;
  // Functions in deferred_ may only be called with mu_ held.
  mutable std::vector<OpRegistrationDataFactory> deferred_ GUARDED_BY(mu_);
  // Values are owned.
  mutable std::unordered_map<string, const OpRegistrationData*> registry_
      GUARDED_BY(mu_);
  mutable bool initialized_ GUARDED_BY(mu_);

  // Registry watcher.
  mutable Watcher watcher_ GUARDED_BY(mu_);
};
```

## OpRegistrationData

OpRegistrationData结构体中包含OpDef和OpShapeInferenceFn

OpDef 包含attr，input，ouput，doc等op注册时传入的信息

OpShapeInferenceFn 包含的是shape推断函数


tensorflow\core\framework\op_def_builder.h
```c++
struct OpRegistrationData {
 public:
  OpRegistrationData() {}
  OpRegistrationData(const OpDef& def) : op_def(def) {}
  OpRegistrationData(const OpDef& def, const OpShapeInferenceFn& fn,
                     bool is_function = false)
      : op_def(def), shape_inference_fn(fn), is_function_op(is_function) {}

  OpDef op_def;
  OpShapeInferenceFn shape_inference_fn;
  bool is_function_op = false;
};
```

## OpDef

OpDef 使用proto3协议进行定义

tensorflow\core\framework\op_def.proto

tensorflow/core/framework/op_def.pb.h

## NodeDef

tensorflow/core/framework/node_def.proto

tensorflow/core/framework/node_def.pb.h

## GraphDef

tensorflow\core\framework\graph.proto

tensorflow/core/framework/graph.pb.h

class GraphDefBuilder

tensorflow\core\graph\graph_def_builder.h


# LoadLibrary

tensorflow\core\framework\load_library.cc
```c++

```

# Variable

```python
# tensorflow\python\ops\variables.py
@tf_export("Variable", v1=[])
class Variable(six.with_metaclass(VariableMetaclass,
                                  trackable.Trackable)):
```

# Tensor 
```python
# tensorflow\python\framework\ops.py
@tf_export("Tensor")
class Tensor(_TensorLike):
```

# GFile

GFile 继承自_FileIO, _FileIO 支持了with语法，

```python
# tensorflow\python\platform\gfile.py
@tf_export('io.gfile.GFile', v1=['gfile.GFile', 'gfile.Open', 'io.gfile.GFile'])
class GFile(_FileIO):

# tensorflow\python\lib\io\file_io.py
class FileIO(object):

  def _preread_check(self):
    if not self._read_buf:
      if not self._read_check_passed:
        raise errors.PermissionDeniedError(None, None,
                                           "File isn't open for reading")
      self._read_buf = pywrap_tensorflow.CreateBufferedInputStream(
          compat.as_bytes(self.__name), 1024 * 512)
```
python 层调用pywrap_tensorflow.CreateBufferedInputStream打开文件

```c++
// tensorflow\python\lib\io\file_io.i
tensorflow::io::BufferedInputStream* CreateBufferedInputStream(
    const string& filename, size_t buffer_size, TF_Status* status) {
  std::unique_ptr<tensorflow::RandomAccessFile> file;
  tensorflow::Status s =
      tensorflow::Env::Default()->NewRandomAccessFile(filename, &file);
  if (!s.ok()) {
    Set_TF_Status_from_Status(status, s);
    return nullptr;
  }
  std::unique_ptr<tensorflow::io::RandomAccessInputStream> input_stream(
      new tensorflow::io::RandomAccessInputStream(
          file.release(), true /* owns_file */));
  std::unique_ptr<tensorflow::io::BufferedInputStream> buffered_input_stream(
      new tensorflow::io::BufferedInputStream(
          input_stream.release(), buffer_size, true /* owns_input_stream */));
  return buffered_input_stream.release();
}

// Ensure that the returned object is destroyed when its wrapper is
// garbage collected.
%newobject CreateBufferedInputStream;

tensorflow::io::BufferedInputStream* CreateBufferedInputStream(
    const string& filename, size_t buffer_size, TF_Status* status);
```

根据文件名， 获取到相应的FileSystem进行处理
```c++
// tensorflow\core\platform\env.cc

Status Env::GetFileSystemForFile(const string& fname, FileSystem** result) {
  StringPiece scheme, host, path;
  io::ParseURI(fname, &scheme, &host, &path);
  FileSystem* file_system = file_system_registry_->Lookup(string(scheme));
  if (!file_system) {
    if (scheme.empty()) {
      scheme = "[local]";
    }

    return errors::Unimplemented("File system scheme '", scheme,
                                 "' not implemented (file: '", fname, "')");
  }
  *result = file_system;
  return Status::OK();
}


Status Env::NewRandomAccessFile(const string& fname,
                                std::unique_ptr<RandomAccessFile>* result) {
  FileSystem* fs;
  TF_RETURN_IF_ERROR(GetFileSystemForFile(fname, &fs));
  return fs->NewRandomAccessFile(fname, result);
}
```



## 文件系统实现
```c++
// 继承FileSystem虚基类， 实现接口
class HadoopFileSystem : public FileSystem {
}

// 注册文件系统， 绑定scheme 和 实现类
REGISTER_FILE_SYSTEM("hdfs", HadoopFileSystem);
```

