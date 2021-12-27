# django

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


