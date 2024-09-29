# NVIDIA-SMI CLI

Info about this CLI utility.

## Running in K8s

Need to use `hostPID: true` and privileged mode in the container.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-smi
spec:
  hostPID: true
  restartPolicy: Never
  containers:
    - name: smi
      image: docker.io/nvidia/cuda:12.5.0-runtime-ubuntu22.04
      command:
        # - nvidia-smi
        # - -L
        - sleep
        - infinity
      securityContext:
        privileged: true
      resources:
        limits:
          # nvidia.com/gpu: 1
          nvidia.com/gpu.shared: 1
```

## Outputs

`nvidia-smi` will show the following:

```
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.183.01             Driver Version: 535.183.01   CUDA Version: 12.5     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       On  | 00000000:00:1E.0 Off |                    0 |
| N/A   50C    P0              72W /  70W |    113MiB / 15360MiB |    100%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A   1933957      C   /cuda-samples/sample                        110MiB |
+---------------------------------------------------------------------------------------+
```

`nvidia-smi --help-query-compute-apps`

```
List of valid properties to query for the switch "--query-compute-apps":

Section about Active Compute Processes properties
List of processes having compute context on the device.

"timestamp"
The timestamp of when the query was made in format "YYYY/MM/DD HH:MM:SS.msec".

"gpu_name"
The official product name of the GPU. This is an alphanumeric string. For all products.

"gpu_bus_id"
PCI bus id as "domain:bus:device.function", in hex.

"gpu_serial"
This number matches the serial number physically printed on each board. It is a globally unique immutable alphanumeric value.

"gpu_uuid"
This value is the globally unique immutable alphanumeric identifier of the GPU. It does not correspond to any physical label on the board.

"pid"
Process ID of the compute application

"process_name" or "name"
Process Name

"used_gpu_memory" or "used_memory"
Amount memory used on the device by the context. Not available on Windows when running in WDDM mode because Windows KMD manages all the memory not NVIDIA driver.
```

Example

```
nvidia-smi --query-compute-apps=name,pid --format=csv
process_name, pid
/cuda-samples/sample, 1895238
```
