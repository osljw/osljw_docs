# django

```
django-admin startproject <project name>
django-admin startapp <app name>
```



## django CORS 

用户可以访问网站A和网站B， 网站B的页面上有javascript向网站A发起http请求， 如果网站A没有开启CORS（返回给浏览器的header未设置字段Access-Control-Allow-Origin）， 浏览器会拒绝将网站A的响应内容返回给网站B的请求，从而保护用户在网站A的响应不被网站B窃取

django开启CORS

```
pip install django-cors-headers
```

settings.py 
```
INSTALLED_APPS = [
   ...
   'corsheaders',
   ...
]

MIDDLEWARE = [
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  #'django.middleware.csrf.CsrfViewMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
```

'django.middleware.common.CommonMiddleware'之前添加'corsheaders.middleware.CorsMiddleware',
注释掉'django.middleware.csrf.CsrfViewMiddleware'





## django models

ORM

创建models
```python
from django.db import models
from django.db.models import BooleanField, CharField, IntegerField

class Banner(models.Model):
    img_url = CharField(max_length=255, verbose_name="img url")
    link_url = CharField(max_length=500, verbose_name="link url")
    is_show = BooleanField(default=True, verbose_name="should img show")
    orders = IntegerField(default=1, verbose_name="img show order")
    title = CharField(max_length=500, verbose_name="ad title")

    class Meta:
        db_table = "banner"
        verbose_name = "banner img"

    def __str__(self) -> str:
        return self.title
```

```py
models.CharField(max_length=8, default='', unique=True)
models.DateTimeField(auto_now_add=True, verbose_name='create_time')
```
- CharField
    - max_length 最大字符长度
    - default 默认值
    - unique
- DateTimeField
    - auto_now_add=True 

更新models对应的数据库
```
python manage.py makemigrations
python manage.py migrate
```

## django views

- GenericAPIView
    - GenericViewSet
        - ModelViewSet
        - ReadOnlyModelViewSet
    
- ListAPIView 当需要返回list数据时，可以继承ListAPIView， 覆盖`query_set`和`serializer_class`
```python
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerSerializer

class BannerView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True).order_by("orders")
    serializer_class = BannerSerializer
```

### ModelViewSet

A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions

views.py
```py
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Article
from .serializers import ArticleSerializer

class ArticleModelViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.filter(is_show=True)
    serializer_class = ArticleSerializer
```

urls.py
```py
from rest_framework.routers import DefaultRouter
from .views import ArticleModelViewSet

urlpatterns = [
]

router = DefaultRouter()
router.register('article', ArticleModelViewSet)
urlpatterns += router.urls
```


## django admin/xadmin

安装xadmin
```
pip install https://github.com/vip68/xadmin_bugfix/tarball/master


# xadmin\plugins\importexport.py 文件修复

#from import_export.admin import DEFAULT_FORMATS, SKIP_ADMIN_LOG, TMP_STORAGE_CLASS
from import_export.formats.base_formats import DEFAULT_FORMATS
from import_export.admin import ImportExportMixinBase, ImportMixin
```

```
python manage.py createsuperuser
```


# ASGI vs WSGI websocket
- CGI:（通用网关接口， Common Gateway Interface）
- WSGI: (Web服务器网关接口, Web Server Gateway Interface)
- ASGI: (异步网关协议接口) 支持HTTP, HTTP2, Websocket等协议

django框架为了同时支持HTTP协议和Websocket协议，引入了ASGI， ASGI分为三层， 第一层根据请求的url（http:// or ws://)解析协议，第二层为Channel，通过队列缓存消息， 第三层为Consumer消费消息

![](media/asgi.png)

settings.py
```py
# 指定ASGI的路由地址
ASGI_APPLICATION = 'django_backend.asgi.application'

# CHANNEL后端，使用内存存储，默认是redis
CHANNEL_LAYERS = {    
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

channel_layer: 可以实现广播/点对点功能


views.py
```py
import json
from channels.generic.websocket import WebsocketConsumer

# Create your views here.
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("websocket receive:", text_data)

        d = {'test': 123}
        self.send(json.dumps(d))
```

urls.py
```py
from user_chat.views import ChatConsumer
websocket_urlpatterns = [
    path('ws/chat', ChatConsumer.as_asgi()),
]
```


# Django REST framework

## 登录（jwt）

settings.py
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

1. `DEFAULT_PERMISSION_CLASSES`配置`rest_framework.permissions.IsAuthenticated`， 表示访问所有接口时需要先通过AUTHENTICATION身份认证，即需要携带有效的认证信息token， 否则接口会直接返回`HTTP 401 Unauthorized`错误。
2. 对于登录接口例如`obtain_jwt_token`, 其permission_classes设置为了空元组(), 因此不需要验证token。
3. 如果想让其他接口避免AUTHENTICATION token检测， 同理可以在views类视图中设置`permission_classes=()`

登录接口url
```
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/login', obtain_jwt_token),
]
```

使用登录接口

1. 前端向后端发送Post /api/login请求，携带username和password， 后端返回jwt token给前端
2. 前端保存jwt token， 并在访问其他接口时在header中携带jwt token信息， 如果未携带token信息，会出现`HTTP 401 Unauthorized`错误

## 注册

serializers.py
```python
from rest_framework.serializers import ModelSerializer

from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
```

views.py
```python

from rest_framework.generics import CreateAPIView
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import User
from .serializers import UserSerializer

class Register(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []

    def post(self,request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            resp = {
                'status_code': -1,
                'msg': '用户名【{}】已注册'.format(username)
            }
        else:
            user = User.objects.create_user(username=username,password=password)
            # token, created = Token.objects.get_or_create(user=user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            resp = {
                'status_code': 0,
                'user_id': user.pk,
                'user_name': user.username,
                'token': token,
            }

        return Response(resp)
```
`serializer_class`: 网页上访问接口时，可以出现表单界面，方便post字段的输入， `permission_classes = []`: 注册接口不需要登录验证


urls.py
```python
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import Register

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', Register.as_view()),
]
```

## 返回格式

```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        # 'utils.renderers.CustomRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
}
```


# django 博客文章

- django-taggit 文章标签