
# pybind11





示例输入

```
int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(gemfield, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("add", &add, "A function which adds two numbers");
}
```

宏展开
```
int add(int i, int j) {
    return i + j;
}
static ::pybind11::module_::module_def pybind11_module_def_gemfield __attribute__ ((__unused__)); __attribute__ ((__unused__)) static void pybind11_init_gemfield(::pybind11::module_ &); extern "C" __attribute__ ((__unused__)) __attribute__ ((visibility("default"))) PyObject *PyInit_gemfield(); extern "C" __attribute__ ((visibility("default"))) PyObject *PyInit_gemfield() { { const char *compiled_ver = "3" "." "7"; const char *runtime_ver = Py_GetVersion(); size_t len = std::strlen(compiled_ver); if (std::strncmp(runtime_ver, compiled_ver, len) != 0 || (runtime_ver[len] >= '0' && runtime_ver[len] <= '9')) { PyErr_Format(PyExc_ImportError, "Python version mismatch: module was compiled for Python %s, " "but the interpreter version is incompatible: %s.", compiled_ver, runtime_ver); return nullptr; } } pybind11::detail::get_internals(); auto m = ::pybind11::module_::create_extension_module( "gemfield", nullptr, &pybind11_module_def_gemfield); try { pybind11_init_gemfield(m); return m.ptr(); } catch (pybind11::error_already_set &e) { pybind11::raise_from(e, PyExc_ImportError, "initialization failed"); return nullptr; } catch (const std::exception &e) { PyErr_SetString(PyExc_ImportError, e.what()); return nullptr; } } void pybind11_init_gemfield(::pybind11::module_ & (m)) {
    m.doc() = "pybind11 example plugin";
    m.def("add", &add, "A function which adds two numbers");
}

```



PYBIND11_MODULE(name, variable) 宏定义

```
#define PYBIND11_MODULE(name, variable)                                                           \
    static ::pybind11::module_::module_def PYBIND11_CONCAT(pybind11_module_def_, name)            \
        PYBIND11_MAYBE_UNUSED;                                                                    \
    PYBIND11_MAYBE_UNUSED                                                                         \
    static void PYBIND11_CONCAT(pybind11_init_, name)(::pybind11::module_ &);                     \
    PYBIND11_PLUGIN_IMPL(name) {                                                                  \
        PYBIND11_CHECK_PYTHON_VERSION                                                             \
        PYBIND11_ENSURE_INTERNALS_READY                                                           \
        auto m = ::pybind11::module_::create_extension_module(                                    \
            PYBIND11_TOSTRING(name), nullptr, &PYBIND11_CONCAT(pybind11_module_def_, name));      \
        try {                                                                                     \
            PYBIND11_CONCAT(pybind11_init_, name)(m);                                             \
            return m.ptr();                                                                       \
        }                                                                                         \
        PYBIND11_CATCH_INIT_EXCEPTIONS                                                            \
    }                                                                                             \
    void PYBIND11_CONCAT(pybind11_init_, name)(::pybind11::module_ & (variable))
```


PYBIND11_CHECK_PYTHON_VERSION宏，  python版本检查
```
PYBIND11_CHECK_PYTHON_VERSION

#define PYBIND11_CHECK_PYTHON_VERSION \
    {                                                                          \
        const char *compiled_ver = PYBIND11_TOSTRING(PY_MAJOR_VERSION)         \
            "." PYBIND11_TOSTRING(PY_MINOR_VERSION);                           \
        const char *runtime_ver = Py_GetVersion();                             \
        size_t len = std::strlen(compiled_ver);                                \
        if (std::strncmp(runtime_ver, compiled_ver, len) != 0                  \
                || (runtime_ver[len] >= '0' && runtime_ver[len] <= '9')) {     \
            PyErr_Format(PyExc_ImportError,                                    \
                "Python version mismatch: module was compiled for Python %s, " \
                "but the interpreter version is incompatible: %s.",            \
                compiled_ver, runtime_ver);                                    \
            return nullptr;                                                    \
        }                                                                      \
    }
```


PYBIND11_ENSURE_INTERNALS_READY
```
#define PYBIND11_ENSURE_INTERNALS_READY \
    pybind11::detail::get_internals();
```


声明模块定义函数(pybind11_module_def_<module_name>), 该函数会在模块初始化函数(pybind11_init_<module_name>)中调用
```
    static ::pybind11::module_::module_def PYBIND11_CONCAT(pybind11_module_def_, name)            \
        PYBIND11_MAYBE_UNUSED;                                                                    \

    static ::pybind11::module_::module_def pybind11_module_def_gemfield __attribute__ ((__unused__)); 
```

声明模块初始化函数
```
static void PYBIND11_CONCAT(pybind11_init_, name)(::pybind11::module_ &);                     \

__attribute__ ((__unused__)) static void pybind11_init_gemfield(::pybind11::module_ &);
```

声明和定义模块的cpython接口函数
```
PYBIND11_PLUGIN_IMPL(name) {                                                                  \
        auto m = ::pybind11::module_::create_extension_module(                                    \
            PYBIND11_TOSTRING(name), nullptr, &PYBIND11_CONCAT(pybind11_module_def_, name));      \
        try {                                                                                     \
            PYBIND11_CONCAT(pybind11_init_, name)(m);                                             \
            return m.ptr();                                                                       \
        }                                                                                         \
        PYBIND11_CATCH_INIT_EXCEPTIONS                                                            \
    } 
void PYBIND11_CONCAT(pybind11_init_, name)(::pybind11::module_ & (variable))


extern "C" __attribute__ ((__unused__)) __attribute__ ((visibility("default"))) PyObject *PyInit_gemfield(); 
extern "C" __attribute__ ((visibility("default"))) PyObject *PyInit_gemfield() { 
    auto m = ::pybind11::module_::create_extension_module( "gemfield", nullptr, &pybind11_module_def_gemfield); 
    try { 
        pybind11_init_gemfield(m); 
        return m.ptr(); 
    } catch (pybind11::error_already_set &e) { 
        pybind11::raise_from(e, PyExc_ImportError, "initialization failed"); 
        return nullptr; 
    } catch (const std::exception &e) { 
        PyErr_SetString(PyExc_ImportError, e.what()); return nullptr; 
    } 
} 
void pybind11_init_gemfield(::pybind11::module_ & (m))
```
PYBIND11_MODULE(name, variable) 声明和定义了`PyObject *PyInit_<module_name>()`函数, 创建pybind11::module_类型的对象， 由用户自己定义`pybind11_init_<module_name>`的函数body


- class cpp_function : public function， class function : public object
- class module_ : public object


pybind11::module_::create_extension_module 静态成员函数构造pybind::module_对象
```c++
    /** \rst
        Create a new top-level module that can be used as the main module of a C extension.

        For Python 3, ``def`` should point to a statically allocated module_def.
        For Python 2, ``def`` can be a nullptr and is completely ignored.
    \endrst */
    static module_ create_extension_module(const char *name, const char *doc, module_def *def) {
#if PY_MAJOR_VERSION >= 3
        // module_def is PyModuleDef
        def = new (def) PyModuleDef {  // Placement new (not an allocation).
            /* m_base */     PyModuleDef_HEAD_INIT,
            /* m_name */     name,
            /* m_doc */      options::show_user_defined_docstrings() ? doc : nullptr,
            /* m_size */     -1,
            /* m_methods */  nullptr,
            /* m_slots */    nullptr,
            /* m_traverse */ nullptr,
            /* m_clear */    nullptr,
            /* m_free */     nullptr
        };
        auto m = PyModule_Create(def);
#else
        // Ignore module_def *def; only necessary for Python 3
        (void) def;
        auto m = Py_InitModule3(name, nullptr, options::show_user_defined_docstrings() ? doc : nullptr);
#endif
        if (m == nullptr) {
            if (PyErr_Occurred())
                throw error_already_set();
            pybind11_fail("Internal error in module_::create_extension_module()");
        }
        // TODO: Should be reinterpret_steal for Python 3, but Python also steals it again when returned from PyInit_...
        //       For Python 2, reinterpret_borrow is correct.
        return reinterpret_borrow<module_>(m);
    }
```

def方法将用户自定义函数封装为cpp_function对象
```c++
    /** \rst
        Create Python binding for a new function within the module scope. ``Func``
        can be a plain C++ function, a function pointer, or a lambda function. For
        details on the ``Extra&& ... extra`` argument, see section :ref:`extras`.
    \endrst */
    template <typename Func, typename... Extra>
    module_ &def(const char *name_, Func &&f, const Extra& ... extra) {
        cpp_function func(std::forward<Func>(f), name(name_), scope(*this),
                          sibling(getattr(*this, name_, none())), extra...);
        // NB: allow overwriting here because cpp_function sets up a chain with the intention of
        // overwriting (and has already checked internally that it isn't overwriting non-functions).
        add_object(name_, func, true /* overwrite */);
        return *this;
    }
```