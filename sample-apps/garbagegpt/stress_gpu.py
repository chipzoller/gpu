import time
import argparse
import pynvml
import pycuda.autoinit
import pycuda.driver as cuda
import numpy as np
from pycuda.compiler import SourceModule
from multiprocessing import Process

# CUDA kernel for stressing the GPU
mod = SourceModule("""
__global__ void stress_test(float *a, float *b, float *c, int n) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx] * 2.0;
    }
}
""")
stress_test = mod.get_function("stress_test")

def stress_gpu(gpu_index, target_utilization):
    """
    Function to stress a specific GPU to reach the target utilization.
    """
    cuda.Device(gpu_index).make_context()

    # Allocate memory on the GPU
    n = 10**7  # Size of the arrays (adjust this to control stress level)
    a = np.random.randn(n).astype(np.float32)
    b = np.random.randn(n).astype(np.float32)
    c = np.zeros_like(a)

    a_gpu = cuda.mem_alloc(a.nbytes)
    b_gpu = cuda.mem_alloc(b.nbytes)
    c_gpu = cuda.mem_alloc(c.nbytes)

    cuda.memcpy_htod(a_gpu, a)
    cuda.memcpy_htod(b_gpu, b)

    while True:
        # Monitor the current utilization
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu

        # Adjust workload based on the current utilization
        if utilization < target_utilization:
            # Execute the CUDA kernel to stress the GPU
            stress_test(a_gpu, b_gpu, c_gpu, np.int32(n), block=(256, 1, 1), grid=(n // 256, 1))

        time.sleep(0.01)  # Small delay to control the stress loop

    cuda.Context.pop()

def main():
    # Initialize NVIDIA Management Library
    pynvml.nvmlInit()

    # Parse input arguments
    parser = argparse.ArgumentParser(description="GPU Stress Test Script")
    parser.add_argument("--gpus", type=int, required=True, help="Number of GPUs to stress test")
    parser.add_argument("--utilization", type=int, required=True, help="Target GPU utilization percentage (0-100)")
    args = parser.parse_args()

    # Check the number of available GPUs
    num_gpus = pynvml.nvmlDeviceGetCount()
    if args.gpus > num_gpus:
        print(f"Error: Requested {args.gpus} GPUs, but only {num_gpus} GPUs are available.")
        return

    # Start stressing the specified number of GPUs
    processes = []
    for i in range(args.gpus):
        process = Process(target=stress_gpu, args=(i, args.utilization))
        process.start()
        processes.append(process)

    # Keep the script running
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

    # Shutdown NVIDIA Management Library
    pynvml.nvmlShutdown()

if __name__ == "__main__":
    main()
