为了测试 SSL 的双向验证（即客户端和服务器双方都验证对方的证书），可以通过以下步骤来生成并配置 CA、服务器证书和客户端证书。双向验证要求服务器和客户端各自持有证书，并且验证对方证书是否是由信任的 CA 签署的。

### 1. 创建 CA 证书和密钥

首先，我们创建一个 CA，用于签署客户端和服务器的证书。

```bash
# 生成 CA 私钥
openssl genrsa -out ca.key 2048

# 创建 CA 自签名证书
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt
```

### 2. 生成服务器证书和私钥

接下来，我们生成服务器端的私钥和证书签名请求（CSR），并用 CA 签署证书。

```bash
# 生成服务器私钥
openssl genrsa -out server.key 2048

# 生成服务器证书签名请求（CSR）
openssl req -new -key server.key -out server.csr

# 用 CA 签署服务器证书
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
```

这样我们就获得了服务器的私钥 (`server.key`) 和签署的证书 (`server.crt`)。

### 3. 生成客户端证书和私钥

类似地，我们为客户端生成私钥和证书，并用同一个 CA 来签署，以确保双方都信任同一 CA。

```bash
# 生成客户端私钥
openssl genrsa -out client.key 2048

# 生成客户端证书签名请求（CSR）
openssl req -new -key client.key -out client.csr

# 用 CA 签署客户端证书
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256
```

现在，客户端的私钥为 `client.key`，证书为 `client.crt`。

### 4. 配置 OpenResty (NGINX) 进行双向验证

将生成的 CA 证书和服务器证书配置到 OpenResty 或 NGINX 上，以支持双向验证：

```nginx
server {
    listen 8883 ssl;

    # SSL 证书配置
    ssl_certificate /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;

    # CA 证书和双向验证设置
    ssl_client_certificate /etc/nginx/certs/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    # 其他配置
    location / {
        # 仅作为示例的响应
        content_by_lua_block {
            ngx.say("SSL双向验证成功!")
        }
    }
}
```

### 5. 测试双向验证

1. **将 CA 证书导入客户端**：需要将 `ca.crt` 导入到客户端的信任链中，确保它信任由 CA 签署的服务器证书。

2. **使用客户端证书进行测试**：

   现在使用 OpenSSL 命令行客户端来测试与服务器的双向验证。客户端会使用 `client.crt` 和 `client.key` 来证明自己的身份：

   ```bash
   openssl s_client -connect <server_ip>:8883 -CAfile ca.crt -cert client.crt -key client.key
   ```

   - `<server_ip>` 是服务器的 IP 地址或域名。
   - `-CAfile ca.crt` 指定客户端信任的 CA 证书。
   - `-cert client.crt` 和 `-key client.key` 是客户端的证书和私钥。

3. **验证连接是否成功**：如果配置正确，OpenResty 会验证客户端证书，并在验证通过后返回响应。这意味着双向 SSL 验证已经成功。

### 6. 检查输出

如果测试成功，客户端会输出服务器的响应信息，比如配置的 “SSL双向验证成功!”。如果有任何一方验证失败，连接将被拒绝，并显示验证错误。