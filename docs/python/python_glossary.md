
https://docs.python.org/3/glossary.html

# iterable
- iterable object: with an __iter__() method or with a __getitem__() method
- iter(iterable object) return iterator
- iterator对象需要__next__()方法， iterable object的__iter__()方法一般返回self，因此iterable object一般也需要实现__next__()方法

# iterator
- 需要实现__next__()方法，当没有元素返回时，StopIteration异常
- 需要实现__iter__()方法，返回self， 将自己变为iterable object

# sequence

# generator