
# service
proto文件定义service


`::google::protobuf::RpcController* cntl_base` -> `brpc::Controller* cntl = static_cast<brpc::Controller*>(cntl_base);`
`::google::protobuf::Closure* done` -> `brpc::ClosureGuard done_guard(done);`

done->Run()被调用时会将response返回给客户端， done->Run()何时被调用决定了是同步还是异步


## 同步service

通过RAII方式，在服务函数返回时自动调用done->Run()
```c++
brpc::ClosureGuard done_guard(done)；
```
## 异步service
在服务函数中手动调用done_guard.release()确保函数返回时不会自动调用done->Run()
```
brpc::ClosureGuard done_guard(done)；
// 把done注册到被等待事件的回调中
done_guard.release()
```

# Server
- AddService 
- Start/Stop/Join
- RunUntilAskedToQuit


```c++
    // Add a service. Arguments are explained in ServiceOptions above.
    // NOTE: Adding a service while server is running is forbidden.
    // Returns 0 on success, -1 otherwise.
    int AddService(google::protobuf::Service* service,
                   ServiceOwnership ownership);
    int AddService(google::protobuf::Service* service,
                   ServiceOwnership ownership,
                   const butil::StringPiece& restful_mappings);
    int AddService(google::protobuf::Service* service,
                   const ServiceOptions& options);

```

Server启动流程

- Server::Start
    - Server::StartInternal
        - tcp_listen
        - Server::BuildAcceptor // 各种协议的process_request
        - Acceptor::StartAccept
            - Socket::Create // 注册回调OnNewConnections
                - Socket::ResetFileDescriptor
                    - GetGlobalEventDispatcher
                        - InitializeGlobalDispatchers
                            - EventDispatcher::Start
                                - EventDispatcher::RunThis // bthread中启动， 该bthread线程负责循环调用epoll_wait
                    - EventDispatcher::AddConsumer
                        - epoll_ctl // 系统调用

GetGlobalEventDispatcher第一次被调用时会初始化全局变量g_edisp, 启动FLAGS_event_dispatcher_num指定数量的EventDispatcher，
调用每个EventDispatcher的Start启动bthread线程

```c++
void InitializeGlobalDispatchers() {
    g_edisp = new EventDispatcher[FLAGS_event_dispatcher_num];
    for (int i = 0; i < FLAGS_event_dispatcher_num; ++i) {
        const bthread_attr_t attr = FLAGS_usercode_in_pthread ?
            BTHREAD_ATTR_PTHREAD : BTHREAD_ATTR_NORMAL;
        CHECK_EQ(0, g_edisp[i].Start(&attr));
    }
    // This atexit is will be run before g_task_control.stop() because above
    // Start() initializes g_task_control by creating bthread (to run epoll/kqueue).
    CHECK_EQ(0, atexit(StopAndJoinGlobalDispatchers));
}

EventDispatcher& GetGlobalEventDispatcher(int fd) {
    pthread_once(&g_edisp_once, InitializeGlobalDispatchers);
    if (FLAGS_event_dispatcher_num == 1) {
        return g_edisp[0];
    }
    int index = butil::fmix32(fd) % FLAGS_event_dispatcher_num;
    return g_edisp[index];
}
```


请求处理过程

- EventDispatcher::RunThis // bthread 线程
    - EventDispatcher::Run
        - Socket::StartInputEvent
            - Socket::ProcessEvent // 一个fd只会启动一个bthread线程， bthread_start_urgent启动


StartInputEvent仅仅是负责判断发生事件的fd上有没有bthread在处理了，没有就原地启动一个，有就直接返回，注意调用的是bthread_start_urgent，这个函数启动bthread会让出当前bthread，也就是官方文档所说的，“EDISP把所在的pthread让给了新建的bthread，使其有更好的cache locality，可以尽快地读取fd上的数据”


# bthread


# brpc::DataFactory
- session-local (ServerOptions.reserved_session_local_data)
- server-thread-local (ServerOptions.thread_local_data_factory)



# 日志
通过`--log_directory`参数指定日志存储目录

```c++
//brpc/include/butil/logging.h
DECLARE_string(log_directory);
```

# redis

```
mutable RedisClient redis_client;

redis_client.Init(, , );

string key;
brpc::RedisResponse rsp;
redis_client.AccessRedis(key, &rep);

```



