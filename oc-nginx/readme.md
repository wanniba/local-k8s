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
kubectl describe pod nginx-mqtt-5554b4fb9f-2srxf 
```

## trouble shooting

``` sh
kubectl get pods | grep nginx-mqtt-
kubectl logs nginx-mqtt-6fbf947b8c-f7gx5  
kubectl describe pod nginx-mqtt-86d455f778-f29gm

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
kubectl create secret generic nginx-certificates --from-file=server.crt=22e24260576a8e48.crt --from-file=server.key=_.optimportal.com.key --from-file=ca.crt=ca.crt



openssl s_client -connect 10.0.1.68:8883 -CAfile ca.crt -cert client.crt -key client.key

mosquitto_pub -h 10.0.1.68 -p 8883 -t "test/topic" -m "Hello World" \
    --cert /home/ubuntu/ca/client.crt \
    --key /home/ubuntu/ca/client.key \
    --cafile /home/ubuntu/ca/ca.crt
    --insecure

mqtt pub -h 10.0.1.68 -p 8883 -t "test/topic" -m "Hello World" \
    --cafile /home/ubuntu/ca/ca.crt \
    --cert /home/ubuntu/ca/client.crt \
    --key /home/ubuntu/ca/client.key
```

## copy file to ec2

```bash
scp -i infra/pem/optim5_ec2.pem apps/oc-nginx/ca/ca.crt ubuntu@10.1.2.63:/home/ubuntu/ca/

echo "" > ca.crt
echo "" > client.crt
echo "" > client.key
```
