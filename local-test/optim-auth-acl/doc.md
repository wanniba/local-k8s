# vernemq

## k8s 切换环境

``` sh
kubectl config get-contexts
kubectl config use-context docker-desktop
```

## helm install

``` sh
helm install mqtt . -f values.yaml
helm uninstall mqtt 
helm upgrade mqtt . -f values.yaml
helm install mqtt vernemq/vernemq
```

## log

``` sh
kubectl get pod
kubectl logs mq-statefulset-0
kubectl describe pod mq-statefulset-0

kubectl exec -it mq-statefulset-0 -c nginx -- cat /var/log/nginx/error.log 

kubectl logs mq-statefulset-0  -c nginx
kubectl logs mq-statefulset-0 -c vernemq
```

## config

``` sh
# 查看配置
kubectl exec -it mqtt-vernemq-0 -- cat /vernemq/etc/vernemq.conf | grep allow_anonymous
# 手动改配置
vi /vernemq/etc/vernemq.conf
# 将 allow_anonymous = off 改为 allow_anonymous = on。
kubectl exec -it mqtt-vernemq-0 -- /bin/sh
echo "allow_anonymous = on" >> /etc/vernemq/vernemq.conf
echo "plugins.vmq_passwd = off" >> /etc/vernemq/vernemq.conf
kubectl exec -it mqtt-vernemq-0 -- sed -i '/^allow_anonymous = off/d' /vernemq/etc/vernemq.conf
# 重载配置
vmq-admin reload
# 重启
kubectl rollout restart statefulset mqtt-vernemq
# 检查已启用的插件：
kubectl exec -it mqtt-vernemq-0 -- vmq-admin plugin show
```

## verify

``` sh
kubectl port-forward svc/mqtt-vernemq 1883:1883
mosquitto_sub -h 127.0.0.1 -p 1883 -t "test/topic"
mosquitto_pub -h 127.0.0.1 -p 1883 -t test/topic -m "Hello MQTT"

kubectl get nodes -o wide

kubectl port-forward service/my-release-vernemq 30083:1883
# 

# ca 只支持 解析 *.optimportal.com
sudo vim /etc/hosts
127.0.0.1 gamma.optimportal.com

```

## passwd

``` sh
kubectl exec -it mqtt-vernemq-0 -- /bin/sh
mkdir -p /etc/vernemq
touch /etc/vernemq/passwd
vmq-passwd /etc/vernemq/passwd admin
mosquitto_pub -h 127.0.0.1 -p 1883 -t test/topic -m "Hello MQTT"
```

## 查看 渲染后的 yaml

``` sh
helm template my-release ./templates/statefulset.yaml --values values.yaml > xxx.yaml
```

## secret 

``` sh
kubectl create secret tls server-tls --cert=./ca/sclient.crt --key=./ca/sclient.key
kubectl create secret tls server-tls --cert=./ca/cserver.crt --key=./ca/cserver.key
kubectl delete secret server-tls
kubectl create secret generic client-ca --from-file=ca-client=./ca/ca-client.crt
kubectl delete secret client-ca

kubectl describe  StatefulSet my-release-vernemq  
kubectl describe  pod my-release-vernemq-0  

kubectl get configmap nginx-config -o yaml


```

## auth

``` sh

helm install mqtt .
helm uninstall mqtt 
cat /etc/vernemq/vmq.passwd 
vim /etc/vernemq/vmq.passwd 

kubectl get pod
kubectl describe pod mqtt-tsl-statefulset-0 
kubectl logs mqtt-tsl-statefulset-0 
kubectl exec -it mqtt-tsl-statefulset-0 -- /bin/bash
vmq-passwd -c /etc/vernemq/vmq.passwd henry
vmq-passwd  /etc/vernemq/vmq.passwd sss
vmq-passwd -c /etc/vernemq/vmq.passwd henry


 vmq-passwd  -U vmq

 kubectl port-forward svc/my-service 8080:80

kubectl create secret generic vernemq-passwd-secret --from-file=vmq.passwd=./passwd.conf
kubectl create secret generic vernemq-acl --from-file=vmq.acl=./user.acl
kubectl delete secret vernemq-passwd-secret
kubectl exec -it mqtt-tsl-statefulset-0 -- /bin/bash
cat /vernemq/data/generated.configs/app.2024.11.28.05.16.39.config 
```
