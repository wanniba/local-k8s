要将本地的 PEM 文件（如 `server.crt` 和 `server.key`）挂载到 Pod 的 `/etc/nginx/certs/` 路径下，可以通过 **Kubernetes Secret** 将证书文件导入 Kubernetes，然后将 Secret 以 Volume 的形式挂载到 Pod。以下是具体步骤：

### 1. 创建 Kubernetes Secret

假设本地证书文件分别为 `server.crt`（证书文件）和 `server.key`（私钥文件），可以使用 `kubectl create secret` 命令创建 Secret：

```bash
kubectl create secret generic nginx-certificates \
  --from-file=server.crt=path/to/server.crt \
  --from-file=server.key=path/to/server.key
```

这样，`nginx-certificates` Secret 中会包含两个文件：`server.crt` 和 `server.key`。

### 2. 更新 Deployment YAML 配置

在 Deployment 中添加 Secret Volume，将其挂载到 `/etc/nginx/certs/` 路径下：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-mqtt
  labels:
    app: nginx-mqtt
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-mqtt
  template:
    metadata:
      labels:
        app: nginx-mqtt
    spec:
      containers:
      - name: nginx
        image: openresty/openresty:alpine
        ports:
        - containerPort: 8883
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: lua-scripts
          mountPath: /etc/nginx/lua/validate_san_hazelcast.lua
          subPath: validate_san_hazelcast.lua
        - name: nginx-certificates
          mountPath: /etc/nginx/certs/            # 挂载到 /etc/nginx/certs/
          readOnly: true                          # 设置为只读，确保安全
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
      - name: lua-scripts
        configMap:
          name: lua-scripts
      - name: nginx-certificates
        secret:
          secretName: nginx-certificates          # 引用创建的 Secret
```

### 3. 应用更新的 Deployment 配置

将更新后的 Deployment 配置应用到集群中：

```bash
kubectl apply -f nginx-deployment.yaml
```

### 验证

完成后，您可以通过进入 Pod 查看 `/etc/nginx/certs/` 路径下的证书文件：

```bash
kubectl exec -it <pod-name> -- ls /etc/nginx/certs/
```

这样，Nginx 就可以使用这些证书文件来支持 SSL。