
# virtual function vbtl

使用虚表调用类成员函数

```c++
#include <iostream>

class Object{

public:
    virtual void print_test() {
        std::cout << "test" << std::endl;
    }
    virtual void print_hello(int input) {
        std::cout << "hello: " << age << ", input: " << input << std::endl;
    }

private:
    int age = 66;
};

typedef void (*test_ptr)(Object*);
typedef void (*hello_ptr)(Object*, int);

int main()
{
    Object obj;

    std::uintptr_t **vbtl_ptr = reinterpret_cast<std::uintptr_t**>(&obj);
    ((test_ptr)vbtl_ptr[0][0])(nullptr);
    ((hello_ptr)vbtl_ptr[0][1])(&obj, 77);

    return 0;
}
```

output
```
test
hello: 66, input: 77
```