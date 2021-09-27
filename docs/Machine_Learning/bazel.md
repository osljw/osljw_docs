
# bazel

https://docs.bazel.build/versions/master/build-ref.html

- Workspace (WORKSPACE)
  - Repositories
    - Packages (BUILD)
      - Targets
        - files
        - rules

- BUILD files： 不能声明function
- .bzl files: 声明function, bazel extension


工作空间目录获取
```
$(bazel info workspace)
```

依赖：
```
bazel info output_base
```


可视化依赖
```
bazel query --noimplicit_deps 'deps(//main:hello-world)' \
  --output graph
```

# cmake
- add_executable
- target_link_libraries
- target_include_directories
- target_link_directories

- set 变量
- option 编译选项
