
# JSON Web Token (JWT) 
- 客户端向服务端发送用户名和密码请求
- 服务端根据用户id生成token，将token返回给客户端
- 客户端保存token信息，在后续向服务端的请求中都携带token信息

(由于token是带签名的，客户端无法修改token，例如修改token中的用户id，或者权限信息后，在服务端检查该token时都会被发现)
- 服务端验证token是否被篡改，如果是有效token，那么从token中提取用户id信息


JWT字符串，由三段字符串构成，通过'.'进行拼接
- header
- payload
- signature

# cookie token
- cookie：用户点击了链接，cookie未失效，导致发起请求后后端以为是用户正常操作，于是进行扣款操作。
- token：用户点击链接，由于浏览器不会自动带上token，所以即使发了请求，后端的token验证不会通过，所以不会进行扣款操作。

CSRF攻击利用浏览器会自动带上会话信息劫持，token属于安全上流程判断；
