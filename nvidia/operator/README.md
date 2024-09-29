# Values reference

https://github.com/NVIDIA/gpu-operator/blob/release-24.6/deployments/gpu-operator/values.yaml

helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm upgrade -i nvidia-gpu-operator -n nvidia-gpu-operator nvidia/gpu-operator -f values-gke.yaml
helm -n nvidia-gpu-operator uninstall nvidia-gpu-operator

## Installation Notes GKE

- Set the Kubernetes Node label `gke-no-default-nvidia-gpu-device-plugin=true` on the GPU node pool. This must be a K8s label and not a standard label.
- Disable driver installation when creating the GPU node pool as it isn't supported when using the operator.
- Installing device drivers via the operator is not currently supported.
- Follow instructions [here](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers) to manually install drivers depending on the OS and GPU type in use.
- Follow general instructions [here](https://cloud.google.com/kubernetes-engine/docs/how-to/gpu-operator) and see GKE-specific values file.
