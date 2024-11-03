# docker

``` sh
docker run --name vernemq1 -d vernemq/vernemq 

docker cp my-vernemq:/vernemq/etc/vernemq.conf ./config/
docker cp my-vernemq:/vernemq/etc/vm.args ./config/

docker exec -it vernemq1 -- /bin/sh

  - name: DOCKER_VERNEMQ_ACCEPT_EULA
    value: "yes"
  - name: DOCKER_VERNEMQ_ALLOW_ANONYMOUS
    value: "on"

docker run -d --name vernemq4 -e DOCKER_VERNEMQ_ACCEPT_EULA=yes -e DOCKER_VERNEMQ_ALLOW_ANONYMOUS=on -p 1883:1883 vernemq/vernemq
```

``` sh
docker exec -it vernemq3 /bin/bash
cat /etc/vernemq/vernemq.conf

```

## nignx

``` sh
docker run --name nginx1 -d -p 8080:80 nginx
docker run --name nginx2 -d -p 8080:80  \
-v D:/project/spq/local-k8s/local-test/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/server.crt:/etc/nginx/crt/server.crt:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/server.key:/etc/nginx/crt/server.key:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/ca.crt:/etc/nginx/crt/ca.crt:ro \

# powershell
docker run --name nginx2 -d -p 8080:443 -v D:/project/spq/local-k8s/local-test/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro -v D:/project/spq/local-k8s/local-test/docker/ca/server.crt:/etc/nginx/crt/server.crt:ro -v D:/project/spq/local-k8s/local-test/docker/ca/server.key:/etc/nginx/crt/server.key:ro -v D:/project/spq/local-k8s/local-test/docker/ca/ca.crt:/etc/nginx/crt/ca.crt:ro --user root nginx

docker logs nginx2


openssl s_client -connect localhost:8080 -cert D:/project/spq/local-k8s/local-test/docker/ca/client.crt -key D:/project/spq/local-k8s/local-test/docker/ca/client.key -CAfile D:/project/spq/local-k8s/local-test/docker/ca/ca.crt


docker exec -it nginx2 /bin/bash

cat /var/log/nginx/error.log
```

## nignx

``` sh
docker run --name nginx2 -d -p 8080:80  \
-v D:/project/spq/local-k8s/local-test/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/server.crt:/etc/nginx/crt/server.crt:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/server.key:/etc/nginx/crt/server.key:ro \
-v D:/project/spq/local-k8s/local-test/docker/ca/ca.crt:/etc/nginx/crt/ca.crt:ro \

# powershell
docker run --name nginx2 -d -p 8080:8883 -v D:/project/spq/local-k8s/local-test/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro -v D:/project/spq/local-k8s/local-test/docker/ca/server.crt:/etc/nginx/crt/server.crt:ro -v D:/project/spq/local-k8s/local-test/docker/ca/server.key:/etc/nginx/crt/server.key:ro -v D:/project/spq/local-k8s/local-test/docker/ca/ca.crt:/etc/nginx/crt/ca.crt:ro --user root --network mqtt-network nginx

docker logs nginx2


openssl s_client -connect localhost:8080 -cert D:/project/spq/local-k8s/local-test/docker/ca/client.crt -key D:/project/spq/local-k8s/local-test/docker/ca/client.key -CAfile D:/project/spq/local-k8s/local-test/docker/ca/ca.crt


docker exec -it nginx2 /bin/bash

cat /var/log/nginx/error.log
```

## network

``` sh
docker network create mqtt-network

docker network connect mqtt-network vernemq4
docker network connect mqtt-network nginx2

docker run -d --name vernemq-container --network mqtt-network vernemq
docker run -d --name nginx-container --network mqtt-network -v /path/to/nginx.conf:/etc/nginx/nginx.conf nginx
docker network ls

mosquitto_pub -h vernemq4 -p 1883 -t test/topic -m "Hello MQTT"
```
