
# 简单工厂模式

```c++
#include <iostream>
#include <memory>

// 抽象产品
class AbstractProduct {
public:
    virtual ~AbstractProduct() {}
    virtual std::string Operation() const = 0;
};

// 具体产品A
class ConcreteProductA : public AbstractProduct {
public:
    std::string Operation() const override {
        return "{Result of the ConcreteProductA}";
    }
};

// 具体产品B
class ConcreteProductB : public AbstractProduct {
public:
    std::string Operation() const override {
        return "{Result of the ConcreteProductB}";
    }
};

// 简单工厂
class SimpleFactory {
public:
    std::unique_ptr<AbstractProduct> CreateProduct(const std::string& productType) const {
        if (productType == "ProductA") {
            return std::make_unique<ConcreteProductA>();
        } else if (productType == "ProductB") {
            return std::make_unique<ConcreteProductB>();
        }
        return nullptr;
    }
};

int main() {
    SimpleFactory factory;

    std::unique_ptr<AbstractProduct> productA = factory.CreateProduct("ProductA");
    if (productA) {
        std::cout << "Product A: " << productA->Operation() << std::endl;
    }

    std::unique_ptr<AbstractProduct> productB = factory.CreateProduct("ProductB");
    if (productB) {
        std::cout << "Product B: " << productB->Operation() << std::endl;
    }

    return 0;
}

```


#  抽象工厂模式

```c++
#include <iostream>
#include <string>

// 抽象产品A
class AbstractProductA {
public:
 virtual ~AbstractProductA(){};
 virtual std::string UsefulFunctionA() const = 0;
};

// 具体产品A1
class ConcreteProductA1 : public AbstractProductA {
public:
 std::string UsefulFunctionA() const override {
    return "The result of the product A1.";
 }
};

// 具体产品A2
class ConcreteProductA2 : public AbstractProductA {
public:
 std::string UsefulFunctionA() const override {
    return "The result of the product A2.";
 }
};

// 抽象产品B
class AbstractProductB {
public:
 virtual ~AbstractProductB(){};
 virtual std::string UsefulFunctionB() const = 0;
 virtual std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const = 0;
};

// 具体产品B1
class ConcreteProductB1 : public AbstractProductB {
public:
 std::string UsefulFunctionB() const override {
    return "The result of the product B1.";
 }
 std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const override {
    const std::string result = collaborator.UsefulFunctionA();
    return "The result of the B1 collaborating with ( " + result + " )";
 }
};

// 具体产品B2
class ConcreteProductB2 : public AbstractProductB {
public:
 std::string UsefulFunctionB() const override {
    return "The result of the product B2.";
 }
 std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const override {
    const std::string result = collaborator.UsefulFunctionA();
    return "The result of the B2 collaborating with ( " + result + " )";
 }
};

// 抽象工厂
class AbstractFactory {
public:
 virtual AbstractProductA *CreateProductA() const = 0;
 virtual AbstractProductB *CreateProductB() const = 0;
};

// 具体工厂1
class ConcreteFactory1 : public AbstractFactory {
public:
 AbstractProductA *CreateProductA() const override {
    return new ConcreteProductA1();
 }
 AbstractProductB *CreateProductB() const override {
    return new ConcreteProductB1();
 }
};

// 具体工厂2
class ConcreteFactory2 : public AbstractFactory {
public:
 AbstractProductA *CreateProductA() const override {
    return new ConcreteProductA2();
 }
 AbstractProductB *CreateProductB() const override {
    return new ConcreteProductB2();
 }
};

void ClientCode(const AbstractFactory &factory) {
 const AbstractProductA *product_a = factory.CreateProductA();
 const AbstractProductB *product_b = factory.CreateProductB();
 std::cout << product_b->UsefulFunctionB() << "\n";
 std::cout << product_b->AnotherUsefulFunctionB(*product_a) << "\n";
 delete product_a;
 delete product_b;
}

int main() {
 std::cout << "Client: Testing client code with the first factory type:\n";
 ConcreteFactory1 *f1 = new ConcreteFactory1();
 ClientCode(*f1);
 delete f1;
 std::cout << std::endl;
 std::cout << "Client: Testing the same client code with the second factory type:\n";
 ConcreteFactory2 *f2 = new ConcreteFactory2();
 ClientCode(*f2);
 delete f2;
 return 0;
}

```



# 原型模式 Prototype

```c++
#include <iostream>
#include <memory>

// 原型类
class Prototype {
public:
    virtual ~Prototype() {}
    virtual std::unique_ptr<Prototype> Clone() const = 0;
};

// 具体原型类
class ConcretePrototype : public Prototype {
public:
    std::unique_ptr<Prototype> Clone() const override {
        return std::make_unique<ConcretePrototype>(*this);
    }

    void Display() const {
        std::cout << "Displaying Prototype" << std::endl;
    }
};

int main() {
    std::unique_ptr<Prototype> prototype = std::make_unique<ConcretePrototype>();
    prototype->Display();

    std::unique_ptr<Prototype> clone = prototype->Clone();
    clone->Display();

    return 0;
}

```

# 单例模式 Singleton

```c++
#include <iostream>

class Singleton {
private:
    Singleton() {
        std::cout << "Singleton instance created" << std::endl;
    }
    // 删除复制构造函数和赋值操作符
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    // 单例实例
    static Singleton instance;

public:
    // 获取单例实例的引用
    static Singleton& getInstance() {
        return instance;
    }

    void someMethod() {
        std::cout << "Singleton method called" << std::endl;
    }
};

// 初始化静态成员
Singleton Singleton::instance;

int main() {
    Singleton& singleton = Singleton::getInstance();
    singleton.someMethod();

    return 0;
}

```


# 生成器模式 Builder


```c++
#include <iostream>
#include <string>

using namespace std;

const int MAXSITE = 4;

class Site {
public:
    Site(string str) : _mName(str) {}
    string _mName;
};

class Wall : public Site {
public:
    Wall() : Site("wall") {}
};

class Wood : public Site {
public:
    Wood() : Site("wood") {}
};

class Grass : public Site {
public:
    Grass() : Site("grass") {}
};

class Door : public Site {
public:
    Door() : Site("door") {}
};

class Window : public Site {
public:
    Window() : Site("window") {}
};

class Room {
public:
    Room() {
        for (int i = 0; i < MAXSITE; i++)
            _mSite[i] = NULL;
    }
    void Printf() {
        for (int i = 0; i < MAXSITE; i++) {
            if (_mSite[i] != NULL)
                cout << _mSite[i]->_mName << endl;
        }
    }
    Site* _mSite[MAXSITE];
};

class RoomBuilder {
public:
    RoomBuilder() : _room(new Room()) {}
    RoomBuilder& setWall() {
        _room->_mSite[0] = new Wall();
        return *this;
    }
    RoomBuilder& setWood() {
        _room->_mSite[1] = new Wood();
        return *this;
    }
    RoomBuilder& setGrass() {
        _room->_mSite[2] = new Grass();
        return *this;
    }
    RoomBuilder& setDoor() {
        _room->_mSite[3] = new Door();
        return *this;
    }
    RoomBuilder& setWindow() {
        _room->_mSite[3] = new Window();
        return *this;
    }
    Room* create() {
        return _room;
    }
private:
    Room* _room;
};

int main() {
    RoomBuilder builder;
    Room* room = builder.setWall().setDoor().setWindow().create();
    room->Printf();
    delete room;
    return 0;
}

```


# 适配器模式 

- 类适配器模式
```c++
#include <iostream>

using namespace std;

/* 连接USB端口 */
class CUsbDisk {
public:
    virtual ~CUsbDisk() {}
    virtual void ConnectDevice() {
        cout << "Connect usb port." << endl;
    }
};

/* 连接Type-C端口 */
class CTypeCInterface {
public:
    virtual ~CTypeCInterface() {}
    void ConnectDevice() {
        cout << "Connect Type-C port." << endl;
    }
};

/* 不仅连接USB端口，还连接Type-C端口 */
class CAdapter : public CUsbDisk, public CTypeCInterface {
public:
    void ConnectDevice() {
        CTypeCInterface::ConnectDevice();
    }
};

int main(int argc, char *argv[]) {
    CUsbDisk *theDisk = new CAdapter();
    theDisk->ConnectDevice();
    delete theDisk;
    return 0;
}

```
- 对象适配器模式

```c++
#include <iostream>

using namespace std;

/* 连接USB端口 */
class CUsbDisk {
public:
    virtual ~CUsbDisk() {}
    virtual void ConnectDevice() {
        cout << "Connect usb port." << endl;
    }
};

/* 连接Type-C端口 */
class CTypeCInterface {
public:
    virtual ~CTypeCInterface() {}
    void ConnectDevice() {
        cout << "Connect Type-C port." << endl;
    }
};

/* USB设备连接手机 */
class CAdapter : public CUsbDisk {
public:
    CAdapter() {
        mpAdaptee = new CTypeCInterface();
    }
    ~CAdapter() {
        if (NULL != mpAdaptee) {
            delete mpAdaptee;
        }
    }
    void ConnectDevice() {
        if (NULL != mpAdaptee) {
            mpAdaptee->ConnectDevice();
        } else {
            cout << "Adapter abnormal. Connect fail!" << endl;
        }
    }
private:
    CTypeCInterface *mpAdaptee;
};

int main(int argc, char *argv[]) {
    CUsbDisk *theDisk = new CAdapter();
    theDisk->ConnectDevice();
    delete theDisk;
    return 0;
}

```


这种设计允许你使用 CUsbDisk 类型的接口来调用 CTypeCInterface 的方法，从而实现了接口的适配和兼容