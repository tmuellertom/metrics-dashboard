# Additonal information for Answers

## Setup

A k3d cluster is used for the project because M1 Mac does not support Vagrant with Virtualbox.  
The Grafana Service is exposed to Nodeport 30000 for usability reasons.


## Port Forwarding
Before starting Prometheus needs to be exposed via port-forward `kubectl port-forward -n monitoring service/prometheus-kube-prometheus-prometheus 9090` 
Forward the simplest query from jaeger `kubectl port-forward -n observability service/simplest-query 16686:16686`
Simplest query could also be used with NodePort


## Notes for Install Jaeger

```
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role_binding.yaml


kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role_binding.yaml

kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.28.0/jaeger-operator.yaml -n observability

```


```
kubectl apply -n observability -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
 name: simplest
EOF
```