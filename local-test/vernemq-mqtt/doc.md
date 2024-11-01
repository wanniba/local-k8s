# vernemq

## helm install

``` sh
helm install mqtt . -f values.yaml
helm install mqtt .
helm uninstall mqtt 
helm upgrade mqtt . -f values.yaml

# 
helm install mqtt vernemq/vernemq
```

## log

``` sh
kubectl get pod
kubectl logs mqtt-vernemq-0
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
```

## passwd

``` sh
kubectl exec -it mqtt-vernemq-0 -- /bin/sh
mkdir -p /etc/vernemq
touch /etc/vernemq/passwd
vmq-passwd /etc/vernemq/passwd admin
mosquitto_pub -h 127.0.0.1 -p 1883 -t test/topic -m "Hello MQTT"
```

