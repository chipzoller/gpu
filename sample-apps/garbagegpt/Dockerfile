# Use the NVIDIA CUDA base image
FROM nvidia/cuda:12.6.0-base-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libboost-python-dev \
    libboost-thread-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install CUDA toolkit development files
RUN apt-get update && apt-get install -y \
    cuda-toolkit-12-6 \
    && rm -rf /var/lib/apt/lists/*

# Install NVIDIA DCGM
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb && \
    add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"

RUN apt-get update && \
    apt-get install -y datacenter-gpu-manager && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for CUDA
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Copy the application code
COPY stress_gpu.py /usr/src/app/stress_gpu.py

# Install Python dependencies if any
RUN pip3 install nvidia-ml-py3 pycuda

# Set the command to run the application
CMD ["python3", "/usr/src/app/stress_gpu.py"]
