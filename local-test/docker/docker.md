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
docker run --name nginx1 -d -p 8080:80 -v D:\nginx\nginx.conf:/etc/nginx/nginx.conf:ro -v D:\nginx\html:/usr/share/nginx/html:ro nginx

```