## Helm Values

https://github.com/NVIDIA/k8s-device-plugin/blob/release-0.15/deployments/helm/nvidia-device-plugin/values.yaml

## Install/Upgrade

helm upgrade -i nvdp nvidia-device-plugin \
--repo https://nvidia.github.io/k8s-device-plugin \
--namespace nvidia-device-plugin \
--create-namespace \
-f values.yaml