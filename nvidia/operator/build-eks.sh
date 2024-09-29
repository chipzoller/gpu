#!/bin/bash
set -euo pipefail

# Test if the required tools are installed
if ! command -v replicated &> /dev/null; then
    echo "replicated CLI is required to run this script. See documentation here: https://docs.replicated.com/reference/replicated-cli-installing"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "jq is required to run this script"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "helm is required to run this script"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "kubectl is required to run this script"
    exit 1
fi

# Test if the environment variable REPLICATED_API_TOKEN is set
if [[ -z "${REPLICATED_API_TOKEN:-}" ]]; then
    echo "The environment variable REPLICATED_API_TOKEN is required to run this script."
    exit 1
fi

# Provision EKS cluster
replicated cluster create --distribution eks \
    --nodegroup instance-type=m6i.large,nodes=1,disk=50 \
    --nodegroup instance-type=g4dn.xlarge,nodes=1,disk=50 \
    --ttl 2h \
    --version 1.29 \
    --name myeks01

# Wait for cluster to be in "running" state
while true; do
    status=$(replicated cluster ls --output json | jq -r '.[] | select(.name == "myeks01") | .status')
    if [[ $status == "running" ]]; then
        break
    fi
    sleep 60
done

# Retrieve kubeconfig for the cluster
replicated cluster kubeconfig --name myeks01

# Create nvidia-gpu-operator Namespace
kubectl create ns nvidia-gpu-operator

# Create the ResourceQuota for good measure.
kubectl create -f- << EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-operator-quota
  namespace: nvidia-gpu-operator
spec:
  hard:
    pods: 100
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
        - system-node-critical
        - system-cluster-critical
EOF

# Helm install the GPU operator using EKS values
helm upgrade -i nvidia-gpu-operator -n nvidia-gpu-operator --repo https://helm.ngc.nvidia.com/nvidia gpu-operator -f values-eks.yaml