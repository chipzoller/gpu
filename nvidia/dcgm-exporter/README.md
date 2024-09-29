https://github.com/NVIDIA/dcgm-exporter/blob/main/deployment/values.yaml

helm repo add gpu-helm-charts https://nvidia.github.io/dcgm-exporter/helm-charts
helm repo update
helm install -n cz-gpu-testing nvidia-dcgm-exporter gpu-helm-charts/dcgm-exporter -f values.yaml

## Test Metrics

k -n cz-gpu-testing port-forward svc/nvidia-dcgm-exporter 9400
curl localhost:9400/metrics

## ConfigMap to Configure Metrics

ConfigMap named `exporter-metrics-config-map` which appears to be a config value. Looks like providing it may be a config option not on by default. No current Helm value to supply your own or override the metrics. Use this snippet to point DCGM at that ConfigMap:

```yaml
extraConfigMapVolumes:
  - name: exporter-metrics-volume
    configMap:
      name: exporter-metrics-config-map
      items:
      - key: metrics
        path: dcp-metrics-included.csv
extraVolumeMounts:
  - name: exporter-metrics-volume
    mountPath: /etc/dcgm-exporter/dcp-metrics-included.csv
    readOnly: true
    subPath: dcp-metrics-included.csv
```

NOTE that when using subPath volumes, an update to the ConfigMap WILL NOT cause Pods to pick that value up. Need to re-roll.