## helm install

``` sh
helm install mqtt . -f values.yaml
helm uninstall mqtt 
helm upgrade mqtt . -f values.yaml
helm install mqtt vernemq/vernemq -f values.yaml
```
## 查看 渲染后的 yaml

``` sh
# Chart 渲染
helm template my-release ./ --values values.yaml > xxx.yaml
```