## passwd

``` sh
docker-compose up -d

# 查看日志
docker-compose logs

# 停止服务
docker-compose down


openssl s_client -connect localhost:8883 -cert ./ca/client.crt -key ./ca/client.key -CAfile ./ca/gd_bundle-g2-g1.crt


mosquitto_sub -h localhost -p 1883 -t test/topic

penssl x509 -in server.crt -text -noout

touch /etc/vernemq/password_file
```
