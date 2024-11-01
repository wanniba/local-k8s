#

## deploy

``` sh

helm upgrade oc-nginx . -f ./values.yaml 
helm install oc-nginx . -f ./values.yaml 
helm uninstall oc-nginx 
```

## verify

``` sh
curl 10.0.1.68:32283


kubectl get pods | grep nginx-mqtt-
kubectl get pods | grep nginx-mqtt-

kubectl logs nginx-mqtt-5f7c8f5c77-fn8vm
```

## trouble shooting

``` sh
kubectl get pods | grep nginx-mqtt-
kubectl logs nginx-mqtt-6fbf947b8c-f7gx5  
kubectl describe pod nginx-mqtt-5f7c8f5c77-dml8j

kubectl exec -it nginx-mqtt-6fbf947b8c-spq5t -- /bin/sh

# 校验nginx 配置
kubectl exec -it nginx-mqtt-5554b4fb9f-c94g7 -- nginx -t
ps aux
# PID   USER     TIME  COMMAND
#     1 root      0:00 {openresty} nginx: master process /usr/local/openresty/bin/openresty -g daemon off;
#     7 nobody    0:00 {openresty} nginx: worker process
#    14 root      0:00 /bin/sh
#    20 root      0:00 ps aux
cat /usr/local/openresty/nginx/logs/error.log

```

```bash
kubectl delete secret nginx-certificates  
kubectl create secret generic nginx-certificates \
  --from-file=server.crt=22e24260576a8e48.crt \
  --from-file=server.key=_.optimportal.com.key \
  --from-file=ca.crt=ca.crt



openssl s_client -connect 10.0.1.68:8883 -CAfile ca.crt -cert client.crt -key client.key

mosquitto_pub -h localhost -p 8883 -t "test/topic" -m "Hello World" \
    --cert client.crt \
    --key client.key \
    --cafile ca.crt
    --insecure

mqtt pub -h localhost -p 8883 -t "test/topic" -m "Hello World" \
    --cafile ca.crt \
    --cert client.crt \
    --key client.key
```

## copy file to ec2

``` bash
scp -i infra/pem/optim5_ec2.pem apps/oc-nginx/ca/ca.crt ubuntu@10.1.2.63:

echo "" > ca.crt
echo "" > client.crt
echo "" > client.key
```

## vernemq

``` bash
helm repo add vernemq https://vernemq.github.io/docker-vernemq
helm repo update
helm install mqtt vernemq/vernemq -f values.yaml
helm install mqtt vernemq/vernemq --set accept_eula=yes
helm uninstall mqtt 
kubectl logs mqtt-vernemq-0
1. Check your VerneMQ cluster status:
  kubectl exec --namespace default vernemq-0 /vernemq/bin/vmq-admin cluster show

1. Get VerneMQ MQTT port
  Subscribe/publish MQTT messages there: 127.0.0.1:1883
  kubectl port-forward svc/mqtt-vernemq 1883:1883

kubectl port-forward svc/mqtt-vernemq 1883:1883
mosquitto_sub -h 127.0.0.1 -p 1883 -t "test/topic"
mosquitto_pub -h 127.0.0.1 -p 1883 -t test/topic -m "Hello MQTT"


helm pull vernemq/vernemq --untar
```
