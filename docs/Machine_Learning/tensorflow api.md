
# shape
静态shape
- x.get_shape().as_list() , get_shape返回list[dimension] , as_list转换为list[int]
- x.shape[0], 转换为整形，int(x.shape[0])

动态shape
- tf.shape(x)， 返回值为tensor，获取axis=0的动态大小，tf.shape(x)[0]