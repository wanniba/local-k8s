# docker

``` sh
docker run --name vernemq1 -d vernemq/vernemq 

docker cp my-vernemq:/vernemq/etc/vernemq.conf ./config/
docker cp my-vernemq:/vernemq/etc/vm.args ./config/

docker exec -it my-vernemq -- /bin/sh
```